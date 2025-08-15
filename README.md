# 应用监听器 (uniappx + UTS)

基于 uniappx + UTS 开发的跨平台应用监听器，支持 Android 和 iOS 平台，可以监听指定应用的启动事件并弹出自定义通知。

## 功能特性

- 🔍 **应用监听**: 实时监听指定应用的启动事件
- 📱 **跨平台支持**: 支持 Android 和 iOS 平台
- 🔔 **自定义通知**: 支持自定义通知标题和内容
- ⚙️ **灵活配置**: 可配置检查间隔、目标应用列表等
- 📊 **历史记录**: 记录应用启动历史
- 🎨 **现代UI**: 采用现代化的用户界面设计

## 技术栈

- **框架**: uniappx
- **语言**: UTS (UniApp TypeScript)
- **平台**: Android + iOS
- **UI**: 原生组件 + CSS3

## 项目结构

```
├── uni_modules/
│   └── app-monitor/           # 应用监听器模块
│       ├── utssdk/
│       │   └── index.uts      # UTS 核心逻辑
│       └── package.json       # 模块配置
├── pages/
│   ├── index/                 # 主页面
│   ├── app-monitor/           # 应用监听器页面
│   └── web-view/              # Web 应用页面
├── components/
│   └── app-launch-popup/      # 应用启动弹窗组件
├── static/                    # 静态资源
└── manifest.json              # 应用配置
```

## 安装和运行

### 环境要求

- HBuilderX 4.0+
- uniappx 项目
- Android/iOS 开发环境

### 运行步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd app-monitor-uniappx
   ```

2. **使用 HBuilderX 打开项目**

3. **配置权限**
   - Android: 确保在 `manifest.json` 中配置了必要的权限
   - iOS: 确保配置了相应的权限描述

4. **编译运行**
   - 选择目标平台 (Android/iOS)
   - 点击运行或发行

## 使用说明

### 1. 主页面

应用启动后，在主页面可以看到两个功能入口：
- **应用监听**: 进入应用监听器功能
- **Web 应用**: 打开原有的 Web 应用

### 2. 应用监听器

在应用监听器页面可以：

#### 配置目标应用
- 添加要监听的应用包名
- 删除不需要监听的应用
- 预设了微信、QQ、支付宝等常用应用

#### 设置监听参数
- **检查间隔**: 设置检查应用启动的间隔时间
- **显示通知**: 开启/关闭系统通知
- **通知标题**: 自定义通知标题模板
- **通知内容**: 自定义通知内容模板

#### 查看历史记录
- 实时显示应用启动历史
- 包含应用名称、包名、启动时间等信息

### 3. 权限管理

#### Android 权限
应用需要以下权限：
- `QUERY_ALL_PACKAGES`: 查询所有应用包
- `PACKAGE_USAGE_STATS`: 使用统计权限
- `SYSTEM_ALERT_WINDOW`: 系统弹窗权限
- `FOREGROUND_SERVICE`: 前台服务权限
- `POST_NOTIFICATIONS`: 通知权限

#### iOS 权限
- `NSUserActivityUsageDescription`: 用户活动使用描述

## 核心功能实现

### UTS 模块 (`uni_modules/app-monitor/utssdk/index.uts`)

#### Android 实现
- 使用 `UsageStatsManager` 监听应用使用统计
- 通过 `MOVE_TO_FOREGROUND` 事件检测应用启动
- 支持自定义通知和权限管理

#### iOS 实现
- 由于 iOS 平台限制，主要提供基础框架
- 可通过系统通知或其他方式扩展功能

### 主要类和方法

```typescript
// 创建监听器实例
const monitor = createAppMonitor({
  targetApps: ['com.tencent.mm', 'com.tencent.mobileqq'],
  checkInterval: 2000,
  showNotification: true,
  notificationTitle: '检测到应用启动: {app}',
  notificationContent: '应用 {app} 已启动\n时间: {time}'
})

// 开始监听
monitor.startMonitoring()

// 停止监听
monitor.stopMonitoring()

// 检查权限
const hasPermission = monitor.checkPermissions()

// 请求权限
monitor.requestPermissions()
```

## 自定义配置

### 通知模板变量

在通知标题和内容中可以使用以下变量：
- `{app}`: 应用名称
- `{package}`: 应用包名
- `{time}`: 启动时间

### 添加新的目标应用

1. 在应用监听器页面点击"添加"
2. 输入应用包名（如：`com.example.app`）
3. 点击确认添加

### 常见应用包名

| 应用名称 | 包名 |
|---------|------|
| 微信 | `com.tencent.mm` |
| QQ | `com.tencent.mobileqq` |
| 支付宝 | `com.eg.android.AlipayGphone` |
| 淘宝 | `com.taobao.taobao` |
| 抖音 | `com.ss.android.ugc.aweme` |
| 微博 | `com.sina.weibo` |

## 注意事项

### Android 平台
1. **权限授权**: 首次使用需要手动授权使用统计权限
2. **后台运行**: 建议开启应用自启动和后台运行权限
3. **电池优化**: 关闭应用的电池优化以保持监听功能

### iOS 平台
1. **平台限制**: iOS 对应用监听有严格限制
2. **功能受限**: 部分功能可能无法在 iOS 上正常工作
3. **审核要求**: 上架 App Store 需要符合苹果审核规范

## 开发扩展

### 添加新的监听方式

可以在 UTS 模块中添加新的监听方式：

```typescript
// 在 AppMonitor 类中添加新方法
private checkNewMethod(): void {
  // 实现新的监听逻辑
}
```

### 自定义弹窗组件

可以修改 `components/app-launch-popup/` 来自定义弹窗样式和行为。

### 数据持久化

可以添加本地存储功能来保存配置和历史记录：

```typescript
// 保存配置
uni.setStorageSync('monitor_config', config)

// 读取配置
const config = uni.getStorageSync('monitor_config')
```

## 故障排除

### 常见问题

1. **权限被拒绝**
   - 检查应用权限设置
   - 重新授权使用统计权限

2. **监听不生效**
   - 确认目标应用包名正确
   - 检查应用是否在后台运行
   - 验证权限是否已授权

3. **通知不显示**
   - 检查通知权限
   - 确认通知渠道配置正确

### 调试方法

1. **查看控制台日志**
   ```typescript
   console.log('监听状态:', isMonitoring)
   console.log('权限状态:', hasPermissions)
   ```

2. **检查事件触发**
   ```typescript
   uni.$on('appLaunched', (appInfo) => {
     console.log('应用启动:', appInfo)
   })
   ```

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 微信/QQ 群

---

**注意**: 本项目仅供学习和研究使用，请遵守相关法律法规和平台政策。