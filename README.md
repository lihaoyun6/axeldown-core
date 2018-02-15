# axeldown-core

基于axel-webm的优化项目. 通过webui调用axel进行下载

## 使用方法

下载和编译:

``` bash
$ git clone https://github.com/lihaoyun6/axeldown-core.git
$ cd axeldown-core
$ chmod a+x build.sh
$ ./build.sh
```

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

## 打赏
<div>
<img src="donate/alipay.png" width = "200" alt="支付宝" align=center />
<img src="donate/wechatpay.png" width = "200" alt="微信" align=center />
</div>
