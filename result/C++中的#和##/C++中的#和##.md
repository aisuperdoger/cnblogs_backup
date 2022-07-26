原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/28/16321773.html
提交日期：Sat, 28 May 2022 12:03:00 GMT
博文内容：
\#\#组合出来的字符串代表一个标识符
\#组合出来的字符串就是一个字符串
```
#include <iostream>
#define t(x) hello##x//合并操作符##将出现在其左右的字符序列合并成一个新的标识符 
#define s(y) #y//将传入的参数变为字符串，字符串化

using namespace std;

int main()
{
	int hello1 = 10;
	cout << t(1) << endl;//将hello和1链接形成hello1,hello1是一个变量。输出：10
	cout << s(hello) << endl;//将hello变为字符串。输出：hello
	return 0;
}
```
[参考链接](https://blog.csdn.net/zhang_chou_chou/article/details/80737339)