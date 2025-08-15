
import { startAbility, stopAbility } from '@ohos.ability.featureAbility';
import { NotificationManager } from '@ohos.notificationManager';
import { BusinessError } from '@ohos.base';
import { Want } from '@kit.AbilityKit';

export class ServiceManager {
  private static instance: ServiceManager;

  private constructor() {}

  public static getInstance(): ServiceManager {
    if (!ServiceManager.instance) {
      ServiceManager.instance = new ServiceManager();
    }
    return ServiceManager.instance;
  }

  // 启动服务并指定通知标题和内容
  startService(notificationTitle: string, notificationContent: string) {
    const want: Want = {
      bundleName: 'com.example.myapp',
      abilityName: 'MyService',
      parameters: {
        notificationTitle: notificationTitle,
        notificationContent: notificationContent
      }
    };

    startAbility(want, (err: BusinessError) => {
      if (err) {
        console.error(`Failed to start service. Code is ${err.code}, message is ${err.message}`);
        return;
      }
      console.info('Succeeded in starting service.');
    });
  }

  // 关闭服务
  stopService() {
    const want: Want = {
      bundleName: 'com.example.myapp',
      abilityName: 'MyService'
    };

    stopAbility(want, (err: BusinessError) => {
      if (err) {
        console.error(`Failed to stop service. Code is ${err.code}, message is ${err.message}`);
        return;
      }
      console.info('Succeeded in stopping service.');
    });
  }

  // 检测通知权限
  checkNotificationPermission() {
    return new Promise<boolean>((resolve, reject) => {
      NotificationManager.isNotificationEnabled((err: BusinessError, isEnabled: boolean) => {
        if (err) {
          reject(err);
        } else {
          resolve(isEnabled);
        }
      });
    });
  }

  // 申请通知权限
  requestNotificationPermission() {
    return new Promise<void>((resolve, reject) => {
      NotificationManager.requestEnableNotification((err: BusinessError) => {
        if (err) {
          reject(err);
        } else {
          resolve();
        }
      });
    });
  }

  // 更新通知内容和标题
  updateNotification(notificationTitle: string, notificationContent: string) {
    const want: Want = {
      bundleName: 'com.example.myapp',
      abilityName: 'MyService',
      parameters: {
        notificationTitle: notificationTitle,
        notificationContent: notificationContent
      }
    };

    startAbility(want, (err: BusinessError) => {
      if (err) {
        console.error(`Failed to update notification. Code is ${err.code}, message is ${err.message}`);
        return;
      }
      console.info('Succeeded in updating notification.');
    });
  }
}
