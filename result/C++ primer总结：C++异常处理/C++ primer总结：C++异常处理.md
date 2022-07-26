原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/22/16505862.html
提交日期：Fri, 22 Jul 2022 07:15:00 GMT
博文内容：
# 1.简介
异常处理：throw在try中抛出异常，根据异常的不同选择不同的catch块。
多层函数调用中，出现异常，程序会一层一层的往上寻找对应的catch语句，找不到就终止程序。
catch块中一般进行内存释放等清理操作。
大多数常见的类都是定义在标准库中的，所以调用的时候，都要带std::，如std::runtime_error。
如果异常类型有一个字符串初始值，则what()返回字符串。
exception是所有标准 C++ 异常的父类

# 2.实例
**1.抛出runtime_error异常：**
```
#include <iostream>
#include <stdexcept>
using std::cin; using std::cout; using std::endl; using std::runtime_error;

int main(void)
{
    for (int i, j; cout << "Input two integers:\n", cin >> i >> j; )
    {
        try 
        {
            if (j == 0) 
                throw runtime_error("divisor is 0");
            cout << i / j << endl;
        }
        catch (runtime_error err) 
        {
            cout << err.what() << "\nTry again? Enter y or n" << endl;
            char c;
            cin >> c;
            if (!cin || c == 'n')
                break;
        }
    }

    return 0;
}
```
**2.直接抛出字符串**
```
#include <iostream>
using namespace std;
 
double division(int a, int b)
{
   if( b == 0 )
   {
      throw "Division by zero condition!";
   }
   return (a/b);
}
 
int main ()
{
   int x = 50;
   int y = 0;
   double z = 0;
 
   try {
     z = division(x, y);
     cout << z << endl;
   }catch (const char* msg) {
     cerr << msg << endl;
   }
 
   return 0;
}
```

**3.catch(...)处理任何异常的代码**

修改“2.直接抛出字符串”中的代码，如下：
```
#include <iostream>
using namespace std;
 
double division(int a, int b)
{
   if( b == 0 )
   {
      throw "Division by zero condition!";
   }
   return (a/b);
}
 
int main ()
{
   int x = 50;
   int y = 0;
   double z = 0;
 
   try {
     z = division(x, y);
     cout << z << endl;
   }catch (...) {
     cerr << "处理异常。。。" << endl;
   }
 
   return 0;
}
```

# 3.定义新的异常
直接看[菜鸟教程](https://www.runoob.com/cplusplus/cpp-exceptions-handling.html)：就是继承了父类exception，重写了成员函数what()
