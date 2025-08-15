# 应用监听器（Linux）

监控用户启动的应用进程，如果命中指定应用，弹出自定义窗口（优先使用 `zenity`，其次 `notify-send`，否则回退控制台输出）。

## 依赖

- Python 3.8+
- 弹窗后端（二选一即可）：
  - `zenity`（GTK 弹窗）
  - `notify-send`（桌面通知）

> 注意：Wayland/X11 环境需有 `DISPLAY` 或 `WAYLAND_DISPLAY` 环境变量。

## 运行

无需安装第三方依赖，直接运行：

```bash
python3 monitor.py --apps "code,firefox" --once-per-pid --debounce 5
```

- 使用正则匹配：

```bash
python3 monitor.py --apps ".*(chrome|firefox).*" --regex --once-per-pid
```

- 自定义弹窗标题和内容（模板支持字段：`{app}`、`{pid}`、`{exe}`、`{cmdline}`）：

```bash
python3 monitor.py \
  --apps "code,firefox" \
  --title "检测到应用: {app}" \
  --message "{app} (PID {pid}) 启动\n命令: {cmdline}" \
  --icon "dialog-information" \
  --width 420 --height 160
```

## 后台运行

```bash
nohup python3 monitor.py --apps "code,firefox" --once-per-pid --debounce 5 >/tmp/app_watcher.log 2>&1 &
```

或创建 systemd 用户服务（`~/.config/systemd/user/app-watcher.service`）：

```
[Unit]
Description=App Watcher

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/monitor.py --apps "code,firefox" --once-per-pid --debounce 5
Restart=on-failure

[Install]
WantedBy=default.target
```

然后：

```bash
systemctl --user daemon-reload
systemctl --user enable --now app-watcher.service
```