原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/10/16255825.html
提交日期：Tue, 10 May 2022 14:51:00 GMT
博文内容：
#1.高并发服务器实现方法
1.阻塞等待：进程开启线程去服务客户，每个线程服务一个客户，阻塞等待客户发送消息——消耗资源
2.非阻塞忙轮询：进程循环询问客户，问它上面是否有消息，有消息就进行处理。——消耗cpu
3.多路IO转接(多路IO复用): **内核**监听多个文件描述符的属性(**读写缓冲区**)变化。如果某个文件描述符的读缓冲区变化了,这个时候就是可以读了,将这个事件告知应用层
三种多路IO
- select：windwos中常用，select可跨平台
- poll：很少用
- epoll：linux中常用 

# 2.select函数
```
#include <sys/select.h>
 /* According to earlier standards */
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

int select(int nfds, fd_set *readfds, fd_set *writefds,
           fd_set *exceptfds, struct timeval *timeout);
功能: 监听多个文件描述符的属性变化(读,写,异常)
在集合中进行增删改查等操作:
       void FD_CLR(int fd, fd_set *set);
       int  FD_ISSET(int fd, fd_set *set);
       void FD_SET(int fd, fd_set *set);
       void FD_ZERO(fd_set *set);
参数:
    nfds  : 最大文件描述符+1。监听0~nfds的文件描述符
    readfds : 需要监听的读的文件描述符存放集合。事件：数据到达了读缓冲区，需要读出来了，触发读事件
    writefds :需要监听的写的文件描述符存放集合。事件：写缓存区满了，当写缓冲区有空余时，就触发可写事件。常设为NULL
    exceptfds : 需要监听的异常的文件描述符存放集合。常设为NULL
    timeout: 多长时间监听一次   固定的时间    NULL：永久监听
        struct timeval {
               long    tv_sec;         /* seconds */ 秒
               long    tv_usec;        /* microseconds */微妙
           };

返回值: 返回的是变化的文件描述符的个数
注意: 变化的文件描述符会存在监听的集合（readfds、writefds和exceptfds）中,未变化的文件描述符会从集合中删除
```

示例代码：
```
#include <stdio.h>
#include <sys/select.h>
#include <sys/types.h>
#include <unistd.h>
#include "wrap.h"
#include <sys/time.h>
#define PORT 8888
int main(int argc, char *argv[])
{
	//创建套接字,绑定
	int lfd = tcp4bind(PORT,NULL);
	//监听
	Listen(lfd,128);
	int maxfd = lfd;//最大的文件描述符
	fd_set oldset,rset;
	FD_ZERO(&oldset);
	FD_ZERO(&rset);
	//将lfd添加到oldset集合中
	FD_SET(lfd,&oldset);
	while(1)
	{	
		rset = oldset;//将oldset赋值给需要监听的集合rset
		
		int n = select(maxfd+1,&rset,NULL,NULL,NULL);
		if(n < 0)
		{
			perror("");
			break;
		}
		else if(n == 0)
		{
			continue;//如果没有变化,重新监听
		}
		else//监听到了文件描述符的变化
		{
			//lfd变化 代表有新的连接到来
			if( FD_ISSET(lfd,&rset))  // 变化的文件描述符都放在了rset集合中，如果lfd在rset中，就说明lfd变化了
			{
				struct sockaddr_in cliaddr;
				socklen_t len =sizeof(cliaddr);
				char ip[16]="";
				//提取新的连接
				int cfd = Accept(lfd,(struct sockaddr*)&cliaddr,&len);
				printf("new client ip=%s port=%d\n",inet_ntop(AF_INET,&cliaddr.sin_addr.s_addr,ip,16),
						ntohs(cliaddr.sin_port));
				//将cfd添加至oldset集合中,以下次监听
				FD_SET(cfd,&oldset);
				//更新maxfd
				if(cfd > maxfd)
					maxfd = cfd;
				//如果只有lfd变化,直接continue
				if(--n == 0)
					continue;

			}


			//cfd  遍历lfd之后的文件描述符是否在rset集合中,如果在则cfd变化
			for(int i = lfd+1;i<=maxfd;i++) // 假设现在 4-1023个文件描述符需要监听,但是5-1000这些文件描述符关闭了
                                                        // 本代码对于这种情况，还是遍历了4-1023
			{
				//如果i文件描述符在rset集合中
				if(FD_ISSET(i,&rset)) 
				{
					char buf[1500]=""; // 因为网络中的最大传输单元为1500
					int ret = Read(i,buf,sizeof(buf));
					if(ret < 0)//出错,将cfd关闭,从oldset中删除cfd
					{
						perror("");
						close(i);
						FD_CLR(i,&oldset);
					}
					else if(ret == 0) // 客户关闭了连接
					{
						printf("client close\n");
						close(i);
						FD_CLR(i,&oldset);
						
					}
					else
					{
						printf("%s\n",buf);
						Write(i,buf,ret);
					
					}
				
				}
				
			
			}
			
		
		}

		
	
	}

	return 0;
}
```

select优点: 跨平台
select缺点:
- 文件描述符数量限制在1024以下，需要修改内核的FD_SETSIZE参数，然后重新编译内核，才能修改1024
- 只是返回变化的文件描述符的个数,具体哪个那个变化需要遍历。当有大量的客户请求了连接但只有少量客户与服务器进行交互（即监听的文件描述符个数多，但是变化的文件描述符少），这种情况下，我们还是需要遍历全部的文件描述符才能找到变化的文件描述符。也就是说大量并发,少了活跃,select效率低。
- select对多个文件描述符进行监听是在内核中进行的，所以每次都需要将需要监听的文件描述集合由应用层符拷贝到内核

假设现在 4-1023个文件描述符需要监听,但是5-1000这些文件描述符关闭了?——本代码修改后，可以解决。解决如下：
```
//进阶版select，通过数组防止遍历1024个描述符
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <ctype.h>

#include "wrap.h"

#define SERV_PORT 8888

int main(int argc, char *argv[])
{
    int i, j, n, maxi;

    int nready, client[FD_SETSIZE];                 /* 自定义数组client, 防止遍历1024个文件描述符  FD_SETSIZE默认为1024 */
    int maxfd, listenfd, connfd, sockfd;
    char buf[BUFSIZ], str[INET_ADDRSTRLEN];         /* #define INET_ADDRSTRLEN 16 */
    struct sockaddr_in clie_addr, serv_addr;
    socklen_t clie_addr_len;
    fd_set rset, allset;                            /* rset 读事件文件描述符集合 allset用来暂存 */

    listenfd = Socket(AF_INET, SOCK_STREAM, 0);
    //端口复用
    int opt = 1;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));


    bzero(&serv_addr, sizeof(serv_addr));
    serv_addr.sin_family= AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port= htons(SERV_PORT);


    Bind(listenfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    Listen(listenfd, 128);

    maxfd = listenfd;                                           /* 起初 listenfd 即为最大文件描述符 */

    maxi = -1;                                                  /* 将来用作client[]的下标, 初始值指向0个元素之前下标位置 */
    for (i = 0; i < FD_SETSIZE; i++)
        client[i] = -1;                                         /* 用-1初始化client[] */

    FD_ZERO(&allset);
    FD_SET(listenfd, &allset);                                  /* 构造select监控文件描述符集 */

    while (1) {   
        rset = allset;                                          /* 每次循环时都从新设置select监控信号集 */

        nready = select(maxfd+1, &rset, NULL, NULL, NULL);      //2  1--lfd  1--connfd
        if (nready < 0)
            perr_exit("select error");

        if (FD_ISSET(listenfd, &rset)) {                        /* 说明有新的客户端链接请求 */

            clie_addr_len = sizeof(clie_addr);
            connfd = Accept(listenfd, (struct sockaddr *)&clie_addr, &clie_addr_len);       /* Accept 不会阻塞 */
            printf("received from %s at PORT %d\n",
                    inet_ntop(AF_INET, &clie_addr.sin_addr, str, sizeof(str)),
                    ntohs(clie_addr.sin_port));

            for (i = 0; i < FD_SETSIZE; i++)
                if (client[i] < 0) {                            /* 找client[]中没有使用的位置 */
                    client[i] = connfd;                         /* 保存accept返回的文件描述符到client[]里 */
                    break;
                }

            if (i == FD_SETSIZE) {                              /* 达到select能监控的文件个数上限 1024 */
                fputs("too many clients\n", stderr);
                exit(1);
            }

            FD_SET(connfd, &allset);                            /* 向监控文件描述符集合allset添加新的文件描述符connfd */

            if (connfd > maxfd)
                maxfd = connfd;                                 /* select第一个参数需要 */

            if (i > maxi)
                maxi = i;                                       /* 保证maxi存的总是client[]最后一个元素下标 */

            if (--nready == 0)
                continue;
        } 

        for (i = 0; i <= maxi; i++) {                               /* 检测哪个clients 有数据就绪 */

            if ((sockfd = client[i]) < 0)
                continue;//数组内的文件描述符如果被释放有可能变成-1
            if (FD_ISSET(sockfd, &rset)) {

                if ((n = Read(sockfd, buf, sizeof(buf))) == 0) {    /* 当client关闭链接时,服务器端也关闭对应链接 */
                    Close(sockfd);
                    FD_CLR(sockfd, &allset);                        /* 解除select对此文件描述符的监控 */
                    client[i] = -1;
                } else if (n > 0) {
                    for (j = 0; j < n; j++)
                        buf[j] = toupper(buf[j]);    // 转化维大写的
                    Write(sockfd, buf, n);
                    Write(STDOUT_FILENO, buf, n);
                }
                if (--nready == 0)
                    break;                                          /* 跳出for, 但还在while中 */
            }
        }
    }

    Close(listenfd);

    return 0;
}
```
虽然本代码还是需要遍历，但是效率提高了一些。


# 3.poll
```
#include <poll.h>
int poll(struct pollfd *fds, nfds_t nfds, int timeout);
功能: 监听多个文件描述符的属性变化
参数:
    fds : 监听的数组的首元素地址
    nfds: 数组有效元素的最大下标+1
    timeout : 超时时间 -1是永久监听 >=0 限时等待

数组元素:
            struct pollfd {
               int   fd;         /* file descriptor */ 需要监听的文件描述符
               short events;     /* requested events */需要监听文件描述符什么事件  EPOLLIN 读事件   EPOLLOUT写事件，其他事件可以通过man poll查看
               short revents;    /* returned events */ 返回监听到的事件    EPOLLIN 读事件   EPOLLOUT写事
           };
```
poll相对与sellect的优缺点
优点:
- 没有文件描述符1024的限制
- 请求和返回是分离的【select中，readfds表示监听的事件集，而且将返回的有读事件的文件描述符也放在readfds中，这就叫做请求和返回是不分离的】

缺点和select一样:
- 只是返回变化的文件描述符的个数,具体哪个那个变化需要遍历。当有大量的客户请求了连接但只有少量客户与服务器进行交互（即监听的文件描述符个数多，但是变化的文件描述符少），这种情况下，我们还是需要遍历全部的文件描述符才能找到变化的文件描述符。也就是说大量并发,少了活跃,poll效率低。
- poll对多个文件描述符进行监听是在内核中进行的，所以每次都需要将需要监听的文件描述集合由应用层符拷贝到内核


poll相对于select没有最大1024文件描述符限制，大小限制。但poll其实也是有最大文件描述符限制，如下：
```
ulimit -a                  # 查看最多打开多少个文件（open files）
ulimit -n 2048             # 将最多打开文件个数修改成2048
cat /proc/sys/fs/file-max  # ulimit -n最大可修改的量
```

示例代码：
```
#include <stdio.h>
#include <stdlib.h>
#include<netinet/in.h>
#include<poll.h>
#include<errno.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <ctype.h>

#include "wrap.h"

#define MAXLINE 80
#define SERV_PORT 8000
#define OPEN_MAX 1024


int main(int argc, char *argv[])
{
	int i, j, maxi, listenfd, connfd, sockfd;
	int nready;   // 接收poll返回值，记录满足监听事件的fd个数
	ssize_t n;

	char buf[MAXLINE],str[INET_ADDRSTRLEN];
	socklen_t clilen;

	struct pollfd client[OPEN_MAX] ;//定义pol1的数组
	struct sockaddr_in cliaddr,servaddr;

	listenfd = Socket(AF_INET, SOCK_STREAM, 0);
	int opt = 1;
	setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR,&opt, sizeof(opt));//设置端口复用

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(SERV_PORT);

	Bind(listenfd, (struct sockaddr *) &servaddr, sizeof(servaddr));
	Listen(listenfd,128);

	client[0].fd = listenfd;   /*要监听的第一一个文件描述符存入client[0]*/
	client[0].events = POLLIN; /* listenfd监听普通读事件*/
	for (i = 1; i < OPEN_MAX; i++)
		client[i].fd = -1;				// 用-1初始化client[]里剩下元素 0也是文件描述符,
	maxi = 0;                            /* client[]数组有效元素中最大元素下标*/




	for (;;) { // 等价与while循环 
		nready = poll(client, maxi + 1, -1); /* 阻塞监听是否有客户端链接请求*/
		if (client[0].revents & POLLIN) {      // listenfd有 读事件就绪。这里用&，而不用==
			clilen = sizeof(cliaddr);
			connfd = Accept(listenfd, (struct sockaddr *) &cliaddr, &clilen);
			printf("received from %s at PORT %d\n",
				inet_ntop(AF_INET, &cliaddr.sin_addr, str, sizeof(str)),
				ntohs(cliaddr.sin_port));
			for (i = 1; i < OPEN_MAX; i++)
				if (client[i].fd < 0) {
					client[i].fd = connfd;  // 找到client []中空闲的位置,存放accept返回的connfd
					break;
				}
			if (i == OPEN_MAX)  /*达到了最大客户端数*/
				perr_exit("too many clients");

			client[i].events = POLLIN;  /*设置刚刚返回的connfd, 监控读事件*/
			if (i > maxi)
				maxi = i;             /*更新client[]中最大元素下标*/
			if (--nready <= 0)
				continue;            /*没有更多就绪事件时,继续回到po11阻塞*/
		}
		for (i = 1; i <= maxi; i++) {

			if ((sockfd = client[i].fd) < 0)
				continue;				//找到第一-个大于0的

			if (client[i].revents & POLLIN) {
				if ((n = Read(sockfd, buf, MAXLINE)) < 0) {
					if (errno == ECONNRESET) { /* 收到RST标志，代表对方想要关闭连接*/
						printf("client[%d] aborted connection\n", i);
						Close(sockfd);
						client[i].fd = -1;    // poll中不监控该文件描述符,直接置为-1即可，不用像se
					}
					else
						perr_exit("read error");
				}
				else if (n == 0) {   /*说明客户端先关闭链接*/
					printf("client[%d] closed connection\n",i);
					Close(sockfd);
					client[i].fd = -1;
				}
				else {
					for (j = 0; j < n; j++)
						buf[j] = toupper(buf[j]);
					Writen(sockfd, buf, n);
				}
				if (--nready <= 0)
					break;
			}
		}
	}
				
	return 0;

}
```


# 4.epoll
## 4.1.epoll API
1.创建一棵红黑树
2.将需要监听的文件描述符放入树中（上树）
3.通过操作树来实现监听

```
// 创建红黑树
#include <sys/epoll.h>
int epoll_create(int size);
参数:
    size :  监听的文件描述符的上限,  2.6版本之后写1即可（因为不够的时候，它会自动扩展）
返回:  返回树的句柄（就相当于返回一棵树）
```

```
// 上树  下树 修改节点
#include <sys/epoll.h>
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
参数:
    epfd : 树的句柄
    op : EPOLL_CTL_ADD 上树   EPOLL_CTL_DEL 下树 EPOLL_CTL_MOD 修改
    fd : 上树或修改或下树的文件描述符
    event : 上树的节点，event里面包含文件描述符和文件描述符需要监听的事件。这不就和fd重复了？
            答：虽然按道理传个event就行，但它就要求你传fd和event，那你就老老实实传啊。
           typedef union epoll_data { // 共用体，一般只使用共用体中的一个数据。
               void        *ptr;
               int          fd;  // 经常使用这个
               uint32_t     u32;
               uint64_t     u64;
           } epoll_data_t;

           struct epoll_event {
               uint32_t     events;      /* Epoll events */  需要监听的事件
               epoll_data_t data;        /* User data variable */ 需要监听的文件描述符，经常只使用fd就行
           };

示例：将cfd上树
int epfd =  epoll_create(1);
struct epoll_event ev;
ev.data.fd = cfd;
ev.events = EPOLLIN;
epoll_ctl(epfd, EPOLL_CTL_ADD,cfd, &ev);
```

```
//监听
#include <sys/epoll.h>
int epoll_wait(int epfd, struct epoll_event *events,
               int maxevents, int timeout);
功能: 监听树上文件描述符的变化
参数：
    epfd : 树
    events : 接收变化的节点的数组的首地址
    maxevents :  数组元素的个数
    timeout : -1 永久监听  大于等于0 限时等待
返回值: 返回的是变化的文件描述符个数

```

优点：
- 和poll一样，没有文件描述符1024的限制，但是还是有上限的。见poll中说明
- 以后每次监听都不要在此将需要监听的文庙描述符拷贝到内核
- 返回的是己经变化的文件描述符,不需要遍历树

## 4.2.示例代码：
**1.父进程监听子进程是否向管道中发送数据。**
```
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/epoll.h>
int main(int argc, char *argv[])
{
	int fd[2];
	pipe(fd);    // fd中保存管道的读端和写端
	//创建子进程
	pid_t pid;
	pid = fork();
	if(pid < 0)
		perror("");
	else if(pid == 0) // 为子进程
	{
		close(fd[0]);  // 子进程的读端没有用，故关掉
		char buf[5];
		char ch='a';
		while(1)
		{
			sleep(3); // 每隔三秒写一次数据
			memset(buf,ch++,sizeof(buf));
			write(fd[1],buf,5); // 子进程向管道的写端写数据
		}

	}
	else
	{
		close(fd[1]);
		//创建树
		int epfd = epoll_create(1);
		struct epoll_event ev,evs[1];
		ev.data.fd = fd[0];
		ev.events = EPOLLIN;  // 读事件：有数据来了，就触发读事件
		epoll_ctl(epfd,EPOLL_CTL_ADD,fd[0],&ev);  //上树
		//监听
		while(1)
		{
			int n = epoll_wait(epfd,evs,1,-1);
			if(n == 1)
			{
				char buf[128]="";
				int ret  = read(fd[0],buf,sizeof(buf));
				if(ret <= 0)
				{
					close(fd[0]);
					epoll_ctl(epfd,EPOLL_CTL_DEL,fd[0],&ev);
					break;
				}
				else
				{
					printf("%s\n",buf);
				}
			
			}
		
		
		}

	
	
	}


	return 0;
}

```

**2.epoll实现服务器**
```
#include <stdio.h>
#include <fcntl.h>
#include "wrap.h"
#include <sys/epoll.h>
int main(int argc, char *argv[])
{
	//创建套接字 绑定
	int lfd = tcp4bind(8000,NULL);
	//监听
	Listen(lfd,128);
	//创建树
	int epfd = epoll_create(1);
	//将lfd上树
	struct epoll_event ev,evs[1024];
	ev.data.fd = lfd;
	ev.events = EPOLLIN; // 读事件，即有连接到达lfd了，需要我们去读。不设置为边沿触发，使用默认的水平触发
	epoll_ctl(epfd,EPOLL_CTL_ADD,lfd,&ev);
	//while监听
	while(1)
	{
		int nready = epoll_wait(epfd,evs,1024,-1);//监听
		printf("epoll wait _________________\n");
		if(nready <0)
		{
			perror("");
			break;
		}
		else if( nready == 0)
		{
			continue;
		}
		else//有文件描述符变化
		{
			for(int i=0;i<nready;i++)
			{
				//判断lfd变化,并且是读事件变化
				if(evs[i].data.fd == lfd && evs[i].events & EPOLLIN)
				{
					struct sockaddr_in cliaddr;
					char ip[16]="";
					socklen_t len = sizeof(cliaddr);
					int cfd = Accept(lfd,(struct sockaddr *)&cliaddr,&len);//提取新的连接

					printf("new client ip=%s port =%d\n",inet_ntop(AF_INET,&cliaddr.sin_addr.s_addr,ip,16)
							,ntohs(cliaddr.sin_port));
					//设置cfd为非阻塞
					int flags = fcntl(cfd,F_GETFL);//获取的cfd的标志位
					flags |= O_NONBLOCK;
					fcntl(cfd,F_SETFL,flags);
					//将cfd上树
					ev.data.fd =cfd;  // 前面将ev中的内容上树完成之后，ev就没什么用，所以这里可以重复使用ev 
					ev.events =EPOLLIN | EPOLLET;  // EPOLLIN表示读事件。EPOLLET设置为边沿触发，不设置的话，默认为水平触发
					epoll_ctl(epfd,EPOLL_CTL_ADD,cfd,&ev);
				
				}
				else if( evs[i].events & EPOLLIN)//cfd变化 ,而且是读事件变化
				{
					while(1) // 循环读取读缓冲区，直到读缓冲区没有数据为止。从而实现epoll边沿模式下可以一次将数据读走
					{
						char buf[4]="";
						// 如果读一个缓冲区,缓冲区没有数据,如果是带阻塞,就阻塞等待。
                                                // 如果是非阻塞,返回值等于-1,并且会将errno 值设置为EAGAIN
						int n = read(evs[i].data.fd,buf,sizeof(buf)); // 由于前面cfd被设为了非阻塞，所以如果读缓冲区中没有数据，这里也不会阻塞，而是返回-1 并将errno 值设置为EAGAIN
						if(n < 0)//出错,cfd下树
						{
							//如果缓冲区读干净了,这个时候应该跳出while(1)循环,继续监听
							if(errno == EAGAIN)
							{
								break;
							
							}
							//普通错误  
							perror("");
							close(evs[i].data.fd);//将cfd关闭
							epoll_ctl(epfd,EPOLL_CTL_DEL,evs[i].data.fd,&evs[i]);
							break;
						}
						else if(n == 0)//客户端关闭 ,
							{
								printf("client close\n");
								close(evs[i].data.fd);//将cfd关闭
								epoll_ctl(epfd,EPOLL_CTL_DEL,evs[i].data.fd,&evs[i]);//下树
								break;
							}
						else
						{
							// printf("%s\n",buf);  // 由于buf的末尾没有'\0'，所以打印会出错
							write(STDOUT_FILENO,buf,4);  // 用于代替printf("%s\n",buf); 
							write(evs[i].data.fd,buf,n);
							

						}
					}

				}
			
			
			}
		
		}
	
	
	}
	
	return 0;
}
```

## 4.3.epoll的工作方式
**1.监听读缓冲区的变化：**
水平触发（LT）:只要读缓冲区有数据就会触发epo11_ wait
边沿触发（ET）:接收到数据来一次, epo11_ wait只触发一次。这就要求必须一次性将数据都读走。
**2.监听写缓冲区的变化:**
水平触发:只要可以写，就会触发。（这会导致一直触发，所以一般不用）
边沿触发:数据从有到无,就会触发

因为设置为水平触发,只要缓存区有数据epoll_wait就会被触发，这样调用的次数就会比较多。而epoll_wait是一个系统调用,应该尽量少调用。
所以尽量使用边沿触发,边沿出触发数据来一次只触发一次,这个时候要求一次性将数据读完。“epoll实现服务器”的代码就使用了边沿触发，并一次性将数据读完。

工作中使用：边沿触发+非阻塞 

## 4.4.epoll反应堆
本小节看懂就行，不需要会写。
epoll反应堆：将文件描述符、事件和回调函数封装在一起。当事件发生时，自动调用回调函数。
使用结构体进行封装。

**一个简单的epoll反应堆：**
```
//反应堆简单版
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/epoll.h>
#include "wrap.h"

#define _BUF_LEN_  1024
#define _EVENT_SIZE_ 1024

//全局epoll树的根
int gepfd = 0;

//事件驱动结构体
typedef struct xx_event{
    int fd;
    int events;
    void (*call_back)(int fd,int events,void *arg);
    void *arg;
    char buf[1024];
    int buflen;
    int epfd;
}xevent;

xevent myevents[_EVENT_SIZE_+1]; // 全局变量默认初始化为零

void readData(int fd,int events,void *arg);

//添加事件
//eventadd(lfd,EPOLLIN,initAccept,&myevents[_EVENT_SIZE_-1],&myevents[_EVENT_SIZE_-1]);
void eventadd(int fd,int events,void (*call_back)(int ,int ,void *),void *arg,xevent *ev)
{
    ev->fd = fd;
    ev->events = events;
    //ev->arg = arg;//代表结构体自己,可以通过arg得到结构体的所有信息
    ev->call_back = call_back;

    struct epoll_event epv;
    epv.events = events;
    epv.data.ptr = ev; //核心思想
    epoll_ctl(gepfd,EPOLL_CTL_ADD,fd,&epv);//上树
}

//修改事件
//eventset(fd,EPOLLOUT,senddata,arg,ev);
void eventset(int fd,int events,void (*call_back)(int ,int ,void *),void *arg,xevent *ev)
{
    ev->fd = fd;
    ev->events = events;
    //ev->arg = arg;
    ev->call_back = call_back;

    struct epoll_event epv;
    epv.events = events;
    epv.data.ptr = ev;
    epoll_ctl(gepfd,EPOLL_CTL_MOD,fd,&epv);//修改
}

//删除事件
void eventdel(xevent *ev,int fd,int events)
{
	printf("begin call %s\n",__FUNCTION__);

    ev->fd = 0;
    ev->events = 0;
    ev->call_back = NULL;
    memset(ev->buf,0x00,sizeof(ev->buf));
    ev->buflen = 0;

    struct epoll_event epv;
    epv.data.ptr = NULL;
    epv.events = events;
    epoll_ctl(gepfd,EPOLL_CTL_DEL,fd,&epv);//下树
}

//发送数据
void senddata(int fd,int events,void *arg)
{
    printf("begin call %s\n",__FUNCTION__);

    xevent *ev = arg;
    Write(fd,ev->buf,ev->buflen);
    eventset(fd,EPOLLIN,readData,arg,ev);
}

//读数据
void readData(int fd,int events,void *arg)
{
    printf("begin call %s\n",__FUNCTION__);
    xevent *ev = arg;

    ev->buflen = Read(fd,ev->buf,sizeof(ev->buf)); // 读完数据，并没有直接将数据发送回去。而是监听fd是否可写（可发送）后，再进行发送
    if(ev->buflen>0) //读到数据
	{	
		//void eventset(int fd,int events,void (*call_back)(int ,int ,void *),void *arg,xevent *ev)
        eventset(fd,EPOLLOUT,senddata,arg,ev); // 修改fd，使其监听写事件。一旦可写就将收到的数据发送回去
											   // senddata中，修改fd，使其重新监听读事件。

    }
	else if(ev->buflen==0) //对方关闭连接
	{
        Close(fd);
        eventdel(ev,fd,EPOLLIN);
    }

}
//新连接处理
void initAccept(int fd,int events,void *arg)
{
    printf("begin call %s,gepfd =%d\n",__FUNCTION__,gepfd);//__FUNCTION__ 函数名

    int i;
    struct sockaddr_in addr;
    socklen_t len = sizeof(addr);
    int cfd = Accept(fd,(struct sockaddr*)&addr,&len);//是否会阻塞？
	
	//查找myevents数组中可用的位置
    for(i = 0 ; i < _EVENT_SIZE_; i ++)
	{
        if(myevents[i].fd==0)
		{
            break;
        }
    }

    //设置读事件
    eventadd(cfd,EPOLLIN,readData,&myevents[i],&myevents[i]);
}

// epoll反应堆的使用
int main(int argc,char *argv[])
{
	//创建socket
    int lfd = Socket(AF_INET,SOCK_STREAM,0);

    //端口复用
    int opt = 1;
    setsockopt(lfd,SOL_SOCKET,SO_REUSEADDR,&opt,sizeof(opt));

	//绑定
    struct sockaddr_in servaddr;
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(8888);
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    Bind(lfd,(struct sockaddr*)&servaddr,sizeof(servaddr));
    
	//监听
    Listen(lfd,128);

	//创建epoll树根节点
    gepfd = epoll_create(1024); 
    printf("gepfd === %d\n",gepfd);

    struct epoll_event events[1024]; // 用保存哪些事件发生了

    // 初始化数据myevents[_EVENT_SIZE_]，并将描述符lfd上树
    eventadd(lfd,EPOLLIN,initAccept,&myevents[_EVENT_SIZE_],&myevents[_EVENT_SIZE_]);
    //void eventadd(int fd,int events,void (*call_back)(int ,int ,void *),void *arg,xevent *ev)

    while(1)
	{
        int nready = epoll_wait(gepfd,events,1024,-1); // 同时监听树上的所有节点，包括节点lfd和cfd
		if(nready<0) //调用epoll_wait失败
		{
			perr_exit("epoll_wait error");
			
		}
        else if(nready>0) //调用epoll_wait成功,返回有事件发生的文件描述符的个数
		{
            int i = 0;
            for(i=0;i<nready; i++)
			{
                xevent *xe = events[i].data.ptr;//取ptr指向结构体地址
                printf("fd=%d\n",xe->fd);

                if(xe->events & events[i].events) // 监听的事件和发生的事件一致时。这个其实写不写都无所谓
				{
                    xe->call_back(xe->fd,xe->events,xe);//调用事件对应的回调
                }
            }
        }
    }

	//关闭监听文件描述符
	Close(lfd);

    return 0;
}

```

**一个较复杂的epoll反应堆（可以不看，看懂上面那个简单的反应堆就可以了）：**
```
/*
 * epoll基于非阻塞I/O事件驱动
 */
#include <stdio.h>
#include <sys/socket.h>
#include <sys/epoll.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define MAX_EVENTS  1024                                    //监听上限数
#define BUFLEN      4096
#define SERV_PORT   8080

void recvdata(int fd, int events, void *arg);
void senddata(int fd, int events, void *arg);

/* 描述就绪文件描述符相关信息 */

struct myevent_s {
    int fd;                                                 //要监听的文件描述符
    int events;                                             //对应的监听事件
    void *arg;                                              //泛型参数
    void (*call_back)(int fd, int events, void *arg);       //回调函数
    int status;                                             //是否在监听:1->在红黑树上(监听), 0->不在(不监听)
    char buf[BUFLEN];
    int len;
    long last_active;                                       //记录每次加入红黑树的时间。如果是不活跃的，就会被剔除掉
};

int g_efd;                                                  //全局变量, 保存epoll_create返回的文件描述符
struct myevent_s g_events[MAX_EVENTS+1];                    //自定义结构体类型数组. +1-->listen fd


/*将结构体 myevent_s 成员变量 初始化*/

void eventset(struct myevent_s *ev, int fd, void (*call_back)(int, int, void *), void *arg)
{
    ev->fd = fd;
    ev->call_back = call_back;
    ev->events = 0;
    ev->arg = arg;
    ev->status = 0;
    //memset(ev->buf, 0, sizeof(ev->buf));
    //ev->len = 0;
    ev->last_active = time(NULL);    //调用eventset函数的时间

    return;
}

/* 向 epoll监听的红黑树 添加一个 文件描述符 */

void eventadd(int efd, int events, struct myevent_s *ev)
{
    struct epoll_event epv = {0, {0}};
    int op;
    epv.data.ptr = ev;
    epv.events = ev->events = events;       //EPOLLIN 或 EPOLLOUT

    if (ev->status == 1) {                                          //已经在红黑树 g_efd 里
        op = EPOLL_CTL_MOD;                                         //修改其属性
    } else {                                //不在红黑树里
        op = EPOLL_CTL_ADD;                 //将其加入红黑树 g_efd, 并将status置1
        ev->status = 1;
    }

    if (epoll_ctl(efd, op, ev->fd, &epv) < 0)                       //实际添加/修改
        printf("event add failed [fd=%d], events[%d]\n", ev->fd, events);
    else
        printf("event add OK [fd=%d], op=%d, events[%0X]\n", ev->fd, op, events);

    return ;
}

/* 从epoll 监听的 红黑树中删除一个 文件描述符*/

void eventdel(int efd, struct myevent_s *ev)
{
    struct epoll_event epv = {0, {0}};

    if (ev->status != 1)                                        //不在红黑树上
        return ;

    epv.data.ptr = ev;
    ev->status = 0;                                             //修改状态
    epoll_ctl(efd, EPOLL_CTL_DEL, ev->fd, &epv);                //从红黑树 efd 上将 ev->fd 摘除

    return ;
}

/*  当有文件描述符就绪, epoll返回, 调用该函数 与客户端建立链接 */
// 回调函数 - 监听的文件描述符发送读事件时被调用
void acceptconn(int lfd, int events, void *arg)
{
    struct sockaddr_in cin;
    socklen_t len = sizeof(cin);
    int cfd, i;

    if ((cfd = accept(lfd, (struct sockaddr *)&cin, &len)) == -1) {
        if (errno != EAGAIN && errno != EINTR) {
            /* 暂时不做出错处理 */
        }
        printf("%s: accept, %s\n", __func__, strerror(errno));
        return ;
    }

    do {
        for (i = 0; i < MAX_EVENTS; i++)                                //从全局数组g_events中找一个空闲元素
            if (g_events[i].status == 0)                                //类似于select中找值为-1的元素
                break;                                                  //跳出 for

        if (i == MAX_EVENTS) {
            printf("%s: max connect limit[%d]\n", __func__, MAX_EVENTS);
            break;                                                      //跳出do while(0) 不执行后续代码
        }

        int flag = 0;
        if ((flag = fcntl(cfd, F_SETFL, O_NONBLOCK)) < 0) {             //将cfd也设置为非阻塞
            printf("%s: fcntl nonblocking failed, %s\n", __func__, strerror(errno));
            break;
        }

        /* 给cfd设置一个 myevent_s 结构体, 回调函数 设置为 recvdata */

        eventset(&g_events[i], cfd, recvdata, &g_events[i]);
        eventadd(g_efd, EPOLLIN, &g_events[i]);                         //将cfd添加到红黑树g_efd中,监听读事件

    } while(0);

    printf("new connect [%s:%d][time:%ld], pos[%d]\n", 
            inet_ntoa(cin.sin_addr), ntohs(cin.sin_port), g_events[i].last_active, i);
    return ;
}

// 回调函数 - 通信的文件描述符发生读事件时候被调用
void recvdata(int fd, int events, void *arg)
{
    struct myevent_s *ev = (struct myevent_s *)arg;
    int len;

    len = recv(fd, ev->buf, sizeof(ev->buf), 0);            //读文件描述符, 数据存入myevent_s成员buf中

    eventdel(g_efd, ev);        //将该节点从红黑树上摘除

    if (len > 0) {

        ev->len = len;
        ev->buf[len] = '\0';                                //手动添加字符串结束标记
        printf("C[%d]:%s\n", fd, ev->buf);

        eventset(ev, fd, senddata, ev);                     //设置该 fd 对应的回调函数为 senddata
        eventadd(g_efd, EPOLLOUT, ev);                      //将fd加入红黑树g_efd中,监听其写事件

    } else if (len == 0) {
        close(ev->fd);
        /* ev-g_events 地址相减得到偏移元素位置 */
        printf("[fd=%d] pos[%ld], closed\n", fd, ev-g_events);
    } else {
        close(ev->fd);
        printf("recv[fd=%d] error[%d]:%s\n", fd, errno, strerror(errno));
    }

    return;
}

// 回调函数 - 通信的文件描述符发生写事件时候被调用
void senddata(int fd, int events, void *arg)
{
    struct myevent_s *ev = (struct myevent_s *)arg;
    int len;

    len = send(fd, ev->buf, ev->len, 0);                    //直接将数据 回写给客户端。未作处理
    /*
    printf("fd=%d\tev->buf=%s\ttev->len=%d\n", fd, ev->buf, ev->len);
    printf("send len = %d\n", len);
    */

    if (len > 0) {

        printf("send[fd=%d], [%d]%s\n", fd, len, ev->buf);
        eventdel(g_efd, ev);                                //从红黑树g_efd中移除
        eventset(ev, fd, recvdata, ev);                     //将该fd的 回调函数改为 recvdata
        eventadd(g_efd, EPOLLIN, ev);                       //从新添加到红黑树上， 设为监听读事件

    } else {
        close(ev->fd);                                      //关闭链接
        eventdel(g_efd, ev);                                //从红黑树g_efd中移除
        printf("send[fd=%d] error %s\n", fd, strerror(errno));
    }

    return ;
}

/*创建 socket, 初始化lfd */

void initlistensocket(int efd, short port)
{
    int lfd = socket(AF_INET, SOCK_STREAM, 0);
    fcntl(lfd, F_SETFL, O_NONBLOCK);                                            //将socket设为非阻塞

    /* void eventset(struct myevent_s *ev, int fd, void (*call_back)(int, int, void *), void *arg);  */
    eventset(&g_events[MAX_EVENTS], lfd, acceptconn, &g_events[MAX_EVENTS]);

    /* void eventadd(int efd, int events, struct myevent_s *ev) */
    eventadd(efd, EPOLLIN, &g_events[MAX_EVENTS]);

    struct sockaddr_in sin;
	memset(&sin, 0, sizeof(sin));                                               //bzero(&sin, sizeof(sin))
	sin.sin_family = AF_INET;
	sin.sin_addr.s_addr = INADDR_ANY;
	sin.sin_port = htons(port);

	bind(lfd, (struct sockaddr *)&sin, sizeof(sin));

	listen(lfd, 20);

    return ;
}

int main(int argc, char *argv[])
{
    unsigned short port = SERV_PORT;

    if (argc == 2)
        port = atoi(argv[1]);                           //使用用户指定端口.如未指定,用默认端口

    g_efd = epoll_create(MAX_EVENTS+1);                 //创建红黑树,返回给全局 g_efd 
    if (g_efd <= 0)
        printf("create efd in %s err %s\n", __func__, strerror(errno));

    initlistensocket(g_efd, port);                      //初始化监听socket

    struct epoll_event events[MAX_EVENTS+1];            //保存已经满足就绪事件的文件描述符数组
	printf("server running:port[%d]\n", port);

    int checkpos = 0, i;
    while (1) {
		
        /* 超时验证，每次测试100个链接，不测试listenfd 当客户端60秒内没有和服务器通信，则关闭此客户端链接。不是重点不用看。 */
        long now = time(NULL);                          //当前时间
        for (i = 0; i < 100; i++, checkpos++) {         //一次循环检测100个。 使用checkpos控制检测对象
            if (checkpos == MAX_EVENTS)
                checkpos = 0;
            if (g_events[checkpos].status != 1)         //不在红黑树 g_efd 上
                continue;

            long duration = now - g_events[checkpos].last_active;       //客户端不活跃的世间

            if (duration >= 60) {
                close(g_events[checkpos].fd);                           //关闭与该客户端链接
                printf("[fd=%d] timeout\n", g_events[checkpos].fd);
                eventdel(g_efd, &g_events[checkpos]);                   //将该客户端 从红黑树 g_efd移除
            }
        }


        /*监听红黑树g_efd, 将满足的事件的文件描述符加至events数组中, 1秒没有事件满足, 返回 0*/
        int nfd = epoll_wait(g_efd, events, MAX_EVENTS+1, 1000);
        if (nfd < 0) {
            printf("epoll_wait error, exit\n");
            break;
        }

        for (i = 0; i < nfd; i++) {
            /*使用自定义结构体myevent_s类型指针, 接收 联合体data的void *ptr成员*/
            struct myevent_s *ev = (struct myevent_s *)events[i].data.ptr;  

            if ((events[i].events & EPOLLIN) && (ev->events & EPOLLIN)) {           //读就绪事件
                ev->call_back(ev->fd, events[i].events, ev->arg);
            }
            if ((events[i].events & EPOLLOUT) && (ev->events & EPOLLOUT)) {         //写就绪事件
                ev->call_back(ev->fd, events[i].events, ev->arg);
            }
        }
    }

    /* 退出前释放所有资源 */
    return 0;
}
```
