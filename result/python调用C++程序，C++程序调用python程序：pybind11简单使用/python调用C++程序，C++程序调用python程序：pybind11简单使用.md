原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/23/16512831.html
提交日期：Sat, 23 Jul 2022 11:28:00 GMT
博文内容：
本博客只是对[链接](https://blog.csdn.net/henuyh/article/details/119341884)进行补充说明。

通过git clone https://github.com/pybind/pybind11.git 下载源码，可以发现源码中并没有cpp文件，只有.h文件，也就是说pybind11将实现的代码都放进了.h文件中了。所以pybind11其实是不用进行编译安装，就可以使用的，直接通过include相关头文件就可以。

# python调用C++程序的实例：
pyadd.cpp：
```
#include <pybind11/pybind11.h>

/***********************调用普通函数***********************/
template <typename T>
T add(T a, T b) {
  return a + b;
}

PYBIND11_MODULE(pyadd, m) {
  m.doc() = "test for add()";
  m.def("add", &add<int>, "add two number.");
  m.def("add", &add<double>, "add two number.");
  m.def("add", &add<long long>, "add two number.");
  m.attr("__version__") = "dev";
}
```
将pyadd编译成动态库：
```
g++ pyadd.cpp -I ./ -I /home/ubuntu1/anaconda3/envs/test/include/python3.9 -L /home/ubuntu1/anaconda3/envs/test/lib -l python3.9  -fPIC -shared  -o pyadd.so 
```
第一个-I用于指明头文件pybind11.h位置，第二个-I指明Python.h所在位置。
这里动态库的名字为pyadd.so，那么在python程序中使用“import pyadd”进行导入，如：
pytest.py
```
import pyadd
print(pyadd.__version__)
# 'dev' 
print(pyadd.add(1.1, 2.2))  
# 3.3000000000000003 
```
由于pyadd.so是由虚拟环境“test” 中python生成的，所以需要使用虚拟环境test中的python执行脚本pytest.py:
```
conda activate test
python3 pytest.py
```
