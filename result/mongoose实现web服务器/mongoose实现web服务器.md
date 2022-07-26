原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/14/16271138.html
提交日期：Sat, 14 May 2022 11:43:00 GMT
博文内容：
# 1.简介
Mongoose Web Server是一款易于使用的Web服务器，它可以嵌入到其它应用程序中，为其提供Web接口。
mongoose的代码着实轻量，先看看它的特点：
1. 在整个的实现是使用C语言编写
2. 整个代码也只有一个mongoose.c和mongoose.h两个文件， 从引入第三方的考虑上也着实不多。
3. 实现的功能还是非常多的，从使用的层面上来说功能还是比较全面。只不过不知道是否是为了第三方使用的方便还是怎么地，它的代码只用了两个源文件罢了。诸多的功能也大以宏的开始与结束来区分。
4. 示例非常齐全，所有的功能都有单独的示例。
5.支持夸平台。


# 2.数据结构
## 2.1.mg_mgr

mg_mgr是mongoose中进行事件管理的结构体，事件分为5种类型， 共享同一个回调函数，事件类型通过传参区分。
```
#define MG_EV_POLL 0    /* Sent to each connection on each mg_mgr_poll() call */
#define MG_EV_ACCEPT 1  /* New connection accepted. union socket_address * */
#define MG_EV_CONNECT 2 /* connect() succeeded or failed. int *  */
#define MG_EV_RECV 3    /* Data has been received. int *num_bytes */
#define MG_EV_SEND 4    /* Data has been written to a socket. int *num_bytes */
#define MG_EV_CLOSE 5   /* Connection is closed. NULL */
#define MG_EV_TIMER 6   /* now >= conn->ev_timer_time. double * */
```
完整数据结构如下：
```
/*
 * Mongoose event manager.
 */
struct mg_mgr {
  struct mg_connection *active_connections;
#if MG_ENABLE_HEXDUMP
  const char *hexdump_file; /* Debug hexdump file path */
#endif
#if MG_ENABLE_BROADCAST
  sock_t ctl[2]; /* Socketpair for mg_broadcast() */
#endif
  void *user_data; /* User data */
  int num_ifaces;
  struct mg_iface **ifaces; /* network interfaces */
  const char *nameserver;   /* DNS server to use */
};

#define MG_SOCKET_IFACE_VTABLE \
{ \
mg_socket_if_init, \
mg_socket_if_free, \
mg_socket_if_add_conn, \
mg_socket_if_remove_conn, \
mg_socket_if_poll, \
mg_socket_if_listen_tcp, \
mg_socket_if_listen_udp, \
mg_socket_if_connect_tcp, \
mg_socket_if_connect_udp, \
mg_socket_if_tcp_send, \
mg_socket_if_udp_send, \
mg_socket_if_recved, \
mg_socket_if_create_conn, \
mg_socket_if_destroy_conn, \
mg_socket_if_sock_set, \
mg_socket_if_get_conn_addr, \
}
```
重要成员：
```
active_connections ：当前活动的连接，如果有多个，则以链表形式挂接
ctl：　broadcast 的socket
ifaces：网络相关的接口集合，在linux下默认为socket相关接口 
```


## 2.2. mg_connection
mg_connection是一个具体连接实例 

完整数据结构如下：
```
/*
 * Mongoose connection.
 */
struct mg_connection {
  struct mg_connection *next, *prev; /* mg_mgr::active_connections linkage */
  struct mg_connection *listener;    /* Set only for accept()-ed connections */
  struct mg_mgr *mgr;                /* Pointer to containing manager */

  sock_t sock; /* Socket to the remote peer */
  int err;
  union socket_address sa; /* Remote peer address */
  size_t recv_mbuf_limit;  /* Max size of recv buffer */
  struct mbuf recv_mbuf;   /* Received data */
  struct mbuf send_mbuf;   /* Data scheduled for sending */
  time_t last_io_time;     /* Timestamp of the last socket IO */
  double ev_timer_time;    /* Timestamp of the future MG_EV_TIMER */
#if MG_ENABLE_SSL
  void *ssl_if_data; /* SSL library data. */
#endif
  mg_event_handler_t proto_handler; /* Protocol-specific event handler */
  void *proto_data;                 /* Protocol-specific data */
  void (*proto_data_destructor)(void *proto_data);
  mg_event_handler_t handler; /* Event handler function */
  void *user_data;            /* User-specific data */
  union {
    void *v;
    /*
     * the C standard is fussy about fitting function pointers into
     * void pointers, since some archs might have fat pointers for functions.
     */
    mg_event_handler_t f;
  } priv_1;
  void *priv_2;
  void *mgr_data; /* Implementation-specific event manager's data. */
  struct mg_iface *iface;
  unsigned long flags;
/* Flags set by Mongoose */
#define MG_F_LISTENING (1 << 0)          /* This connection is listening */
#define MG_F_UDP (1 << 1)                /* This connection is UDP */
#define MG_F_RESOLVING (1 << 2)          /* Waiting for async resolver */
#define MG_F_CONNECTING (1 << 3)         /* connect() call in progress */
#define MG_F_SSL (1 << 4)                /* SSL is enabled on the connection */
#define MG_F_SSL_HANDSHAKE_DONE (1 << 5) /* SSL hanshake has completed */
#define MG_F_WANT_READ (1 << 6)          /* SSL specific */
#define MG_F_WANT_WRITE (1 << 7)         /* SSL specific */
#define MG_F_IS_WEBSOCKET (1 << 8)       /* Websocket specific */

/* Flags that are settable by user */
#define MG_F_SEND_AND_CLOSE (1 << 10)       /* Push remaining data and close  */
#define MG_F_CLOSE_IMMEDIATELY (1 << 11)    /* Disconnect */
#define MG_F_WEBSOCKET_NO_DEFRAG (1 << 12)  /* Websocket specific */
#define MG_F_DELETE_CHUNK (1 << 13)         /* HTTP specific */
#define MG_F_ENABLE_BROADCAST (1 << 14)     /* Allow broadcast address usage */
#define MG_F_TUN_DO_NOT_RECONNECT (1 << 15) /* Don't reconnect tunnel */

#define MG_F_USER_1 (1 << 20) /* Flags left for application */
#define MG_F_USER_2 (1 << 21)
#define MG_F_USER_3 (1 << 22)
#define MG_F_USER_4 (1 << 23)
#define MG_F_USER_5 (1 << 24)
#define MG_F_USER_6 (1 << 25)
};
```
结构体重要成员：
```
next、prev：  下、上一个连接
mgr：对应的事件管理
sock： 对应的socket
sa： socket的地址
recv_mbuf、send_mbuf ： 发送和接受的buffer
proto_handler、handler： 协议的回调函数和事件回调函数
```



## 2.3.实现方式

整个流程其实很简单，可分为以下三步

1.mg_mgr_init：先对mgr进行初始化，主要是将相关的socket接口函数集合赋值给mgr.ifaces

2.mg_bind：该步骤主要为一个mg_connection申请内存，并将事件回调函数ev_handler注册到该连接里，并且初始化若干个（由网卡数量决定）http端口的socket进行监听

3.mg_mgr_poll：该函数调用mongoose中提供的poll接口：mg_socket_if_poll。在该函数中，对所有初始化的socket进行select操作,在退出select的阻塞后，根据read_fd_set, write_fd_set, err_fd_set 进行判断，将退出阻塞的socket分类，然后进行分类处理。


# 3.使用 mongoose 实现简单的封装

在https://github.com/cesanta/mongoose中下载mongoose.c和mongoose.h两个文件

HttpService .h 的实现：
```
#pragma once
 
/*
Http服务
*/
 
 
#ifdef _WIN32
#include <winsock2.h>
#include <stdio.h>
#pragma comment(lib,"ws2_32.lib")
#endif
 
#include "mongoose.h"
 
class HttpService {
  public:
    bool start(const char *port);
  private:
    static void mgEvHandler(struct mg_connection *nc, int ev, void *p);
    static void mgSendBody(struct mg_connection *nc, const char *content); //发送body信息
    static void mgSendFile(struct mg_connection *nc, struct http_message *hm, const char* filePath);
    static struct mg_serve_http_opts s_http_server_opts;
};
```
HttpService .cpp 的实现：
```
  
#include "HttpService.h"
 
struct mg_serve_http_opts HttpService::s_http_server_opts;
 
//请求事件处理
void HttpService::mgEvHandler(struct mg_connection *nc, int ev, void *p) { // 形参好像固定是这三种类型
    //处理request
    if (ev == MG_EV_HTTP_REQUEST) {
        struct http_message *msg = (struct http_message *)p;
 
        //body内容
        char* body = new char[msg->body.len + 1];
        memset(body, 0, msg->body.len + 1);
        memcpy(body, msg->body.p, msg->body.len);
 
        //uri内容
        char* uri = new char[msg->uri.len + 1];
        memset(uri, 0, msg->uri.len + 1);
        memcpy(uri, msg->uri.p, msg->uri.len);
 
        //返回body信息
        mgSendBody(nc, "body content");
 
        //返回下载文件
        //mgSendFile("相对于s_http_server_opts.document_root的文件路径");
 
        delete uri;
        delete body;
    }
}
 
//发送body信息
void HttpService::mgSendBody(struct mg_connection *nc, const char *content) {
    mg_send_head(nc, 200, strlen(content), "Content-Type: text/plain\r\nConnection: close");
    mg_send(nc, content, strlen(content));
    nc->flags |= MG_F_SEND_AND_CLOSE;
}
 
//发送文件，文件的位置是相对于s_http_server_opts.document_root的路径
void HttpService::mgSendFile(struct mg_connection *nc, struct http_message *hm, const char* filePath) {
    mg_http_serve_file(nc, hm, filePath, mg_mk_str("text/plain"), mg_mk_str(""));
}
 
//初始化并启动
bool HttpService::start(const char *port) {
    struct mg_mgr mgr;
    struct mg_connection *nc;
 
    mg_mgr_init(&mgr, NULL);
    printf("Starting web server on port %s\n", port);
    nc = mg_bind(&mgr, port, mgEvHandler);
    if (nc == NULL) {
        printf("Failed to create listener\n");
        return false;
    }
 
    // Set up HTTP server parameters
    mg_set_protocol_http_websocket(nc);
    s_http_server_opts.document_root = ".";  //文件相对路径 Serve current directory
    s_http_server_opts.enable_directory_listing = "yes";
 
    for (;;) {
        mg_mgr_poll(&mgr, 1000); //1s轮训一次
    }
    mg_mgr_free(&mgr);
 
    return true;
}

int main(){
	HttpService server;
	server.start("8090");
	return 0;
}
```

运行命令：
```
g++ mongoose.c HttpService.cpp -lpthread -o server
```
HttpService.cpp调用mongoose.c中的函数，即C++中调用c，不知道为什么，可以直接进行编译，不过要加上-lpthread就行










参考：[mongoose(WEB服务器) 简单走读](https://www.cnblogs.com/luo-ruida/p/7732287.html)

[利用mongoose实现http服务](https://blog.csdn.net/houxian1103/article/details/113765217)
[C语言和C++的混合编译](http://c.biancheng.net/view/7494.html)