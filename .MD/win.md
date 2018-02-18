## 请注意

此版Windows平台预编译版本使用了cygwin提供的桥接api来初步实现免移植的os.fork()函数使用  

(已使用Pyinstaller进行打包, 无需安装cygwin即可运行)  

不过也有许多适配性的bug, 比如某些链接下载时无法显示进度与速度, 部分情况下下载进度可以超过100%等  

- 仅供测试以及预览axeldown在Windows中的运行效果之用. 不推荐普通用户日常使用!!

欢迎fork, 欢迎移植  

# 使用方法

[点此](https://github.com/lihaoyun6/axeldown-core/releases/tag/1.2)前往下载页面, 并下载"Axeldown_beta_win.zip"  

解压后进入"axeldown"目录, 并双击运行"axeldown.exe"即可开启服务, 服务默认运行在8080端口 

(需要自定义服务端口请使用cmd调用axeldown.exe, 并将指定的端口号作为第一个输入参数)

然后在浏览器中打开"<http://127.0.0.1:端口>"即可看到管理界面  

![dwin](https://github.com/lihaoyun6/axeldown-core/blob/master/screenshot/dwin.jpg)

## 下载百度云文件

首先保证下载服务已经开启, 然后[点此](baidu.md)查看百度云下载任务导出教程    
