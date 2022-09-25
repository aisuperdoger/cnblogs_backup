原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/08/29/16636443.html
提交日期：Mon, 29 Aug 2022 08:43:00 GMT
博文内容：
Nginx中有一个 master 进程和多个 worker 进程，master 进程主要用来管理 worker 进程， worker用于处理网络请求。通过向master发送信号，就可以管理master和worker，如./nginx -s reload就是向master发送了reload信号。

一个连接请求过来，每个进程worker都有可能处理这个连接，怎么做到的呢？首先，每个 worker 进程都是从 master 进程 fork 过来，在 master 进程里面，先建立好需要 listen 的 socket（listenfd）之后，然后再 fork 出多个 worker 进程。所有 worker 进程的 listenfd 会在新连接到来时变得可读，为保证只有一个进程处理该连接，所有 worker 进程在注册 listenfd 读事件前抢 accept_mutex，抢到互斥锁的那个进程注册 listenfd 读事件，在读事件里调用 accept 接受该连接。当一个 worker 进程在 accept 这个连接之后，就开始读取请求，解析请求，处理请求，产生数据后，再返回给客户端，最后才断开连接，这样一个完整的请求就是这样的了。我们可以看到，一个请求，完全由 worker 进程来处理，而且只在一个 worker 进程中处理。
使用epoll等实现高并发。

参考：https://www.w3cschool.cn/nginx/sd361pdz.html