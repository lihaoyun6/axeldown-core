## 下载和编译:

``` bash
$ git clone https://github.com/lihaoyun6/axeldown-core.git
$ cd axeldown-core
$ chmod a+x build.sh
$ ./build.sh
```
![clone](https://github.com/lihaoyun6/axeldown-core/blob/master/screenshot/build.jpg)

## 环境准备:

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

默认下载目录为当前用户的家目录, 如需永久更改请使用"设置"按钮进行更改, "新建"界面设置下载目录仅对当前任务生效 

PS: 下载过程中可以关闭浏览器, 但不要关闭终端窗口

## 下载百度云文件

首先保证下载服务已经开启, 然后[点此查看](baidu.md)百度云下载任务导出教程    

## 打赏
<div>
<img src="../donate/alipay.png" width = "200" alt="支付宝" align=center />
<img src="../donate/wechatpay.png" width = "200" alt="微信" align=center />
</div>
