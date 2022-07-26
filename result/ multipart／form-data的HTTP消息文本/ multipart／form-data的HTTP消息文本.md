原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/28/16321759.html
提交日期：Sat, 28 May 2022 11:53:00 GMT
博文内容：
下面是通过post方式发送的请求：
```
POST http://www.example.com HTTP/1.1
Content-Type:multipart/form-data; boundary=----WebKitFormBoundaryyb1zYhTI38xpQxBK

------WebKitFormBoundaryyb1zYhTI38xpQxBK
Content-Disposition: form-data; name="city_id"

111111
------WebKitFormBoundaryyb1zYhTI38xpQxBK
Content-Disposition: form-data; name="company_id"

222222
------WebKitFormBoundaryyb1zYhTI38xpQxBK
Content-Disposition: form-data; name="file"; filename="chrome.png"
Content-Type: image/png

PNG ... content of chrome.png ...
```
第一行是请求行，指明了方法、URI 和 HTTP 版本号；
第二行是消息头（简单起见，只有一个 Content-Type)；
然后空出一行；
接下来就是消息体。可以看到使用 multipart/form-data 时，消息体通过 boundary 来分隔多个字段，被分隔的每个字段都有自己的小头部和小消息体，且也用空行分隔。






参考：[multipart/form-data的HTTP消息文本](https://www.jianshu.com/p/8251fff48a59)