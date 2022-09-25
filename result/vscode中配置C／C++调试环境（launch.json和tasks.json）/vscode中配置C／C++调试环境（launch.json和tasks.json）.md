原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/08/16459417.html
提交日期：Fri, 08 Jul 2022 11:09:00 GMT
博文内容：
# 1.launch.json和tasks.json
## 1.1 launch.json


launch.json中存放运行或者调试可执行文件时的配置：
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "g++ - Build and debug active file",  // 名字随便取
            "type": "cppdbg",
            "request": "launch",
            // program 指定调试那个可执行文件，需要绝对路径
            // ${fileDirname} 当前打开的文件所在的绝对路径，不包括文件名
            // ${fileBasenameNoExtension} 当前打开的文件的文件名，不包括路径和后缀名
            "program": "${fileDirname}/${fileBasenameNoExtension}.out", 
            "args": [],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description": "Set Disassembly Flavor to Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "C/C++: g++ build active file",  // 在执行lanuch.json之前要做的任务
            "miDebuggerPath": "/bin/gdb"        // 指定调试工具
        }
    ]
}

```
其他参数解释：
```
${fileBasename}  当前打开的文件名+后缀名，不包括路径
${fileExtname} 当前打开的文件的后缀名
${cwd} the task runner's current working directory on startup
${workspaceFolder} .vscode所在目录的绝对路径
```


【注】文件名launch.json的前后不能有空格。如果你发现launch.json中明明正确的地方竟然都有红色的波浪线，很可能就是你的文件名launch.json有问题。

## 1.2 tasks.json

tasks.json中存放生成可执行文件的命令：
```
{
    "tasks": [
        {
            "type": "cppbuild",
            "label": "C/C++: g++ build active file",  // 任务名，在lanuch.json使用此任务名，从而执行此任务
            "command": "/bin/g++",
            "args": [
                "-fdiagnostics-color=always",
                "-g",
                // "${file}",
                "${fileDirname}/*.cpp",   // 编译当前打开的文件所在目录下的所有.cpp文件
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}.out"  // 目标文件名
            ],
            "options": {
                "cwd": "${fileDirname}"
            },
            "problemMatcher": [
                "$gcc"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "detail": "调试器生成的任务。"
        }
    ],
    "version": "2.0.0"
}
```

## 1.3 c_cpp_properties.json
本小节使用cmake生成compile_commands.json，然后在c_cpp_properties.json中配置c_cpp_properties.json文件实现代码的跳转。具体见[vscode使用compile_commands.json配置includePath环境](https://blog.csdn.net/qq_37868450/article/details/105013325).
这里的代码跳转指的是：光标移动到相应函数，然后按“ctrl+点击”就可以进行跳转。如果需要在debug的时候实现代码跳转，直接在launch.json中指定cmake生成的可执行文件就可以。



# 2.测试项目
项目结构：
```
├── include
│   └── Sales_item.h
├── src
│   ├── main.cpp
│   └── Sales_item.cpp
└── .vscode
    ├── launch.json
    └── tasks.json

```
main.cpp
```
#include <iostream>
#include "../include/Sales_item.h"

using namespace std;

int main() {
    Sales_item item1, item2;

    item1.isbn = "0-201-78345-X";
    item1.units_sold = 10;
    item1.revenue = 300.0;

    cout << item1.avg_price() << endl;

    item2.isbn = "0-201-78345-X";
    item2.units_sold = 2;
    item2.revenue = 70;

    cout << item2.avg_price() << endl;

    if (item2.same_isbn(item1)) {
        cout << "same" << endl;
    } else {
        cout << "not same" << endl;
    }

    return 0;
}
````

Sales_item.h
```
#ifndef __SALES_ITEM_H_
#define __SALES_ITEM_H_

#include <string>

class Sales_item {
public:
    // 常量成员函数
    // 由于这个函数不对类的数据成员做任何修改，所以可以定义为常函数【参数列表后面加上const】
    bool same_isbn(const Sales_item &rhs) const {
        // this->isbn = "1";  // 错误，常函数不能修改数据成员
        return this->isbn == rhs.isbn;
    }

    double avg_price() const;

public:
    Sales_item() : units_sold(0), revenue(0) {}

    // 本来应该将成员变量设为private的，但是为了方便，写成public
public:
    std::string isbn;
    unsigned units_sold;
    double revenue;
};

#endif  // !__SALES_ITEM_H_
```
Sales_item.cpp
```
#include "../include/Sales_item.h"

// 类外定义成员函数体，需要加上类作用域，即类的名字
double Sales_item::avg_price() const {
    if (!this->units_sold) {
        return 0;
    } else {
        return this->revenue / this->units_sold;
    }
}
```
直接复制上面提到的lanuch.json和task.json到.vscode文件夹下，然后在main.cpp文件下点击“运行——》启动调试”
