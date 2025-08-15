# xtf-usage
# Android监听系统所有应用进入前后台
# uniapp
~~~
<template>
	<view class="content">
		<button style="margin: 10rpx;" type="primary" @click="onClick(0)">检测是否有使用记录权限</button>
		<button style="margin: 10rpx;" type="primary" @click="onClick(1)">申请使用记录权限</button>
		<button style="margin: 10rpx;" type="primary" @click="onClick(2)">开启监听手机前后台应用</button>
		<button style="margin: 10rpx;" type="primary" @click="onClick(3)">取消监听手机前后台应用</button>
	</view>
</template>

<script>
	import {hasUsageStatsPermission,requestUsageStatsPermission,appListener,stopAppListener} from "@/uni_modules/xtf-usage"
	
	export default {
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {
			onClick(id){
				var that=this;
				if(id==0){
					
					uni.showToast({
						icon:"none",
						title:""+hasUsageStatsPermission()
					})
				}else if(id==1){
					requestUsageStatsPermission();
				}else if(id==2){
					appListener(function(b,pkg){
						console.log(b,pkg);
						
					})
				}else if(id==3){
					stopAppListener();
				}else if(id==4){
				}
			},
		}
	}
</script>

<style>
	.logo {
		height: 100px;
		width: 100px;
		margin: 100px auto 25px auto;
	}

	.title {
		font-size: 18px;
		color: #8f8f94;
    text-align: center;
	}
</style>

~~~

# uniappx
~~~
<template>
	<view class="content">
		<button style="margin: 10rpx;" type="primary" @click="onClick(0)">检测是否有使用记录权限</button>
		<button style="margin: 10rpx;" type="primary" @click="onClick(1)">申请使用记录权限</button>
		<button style="margin: 10rpx;" type="primary" @click="onClick(2)">开启监听手机前后台应用</button>
		<button style="margin: 10rpx;" type="primary" @click="onClick(3)">取消监听手机前后台应用</button>
	</view>
</template>

<script>
	import {hasUsageStatsPermission,requestUsageStatsPermission,appListener,stopAppListener} from "@/uni_modules/xtf-usage"
	
	export default {
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {
			onClick(id:number){
				var that=this;
				if(id==0){
					
					uni.showToast({
						icon:"none",
						title:""+hasUsageStatsPermission()
					})
				}else if(id==1){
					requestUsageStatsPermission();
				}else if(id==2){
					appListener(function(b:boolean,pkg:string){
						console.log(b,pkg);
						
					})
				}else if(id==3){
					stopAppListener();
				}else if(id==4){
				}
			},
		}
	}
</script>

<style>
	.logo {
		height: 100px;
		width: 100px;
		margin: 100px auto 25px auto;
	}

	.title {
		font-size: 18px;
		color: #8f8f94;
    text-align: center;
	}
</style>

~~~



### 开发文档
[UTS 语法](https://uniapp.dcloud.net.cn/tutorial/syntax-uts.html)
[UTS API插件](https://uniapp.dcloud.net.cn/plugin/uts-plugin.html)
[UTS uni-app兼容模式组件](https://uniapp.dcloud.net.cn/plugin/uts-component.html)
[UTS 标准模式组件](https://doc.dcloud.net.cn/uni-app-x/plugin/uts-vue-component.html)
[Hello UTS](https://gitcode.net/dcloud/hello-uts)