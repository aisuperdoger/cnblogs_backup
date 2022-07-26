原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/06/13/16372215.html
提交日期：Mon, 13 Jun 2022 12:20:00 GMT
博文内容：
# 1.Python调用C++程序

1、编写C/C++实现程序。
2、将C/C++程序编译成动态库。
3、在Python中调用编译生成的库。

请参考：[简单的Python调用C++程序（使用ctypes模块）](https://blog.csdn.net/weixin_40313940/article/details/109515357)

python调用C++程序的其他方法：
boost.python：将c/c++的函数接口转换为Python接口有好几种解决方案，不同于C语言的简单直接，C++因使用了大量的面向对象编程的思想导致转换为Python接口时相对比较复杂，boost.python的目标就是为了简单方便地将C++程序转换成Python的接口。

# 2.C++中使用python程序
参考：[在C++中调用Python](https://www.cnblogs.com/dechinphy/p/cpp-python.html)



## 2.1.hello world

```
// cp.cpp
#include <Python.h>
int main(int argc, char *argv[]) {
  Py_Initialize();
  PyRun_SimpleString("print('hello world')\n");
  Py_Finalize();
  return 0;
}
```
执行命令：
```
g++ -o cpy cp.cpp  -I /usr/include/python3.9/ -l python3.9
```
使用-I（大写地i）指定头文件所在路径
虽然编译器会自动地去目录/usr/lib/查找库文件，但我们还是需要使用-l选项指定具体地库python3.9

【问题：/usr/lib/python3.9中几乎都是.py文件，为什么.py文件可以成为库文件】


## 2.2.调用Python函数string.split() 
在C++中如果我们想分割一个字符串，虽然说也是可以实现的，但是应该没有比Python中执行一个string.split()更加方便快捷的方案了，因此我们测试一个用C++调用Python的split函数的功能。

首先编写一个 pysplit.py文件：
```
# pysplit.py

def sp(string):
    return string.split()
```

cp.cpp中将 pysplit.py当成包进行调用。
```
#include <Python.h>
#include <iostream>
using namespace std;
int main(int argc, char *argv[])
{
  Py_Initialize();
  if (!Py_IsInitialized())
	{
		cout << "Initialize failed!" << endl;
		return 0;
	}
  PyObject* pModule = NULL;
  PyObject* pFunc;
  PyRun_SimpleString("import sys");
  PyRun_SimpleString("sys.path.append('./')");
  pModule = PyImport_ImportModule("pysplit");
  if (pModule == NULL)
	{
		cout << "Module Not Found!" << endl;
	}
  pFunc = PyObject_GetAttrString(pModule, "sp");
  PyObject* args1 = Py_BuildValue("s", "Test String");
  PyObject* args2 = Py_BuildValue("s", " Hello Every One !");

  PyObject* pRet = PyObject_CallFunctionObjArgs(pFunc, args1, args2, NULL); // PyObject_CallFunctionObjArgs(函数,参数1,参数2,……,NULL)
  int size = PyList_Size(pRet);
  cout << "List size is: " << size << endl;
  for(int i=0;i<size;i++)
  {
    PyObject* cRet = PyList_GET_ITEM(pRet, i);
    char* s;
    PyArg_Parse(cRet, "s", &s);
    cout << "The " << i << "th term is: " << s << endl;
  }
  Py_Finalize();
  return 0;
}
```
执行命令：
```
g++ -o cpy cp.cpp -lm -std=c++11 -I/usr/include/python3.9/ -lpython3.9 && ./cpy
```
最后，因为从Python中获取的是一个List格式的数据，因此我们首先需要用PyList_GET_ITEM去逐项提取，然后用PyArg_Parse将提取出来的元素保存到一个C++的char字符串中，执行结果如下：
```
dechin@ubuntu2004:~/projects/gitlab/dechin/$ g++ -o cpy cp.cpp -lm -std=c++11 -I/usr/include/python3.9/ -lpython3.9 && ./cpy
List size is: 6
The 0th term is: Test
The 1th term is: String
The 2th term is: Hello
The 3th term is: Every
The 4th term is: One
The 5th term is: !
```

说明：
1.代码中使用了sys.path.append('./')，这是因为：即使是在相同的路径下，也需要通过Python的sys将当前目录添加到系统路径中，才能够识别到这个模块。




tuple格式和**args有什么关系？？
答：[链接](https://www.cnblogs.com/dechinphy/p/args.html)

PyObject_CallFunctionObjArgs和PyObject_CallObject的区别？
答：[链接](https://stackoverflow.com/questions/60487083/passing-array-tuple-from-python-back-to-c)




## 2.5.python中如果有其他模块时





```
#include <Python.h>
#include <iostream>
using namespace std;
int main(int argc, char *argv[])
{
  Py_Initialize();
  if (!Py_IsInitialized())
	{
		cout << "Initialize failed!" << endl;
		return 0;
	}
  PyObject* pModule = NULL;
  PyObject* pFunc;
  PyRun_SimpleString("import sys");
  PyRun_SimpleString("sys.path.append('./')");
  pModule = PyImport_ImportModule("pyYolov5");
  if (pModule == NULL)
	{
		cout << "Module Not Found!" << endl;
	}
  pFunc = PyObject_GetAttrString(pModule, "run");
  PyObject* args = Py_BuildValue("s", "Test String Hello Every One !");
  PyObject* pRet = PyObject_CallFunctionObjArgs(pFunc, args, NULL);

  Py_Finalize();
  return 0;
}
```













使用PyRun_SimpleString，然后在python中调用python程序，从而传入参数
https://blog.csdn.net/qq_30694087/article/details/113748702
https://blog.csdn.net/sspdfn/article/details/62894607




仿照上面例子，调用yolov5，有什么问题再查，
调用成功，再对python.h进行学习。






使用Python.h调用python程序

如何使用C++执行python文件：
https://blog.csdn.net/dingyanxxx/article/details/46949405

https://zhuanlan.zhihu.com/p/80637788
https://zhuanlan.zhihu.com/p/79896193

https://docs.python.org/3/extending/embedding.html#embedding-python-in-c

https://blog.csdn.net/m0_46656879/article/details/124490820

【问题：/usr/lib/python3.9中几乎都是.py文件，为什么.py文件可以成为库文件】
答:主流的用法是把python作为一种文本形式的链接库，在c/c++程序中调用其中定义的函数。什么叫做文本形式的链接库？？
什么类型的文件可以作为C++链接库？？即可以用于-l后？


是不是还有其他在C++里面调用python程序的办法？？


# 其他

void Py_Initialize(void)
初始化Python解释器，如果初始化失败，继续下面的调用会出现各种错误，可惜的是此函数没有返回值来判断是否初始化成功，如果失败会导致致命错误。

int Py_IsInitialized(void)
检查是否已经进行了初始化，如果返回0，表示没有进行过初始化。

void Py_Finalize()
反初始化Python解释器，包括子解释器，调用此函数同时会释放Python解释器所占用的资源。

int PyRun_SimpleString(const char *command)
实际上是一个宏，执行一段Python代码。所以在PyRun_SimpleString中执行的代码，相当于作用于整个代码【我猜的】。




[python与C/C++相互调用](https://www.jianshu.com/p/335253cd688f)



# 1 官方文档
https://docs.python.org/3.9/c-api/

## 1.1 概述
**1.引入头文件：**
```
#define PY_SSIZE_T_CLEAN
#include <Python.h>
```
Python.h中定义的所有函数都是以Py_开头的。

**2.Python.h所处位置**
在 Unix 上，头文件Python.h位于以下目录：prefix/include/pythonversion/ 和 exec_prefix/include/pythonversion/，其中 prefix 和 exec_prefix 是由向 Python 的 configure 脚本传入的对应形参所定义。在 Windows 上，头文件安装于 prefix/include，其中 prefix 是向安装程序指定的安装目录。

我曾经用过的执行命令：
```
g++ -o test test.cpp  -I xx/anaconda3/envs/yolov5Env/include/python3.9/ -L xx/anaconda3/envs/yolov5Env/lib -l python3.9 -Wl,-rpath=xx/anaconda3/envs/yolov5Env/lib
```

**3.C++与C的API**
C++ 用户应该注意，尽管 API 是完全使用 C 来定义的，但头文件正确地将入口点声明为 extern "C"，因此 API 在 C++ 中使用此 API 不必再做任何特殊处理。


**4.有用的宏**
有用的宏：这一小节就是介绍一些有用的函数。


**5.PyObject*类型指针**
PyObject*类型指针，用于指向python的的任意对象，如整型、字符串、列表、函数等。
通过PyObject*，C++程序可以向python函数传递参数，python程序可以给C++程序返回运算结果。
由于几乎所有Python 对象都存在于堆上：所以您不能声明PyObject类型的自动或静态变量，只能声明 PyObject*类型的指针变量。唯一的例外是type objects；因为这些永远不能被释放，它们通常是静态的PyTypeObject对象【看不懂】。

每一种python中常见的类型都对应一个检测类型的宏，如PyList_Check(a)用于检测a是否为python中的list


python程序和c程序在互传变量的时候，注意引用计数的问题。


变量和引用的生命一样长，就不需要考虑增加引用计数。


PyTuple_SetItem()是设置元组的唯一方法；PySequence_SetItem()和PyObject_SetItem()不用于设置元组，因为元组是不可变的数据类型
使用PyTuple_New()和PyTuple_SetItem()创建python tuple  
使用PyList_New()和PyList_SetItem()创建python list
一般不使用上面两种方法，而使用通用的方法Py_BuildValue()来创建元组和列表。



问题：
类似PyImport_ImportModule这样常用的函数怎么都找不到？？
答：PyImport_ImportModule在工具——》导入模块中。


extern "C"中不能创建类和对象吗？？


PyObject_CallFunctionObjArgs如何传递多个参数？
