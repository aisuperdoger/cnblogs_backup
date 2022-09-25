原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/09/23/16724400.html
提交日期：Fri, 23 Sep 2022 13:14:00 GMT
博文内容：
# 1.C++语言

[C++中的头文件（.h）](https://blog.csdn.net/qq_42775938/article/details/123168445#comments_21679785)


## 1.1 virtual
[C++ static静态成员函数详解](http://c.biancheng.net/view/2228.html)：普通成员函数隐含形参this
[ C++中类的普通成员函数不能作为 pthread_create的线程函数](https://blog.csdn.net/hsd2012/article/details/51207585)：因为普通成员函数隐含形参this
[C++中虚析构函数的作用及其原理分析](https://blog.csdn.net/weicao1990/article/details/81911341)：当父类的析构函数不声明成虚析构函数的时候，当子类继承父类，父类的指针指向子类时，delete掉父类的指针，只调动父类的析构函数，而不调动子类的析构函数


# 2.C++编译


## 2.1 gcc编译和gdb调试的学习
C程序编译成可执行文件后，才能有运行。我常用gcc工具将c程序编译成可执行文件。
GCC编译流程分为四个步骤： 编译预处理、编译、汇编和链接
请参考：[gcc编译和gdb调试的学习](https://blog.csdn.net/qq_42775938/article/details/122346013)

我觉得gdb对我没什么用。知道gdb是对生成的二进制文件进行调试就行。
确实有兴趣的可参考： [gdb调试](https://www.cnblogs.com/codingbigdog/p/16424650.html)



## 2.2 C\C++ 静态库和动态库
[静态库和动态库的简介和制作](https://www.cnblogs.com/codingbigdog/p/16412416.html)
[linux Ｃ\C++动态库（共享库）编译和运行时的链接](https://www.cnblogs.com/codingbigdog/p/16320965.html)
[动态链接库的隐式加载和显示加载](https://www.cnblogs.com/codingbigdog/p/16414555.html)



## 2.3 makefile、cmake和configure脚本
使用g++编译程序的时候，需要依赖很多库文件和头文件，当工程很大时，在命令行中使用一条gcc命令编译整个工程就会显得困难。
所以我们将gcc编译各种程序的命令放入一个文件中，这个文件命名为Makefile。
[makefile使用](https://www.cnblogs.com/codingbigdog/p/16262239.html)

上面我们学到的是linux下Makefile的编写规则，但是不同平台有不同的Makefile文件编写规则，为了解决不同平台编写规则的不同，就需要使用cmake。在使用cmake时，需要开发者编写一种平台无关的CMakeList.txt 文件来定制整个编译流程，然后通过cmake命令就可以根据目标的平台生成所需的本地化Makefile和工程文件。
[cmake入门](https://www.cnblogs.com/codingbigdog/p/16459532.html)

./configure是一种叫autoconf的构建工具自动生成的构建文件，它以shell script的形式存储，在cmake之前是c/c++的主流构建工具。近年来很多项目有从autoconf转向cmake的趋势。autoconf和cmake的共同点是会生成makefile，然后从makefile执行真正的编译构建过程。
[configure生成Makefile文件全过程](https://www.cnblogs.com/Braveliu/p/11340132.html)




# C++与python的互相调用
[python调用C++程序，C++程序调用python程序：pybind11简单使用](https://www.cnblogs.com/codingbigdog/p/16512831.html)
