# 百度云直接调用Axel下载教程  

## 安装插件与脚本  

[点此](http://tampermonkey.net)前往浏览器插件安装页面\(Chrome用户[点此](https://raw.githubusercontent.com/lihaoyun6/web/master/Tampermonkey_v4.6.crx)免翻墙下载\)  

[点此](https://greasyfork.org/zh-CN/scripts/38418-ax-百度云盘)前往用户脚本下载页面  

## 使用脚本  

安装好插件和脚本后, 再打开百度云分享或自己的文件管理页面, 会看到页面上多了一个"AX-下载"按钮  

![axmain](https://github.com/lihaoyun6/ax-baiduyunpan/blob/master/screenshot/axdmain.jpg)  

![axmain](https://github.com/lihaoyun6/ax-baiduyunpan/blob/master/screenshot/axdmain2.jpg)  

````
•"AX-压缩下载"可以在一定程度上绕过百度云的10KB限速, 但是不建议经常使用
````

点击"Axel下载"按钮会展开一个对话框  

"发送到Axeldown下载"按钮会将解析出的链接发送至指定的下载服务器端口, 可以设置当前任务使用的线程数量  

![axdown](https://github.com/lihaoyun6/ax-baiduyunpan/blob/master/screenshot/axdurl.jpg)  

发送下载任务需要授予跨站访问权限, 弹出此窗口时, 请点击"允许域名"即可  

![xss](https://github.com/lihaoyun6/ax-baiduyunpan/blob/master/screenshot/xss.jpg)  

通过"AX-下载">"下载设置"可以自定义Axeldown服务器地址和端口以及默认下载线程数(默认为http://127.0.0.1:2333).  

![axconf](https://github.com/lihaoyun6/ax-baiduyunpan/blob/master/screenshot/axdconf.jpg)  

````
•发送下载任务需要保证Axeldown服务已经开启, 并同意脚本的跨站请求.    
•脚本支持自动解析单选/多选模式下的文件名, 以及单选/多选模式下的文件夹打包文件名, 无需手动指定下载文件名.  
````

## 修复解压  

通过多选方式打包下载的文件, 如果大小超过4G, 很有可能导致无法正常解压.  

macOS平台可以点击Axeldown管理界面中的"设置">"修复解压"并选择要解压的打包zip文件来进行解压 

Linux以及Unix平台可以使用[此项目](https://github.com/ccloli/baidupan-zip-extract)来修复并解压此种特殊zip文件(需nodejs环境)  

## 打赏
<div>
<img src="../donate/alipay.png" width = "200" alt="支付宝" align=center />
<img src="../donate/wechatpay.png" width = "200" alt="微信" align=center />
</div>
