原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/26/16313563.html
提交日期：Thu, 26 May 2022 07:13:00 GMT
博文内容：
安装 pip 包报错：
```
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7fc50528c710>: Failed to establish a new connection: [Errno 111] Connection refused'))': /simple
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7fc50528c590>: Failed to establish a new connection: [Errno 111] Connection refused'))': /simple
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7fc50528cd50>: Failed to establish a new connection: [Errno 111] Connection refused'))': /simple
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7fc50528cbd0>: Failed to establish a new connection: [Errno 111] Connection refused'))': /simple
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7fc50528cd90>: Failed to establish a new connection: [Errno 111] Connection refused'))': /simple
ERROR: Could not install packages due to an EnvironmentError: HTTPSConnectionPool(host='pypi.doubanio.com', port=443): Max retries exceeded with url: /simple (Caused by ProxyError('Cannot connect to proxy.', NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7fc50528ce10>: Failed to establish a new connection: [Errno 111] Connection refused')))
```
代理问题，解决方案
```
unset no_proxy;unset https_proxy
```
[参考连接](https://blog.csdn.net/ao1886/article/details/114283556)
