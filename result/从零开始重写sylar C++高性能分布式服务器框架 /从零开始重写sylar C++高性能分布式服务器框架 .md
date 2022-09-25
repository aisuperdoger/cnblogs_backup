原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/08/07/16560076.html
提交日期：Sun, 07 Aug 2022 14:15:00 GMT
博文内容：
本博客是对此视频的总结：https://www.bilibili.com/video/BV184411s7qF
作者博客：http://www.sylar.top
项目地址：https://github.com/sylar-yin/sylar

# 随笔

一个项目一般具有以下目录结构：
```
bin — 二进制
build — 中间文件路径
cmake — cmake函数文件夹
CMakeLists.txt — cmake的定义文件
lib — 库的输出路径
Makefile
sylar — 源代码路径
tests — 测试代码
```

先写头文件，

看到第3讲，准备看第四讲

前三讲说了三个类——Logger 、LogAppender、LogFormatter
Logger 相当于是主类
LogAppender是一个基类，有两种子类，两个子类分别为“输出日志到文件”和“输出日志到终端”
LogFormatter：日志格式化



LogEvent是存放信息的地方，包括文件名、线程号、协程号等内容。
LogFormatter是安排数据摆放顺序，包含模式解析等功能（可以看看log4j标准)
LogAppender是输出地，可以选择文件或控制台进行输出，里面也包含了LogFormatter对象，来保证不同的输出地可以以不同的格式呈现。
Logger是日志器，作为控制中枢可以将同一个信息添加多个LogAppender和LogFormatter对象来保证可以同时往多个地方输出

可以看出LogEvent、LogFormatter和LogAppender都是可以扩展的，即可扩展输出内容、扩展输出格式和扩展输出地。

参考：[链接](https://blog.csdn.net/m0_55292629/article/details/125147780)

LogEvent用于存放各种信息。LogFormatter用于组织LogEvent的信息成一定的格式，如下：
2019-06-17 00:28:45     9368    main    6       [INFO]  [system]        sylar/tcp_server.cc:64  server bind success: [Socket sock=9 is_connected=0 family=2 type=1 protocol=0 local_address=0.0.0.0:8020]



每一个类中都定义了本类的智能指针类型ptr，如LogFormatter类中：
```
class LogFormatter {
 public:
     typedef std::shared_ptr<LogFormatter> ptr;
};
```


C++11以后，可以直接在定义成员变量的时候进行初始化，如
```
class{
  int getA(){return A;}
private:
  int A=1
};
```


一般现在头文件中规划要实现那几个类和类中的函数，然后再去写具体的cpp文件。


要学会使用int32_t和uint32_t等类型，而不是只会使用int。

# C++ 宏的高级使用
```
#include <iostream>
#include<string>
using namespace std;

enum Level
{
    /// 未知级别
    UNKNOW = 0,
    /// DEBUG 级别
    DEBUG = 1,
    /// INFO 级别
    INFO = 2,
    /// WARN 级别
    WARN = 3,
    /// ERROR 级别
    ERROR = 4,
    /// FATAL 级别
    FATAL = 5
};

int main()
{
     Level level = DEBUG;

    switch (level)
    {
#define XX(name)      \
    case name:        \
        cout<< #name; \
        break;   // 到此为止相当于宏的定义。宏XX是一个一个case语句。

        XX(DEBUG);
        XX(INFO);
        XX(WARN);
        XX(ERROR);
        XX(FATAL);
#undef XX  // XX是一个临时使用的宏，这里进行取消定义
    default:
        cout<<"UNKNOW";
    }

    return 0;
}  
```


变量、函数、类的命名：
