原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16244095.html
提交日期：Sat, 07 May 2022 12:45:00 GMT
博文内容：
# 1.select处理带外数据
Linux下实现I/O复用的系统调用主要有select、poll和epoll
select系统调用：在一段指定时间内，监听用户感兴趣的文件描述符上的可读、可写和异常等事件
socket上接收到普通数据和带外数据都将使select返回，但socket处于不同的就绪状态：前者处于可读状态，后者处于异常状态。代码清单9-1描述了select是如何同时处理二者的。
```
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <assert.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
	if (argc <= 2)
	{
		printf("usage: %s ip_address port_number\n", basename(argv[0]));
		return 1;
	}
	const char* ip = argv[1];
	int port = atoi(argv[2]);
	printf("ip is %s and port is %d\n", ip, port);

	int ret = 0;
	struct sockaddr_in address;
	bzero(&address, sizeof(address));
	address.sin_family = AF_INET;
	inet_pton(AF_INET, ip, &address.sin_addr);
	address.sin_port = htons(port);

	int listenfd = socket(PF_INET, SOCK_STREAM, 0);
	assert(listenfd >= 0);

	ret = bind(listenfd, (struct sockaddr*)&address, sizeof(address));
	assert(ret != -1);

	ret = listen(listenfd, 5);
	assert(ret != -1);

	struct sockaddr_in client_address;
	socklen_t client_addrlength = sizeof(client_address);
	int connfd = accept(listenfd, (struct sockaddr*)&client_address, &client_addrlength);
	if (connfd < 0)
	{
		printf("errno is: %d\n", errno);
		close(listenfd);
	}

	char remote_addr[INET_ADDRSTRLEN];
	printf("connected with ip: %s and port: %d\n", inet_ntop(AF_INET, &client_address.sin_addr, remote_addr, INET_ADDRSTRLEN), ntohs(client_address.sin_port));

	char buf[1024];
	fd_set read_fds;
	fd_set exception_fds;

	// 每次调用select前都要重新在read_fds和exception_fds中设置文件描述符connfd，
	// 因为事件发生之后，文件描述符集合将被内核修改
	FD_ZERO(&read_fds);  // 清除fdset的所有位
	FD_ZERO(&exception_fds);

	int nReuseAddr = 1;
	setsockopt(connfd, SOL_SOCKET, SO_OOBINLINE, &nReuseAddr, sizeof(nReuseAddr));
	while (1)
	{
		memset(buf, '\0', sizeof(buf));
		FD_SET(connfd, &read_fds);
		FD_SET(connfd, &exception_fds);

		ret = select(connfd + 1, &read_fds, NULL, &exception_fds, NULL);
		printf("select one\n");
		if (ret < 0)
		{
			printf("selection failure\n");
			break;
		}

		// 对于可读事件，采用普通的recv函数读取数据
		if (FD_ISSET(connfd, &read_fds))
		{
			ret = recv(connfd, buf, sizeof(buf) - 1, 0);
			if (ret <= 0)
			{
				break;
			}
			printf("get %d bytes of normal data: %s\n", ret, buf);
		}

		// 对于异常事件，采用带MSG_OOB标志的recv函数读取带外数据
		else if (FD_ISSET(connfd, &exception_fds))
		{
			ret = recv(connfd, buf, sizeof(buf) - 1, MSG_OOB);
			if (ret <= 0)
			{
				break;
			}
			printf("get %d bytes of oob data: %s\n", ret, buf);
		}

	}

	close(connfd);
	close(listenfd);
	return 0;
}
```
采用书中代码清单5-6（即[链接](https://www.cnblogs.com/codingbigdog/p/16243321.html)第五节的）来发送外带数据，为什么无法进入else if (FD_ISSET(connfd, &exception_fds))中



# 2. LT和ET模式
这段代码没看懂。。。
```
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <assert.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <pthread.h>

#define MAX_EVENT_NUMBER 1024
#define BUFFER_SIZE 10

// 将文件描述符设置成非阻塞的
int setnonblocking(int fd)
{
	int old_option = fcntl(fd, F_GETFL); //fcntl()用来操作文件描述词的一些特性.。
										 // F_GETFL 取得文件描述词状态旗标, 此旗标为open()的参数flags.常见的flags为只读只写等
	int new_option = old_option | O_NONBLOCK; // 设置成非阻塞的
	fcntl(fd, F_SETFL, new_option);		 // F_SETFL 设置文件描述词状态旗标, 参数arg 为新旗标, 但只允许O_APPEND、
										// O_NONBLOCK 和O_ASYNC 位的改变, 其他位的改变将不受影响
	return old_option;
}

// 将文件描述符fd上的EPOLLIN注册到epollfd指示的epoll内核事件表中，参数enable_et指定是否对fd启用ET模式
void addfd(int epollfd, int fd, bool enable_et)
{
	epoll_event event;
	event.data.fd = fd;
	event.events = EPOLLIN;
	if (enable_et)
	{
		event.events |= EPOLLET;
	}
	epoll_ctl(epollfd, EPOLL_CTL_ADD, fd, &event);
	setnonblocking(fd);
}

// LT模式的工作流程
void lt(epoll_event* events, int number, int epollfd, int listenfd)
{
	char buf[BUFFER_SIZE];
	for (int i = 0; i < number; i++)
	{
		int sockfd = events[i].data.fd;
		if (sockfd == listenfd)
		{
			struct sockaddr_in client_address;
			socklen_t client_addrlength = sizeof(client_address);
			int connfd = accept(listenfd, (struct sockaddr*)&client_address, &client_addrlength);
			addfd(epollfd, connfd, false);   // 对connfd禁用ET模式
		}
		else if (events[i].events & EPOLLIN)
		{
		// 只要socket读缓存中还有未读出的数据，这段代码就被触发
			printf("event trigger once\n");
			memset(buf, '\0', BUFFER_SIZE);
			int ret = recv(sockfd, buf, BUFFER_SIZE - 1, 0);
			if (ret <= 0)
			{
				close(sockfd);
				continue;
			}
			printf("get %d bytes of content: %s\n", ret, buf);
		}
		else
		{
			printf("something else happened \n");
		}
	}
}

// ET模式的工作流程
void et(epoll_event* events, int number, int epollfd, int listenfd)
{
	char buf[BUFFER_SIZE];
	for (int i = 0; i < number; i++)
	{
		int sockfd = events[i].data.fd;
		if (sockfd == listenfd)
		{
			struct sockaddr_in client_address;
			socklen_t client_addrlength = sizeof(client_address);
			int connfd = accept(listenfd, (struct sockaddr*)&client_address, &client_addrlength);
			addfd(epollfd, connfd, true);
		}
		else if (events[i].events & EPOLLIN)
		{
			printf("event trigger once\n");
			while (1)
			{
				memset(buf, '\0', BUFFER_SIZE);
				int ret = recv(sockfd, buf, BUFFER_SIZE - 1, 0);
				if (ret < 0)
				{
					if ((errno == EAGAIN) || (errno == EWOULDBLOCK))
					{
						printf("read later\n");
						break;
					}
					close(sockfd);
					break;
				}
				else if (ret == 0)
				{
					close(sockfd);
				}
				else
				{
					printf("get %d bytes of content: %s\n", ret, buf);
				}
			}
		}
		else
		{
			printf("something else happened \n");
		}
	}
}

int main(int argc, char* argv[])
{
	if (argc <= 2)
	{
		printf("usage: %s ip_address port_number\n", basename(argv[0]));
		return 1;
	}
	const char* ip = argv[1];
	int port = atoi(argv[2]);

	int ret = 0;
	struct sockaddr_in address;
	bzero(&address, sizeof(address));
	address.sin_family = AF_INET;
	inet_pton(AF_INET, ip, &address.sin_addr);
	address.sin_port = htons(port);

	int listenfd = socket(PF_INET, SOCK_STREAM, 0);
	assert(listenfd >= 0);

	ret = bind(listenfd, (struct sockaddr*)&address, sizeof(address));
	assert(ret != -1);

	ret = listen(listenfd, 5);
	assert(ret != -1);

	epoll_event events[MAX_EVENT_NUMBER];
	int epollfd = epoll_create(5);
	assert(epollfd != -1);
	addfd(epollfd, listenfd, true);

	while (1)
	{
		int ret = epoll_wait(epollfd, events, MAX_EVENT_NUMBER, -1);
		if (ret < 0)
		{
			printf("epoll failure\n");
			break;
		}

		lt(events, ret, epollfd, listenfd);
		//et( events, ret, epollfd, listenfd );
	}

	close(listenfd);
	return 0;
}
```
