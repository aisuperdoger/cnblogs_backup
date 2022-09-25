原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/09/01/16646690.html
提交日期：Thu, 01 Sep 2022 07:29:00 GMT
博文内容：



```
#include<iostream>

class A{
public:
        void t(){
                std::cout<< "hello world!" << std::endl;
        }
        ~A(){
                std::cout<< "调用析构函数" << std::endl;
        }
        int a;
};

int main(){
        A *p = new A;
        p->a = 2;
        delete p;
        p->t();
        std::cout << "p->a:" << p->a << std::endl;

        return 0;
}
```
输出：
```
调用析构函数
hello world!
p->a:0
```
delete p操作首先会调用p指向对象的析构函数，然后将成员变量a置空，但是delete操作并没有将p所指向的内存全部置空，这就是为什么依然可以通过p->t()和p->a访问成员的原因。

还需要注意的是：delete操作并没有将t()删除，因为t()是所有对象共有的。

还可以参考[链接](https://bbs.csdn.net/topics/392044647)进行学习。
