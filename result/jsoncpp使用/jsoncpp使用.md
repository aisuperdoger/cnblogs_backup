原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/06/06/16350049.html
提交日期：Mon, 06 Jun 2022 14:44:00 GMT
博文内容：
jsoncpp源码位置：https://github.com/open-source-parsers/jsoncpp

# 1.jsoncpp简介
jsoncpp是一个用来存储键值对的库。
键值对的值可以是双引号包起来的字符串、数、布尔类型、null、对象或者数组
上面所说的大家都很熟悉，只有最后两个是比较特殊的：
对象：这里对象的概念和C++中对象的概念不一样，这里的对象指的是用{}括起来的多个键值对组成的集合。一个对象由花括号{}包起来，每一个键：值之间用逗号, 隔开，如 {“name”: Any, “age”:18}
数组：一个数组由中括号[]包起来，每一个键：值之间用逗号, 隔开，如 [“friend1”: William, “friend2”: Austy]
也就是说对象和数组都是键值对的集合，只是一个用{}，一个用[]。

**jsoncpp中含有三种基础类：Value、Write、Reader。**
1. Json::Value：用于存储键值对
2. Json::Writer
这个类负责将内存中的value对象转换为json文档，输出到文件或者字符串中
它有两种主要的方法：FastWriter、StyledWriter
FastWriter：快速无格式的将value转换成json文档
StyledWriter：有格式的将value转换成json文档
3. Json::Reader
用于读取json文档，或者说是用于将字符串或者文件输入流转换为Json::Value对象

**实用函数**
1. 判断某个键是否存在
bool Json::Value::isMember(const char *key) const;
若存在则返回1，反之为0
2. 得到Value中的所有键
Json::Value::getMemberBames() const;
返回一个string类型的vector
3. 删除某个键
Json::Value::removeMember(const char *key);
返回删除的值或者null







# 2.下载安装jsoncpp
首先下载项目https://github.com/open-source-parsers/jsoncpp，我们需要的文件有include/json/和src/lib_json，将这两个文件夹复制到同一目录下，结构如下：
```
lib_json/
  CMakeLists.txt 【这个文件没用，可以删了】
  json_reader.cpp
  json_tool.h
  json_value.cpp
  json_valueiterator.inl
  json_writer.cpp

json/
  allocator.h
  assertions.h
  config.h
  forwards.h
  json.h
  json_features.h
  reader.h
  value.h
  version.h
  writer.h
```

然后在json/目录下创建json.hpp，并include include/json/下所有头文件，内容如下：
```
#ifndef JSON_HPP_INCLUDED
#define JSON_HPP_INCLUDED

#include "allocator.h"
#include "writer.h"
#include "version.h"
#include "value.h"
#include "reader.h"
#include "json.h"
#include "json_features.h"
#include "forwards.h"
#include "config.h"
#include "assertions.h"

#endif // JSON_HPP_INCLUDED
```
然后我们就可以使用jsoncpp。


在lib_json/目录下创建test.cpp，内容如下：
```
#include <iostream>
#include <fstream>
#include "../json/json.hpp"

#if defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#elif defined(_MSC_VER)
#pragma warning(disable : 4996)
#endif

using namespace std;

int createjson()
{
    Json::Value root;
    Json::Value language;
    Json::Value mail;
    Json::StyledWriter writer;
    // Json::FastWriter writer;

    root["Name"] = "pikashu";
    root["Age"] = 18;

    language[0] = "C++";
    language[1] = "Python";
    root["Language"] = language;

    mail["QQ"] = "789123456@qq.com";
    mail["Google"] = "789123456@gmail.com";
    root["E-mail"] = mail;

    string json_file = writer.write(root);

    ofstream ofs;
    ofs.open("test1.json");
    if (!ofs.is_open())
    {
        cout << "open file error." << endl;
        return -1;
    }
    ofs << json_file;
    ofs.close(); 
    return 0;
}

int readjson()
{
    Json::Reader reader;
    Json::Value root;
    Json::Value language;
    Json::Value mail;

    ifstream ifs;
    ifs.open("test1.json");
    if (!ifs.is_open())
    {
        cout << "open file error." << endl;
        return -1;
    }

    if (!reader.parse(ifs, root))
    {
        cout << "parse error" << endl;
        return -1;
    }

    string Name = root["Name"].asString();
    int Age = root["Age"].asInt();  // jsoncpp中获取int类型数据
    cout << "Name: " << Name << endl;
    cout << "Age: " << Age << endl;

    if (root["language"].isArray())
    {
        Json::Value array_l = root["language"];
        cout << "Language: ";
        for (int i = 0; i < array_l.size(); i++)
        {
            cout << array_l[i] << " ";
        }
        cout << endl;
    }

    cout << "Google: " << root["E-mail"].get("Google", "").asString() << endl;
    cout << "QQ: " << root["E-mail"].get("QQ", "").asString() << endl;

    return 1;
}
int main()
{
    createjson();
    readjson();
    return 0;
}
```
运行命令：
```
g++ json_reader.cpp json_value.cpp json_writer.cpp  test.cpp  -o result
./result
```
结果：
```
Name: pikashu
Age: 18
Google: 789123456@gmail.com
QQ: 789123456@qq.com
```
参考：[JSONCPP安装及学习使用](https://blog.csdn.net/qq_44299067/article/details/121929266)
其他jsoncpp安装方法自行百度。
