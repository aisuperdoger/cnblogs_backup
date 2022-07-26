原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/06/29/16424650.html
提交日期：Wed, 29 Jun 2022 11:14:00 GMT
博文内容：
我认为与IDE相比，GDB没什么好处，如果能用IDE就尽量用IDE。

# 1.gdb常用命令
可参考：[gdb调试](https://freecplus.net/b72113dda88a43b48728e0552fd8a74c.html)
bt：查看函数的调用栈。比如main函数中调用func函数，那么调用栈为：main在栈底，func在main的上方
info b：查看断点的信息
info threads：查看线程信息

# 2.调试core文件
程序运行时由于非法访问内存，程序可能挂掉，但是不返回发生错误的代码的位置。此时在gdb调试的时候引入core文件，就可以查看到发生core dump的位置。
可参考[gdb调试——②调试core文件](https://blog.csdn.net/shi_xiao_xuan/article/details/117402434)调试core文件
参考[Ubuntu下不产生core文件](https://blog.csdn.net/qq_38229124/article/details/123325016)，解决Ubuntu下不产生core文件问题。

# 3.调试正在运行的程序
可参考：[gdb调试——③调试正在运行的程序](https://blog.csdn.net/shi_xiao_xuan/article/details/117454802)



# 4.父子进程调试

我以为调试子进程，直接在子进程中打断点就可以了，但其实还需要输入set follow-fork-mode child。
```
set follow-fork-mode parent(缺省)
set follow-fork-mode child
```
**实例：**
```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    printf("begin\n");

    if (fork() != 0)
    {
        printf("我是父进程:pid=%d.ppid=%d\n", getpid(), getppid());

        int ii = 0;
        for (ii = 0; ii < 10; ii++)
        {
            printf("ii=%d\n",ii);
            sleep(1);
        }
        exit(0);
    }
    else{
        printf("我是子进程:pid=%d.ppid=%d\n", getpid(), getppid());

        int jj = 0;
        for (jj = 0; jj < 10; jj++)
        {
            printf("jj=%d\n",jj);
            sleep(1);
        }
        exit(0);
    }
}
```
运行命令：
```
(gdb) b 24                             # 在第24行（int jj = 0;）设置断点
Breakpoint 1 at 0x12b6: file test.cpp, line 24.
(gdb) set follow-fork-mode child       # 调试子进程
(gdb) r
Starting program: /home/ubuntu1/projects/c++/restful_api/test/test 
begin
[Attaching after process 42641 fork to child process 42645]
[New inferior 2 (process 42645)]
[Detaching after fork from parent process 42641]
我是父进程:pid=42641.ppid=42594
ii=0
[Inferior 1 (process 42641) detached]
我是子进程:pid=42645.ppid=42641
[Switching to process 42645]

Thread 2.1 "test" hit Breakpoint 1, main () at test.cpp:24
24              int jj = 0;          # 子进程在第24行停止运行
(gdb) ii=1
ii=2                                 # 父进程执行完毕
(gdb) n                              # 输入n，一步一步调试子进程
25              for (jj = 0; jj < 3; jj++)
(gdb) 
·
·
·
```

如果需要同时调试父进程和子进程，需要先介绍一下detach-on-fork。
```
set detach-on-fork [on | off]：默认为on，表示调试当前进程的时候，其它的进程继续运行。如果为off, 调试当前进程的时候，其它进程被GDB挂起。
为off时的运行机制：在fork()函数之后，判断follow-fork-mode类型。当follow-fork-mode为parent时，代表调试的是父进程，此时将子进程挂起。
```
detach-on-fork和follow-fork-mode组合起来的效果如下表：

follow-fork-mode|detach-on-fork|效果 
---|---|---
parent|	on|	只调试父进程
child	|on|	只调试子进程
parent	|off|	同时调试两个进程，子进程暂停
child	|off|	同时调试两个进程，父进程暂停

```
info inferiors，查看当前所有进程
inferior <num>，切换当前GDB调试进程，其中num为上一条指令中列出的进程Num
```
若同时调试两个进程，并且切换进程的效果如下:
```
(gdb) set detach-on-fork off 
(gdb) b 13                 # 在第13行（int jj = 0;）设置断点
Breakpoint 1 at 0x1251: file test.cpp, line 13.
(gdb) b24                   # 在第24行（int ii = 0;）设置断点
Undefined command: "b24".  Try "help".
(gdb) r
Starting program: /home/ubuntu1/projects/c++/restful_api/test/test 
begin
[New inferior 2 (process 44543)]
Reading symbols from /home/ubuntu1/projects/c++/restful_api/test/test...
Reading symbols from /usr/lib/debug/lib/x86_64-linux-gnu/libc-2.31.so...
我是父进程:pid=44539.ppid=44462

Thread 1.1 "test" hit Breakpoint 1, main () at test.cpp:13
warning: Source file is more recent than executable.
13              int ii = 0;
(gdb) n                    # 调试父进程
14              for (ii = 0; ii < 3; ii++)
(gdb) info inferiors
  Num  Description       Executable        
* 1    process 44539     /home/ubuntu1/projects/c++/restful_api/test/test 
  2    process 44543     /home/ubuntu1/projects/c++/restful_api/test/test 
(gdb) inferior 2          # 切换到子进程
[Switching to inferior 2 [process 44543] (/home/ubuntu1/projects/c++/restful_api/test/test)]
[Switching to thread 2.1 (process 44543)]
#0  arch_fork (ctid=0x7ffff7fb7810) at ../sysdeps/unix/sysv/linux/arch-fork.h:49
49      ../sysdeps/unix/sysv/linux/arch-fork.h: No such file or directory.
(gdb) n
53      in ../sysdeps/unix/sysv/linux/arch-fork.h
(gdb) n
__libc_fork () at ../sysdeps/nptl/fork.c:78
78      ../sysdeps/nptl/fork.c: No such file or directory.    # 这一堆信息应该是代表进入子进程前要经过的初始化函数
(gdb) n
83      in ../sysdeps/nptl/fork.c # 这一堆信息应该是代表进入子进程前要经过的初始化函数
(gdb) n
100     in ../sysdeps/nptl/fork.c # 这一堆信息应该是代表进入子进程前要经过的初始化函数
(gdb) n
102     in ../sysdeps/nptl/fork.c # 这一堆信息应该是代表进入子进程前要经过的初始化函数
(gdb) n
113     in ../sysdeps/nptl/fork.c # 这一堆信息应该是代表进入子进程前要经过的初始化函数
(gdb) n
126     in ../sysdeps/nptl/fork.c # 这一堆信息应该是代表进入子进程前要经过的初始化函数
(gdb) n
129     in ../sysdeps/nptl/fork.c # 这一堆信息应该是代表进入子进程前要经过的初始化函数，下次切换进程就没这些信息了
(gdb) n
main () at test.cpp:9
9           if ( pid != 0)
(gdb) n
22              printf("我是子进程:pid=%d.ppid=%d\n", getpid(), getppid());
(gdb) 
```
参考：[GDB调试之多进程/线程](https://blog.csdn.net/Augusdi/article/details/118864353)


# 5.多线程调试

调试多线的常用命令：
```
查看线程: info threads
切换线程: thread 线程id
指定某线程执行某gdb命令: thread apply 线程id cmd
全部的线程执行某adb命令: thread apply all cmd

使用 GDB 调试多线程程序时，默认的调试模式为：一个线程暂停运行，其它线程也随即暂停；一个线程启动运行，其它线程也随即启动。要知道，
这种调试机制确实能帮我们更好地监控各个线程的“一举一动”，但并非适用于所有场景。
一些场景中，我们可能只想让某一特定线程运行，其它线程仍维持暂停状态。要想达到这样的效果，就需要借助 set scheduler-locking 命令。
此命令可以帮我们将其它线程都“锁起来”，使后续执行的命令只对当前线程或者指定线程有效，而对其它线程无效。
set scheduler-locking mode，mode可以为：
off：不锁定线程，任何线程都可以随时执行；
on：锁定线程，只有当前线程或指定线程可以运行；
step：当单步执行某一线程时，其它线程不会执行，同时保证在调试过程中当前线程不会发生改变。但如果该模式下执行 continue、until、finish
命令，则其它线程也会执行，并且如果某一线程执行过程遇到断点，则 GDB 调试器会将该线程作为当前线程。
```
实例：
```
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
int x = 0, y = 0; // x用于线程一，y用于线程二。
pthread_t pthid1, pthid2;
//第一个线程的主函数
void *pth1_main(void *arg);
//第二个线程的主函数
void *pth2_main(void *arg);
int main()
{
    //创建线程一
    if (pthread_create(&pthid1, NULL, pth1_main, (void *)0) != 0)
    {
        printf("pthread_ create pthid1 failed.\n");
        return -1;
    }
    //创建线程二
    if (pthread_create(&pthid2, NULL, pth2_main, (void *)0) != 0)
    {
        printf("pthread_ create pthid2 failed.\n");
        return -1;
    }
    printf(" 111\n");
    pthread_join(pthid1, NULL);
    printf("222\n");
    pthread_join(pthid2, NULL);
    printf("333\n");
    return 0;
}

//第一个线程的主函数
void *pth1_main(void *arg)
{
    for(x = 0; x < 100; x++)
    {
        printf(" x=%d\n", x);
        sleep(1);
    } 
    pthread_exit(NULL);
}

//第二个线程的主函数
void *pth2_main(void *arg)
{
    for (y = 0; y < 100; y++)
    {
        printf(" y=%d\n", y);
        sleep(1) ;
    } 
    pthread_exit(NULL);
}
```
效果如下:
```
**(gdb) b 13    # 在第13行设置断点（if (pthread_create(&pthid1, NULL, pth1_main, (void *)0) != 0)）
Breakpoint 1 at 0x11f1: file test.cpp, line 13.
(gdb) b 35       # 在第35行设置断点（for(x = 0; x < 100; x++)）
Breakpoint 2 at 0x12c9: file test.cpp, line 35.
(gdb) b 46        # 在第46行设置断点（for (y = 0; y < 100; y++)）
Breakpoint 3 at 0x132c: file test.cpp, line 46.
(gdb) r
Starting program: /home/ubuntu1/projects/c++/restful_api/test/test 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, main () at test.cpp:13
13          if (pthread_create(&pthid1, NULL, pth1_main, (void *)0) != 0)
(gdb) n
[New Thread 0x7ffff7d9d700 (LWP 48569)]
[Switching to Thread 0x7ffff7d9d700 (LWP 48569)]

Thread 2 "test" hit Breakpoint 2, pth1_main (arg=0x0) at test.cpp:35
35          for(x = 0; x < 100; x++)             # 处于线程1
(gdb) n
[New Thread 0x7ffff759c700 (LWP 48581)]
 111                                            # 主线程输出111
[Switching to Thread 0x7ffff759c700 (LWP 48581)]

Thread 3 "test" hit Breakpoint 3, pth2_main (arg=0x0) at test.cpp:46
46          for (y = 0; y < 100; y++)          # 主线程开启了线程2，并在线程2的断点处停止
(gdb) n                                        # 调试线程2
 x=0                                          # 默认的调试模式为：一个线程暂停运行，其它线程也随即暂停，即这里每输入一个n，
                                              # 线程2都前进一步，线程1就开始运行。线程2运行停止，线程1也跟着停止。
48              printf(" y=%d\n", y);
(gdb) set scheduler-locking on                 # 设定只有当前线程或指定线程可以运行
(gdb) n                    
 y=0            
49              sleep(1) ;**
```

# 6.运行日志
日志：平时经常使用print来进行代码的调试，日志就相当于将print的内容放入一个文件中，这个文件也叫做日志文件。





参考：[C语言gdb调试之精髓](https://www.bilibili.com/video/BV1ei4y1V758)