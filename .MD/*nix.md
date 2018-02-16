下载和编译:

``` bash
$ git clone https://github.com/lihaoyun6/axeldown-core.git
$ cd axeldown-core
$ chmod a+x build.sh
$ ./build.sh
```
![clone](https://github.com/lihaoyun6/axeldown-core/blob/master/screenshot/build.jpg)

环境准备:

因为项目基于web.py模块提供服务, 故需要先安装web.py

``` bash
$ sudo easy_install web.py
```

启动运行:

``` bash
$ cd axeldown-core
$ python axeldown.py [自定义端口]
```
例如
``` bash
$ python axeldown.py 2333
```
(不使用自定义端口时, 默认在8080端口开启服务)

启动服务后在浏览器中打开"<http://127.0.0.1:端口>"即可看到管理界面

![run](https://github.com/lihaoyun6/axeldown-core/blob/master/screenshot/run.jpg)

PS: 下载过程中可以关闭浏览器, 但不要关闭终端窗口

## 下载百度云文件

首先需要提取待下载的百度云文件的直链([点此](baidu.md)查看提取教程)

点击管理界面左上角的"+", 弹出新建任务界面, 然后将复制好的直链地址粘贴到"下载地址"输入框内

再根据当前网络的带宽以及待下载文件的体积, 设定合适的"线程数"(对于百度云文件, 建议最少不要低于32线程)

由于当前版本不支持自动解析百度云直链文件名, 需要手动设置文件名

PS: 建议在"设置"中
