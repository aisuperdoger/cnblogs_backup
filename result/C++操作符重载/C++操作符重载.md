原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16243232.html
提交日期：Sat, 07 May 2022 08:58:00 GMT
博文内容：
操作符重载：定义用操作符来操作对象时所产生的效果，如定义用加号来操作对象时所产生的效果（加法的重载）：
```
#include <iostream>
using namespace std;

class complex
{
public:
	complex(double a, double b);
	complex operator+(const complex & A)const;

	void display()const;
private:
	double real;   //复数的实部
	double imag;   //复数的虚部
};


complex::complex(double a, double b)
{
	real = a;
	imag = b;
}

//打印复数
void complex::display()const
{
	cout << real << " + " << imag << " i ";
}

//重载加法操作符
complex complex::operator+(const complex & A)const
{
	complex B(0,0);
	B.real = real + A.real;
	B.imag = imag + A.imag;
	return B;
}


int main()
{
	complex c1(4.3, -5.8);
	complex c2(8.4, 6.7);
	complex c3(0,0);

	//复数的加法
	c3 = c1 + c2;
	cout << "c1 + c2 = ";
	c3.display();
	cout << endl;

	return 0;
}
```