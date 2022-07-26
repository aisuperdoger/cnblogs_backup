原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16243223.html
提交日期：Sat, 07 May 2022 08:57:00 GMT
博文内容：
#　1.模板
模版分为：类模版、函数模版、成员模板。
## 1.1.类模板
用一个实例进行说明：
```
template<typename T>	// 类模板，
class complex{
private:
    T re, im;	// 模板
    friend complex& __doap1 (complex *ths, const complex& r); 	// 友元函数

public:
    complex(T r = 0, T i = 0) : re(r), im(i){}	// 默认参数、初始化列表
    complex& operate+=(const complex&);	// 重载运算符
    T real() const { return re; }		// 成员函数-常函数
    T imag() const { return im; }
};

int main(){
    complex<double> c1(1.1, 2.2);
    complex<int> c2(3, 4);
}
```
在类complex的定义前，加一个template<typename T>：代表数据类型T是在声明对象的时候指定的，如complex<double> c1(1.1, 2.2);指定了T为double类型。
注：template<typename T>有时也写成template<class T>，它们是一样的，只是早期一般使用template<class T>。


## 1.2. 函数模板
用一个实例进行说明：
```
#include <iostream>

// 函数模板
template<class T>
inline T& min(T& a,  T& b) {
	return b < a ? b : a;	// 运算符< 可被重载
}

class stone {
	private:
		int _w, _h, _weight;
	public:
		stone(int w, int h, int we) : _w(w), _h(h), _weight(we) {}
		// 重载运算符<
		bool operator <(const stone& rhs) {
			return this->_weight < rhs._weight;
		}

		int getWeight() {
			return _weight;
		}
};

int main() {
	stone r1(2, 3,5), r2(3, 3,1);
	// 调用模板函数min，类型推导
	// 类型推导T为stone类型，进一步调用stone::operator<()
	stone r3 = min(r1, r2);
	std::cout << r3.getWeight();

	return 0;
}
```
注：函数模板使用时，不必显式指定具体的泛型类型。编译器会对函数模板进行实参推导/类型推导（argument deduction）。类模板使用时，需显式指定具体的泛型类型。


## 1.3.成员模版
成员模板：类模板中的成员函数也为模板。举例如下：
```
template <typename T>
 
class A {
public:
  template <typename U>
  void assign(const D<U>& u)
  {
    v = u.getvalue();
  }
  
  T getvalue()
  {
    return v;
  }
private:
  T v;
}
```
【注】成员模板不能是virtual

模板构造函数：一种特殊的成员模板
```
#include <iostream>

template <typename T>
class A
{
public:
	template <typename U>
	A(const U& a) {
		std::cout << "template constructor" << std::endl;
	}

	A(const A& a) {
		std::cout << "copy constructor" << std::endl;
	}
	A() {
		std::cout << "default constructor" << std::endl;
	}
};

int main() {
	A<int> i; // default constructor
	A<int> ii(i); // implicitly generated copy constructor
	A<double> d(i); // template constructor

	std::cin.get();
	return 0;
}
```
结果为：
```
default constructor
copy constructor
template constructor
```
由于ii和i的类型是一样的，所以调用类A<int>的拷贝构造函数A(const A& a) 对ii进行初始化。
由于d和i的类型是不一样的，所以调用A<double>的模板构造函数 A(const U& a) 来对d进行初始化。其中U的类型为A<int>。这就相当于A<double> d(i)就实现了用类A<int>初始化类A<double>，也就是说实现了隐式的类型转换。
”ii和i的类型是一样时，调用类A<int>的拷贝构造函数对ii进行初始化“，这就说明了A<int> ii(i)没有调用模板构造函数 A(const U& a) ，而是调用了拷贝构造函数A(const A& a)。也就是说模板构造函数 A(const U& a)没有覆盖掉拷贝构造函数A(const A& a)的作用。

参考：[链接1](https://blog.csdn.net/luoshabugui/article/details/104619151)
