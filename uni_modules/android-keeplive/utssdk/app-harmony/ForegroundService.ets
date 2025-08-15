import { ServiceExtensionAbility, Want } from '@ohos.ability.ServiceExtensionAbility';
import { NotificationManager } from '@ohos.notificationManager';
import { BusinessError } from '@ohos.base';

export default class ForegroundService extends ServiceExtensionAbility {
  onCreate(want: Want) {
    super.onCreate(want);
    // 初始化通知
    this.initNotification(want.parameters?.notificationTitle, want.parameters?.notificationContent);
  }

  initNotification(title: string, content: string) {
    const notificationRequest: NotificationManager.NotificationRequest = {
      id: 1,
      slotType: NotificationManager.SlotType.SERVICE_INFORMATION,
      content: {
        contentType: NotificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT,
        normal: {
          title: title || '服务运行中',
          text: content || '服务正在运行，更新中...',
          additionalText: ''
        }
      },
      wantAgent: {
        want: {
          bundleName: 'com.example.myapp',
          abilityName: 'EntryAbility'
        }
      }
    };

    NotificationManager.publish(notificationRequest, (err: BusinessError) => {
      if (err) {
        console.error(`Failed to publish notification. Code is ${err.code}, message is ${err.message}`);
        return;
      }
      console.info('Succeeded in publishing notification.');
    });
  }

  // 更新通知栏内容
  updateNotification(title: string, content: string) {
    const notificationRequest: NotificationManager.NotificationRequest = {
      id: 1,
      slotType: NotificationManager.SlotType.SERVICE_INFORMATION,
      content: {
        contentType: NotificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT,
        normal: {
          title: title,
          text: content,
          additionalText: ''
        }
      },
      wantAgent: {
        want: {
          bundleName: 'com.example.myapp',
          abilityName: 'EntryAbility'
        }
      }
    };

    NotificationManager.publish(notificationRequest, (err: BusinessError) => {
      if (err) {
        console.error(`Failed to update notification. Code is ${err.code}, message is ${err.message}`);
        return;
      }
      console.info('Succeeded in updating notification.');
    });
  }

  // 保活逻辑
  onForeground() {
    // 这里可以添加保活逻辑，例如定时更新通知
    setInterval(() => {
    //  this.updateNotification('服务运行中', '服务正在运行，更新中...');
    }, 60 * 1000); // 每分钟更新一次
  }

  // 服务销毁时的清理逻辑
  onDestroy() {
    super.onDestroy();
    // 取消通知
    NotificationManager.cancel(1, (err: BusinessError) => {
      if (err) {
        console.error(`Failed to cancel notification. Code is ${err.code}, message is ${err.message}`);
        return;
      }
      console.info('Succeeded in canceling notification.');
    });
  }
}