#!/usr/bin/env python3

import argparse
import os
import re
import shlex
import signal
import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from shutil import which
from typing import Dict, Iterable, List, Optional, Pattern, Set, Tuple


@dataclass(frozen=True)
class AppPattern:
	pattern: str
	is_regex: bool
	compiled: Optional[Pattern[str]]

	@staticmethod
	def from_string(value: str, is_regex: bool) -> "AppPattern":
		value = value.strip()
		if not value:
			raise ValueError("Empty pattern provided")
		compiled = re.compile(value, re.IGNORECASE) if is_regex else None
		return AppPattern(pattern=value, is_regex=is_regex, compiled=compiled)

	def matches(self, text: str) -> bool:
		if self.is_regex and self.compiled is not None:
			return bool(self.compiled.search(text))
		return self.pattern.lower() in text.lower()


class PopupBackend:
	ZENITY = "zenity"
	NOTIFY_SEND = "notify-send"
	NONE = "none"


def detect_backend() -> str:
	if which("zenity") and (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
		return PopupBackend.ZENITY
	if which("notify-send") and (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
		return PopupBackend.NOTIFY_SEND
	return PopupBackend.NONE


def show_popup(backend: str, title: str, message: str, icon: Optional[str] = None, width: Optional[int] = None, height: Optional[int] = None) -> None:
	try:
		if backend == PopupBackend.ZENITY:
			cmd: List[str] = ["zenity", "--info", "--no-wrap", "--title", title, "--text", message]
			if icon:
				cmd.extend(["--window-icon", icon])
			if width:
				cmd.extend(["--width", str(width)])
			if height:
				cmd.extend(["--height", str(height)])
			subprocess.Popen(cmd)
			return
		if backend == PopupBackend.NOTIFY_SEND:
			cmd = ["notify-send", title, message]
			if icon:
				cmd.extend(["--icon", icon])
			subprocess.Popen(cmd)
			return
		print(f"[POPUP] {title}: {message}")
	except Exception as exc:
		print(f"[WARN] Failed to show popup via {backend}: {exc}", file=sys.stderr)
		print(f"[POPUP] {title}: {message}")


def build_message(template: str, fields: Dict[str, str]) -> str:
	class SafeDict(defaultdict):
		def __missing__(self, key):  # type: ignore
			return ""

	return template.format_map(SafeDict(str, fields))


def parse_patterns(values: Iterable[str], is_regex: bool) -> List[AppPattern]:
	patterns: List[AppPattern] = []
	for raw in values:
		if not raw:
			continue
		for part in re.split(r"[,\n]", raw):
			part = part.strip()
			if part:
				patterns.append(AppPattern.from_string(part, is_regex))
	return patterns


def list_pids() -> List[int]:
	try:
		entries = os.listdir("/proc")
	except Exception:
		return []
	pids: List[int] = []
	for name in entries:
		if name.isdigit():
			try:
				pids.append(int(name))
			except Exception:
				pass
	return pids


def read_file(path: str) -> Optional[bytes]:
	try:
		with open(path, "rb") as f:
			return f.read()
	except Exception:
		return None


def read_text(path: str) -> str:
	data = read_file(path)
	if not data:
		return ""
	try:
		return data.decode(errors="ignore").strip()
	except Exception:
		return ""


def get_process_info(pid: int) -> Optional[Tuple[str, str, str]]:
	base = f"/proc/{pid}"
	# cmdline
	raw = read_file(os.path.join(base, "cmdline"))
	if raw is None:
		return None
	parts = [p for p in raw.split(b"\x00") if p]
	cmdline = " ".join(shlex.quote(p.decode(errors="ignore")) for p in parts)
	# exe
	exe_path = ""
	try:
		exe_path = os.readlink(os.path.join(base, "exe"))
	except Exception:
		exe_path = ""
	# name
	name = read_text(os.path.join(base, "comm"))
	if not name:
		if exe_path:
			name = os.path.basename(exe_path)
		elif parts:
			first = parts[0].decode(errors="ignore")
			name = os.path.basename(first)
		else:
			name = str(pid)
	return name, exe_path, cmdline


def process_matches_patterns(name: str, exe: str, cmdline: str, patterns: List[AppPattern]) -> bool:
	candidates = [name, exe, cmdline]
	for pattern in patterns:
		for candidate in candidates:
			if candidate and pattern.matches(candidate):
				return True
	return False


def monitor(app_patterns: List[AppPattern], title_tpl: str, message_tpl: str, icon: Optional[str], interval: float, debounce_seconds: float, only_once_per_pid: bool, width: Optional[int], height: Optional[int]) -> None:
	backend = detect_backend()
	if backend == PopupBackend.NONE:
		print("[INFO] No GUI popup backend found (zenity/notify-send). Will print to stdout.")

	seen_pids: Set[int] = set()
	last_fired_for_key: Dict[str, float] = {}
	stopping = False

	def handle_sigterm(_signum, _frame):
		print("[INFO] Stopping monitor...")
		nonlocal stopping
		stopping = True

	signal.signal(signal.SIGINT, handle_sigterm)
	signal.signal(signal.SIGTERM, handle_sigterm)

	while not stopping:
		start_time = time.time()
		try:
			for pid in list_pids():
				if only_once_per_pid and pid in seen_pids:
					continue
				info = get_process_info(pid)
				if info is None:
					continue
				name, exe, cmdline = info
				if not process_matches_patterns(name, exe, cmdline, app_patterns):
					continue

				key = name or exe or str(pid)
				now = time.time()
				last_time = last_fired_for_key.get(key, 0.0)
				if debounce_seconds > 0 and (now - last_time) < debounce_seconds:
					continue

				fields = {
					"app": name or os.path.basename(exe) or key,
					"pid": str(pid),
					"exe": exe,
					"cmdline": cmdline,
				}
				title = build_message(title_tpl, fields)
				message = build_message(message_tpl, fields)

				show_popup(backend, title, message, icon=icon, width=width, height=height)
				last_fired_for_key[key] = now
				if only_once_per_pid:
					seen_pids.add(pid)
		except Exception as exc:
			print(f"[WARN] Monitor loop error: {exc}", file=sys.stderr)

		elapsed = time.time() - start_time
		sleep_for = max(0.05, interval - elapsed)
		time.sleep(sleep_for)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Monitor newly started processes and pop a custom window when matched",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	parser.add_argument(
		"--apps",
		required=True,
		help="Comma-separated list of app names, executable paths, or regex patterns (use --regex for regex mode)",
	)
	parser.add_argument(
		"--regex",
		action="store_true",
		help="Interpret --apps entries as regular expressions",
	)
	parser.add_argument(
		"--interval",
		type=float,
		default=1.0,
		help="Polling interval in seconds",
	)
	parser.add_argument(
		"--debounce",
		type=float,
		default=5.0,
		help="Debounce window per app name in seconds",
	)
	parser.add_argument(
		"--once-per-pid",
		action="store_true",
		help="Trigger at most once per process id",
	)
	parser.add_argument(
		"--title",
		default="检测到应用已启动: {app}",
		help="Popup title template. Fields: {app}, {pid}, {exe}, {cmdline}",
	)
	parser.add_argument(
		"--message",
		default="应用 {app} (PID {pid}) 已启动\n{cmdline}",
		help="Popup message template. Fields: {app}, {pid}, {exe}, {cmdline}",
	)
	parser.add_argument(
		"--icon",
		help="Icon path or name for popup (if supported)",
		default=None,
	)
	parser.add_argument(
		"--width",
		type=int,
		help="Popup window width (zenity only)",
		default=None,
	)
	parser.add_argument(
		"--height",
		type=int,
		help="Popup window height (zenity only)",
		default=None,
	)
	return parser.parse_args(argv)


def main() -> None:
	args = parse_args()
	patterns = parse_patterns([args.apps], is_regex=args.regex)
	if not patterns:
		print("[ERROR] No valid app patterns provided", file=sys.stderr)
		sys.exit(2)

	monitor(
		app_patterns=patterns,
		title_tpl=args.title,
		message_tpl=args.message,
		icon=args.icon,
		interval=max(0.1, float(args.interval)),
		debounce_seconds=max(0.0, float(args.debounce)),
		only_once_per_pid=bool(args.once_per_pid),
		width=args.width,
		height=args.height,
	)


if __name__ == "__main__":
	main()