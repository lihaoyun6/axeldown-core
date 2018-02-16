# 百度云分享直链提取方法  

## 安装插件与脚本  

[点此](http://tampermonkey.net)前往浏览器插件安装页面  

[点此](https://greasyfork.org/zh-CN/scripts/38418-ax-百度云盘)前往用户脚本下载页面  

## 使用脚本  

安装好插件和脚本后, 再打开百度云分享链接网页, 会看到页面上多了一个按钮  

![axmain](https://github.com/lihaoyun6/axeldown-core/blob/master/screenshot/axmain.jpg)  

"普通下载"是使用浏览器来下载文件, 速度很慢, 不建议使用

"Axel下载"按钮会展开一个对话框  

![axdown](https://github.com/lihaoyun6/axeldown-core/blob/master/screenshot/axdown.jpg)  

"复制链接并用Axeldown下载"按钮会将解析出的链接发送至剪贴板, 并向9998端口发送下载请求  

````
•发送下载任务需要保证Axeldown服务已经开启, 并同意脚本的跨站请求.  
•此功能暂时不太成熟, 无法自动解析文件名, 所以不太建议点击此按钮, 而是建议直接全选并复制框内的链接.  
•另外建议启动Axeldown时请避开9998端口, 此端口是我为调试预留的, 可能会有很多实验性功能指向此端口.  
````

将复制后的下载地址粘贴到Axeldown控制面板的新建任务界面, 然后按照步骤设置参数进行下载即可
