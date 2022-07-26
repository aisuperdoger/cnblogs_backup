原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/11/16256860.html
提交日期：Wed, 11 May 2022 02:22:00 GMT
博文内容：

学会使用vscode编程c++、python，学会vscode和vim一样——“机会不碰鼠标”


[【c++】VSCode配置 c++ 环境（小白教程）](https://blog.csdn.net/Zhouzi_heng/article/details/115014059)
[vscode ssh远程连接服务器 无法跳转函数定义](https://blog.csdn.net/qq_41381865/article/details/116120074)

[VSCode 返回上一个光标 (上一个浏览位置)](https://blog.csdn.net/M_N_N/article/details/84581840)


# 添加C++库文件
参考：[链接](https://www.cnblogs.com/dechinphy/p/cpp-python.html)
原文件：
```
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/gcc",
            "cStandard": "gnu17",
            "cppStandard": "c++11",
            "intelliSenseMode": "linux-gcc-x64"
        }
    ],
    "version": 4
}
```
在includePath中添加头文件路径：
```
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "/usr/include/python3.9/",
                "/usr/lib/python3.9/",
                "/usr/include/python3.9/cpython/"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/gcc",
            "cStandard": "gnu17",
            "cppStandard": "c++11",
            "intelliSenseMode": "linux-gcc-x64"
        }
    ],
    "version": 4
}
```
