原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/08/14/16585553.html
提交日期：Sun, 14 Aug 2022 07:43:00 GMT
博文内容：
请直接参考：[C++11中enable_shared_from_this的用法解析](https://blog.csdn.net/breadheart/article/details/112451022)

> std::enable_shared_from_this 能让一个对象（假设其名为 t ，且已被一个 std::shared_ptr 对象 pt 管理）安全地生成其他额外的 std::shared_ptr 实例（假设名为 pt1, pt2, ... ） ，它们与 pt 共享对象 t 的所有权。
       
> 若一个类 T 继承 std::enable_shared_from_this<T> ，则会为该类 T 提供成员函数： shared_from_this 。 当 T 类型对象 t 被一个为名为 pt 的 std::shared_ptr<T> 类对象管理时，调用 T::shared_from_this 成员函数，将会返回一个新的 std::shared_ptr<T> 对象，它与 pt 共享 t 的所有权。







**什么时候使用：**当一个类被共享智能指针 share_ptr 指向，且在类的成员函数里需要把当前类对象作为参数传给其他函数时，这时就需要传递一个指向自身的 share_ptr。下面例子描述了这一种情况：



```
#include <iostream>
#include <stdlib.h>
#include <memory>
using namespace std;

// 比较推荐的写法
struct Good : std::enable_shared_from_this<Good> // note: public inheritance
{
    std::shared_ptr<Good> getptr() {
        return shared_from_this();
    }
};

int main()
{
    // 正确的用法: 两个 shared_ptr 共享同一个对象
    std::shared_ptr<Good> gp1 = std::make_shared<Good>();
    std::shared_ptr<Good> gp2 = gp1->getptr();
    std::cout << "gp2.use_count() = " << gp2.use_count() << '\n';
}
```
首先在main函数，使用make_shared创建了一个对象，并使用智能指针gp1管理这个对象
然后gp1->getptr()中调用shared_from_this()，shared_from_this()的作用是：返回一个智能指针，此智能指针和gp1共享同一个对象。

**不能够直接返回this**：一般来说，我们不能直接将 this 指针返回。如果函数将 this 指针返回到外部某个变量保存，然后这个对象自身已经析构了，但外部变量并不知道，此时如果外部变量再使用这个指针，就会使得程序崩溃。
