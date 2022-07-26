原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16243235.html
提交日期：Sat, 07 May 2022 08:59:00 GMT
博文内容：
#1.简介
拷贝构造函数（一种特殊的构造函数）：用一个对象初始化一个新建立的对象。默认拷贝构造函数的功能是把传入的对象的每个数据成员的值依次复制到新建立的对象中。
拷贝构造函数在三种情况下被调用：1）用于用一个对象初始化另一个对象 2）对象作为实参传递给形参 3）作为函数的返回值。举例如下：
```
#include<iostream>
using namespace std;

class Clock {
private:
	int H, M, S;
public:
	Clock(int h = 0, int m = 0, int s = 0) {	// 构造函数 
		H = h, M = m, S = s;
		cout << "constructor:" << H << ":" << M << ":" << S << endl;
	}

	~Clock() {
		cout<<"destructor:" << H << ":" << M << ":" << S << endl;
	}

	// 拷贝构造函数
	Clock(Clock &p) { // 由于一般不修改p，所以Clock(Clock &p)一般写为Clock(const Clock &p)
		H = p.H;
		M = p.M;
		S = p.S;
		cout << "copy constructor,before call:" << H << ":" << M << ":" << S << endl;
	}
};

Clock fun(Clock c) {
	return c;
}

int main() {
	Clock c1(8, 0, 0); // 调用构造函数
	Clock c2(9, 0, 0); // 调用构造函数
	Clock c3(c2); // 等价于Clock c3 =c2;，这里调用拷贝构造函数
	fun(c2); // c2作为实参传入时，调用一次拷贝构造函数。返回Clock对象时，又调用一次拷贝构造函数

	Clock c4;
	c4 = c2;	// c2和c4都是已存在的对象。此时不调用拷贝构造函数

	return 0;
}
```
结果如下：
```
constructor:8:0:0           // Clock c1(8, 0, 0); 输出
constructor:9:0:0           // Clock c2(9, 0, 0);输出
copy constructor,before call:9:0:0      // Clock c3(c2); 输出
copy constructor,before call:9:0:0      // c2作为实参传入fun(c2)时，调用一次拷贝构造函数。
copy constructor,before call:9:0:0      // fun(c2)返回Clock对象时，又调用一次拷贝构造函数
destructor:9:0:0
destructor:9:0:0
constructor:0:0:0          //  Clock c4;输出
```
额外说明：当对象作为函数的返回值时需要调用拷贝构造函数，此时C++将从堆中动态建立一个临时对象，将函数返回的对象复制给该临时对象，并把该临时对象的地址存储到寄存器里，从而由该临时对象完成函数返回值的传递。

# 2.深拷贝构造函数
深拷贝构造函数：默认拷贝构造函数是将一个对象的所有数据成员的值，复制给另一个对象的所有数据成员。但是当数据成员中存在指针时，默认拷贝构造函数只会拷贝地址到另一个对象。这就会导致两个不同的指针指向同一个地址，两个对象中的指针指向同一个内存空间，可能会导致内存的多次释放。
这个时候就需要重写拷贝构造函数来开辟新的内存空间，从而让两个不同的指针指向的地址不同且不同地址中存储的数据是相同的。举例如下：
```
#include <iostream>
using namespace std;

class test {
public:
	char* Str;

	test(const char* str) {
		int a = strlen(str);//改为sizeof就是错的
		Str = new char[a + 1];
	
		strcpy_s(Str, a+1,str); 
	}
	~test() {
		delete[] Str;
		Str = nullptr;
	}
};



int main() {
	test t1("aaaaaaa1"); // 
	test t2(t1);		//  t2.Str指向的地址和t1.Str指向的地址是一样的。

	return 0;
}
```
test t2(t1);使用默认拷贝构造函数，t2.Str指向的地址和t1.Str指向的地址是一样的，假设都指向地址A。那么对象t1和t2都会调用析构函数来释放地址A上的空间，这就会导致重复释放同一个空间，从而导致错误。
重写拷贝构造函数，修改代码为：
```
#include <iostream>
using namespace std;

class test {
public:
	char* Str;

	test(const char* str) {
		int a = strlen(str);//改为sizeof就是错的
		Str = new char[a + 1];
	
		strcpy_s(Str, a+1,str); 
	}
	~test() {
		delete[] Str;
		Str = nullptr;
	}
	test(const test &p) {
		int a = strlen(p.Str);//改为sizeof就是错的
		Str = new char[a + 1];

		strcpy_s(Str, a + 1, p.Str);
	}

	
};

int main() {
	test t1("aaaaaaa1"); // 
	test t2(t1);		// t2,Str指向的地址和t1.Str指向的地址是一样的。

	return 0;
}
```