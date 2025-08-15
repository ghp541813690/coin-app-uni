# android-keeplive
### 本插件支持uniapp/uniappx 双端
 长期维护，有任何问题请在插件群联系作者
### 功能介绍和注意事项

### 源码版本不包含aar文件源码

#### 本插件为后台无声音乐保活，为推送蓝牙后台传数据等保驾护，增加程序存活率，防止程序进入后台后或者系统休眠后程序停止执行的问题(用本插件定时器1和定时器2可保证任何状态下准确执行)无定位需求直接集成即可，若需要定位则合并集成作者定位插件
1.android/iOS端需要自定义基座

2.ios 端若觉得效果不佳，可以解压ios 插件目录下的uni_modules\android-keeplive\utssdk\app-ios\info.zip 将info.plist 文件和uts 文件在同一个级别 文件（上架可能会困难一点）
 
3.推荐android端合井使用作者一像素保活效果更佳[链接](https://ext.dcloud.net.cn/plugin?id=20324)


#### Android端 其它增加存活机会方法
1.最近任务给程序加锁，2.在系统设置启动项开启应用程序后台运行


#### 插件测试使用方法
1. 选择试用，绑定要试用的项目appid，

2. 选择后下载到对应的本地项目，

3. 按照文档 -》把插件引入项目（即 import { KeepLive } from '@/uni_modules/android-keeplive' 需要先引入），

4. 发布-》云打包-》选择制作基座-》打包等基座制作完成 

5. 运行 -》 运行到手机或模拟器-》运行到Androidapp基座-》选择使用自定义基座运行-》选择手机-》运行

6. 若之前手机安装过基座需要先卸载之前的基座


###  uniappx
~~~
// #ifdef APP
import { KeepLive } from '@/uni_modules/android-keeplive' // 放在页面导入的地方
// #endif


//<!-- ------------------------------下方代码需要放进方法中-------------------------------------------------- -->	
// #ifdef APP
var keep=new KeepLive();
keep.setTitle("app");
keep.setContent("app is runing");
// keep.setLargeIcon("icon");
keep.setSmallIcon("icon"); //图标名字  图标放在 插件下面的 uni_modules\android-keeplive\utssdk\app-android\res 文件夹下
keep.onAddBackgroundCallback(function(res:boolean){
	console.log("后台运行 "+res)
	
})
keep.onAddScrrenListenerCallback(function(res:boolean){
	console.log("屏幕开启状态 "+res)
	
})	
keep.setWakeLock(1,"keeptag");// 设置唤醒类型

if(!keep.checkAppNotification()){
	keep.onOpenNotificationSetting(function(res:boolean){
		keep.register();
		var ignoring=  keep.isIgnoringBatteryOptimizations();
		if(!ignoring){
			keep.requestIgnoreBatteryOptimizations();
		}
	})
}else{
	keep.register();
	var ignoring=  keep.isIgnoringBatteryOptimizations();
	if(!ignoring){
		keep.requestIgnoreBatteryOptimizations();
	}
}
// 稳定定时器 需要的用户使用（默认定时器1 ）
keep.onStartCSystemTimer(120,function(){
	console.log("onStartCSystemTimer ");
	keep.acquire(1000);// 唤醒一秒钟
});
// 需要插件增加程序后台运行能力的可以加下面代码 想程序始终保持活性（即稳定推送 scocket等）（体验好） 还是建议用户打开系统设置 启动项 后台运行
//keep.wifilock();//部分手机可能会断
// 定时器时间改成10秒 去掉上方的
//keep.onStartCSystemTimer(10,function(){
//	console.log("onStartCSystemTimer ");
//	keep.acquire(1000);// 唤醒一秒钟
//});
// #endif
~~~


###  uniapp
~~~
// #ifdef APP
import { KeepLive } from '@/uni_modules/android-keeplive' // 放在页面导入的地方
// #endif


//<!-- ------------------------------下方代码需要放进方法中-------------------------------------------------- -->	
// #ifdef APP	
var keep=new KeepLive();
keep.setTitle("app");
keep.setContent("app is runing");
// keep.setLargeIcon("icon");
keep.setSmallIcon("icon"); //图标名字  图标放在 插件下面的 res/drawable 文件夹下
keep.onAddBackgroundCallback(function(res){
	console.log("后台运行 "+res)
	
})
keep.onAddScrrenListenerCallback(function(res){
	console.log("屏幕开启状态 "+res)
	
})	
keep.setWakeLock(1,"keeptag");// 设置唤醒类型


if(!keep.checkAppNotification()){
	keep.onOpenNotificationSetting(function(res){
		keep.register();
		var ignoring=  keep.isIgnoringBatteryOptimizations();
		if(!ignoring){
			keep.requestIgnoreBatteryOptimizations();
		}
	})
}else{
	keep.register();
	var ignoring=  keep.isIgnoringBatteryOptimizations();
	if(!ignoring){
		keep.requestIgnoreBatteryOptimizations();
	}
}
var ignoring=  keep.isIgnoringBatteryOptimizations();
if(!ignoring){
	keep.requestIgnoreBatteryOptimizations();
}
keep.onStartCSystemTimer(120,function(){
	console.log("onStartCSystemTimer ");
		keep.acquire(1000);// 唤醒一秒钟
});
// 需要插件增加程序后台运行能力的可以加下面代码 想程序始终保持活性（即稳定推送 scocket等）（体验好） 还是建议用户打开系统设置 启动项 后台运行
//keep.wifilock();//部分手机可能会断
// 定时器时间改成3秒 去掉上方的
//keep.onStartCSystemTimer(3,function(){
//	console.log("onStartCSystemTimer ");
//	keep.acquire(1000);// 唤醒一秒钟
//});
// #endif
~~~



### 需要gps定位用户 可合并作者定位插件（推荐使用作者定时器1 ，系统休眠后可执行）
#### 
[安卓 ios原生gps定位](https://ext.dcloud.net.cn/plugin?id=21745)

[高德定位](https://ext.dcloud.net.cn/plugin?id=20916)

[安卓腾讯定位](https://ext.dcloud.net.cn/plugin?id=20875)（后续支持ios）

[安卓百度定位](https://ext.dcloud.net.cn/plugin?id=20562)

#### uniappx

~~~
// #ifdef APP
import { isProviderEnabled, openLocSetting,  onStartLocs,LocData,stop,LocationData} from "@/uni_modules/xtf-gpslocation"
// #endif
// #ifdef APP
// 停用后台播放音乐
keep.setBackgroundMusicEnabled(false);

// 后台定位则需要使用插件的定时器 息屏也能执行，自定定时器易休眠停止执行
// 先启动定位
var on=isProviderEnabled();// 是否开启gps
if(on){
	keep.onStartCSystemTimer(60,function(){
onStartLocs({
    backgroud:true,
} as LocData,function(data:LocationData){
    console.log(data)
})
	
	});	
}
// #endif


~~~

#### uniapp

~~~
import { isProviderEnabled, openLocSetting,  onStartLocs,LocData,stop} from "@/uni_modules/xtf-gpslocation"


// 停用后台播放音乐
keep.setBackgroundMusicEnabled(false);

// 后台定位则需要使用插件的定时器 息屏也能执行，自定定时器易休眠停止执行
// 先启动定位
var on=isProviderEnabled();// 是否开启gps
if(on){
	keep.onStartCSystemTimer(60,function(){
onStartLocs({
    backgroud:true,
} ,function(res){
    console.log(res)
})
	
	});	
}



~~~

### 注册开启运行

#### register
~~~
keep.register();
~~~

### 重启

#### restart
~~~
keep.restart();
~~~

### 取消运行

#### unregister
~~~
keep.unregister();
~~~

### 是否运行
#### isRunning
return  boolean
~~~
var run=keep.isRunning();
~~~
### 判断通知权限是否开启（安卓有效,ios 无功能）
#### checkAppNotification
~~~
var on=keep.checkAppNotification();
~~~

#### 打开应用通知设置（安卓有效,ios 无功能）
#### goNotificationSetting
~~~
keep.goNotificationSetting();
~~~
#### 打开应用通知设置并返回状态（安卓有效,ios 无功能）
uniappx
~~~
	keep.onOpenNotificationSetting(function(on:boolean){
	
	})
~~~
uniapp
~~~
	keep.onOpenNotificationSetting(function(on){
	})
~~~

### 通过包名打开应用程序（安卓有效,ios 无功能）
#### doStartApplicationWithPackageName
参数1 应用包名 string 
~~~
keep.doStartApplicationWithPackageName("com.test");
~~~


### 开启应用省电后台运行 （安卓有效,ios 无功能）
#### requestIgnoreBatteryOptimizations
~~~
keep.requestIgnoreBatteryOptimizations();
~~~

### 判断应用是否开启省电后台运行 （安卓有效,ios 无功能）
#### isIgnoringBatteryOptimizations
return  boolean 
~~~
var ignoring=  keep.isIgnoringBatteryOptimizations();
~~~

### 设置后台无声音乐是否开启 （安卓有效,ios 无功能）
#### setBackgroundMusicEnabled
参数1 boolean
~~~
keep.setBackgroundMusicEnabled(true);
~~~



### 是否隐藏通知栏 （弃用，后续删除）
#### hideNotification（安卓有效,ios 无功能）
参数1 boolean
~~~
keep.hideNotification(false);
~~~
### 静音通知
#### setNotifaicationSoundEnable
 参数1 boolean
 ~~~
 keep.setNotifaicationSoundEnable(true);
 ~~~

 
### 设置通知栏 ChannelId 默认keeplive（安卓有效,ios 无功能）
#### setChannelId
参数1 string 
 ~~~
 keep.setChannelId("keeplive");
 ~~~
 
### 更新通知栏
#### updateNotification
 ~~~
keep.setTitle("Test");
keep.setContent("test runing");
keep.updateNotification();
 ~~~

### 设置通知栏标题
#### setTitle
参数1 string 
 ~~~
 keep.setTitle("title");
 ~~~

### 设置通知栏内容
#### setContent
参数1 string 
 ~~~
 keep.setContent("msg");
 ~~~
### 设置通知重要性（安卓有效,ios 无功能）
#### setChannelImportance
参数1 number  0-4 低到高 
~~~
keep.setChannelImportance(3);
~~~


### 设置通知栏小图标（安卓有效,ios 无功能）
#### setSmallIcon
参数1 string   插件的res  drawable 目录下 名称

~~~
 keep.setSmallIcon("icon");

~~~

### 设置通知栏大图标（安卓有效,ios 无功能）
#### setLargeIcon
参数1 string   插件的res  drawable 目录下 名称
~~~
 keep.setLargeIcon("icon");

~~~

### 设置唤醒cpu类型（安卓有效,ios 无功能）
#### setWakeLock
参数1 number   
1:保持CPU 运转，屏幕和键盘灯有可能是关闭的。

参数2 string tag

~~~
keep.setWakeLock(1,"tag");
~~~

### 唤醒cpu  需先设置唤醒cpu 类型（安卓有效,ios 无功能）
#### acquire
参数1 number 时间

~~~
keep.acquire(-1);
~~~
### 释放cpu  需先设置唤醒cpu 类型（安卓有效,ios 无功能）
####  releaseAcquire
~~~
keep.releaseAcquire();
~~~


### 后台背景音乐测试  启动保活之前调用 （安卓有效,ios 无功能）
~~~
keep.setMusicVol(0) // 0~1 范围
keep.setMusicId("music")   // 将音乐放进  插件目录 /res/raw/music.mp3  
~~~

### 主动退出应用后台运行，相当于单击home （安卓有效,ios 无功能）
~~~
keep.toBackground();
~~~


### android 息屏准确执行定时器  (二者选择一个就可)

#### 定时器1   android/iOS/ web 三端均可用无需判断平台
~~~
//开启定时器     60时间为秒
 keep.onStartCSystemTimer(60,function(){
	console.log("onStartCSystemTimer ")
});
	
//keep.cancelCSystemTimer();// 取消定时器
//keep.clearAllCTimer();  // 取消全部定时器
~~~




#### 定时器2 
~~~
// android 原生定时任何状态一秒误差, 开始时间 1000为1秒0是马上执行, 开启周期 65*1000, 循环时间 大于60s 精准有效 低于60秒偏差误差
 keep.startAleraTask(0,65*1000,function(){
   	console.log("onAleraTaskListener ")
 }); 
     
   	//取消循环定时
keep.cancleAleraTask()
~~~


<!-- #### 定时器3 （待测试） 推荐  android/iOS/ web 微信小程序四端可用无需判断平台
~~~
//开启定时器     3时间为秒
 keep.startKeepClcokTimer(3,function(){
	console.log("startCSystemTimer ")
});
	
//keep.cancelKeepClcokTimer();// 取消定时器
//keep.cancelAllKeepClcokTimer();  // 取消全部定时器
~~~ -->

### 获取插件存活时间
~~~
var liveTime=keep.getLiveTime();// 毫秒时间
~~~


### 隐藏最近任务（安卓有效,ios 无功能）
参数1  boolean   true 为隐藏，false为显示
~~~
keep.hideRecentTask(true);// 隐藏
~~~
### 打开安卓系统应用设置 方便用户设置自启动（安卓有效,ios 无功能）
~~~
keep.goAndroidSystemAppSetting();
~~~
### 崩溃后重启 （原生Rom 有效 ）
~~~
keep.setCrashRestartUIEnabled(true);
~~~


### 其它功能
~~~
android channel 为android通知栏通配置
对使用插件app的新用户
本插件的channelId 默认为keeplive channelName 默认为keeplive  默认为有声通知。首次调用keep.register()/keep.updateNotification() 这个channel 就会自定创建好，并且不可修改
本插件可自定义channel 在调用keep.register()/keep.updateNotification()之前调用下面代码
keep.setNotifaicationSoundEnable(false);
keep.setChannelId("保活");
keep.setChannelName("保活") //通知名称
keep.register();//keep.updateNotification()/* 同样为调用即为创建，之后不可修改，但是可以添加新的， 调用其中一个即可，之后就一直按照新的配置发送通知*/

~~~

### 安卓部分手机wifi状态下，休眠的时候 wifi 会断开连接，可以调用下面的代码 使休眠的时候保持wifi 连接
~~~
keep.wifilock();// 休眠时锁定wifi

~~~
~~~
keep.wifiunlock();// 休眠时取消锁定wifi
~~~

### android保活插件QQ 群  
### 
群号  1015300456 ，欢迎进群交流学习









