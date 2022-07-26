原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16244318.html
提交日期：Sat, 07 May 2022 14:10:00 GMT
博文内容：
fcntl系统调用是控制文件描述符属性的通用POSIX(POSIX是一种通用的规范)方法。
```
//头文件：
#include <unistd.h>    
#include <fcntl.h>

//定义函数：
int fcntl(int fd, int cmd);
int fcntl(int fd, int cmd, long arg);
int fcntl(int fd, int cmd, struct flock * lock);
```
fd：文件描述符
cmd：对fd的操作

# cmd选项

参考：[链接1](http://c.biancheng.net/cpp/html/233.html)
[链接2](https://www.cnblogs.com/xuyh/p/3273082.html)
还没参考，这两写呢.........


close-on-exec, 从字面意思即可理解为：如果对描述符设置了FD_CLOEXEC，在使用execl调用执行的程序里，此描述符将在子进程中会被自动关闭，不能使用了。




# execl函数
```
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/types.h>
#include <string.h>

int main(int argc, char *argv[])
{
    // execl函数
    // int execl(const char *pathname, const char *arg, ...

    //  pathname: 要执行的文件的路径（推荐使用绝对路径）
    //  接下来的参数代表执行该文件时传递过去的argv[0], argv[1], ..., 最后一个参数必须用空指针(NULL)作结束.
    //  argv[0]是程序名称，argv[1],...为程序后面所需要跟着的参数

    if (fork() > 0)
    {
        printf("I'm parent process: pid: %d\n", getpid());
        sleep(1);
    }
    else
    {
        // 当前是子进程
        // execl("/mnt/c/Users/x/Pictures/code/lesson14/2", "2", NULL);

        execl("/bin/ps", "ps", "a", "u", "x", NULL);

        printf("I'm child process: %d", getpid());
    }
    for (int i = 0; i < 3; i++)
    {
        printf("i=%d, pid: %d\n", i, getpid());
    }
}

```
这个函数是没有返回值的，因为从调用该函数开始，用户区就被调用的二进制程序给替换掉了，已经不再受我们控制
可以看到在程序运行时，printf("I'm child process: %d", getpid())并没有执行


参考：[链接1](https://blog.csdn.net/ma_de_hao_mei_le/article/details/122952159)
[链接2](http://c.biancheng.net/cpp/html/271.html)