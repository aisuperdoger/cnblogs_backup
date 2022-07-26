原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16243176.html
提交日期：Sat, 07 May 2022 08:49:00 GMT
博文内容：
C++ 不包含多线程应用程序的任何内置支持。相反，它完全依赖于操作系统来提供此功能，如在Linux中就使用POSIX 编写多线程 C++ 程序。下面介绍POSIX 编写多线程 C++ 程序。
```
#include <pthread.h>
pthread_t tid;  // 创建一个用于保存线程的变量
pthread_create (thread, attr, start_routine, arg) 
// thread：被创建的线程
// attr：设置线程属性
// start_routine：线程执行的函数
// arg：start_routine中传入的参数
pthread_exit (status) 
```

写个鸡巴，不想写了，待续。。。。。。。


# 问题
void 类型数据是什么？
什么时候用？
函数前的void *又是干嘛用的？？
pthread_exit (status)中的status除了是NULL，还可以是什么？














参考：[链接](https://www.w3cschool.cn/cpp/cpp-multithreading.html)