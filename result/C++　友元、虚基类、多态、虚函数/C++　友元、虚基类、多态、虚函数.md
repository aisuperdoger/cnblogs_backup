原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16243244.html
提交日期：Sat, 07 May 2022 08:59:00 GMT
博文内容：
本文对友元、虚基类、多态和虚函数四个看起来高大上的概念进行介绍。

# 1.友元
友元：让其他函数（类外函数或者其他类的成员函数）可以访问对象的private和protect类型成员
## 1.1.友元函数
友元函数：在类内定义或声明的一个函数为友元，友元函数中创建的对象可以访问private和protect类型的数据成员。【注】友元函数不属于这个类中的成员函数，而是一个普通的类外函数或者其他类的成员函数。下面举两个实例进行说明：
友元函数为普通的类外函数：
```
#include <iostream>
#include <string>

class A {
private:
	int a;
	void printFun() {
		std::cout << a;
	}
public:
	A() {
		a = 1;
	}
	friend void accessPrivate(A b);  
};
void accessPrivate(A b) {
	b.printFun();
}

int main()
{
	A b = A();
	accessPrivate(b);
}
```
友元函数friend void accessPrivate(A b) 声明在类的任何位置都是可以的，即使声明在private下也可以。不过习惯将友元函数声明在类的最后面。

友元函数为其他类的成员函数：
```
#include <iostream>
#include <string>

class A;

class B {
public:
	void accessPrivate(A A1);  // 使用A，所以前面必须有A的声明
};

class A {
private:
	int a;
	void printFun() {
		std::cout << a;
	}
public:
	A() {
		a = 1;
	}
	friend void B::accessPrivate(A b); 
};

// 由于函数accessPrivate中调用了类A的printFun()函数，
// 所以必须等到类A的函数printFun()声明或定义完成后，
// 函数accessPrivate才能具体进行定义。
void B::accessPrivate(A A1) {  
	A1.printFun();
}


int main()
{
	B B1 = B();
	A A1 = A();
	B1.accessPrivate(A1);
}

```
## 1.2.友元类
友元类：将A声明为B的友元类，那么A的任意成员函数中创建的B类对象b，b都可以访问private和protect类型的数据成员。
``` 
#include <iostream>
#include <string>

class B;

class A {
private:
	int a;
	void printFun() {
		std::cout << a;
	}
public:
	A() {
		a = 1;
	}
	friend class B; 
};

class B {
public:
	void accessPrivate(A A1) {
		A1.printFun();
	}
};

int main()
{
	B B1 = B();
	A A1 = A();
	B1.accessPrivate(A1);
}
```
# 2.二义性问题
## 2.1.间接二义性问题（由虚基类解决）
间接二义性：首先我们知道子类继承父类中成员是将成员复制一份。当B和C都继承了A，然后D又继承了B和C。如果A中有成员a，那么D中就有两个名字相同的a。
虚基类：虚基类就是让当B和C都“虚”继承了A，如果D又继承了B和C。如果A中有成员a，那么D只有一个a。
举例如下：
```
#include<iostream>
using namespace std;

class base {
public:
	base() {
		a = 5; 
		cout << "base=" << a << endl;
	}

protected:
	int a;
};

class base1 :virtual public base {
public:
	base1() { 
		a += 10;
		cout << "base1=" << a << endl;
	}
};

class base2 :virtual public base {
public:
	base2() { 
		a += 20; 
		cout << "base2=" << a << endl; 
	}
};

class derived :public base1, public base2 {
public:
	derived() {
		cout << "derived a =" << a << endl; 
	}
};

int  main()
{
	derived obj;
	return 0;
}
```


## 2.2.多继承的二义性问题

多继承：子类有两个或两个以上的父类。
 二义性问题：多个基类中拥有同名的成员A，子类调用A时编译器无法确定调用的是哪个A。
二义性解决：
1）利用类的作用域分辨符。如Car::show()代表调用了类Car的函数show。
2）派生类中重定义此函数。
 3）将部分基类中的A改名。

# 3.多态
##3.1.多态
多态：假设B和C都继承于基类A，则B和C的对象都可以用基类的对象的指针a进行指向。当a调用方法x时，由于B和C类的方法x的实现是不一样，同样使用a->x得到的效果是不同。多态指的就是：使用相同的代码a->x，却可以根据a具体指向的对象而实现出不同的效果，这个不同的效果就是多态。
举例：
```
#include <iostream> 
using namespace std;

class Shape {
protected:
	int width, height;
public:
	Shape(int a = 0, int b = 0)
	{
		width = a;
		height = b;
	}
	int area()
	{
		cout << "Parent class area :" << endl;
		return 0;
	}
};
class Rectangle : public Shape {
public:
	Rectangle(int a = 0, int b = 0) :Shape(a, b) { }
	int area()
	{
		cout << "Rectangle class area :" << width * height << endl;
		return (width * height);
	}
};
class Triangle : public Shape {
public:
	Triangle(int a = 0, int b = 0) :Shape(a, b) { }
	int area()
	{
		cout << "Triangle class area :" << width * height / 2 << endl;
		return (width * height / 2);
	}
};
// 程序的主函数
int main()
{
	Shape *shape;
	Rectangle rec(10, 7);
	Triangle  tri(10, 5);

	// 存储矩形的地址
	shape = &rec;
	// 调用矩形的求面积函数 area
	shape->area();

	// 存储三角形的地址
	shape = &tri;
	// 调用三角形的求面积函数 area
	shape->area();

	return 0;
}
```
当上面的代码被编译和执行时，它会产生下列结果：
```
Parent class area :
Parent class area :
```
这就说明了shape->area()只调用了基类Shape中的area函数。
导致错误输出的原因是，调用函数 area() 被编译器设置为基类中的版本，这就是所谓的静态多态，或静态链接 - 函数调用在程序执行前就准备好了。有时候这也被称为早绑定，因为 area() 函数在程序编译期间就已经设置好了。
但现在，让我们对程序稍作修改，在 Shape 类中，area() 的声明前放置关键字 virtual，如下所示：
```
#include <iostream> 
using namespace std;

class Shape {
protected:
	int width, height;
public:
	Shape(int a = 0, int b = 0)
	{
		width = a;
		height = b;
	}
	virtual int area()
	{
		cout << "Parent class area :" << endl;
		return 0;
	}
};
class Rectangle : public Shape {
public:
	Rectangle(int a = 0, int b = 0) :Shape(a, b) { }
	int area()
	{
		cout << "Rectangle class area :" << width * height << endl;
		return (width * height);
	}
};
class Triangle : public Shape {
public:
	Triangle(int a = 0, int b = 0) :Shape(a, b) { }
	int area()
	{
		cout << "Triangle class area :" << width * height / 2 << endl;
		return (width * height / 2);
	}
};
// 程序的主函数
int main()
{
	Shape *shape;
	Rectangle rec(10, 7);
	Triangle  tri(10, 5);

	// 存储矩形的地址
	shape = &rec;
	// 调用矩形的求面积函数 area
	shape->area();

	// 存储三角形的地址
	shape = &tri;
	// 调用三角形的求面积函数 area
	shape->area();

	return 0;
}
```
修改后，当编译和执行前面的实例代码时，它会产生以下结果：
```
Rectangle class area :70
Triangle class area :25
```
此时，编译器看的是指针的内容，而不是它的类型。因此，由于 tri 和 rec 类的对象的地址存储在 *shape 中，所以会调用各自的 area() 函数。
#3.2.虚函数
虚函数是在基类中使用关键字 virtual 声明的函数。在派生类中重新定义基类中定义的虚函数时，会告诉编译器不要静态链接到该函数。我们想要的是在程序中任意点可以根据所调用的对象类型来选择调用的函数，这种操作被称为动态链接，或后期绑定。
**纯虚函数：**
您可能想要在基类中定义虚函数，以便在派生类中重新定义该函数更好地适用于对象，但是您在基类中又不能对虚函数给出有意义的实现，这个时候就会用到纯虚函数。
我们可以把基类中的虚函数 area() 改写如下：
```
class Shape {
   protected:
      int width, height;
   public:
      Shape( int a=0, int b=0)
      {
         width = a;
         height = b;
      }
      // pure virtual function
      virtual int area() = 0;
};
```
= 0 告诉编译器，函数没有主体，上面的虚函数是纯虚函数。


[菜鸟教程](https://www.runoob.com/cplusplus/cpp-polymorphism.html)还有七篇笔记没看，我先去睡觉，以后再看。。。。。。

参考：[菜鸟教程](https://www.runoob.com/cplusplus/cpp-polymorphism.html)
C++语言程序设计教程 第3版  沈显君 
