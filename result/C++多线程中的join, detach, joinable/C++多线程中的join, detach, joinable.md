原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/27/16526544.html
提交日期：Wed, 27 Jul 2022 13:21:00 GMT
博文内容：
thread对象构造完成（线程开始执行）之后，对象析构之前，我们必须选择是等待它（join）或者让它在后台运行（detach），如果你在thread对象析构前没有这么做，那么线程将会终止，因为thread的析构函数中调用了std::terminate()。
join的意思是父线程等待子线程结束
detach的含义是主线程和子线程相互分离，但是主线程结束了，子线程也会结束。

joinable()函数是一个布尔类型的函数，他会返回一个布尔值来表示当前的线程是否是可执行线程(能被join或者detach)，因为相同的线程不能join两次，也不能join完再detach，同理也不能detach完再join，所以joinable函数就是用来判断当前这个线程是否可以joinable的。通常不能被joinable有以下几种情况：

       1）由thread的缺省构造函数而造成的（thread()没有参数）。

       2）该thread被move过（包括move构造和move赋值）。

       3）该线程被join或者detach过。


线程没有执行join和detach时：
```
#include <iostream>
#include <thread>
#include <unistd.h>

using namespace std;
void func2(){
    cout<<"22222"<<endl;
}
 
void func(){
    cout<<"11111111"<<endl;
    thread t(func2);
    cout<<"33333333"<<endl;
}

int main(){
    func();
    cout<<"main"<<endl;

    sleep(10);

    return 0;
}
```
结果：
```
g++ -Wall -g -std=c++11 -pthread test2.cpp -o test2
./test2 
11111111
33333333
terminate called without an active exception
Aborted (core dumped)
```
在函数func中，启动线程t，但是线程t没有执行join或detach，那么在函数func执行完毕的时候就会发生错误，从而中断整个程序。

[使用detach时，如果子线程还没清理垃圾，主线程就结束了，那么就会导致内存溢出](https://blog.csdn.net/yixinuestc/article/details/122229052)

[C++多线程，请参考此链接进行学习](https://blog.csdn.net/m0_37621078/article/details/104909834)


参考：[C++多线程中的join, detach, joinable](https://blog.csdn.net/Charles_Zaqdt/article/details/104134965)
