原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/19/16290593.html
提交日期：Thu, 19 May 2022 14:50:00 GMT
博文内容：
#1.UDP和TCP区别
TCP: 传输控制协议   安全可靠  丢包重传   面向连接(电话模型) 
UDP: 用户数据报协议  不安全不可靠 丢包不重传  快 不面向连接(邮件模型)，可在应用层是实现安全可靠和丢包重传等内容


**tcp通信流程:**
服务器: 创建流式套接字 绑定 监听 提取 读写 关闭
客户端: 创建流式套接字 连接 读写 关闭
收发数据:
read或recv（推荐使用recv）:
ssize_t recv(int sockfd, void *buf, size_t len, int flags);//flags==MSG_PEEK时， 读数据但不会删除缓冲区的数据
write或send（推荐使用send）:
ssize_t send(int sockfd, const void *buf, size_t len, int flags);//flags一般填0，flags=1代表发送紧急数据

**udp通信流程：**
服务器: 创建报式套接字 绑定 读写 关闭
客户端: 创建报式套接字 读写  关闭
发数据:
```
ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
                      const struct sockaddr *dest_addr, socklen_t addrlen);
flags一般写0
dest_addr: 目的地的地址信息
addrlen: 结构体大小
```
收数据:
```
ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags,
                        struct sockaddr *src_addr, socklen_t *addrlen);
flags一般写0
src_addr: 对方的地址信息
addrlen: 结构体大小的地址
```




#　2.UDP通信
创建报式套接字
```
int socket(int domain, int type, int protocol);
参数:
    domain : AF_INET
    type :SOCK_DGRAM
    protocol :0
```
**UDP服务器upd_server.c**
```
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char *argv[])
{
	//创建套接字
	int fd = socket(AF_INET,SOCK_DGRAM,0);
	//绑定
	struct sockaddr_in myaddr;
	myaddr.sin_family = AF_INET;
	myaddr.sin_port = htons(8888);
	myaddr.sin_addr.s_addr = inet_addr("127.0.0.1"); // inet_addr只用于IPv4，inet_pton可用于IPv4和IPv6
	int ret = bind(fd,(struct sockaddr*)&myaddr,sizeof(myaddr));
	if(ret < 0)
	{
		perror("");
		return 0;
	}
	//读写
	char buf[1500]="";
	struct sockaddr_in cliaddr;
	socklen_t len = sizeof(cliaddr);
	while(1)
	{
		memset(buf,0,sizeof(buf)); // 清空，不然会残留上次收到的数据
		int n = recvfrom(fd,buf,sizeof(buf),0,(struct sockaddr *)&cliaddr,&len);
		if(n < 0)
		{
			perror("");
			break;
		}
		else
		{
			printf("%s\n",buf);
			sendto(fd,buf,n,0,(struct sockaddr *)&cliaddr,len);
		
		}
	}
	//关闭
	close(fd);
	return 0;
}
```
**UDP客户端udp_client.c**
```
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <stdlib.h>
int main(int argc, char *argv[])
{
	//创建套接字
	int fd = socket(AF_INET,SOCK_DGRAM,0);
	//绑定
	struct sockaddr_in myaddr;
	myaddr.sin_family = AF_INET;
	myaddr.sin_port = htons(9000);
	//inet_pton
	myaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	int ret = bind(fd,(struct sockaddr*)&myaddr,sizeof(myaddr));
	if(ret < 0)
	{
		perror("");
		return 0;
	}
	//读写
	char buf[1500]="";
	struct sockaddr_in cliaddr;
	socklen_t len = sizeof(cliaddr);

	struct sockaddr_in dstaddr;
	dstaddr.sin_family = AF_INET;
	dstaddr.sin_port = htons(8888);
	dstaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	int n=0;
	while(1)
	{
		n = read(STDIN_FILENO,buf,sizeof(buf));	
		sendto(fd,buf,n,0,(struct sockaddr *)&dstaddr,sizeof(dstaddr));
		memset(buf,0,sizeof(buf));
		 n = recvfrom(fd,buf,sizeof(buf),0,NULL,NULL);
		if(n < 0)
		{
			perror("");
		}
		else{
			printf("%s\n",buf);
		
		}
	}
	//关闭
	close(fd);
	return 0;
}
```
# 3.本地套接字实现进程通信（unix domain socket）
可以直接使用网络套接字实现进程通信，也可以使用本地套接字实现进程通信。

套接字用文件来标识,这个文件在绑定之前是不能存在

本地套接字可用于tcp和udp通信，这里以tcp通信为例。
```
int socket(int domain, int type, int protocol);
参数:
    domain : AF_UNIX
    type :SOCK_STREAM
    protocol : 0


绑定
int bind(int sockfd, const struct sockaddr *addr,
                socklen_t addrlen);
sockfd: 本地套接字
addr:  本地套接字结构体地址sockaddr_un
    struct sockaddr_un {
               sa_family_t sun_family;               /* AF_UNIX */
               char        sun_path[108];            /* pathname *///文件的路径名
               };
addrlen: sockaddr_un大小 


提取
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
    addr: struct sockaddr_un 结构体地址
```

**本地套接字实现tcp服务器：**
```
#include <stdio.h>
#include <fcntl.h>
#include <stddef.h>
#include <sys/socket.h>
#include <unistd.h>
#include <sys/un.h>
#include <arpa/inet.h>
int main(int argc, char *argv[])
{
	unlink("sock.s"); 	// 套接字用文件来标识,这个文件在绑定之前是不能存在。故先删除sock.s
	//创建unix流式套接
	int lfd = socket(AF_UNIX,SOCK_STREAM,0);
	//绑定
	struct sockaddr_un myaddr;
	myaddr.sun_family = AF_UNIX;
	strcpy(myaddr.sun_path ,"sock.s"); // 不能用myaddr.sun_path = "sock.s"。字符串不能用等号
	int len = offsetof(struct sockaddr_un,sun_path)+strlen(myaddr.sun_path); // offsetof(struct sockaddr_un,sun_path)相当于myaddr.sun_family的大小
	bind(lfd,(struct sockaddr *)&myaddr,len); // 也可以写成bind(lfd,(struct sockaddr *)&myaddr,sizeof(myaddr));
	//监听
	listen(lfd,128);
	
	//提取
	struct sockaddr_un cliaddr;
	socklen_t len_c = sizeof(cliaddr);
	int cfd = accept(lfd,(struct sockaddr*)&cliaddr,&len_c);

	printf("new cilent file = %s\n",cliaddr.sun_path);
	//读写
	char buf[1500]="";
	while(1)
	{
		int n = recv(cfd,buf,sizeof(buf),0);
		if(n <= 0)
		{
			printf("err or client close\n");
			break;
		}
		else
		{
			printf("%s\n",buf);
			send(cfd,buf,n,0);
		
		}
	
	}
	//关闭
	close(cfd);
	close(lfd);
	return 0;
}
```
**本地套接字客户端实现:**
```
#include <stdio.h>
#include <stddef.h>
#include <arpa/inet.h>
#include <sys/un.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char *argv[])
{
	unlink("sock.c");
	//创建unix流式套接字
	int cfd = socket(AF_UNIX,SOCK_STREAM,0);
	//如果不绑定,就是隐式绑定
	struct sockaddr_un myaddr;
	myaddr.sun_family = AF_UNIX;
	strcpy(myaddr.sun_path,"sock.c");
	int len = offsetof(struct sockaddr_un,sun_path)+strlen("sock.c");
	if(bind(cfd,(struct sockaddr*)&myaddr,len)< 0)
	{
		perror("");
		return 0;
	}
	//连接
	struct sockaddr_un seraddr;
	seraddr.sun_family = AF_UNIX;
	strcpy(seraddr.sun_path,"sock.s");
	connect(cfd,(struct sockaddr*)&seraddr,sizeof(seraddr));
	//读写
	while(1)
	{
		char buf[1500]="";
		int n = read(STDIN_FILENO,buf,sizeof(buf));
		send(cfd,buf,n,0);
		memset(buf,0,sizeof(buf));
		n = recv(cfd,buf,sizeof(buf),0);
		if(n <=0 )
		{
		
			printf("err or server close\n");
			break;
		
		}
		else
		{
			printf("%s\n",buf);
		
		}
	
	
	}
	//关闭
	close(cfd);
	return 0;
}
```
