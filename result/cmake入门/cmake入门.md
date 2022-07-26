原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/08/16459532.html
提交日期：Fri, 08 Jul 2022 12:12:00 GMT
博文内容：
# 1 cmake基础
## 1.1 简介
[CMake 和makefile关系](https://blog.csdn.net/u013827488/article/details/123804786)
不同平台有自己的make标准。如果软件想跨平台，必须要保证能够在不同平台编译。而如果使用上面的 Make 工具，就得为每一种标准写一次 Makefile ，这将是一件让人抓狂的工作。
CMake就是针对上面问题所设计的工具：它首先允许开发者编写一种平台无关的 CMakeList.txt 文件来定制整个编译流程，然后再根据目标用户的平台进一步生成所需的本地化 Makefile 和工程文件，如 Unix 的 Makefile 或 Windows 的 Visual Studio 工程。从而做到“Write once, run everywhere”。



## 1.2 语法特性介绍
基本语法格式：指令(参数 1 参数 2...) 
- 参数使用括弧括起
- 参数之间使用空格或分号分开 

指令是大小写无关的，参数和变量是大小写相关的，如：
```
set(HELLO hello.cpp)
add_executable(hello main.cpp hello.cpp)
ADD_EXECUTABLE(hello main.cpp ${HELLO})
```
变量使用${}方式取值，但是在 IF 控制语句中是直接使用变量名


## 1.3 重要指令和CMake常用变量
**重要指令:**
```
cmake_minimum_required(VERSION versionNumber [FATAL_ERROR]) 指定CMake的最小版本要求
# CMake最小版本要求为2.8.3
cmake_minimum_required(VERSION 2.8.3)

project(projectname [CXX] [C] [Java])   定义工程名称，并可指定工程支持的语言。一般只定义工程名称。
# 指定工程名为HELLOWORLD
project(HELLOWORLD) 

set(VAR [VALUE] [CACHE TYPE DOCSTRING [FORCE]])  显式的定义变量
# 定义SRC变量，其值为sayhello.cpp hello.cpp
set(SRC sayhello.cpp hello.cpp)

include_directories([AFTER|BEFORE] [SYSTEM] dir1 dir2 ...)    向工程添加多个特定的头文件搜索路径 --->相当于指定g++编译器的-I参数
# 将/usr/include/myincludefolder 和 ./include 添加到头文件搜索路径
include_directories(/usr/include/myincludefolder ./include)

link_directories(dir1 dir2 ...) 向工程添加多个特定的库文件搜索路径 --->相当于指定g++编译器的-L参数
# 将/usr/lib/mylibfolder 和 ./lib 添加到库文件搜索路径
link_directories(/usr/lib/mylibfolder ./lib)

add_library(libname [SHARED|STATIC|MODULE] [EXCLUDE_FROM_ALL] source1 source2 ... sourceN) 生成库文件
# 通过变量 SRC 生成 libhello.so 共享库，即将SRC中的文件编译成共享库文件
add_library(hello SHARED ${SRC}) 

add_compile_options(）添加编译参数
# 添加编译参数 -Wall -std=c++11 -O2
add_compile_options(-Wall -std=c++11 -O2)

add_executable(exename source1 source2 ... sourceN)  生成可执行文件
# 编译main.cpp生成可执行文件main
add_executable(main main.cpp)

target_link_libraries(target library1<debug | optimized> library2...)  为 target 添加需要链接的共享库 --->相同于指定g++编译器-l参数
# 将hello动态库文件链接到可执行文件main
target_link_libraries(main hello)

add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL])  向当前工程添加存放源文件的子目录，并可以指定中间二进制和目标二进制存放的位置
# 添加src子目录，src中需有一个CMakeLists.txt
add_subdirectory(src)
  
aux_source_directory(dir VARIABLE) 发现一个目录下所有的源代码文件并将列表存储在一个变量中，这个指令临时被用来自动构建源文件列表
# 定义SRC变量，其值为当前目录下所有的源代码文件
aux_source_directory(. SRC)
# 编译SRC变量所代表的源代码文件，生成main可执行文件
add_executable(main ${SRC})
```


**CMake常用变量:**
```
CMAKE_C_FLAGS gcc编译选项
CMAKE_CXX_FLAGS g++编译选项
# 在CMAKE_CXX_FLAGS编译选项后追加-std=c++11
set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

CMAKE_BUILD_TYPE 编译类型(Debug, Release)
# 设定编译类型为debug，调试时需要选择debug。相当于gcc中的-g选项
set(CMAKE_BUILD_TYPE Debug)  
# 设定编译类型为release，发布时需要选择release
set(CMAKE_BUILD_TYPE Release)

CMAKE_BINARY_DIR 
PROJECT_BINARY_DIR
_BINARY_DIR
1. 这三个变量指代的内容是一致的。
2. 如果是 in source build，指的就是工程顶层目录。
3. 如果是 out of source 编译,指的是工程编译发生的目录。
4. PROJECT_BINARY_DIR 跟其他指令稍有区别，不过现在，你可以理解为他们是一致的。

CMAKE_SOURCE_DIR
PROJECT_SOURCE_DIR
_SOURCE_DIR
1. 这三个变量指代的内容是一致的,不论采用何种编译方式,都是工程顶层目录。
2. 也就是在 in source build时,他跟 CMAKE_BINARY_DIR 等变量一致。
3. PROJECT_SOURCE_DIR 跟其他指令稍有区别,现在,你可以理解为他们是一致的。

CMAKE_C_COMPILER：指定C编译器
CMAKE_CXX_COMPILER：指定C++编译器
EXECUTABLE_OUTPUT_PATH：可执行文件输出的存放路径
LIBRARY_OUTPUT_PATH：库文件输出的存放路径
```


# 1.4  CMake编译工程
**CMake目录结构：**项目主目录存在一个CMakeLists.txt文件

**两种方式设置编译规则：**
1. 包含源文件的子文件夹包含CMakeLists.txt文件，主目录的CMakeLists.txt通过add_subdirectory添加子目录即可；
2. 包含源文件的子文件夹未包含CMakeLists.txt文件，子目录编译规则体现在主目录的CMakeLists.txt中；

**两种构建方式:**
内部构建(in-source build)【不推荐使用】：内部构建会在同级目录下产生一大堆中间文件，这些中间文件并不是我们最终所需要的，和工程源文件放在一起会显得杂乱无章。
```
## 内部构建
# 在当前目录下，编译本目录的CMakeLists.txt，生成Makefile和其他文件
cmake .
# 执行make命令，生成target
make
```
外部构建(out-of-source build)【推荐使用】：将编译输出文件与源文件放到不同目录中
```
## 外部构建
# 1. 在当前目录下，创建build文件夹
mkdir build 
# 2. 进入到build文件夹
cd build
# 3. 编译上级目录的CMakeLists.txt，生成Makefile和其他文件
cmake ..
# 4. 执行make命令，生成target
make
```



# 2 实例
## 2.1 实例1
helloworld.cpp:
```
#include <iostream>
using namespace std;

int main(int argc, char **argv)
{
    cout << "Hello World!" << endl;
    return 0;
}
```
CMakeLists.txt：
```
cmake_minimum_required(VERSION 3.0) 

project(HELLOWORLD)

add_executable(helloWorld_cmake helloworld.cpp) # 等价于g++ helloworld.cpp -o helloWorld_cmake
```



### 内部构建（in source build）


cmake
```
cmake .
-- The C compiler identification is GNU 9.4.0
-- The CXX compiler identification is GNU 9.4.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done   #检查c和c++语言编译器
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /home/ubuntu1/projects/test_c++/test2/Class_5/5.3.1 helloWorld
```
cmake命令生成了四个个文件：
```
CMakeCache.txt  
CMakeFiles  
cmake_install.cmake   
# 初学者不需要管上面三个文件
Makefile
```
make:
```
make
Scanning dependencies of target helloWorld_cmake
[50%] Building CXX object CMakeFiles/helloWorld_cmake.dir/helloworld.cpp.o  # 正在生成.o文件
[100%] Linking CXX executable helloWorld_cmake    # 连接
[100%] Built target helloWorld_cmake
```
make命令生成了可执行文件helloWorld_cmake


### 外部构建（out of source）【推荐】

```
mkdir build
cd build
cmake ..
make

```
外部构建就是将cmake生成的中间文件、Makefile和可执行文件都放在build目录中了。


## 2.2 实例2
实例2的目录结构如下所示：
```
tree .   # tree .命令获取当前目录的结构
.
├── CMakeLists.txt
├── include
│   └── swap.h
├── main.cpp
└── src
    └── swap.cpp
```
main.cpp:
```
#include "swap.h"

int main(int argc, char **argv)
{
    swap myswap(10, 20);
    std::cout << "Before swap:" << std::endl;
    myswap.printInfo();
    myswap.run();
    std::cout << "After  swap:" << std::endl;
    myswap.printInfo();

    return 0;

}
```
swap.h:
```
#pragma once   # 用于防止头文件的重复包含
#include <iostream>

class swap
{
public:
    swap(int a, int b){
        this->_a = a;
        this->_b = b;
    }
    void run();
    void printInfo();
private:
    int _a;
    int _b;
};
```
swap.cpp:
```
#include "swap.h"

void swap::run()
{
    int temp;
    temp  = _a;
    _a = _b;
    _b = temp;
}

void swap::printInfo()
{
    std::cout << "_a = " << _a << std::endl;
    std::cout << "_b = " << _b << std::endl;
}
```
CMakeLists.txt:
```
cmake_minimum_required(VERSION 3.0)

project(SWAP)

include_directories(include)  # 等价于-I include

add_executable(main_cmake main.cpp src/swap.cpp)
```
编译：
```
mkdir build
cd build
cmake ..
make

```







# 3  CMakeLists.txt文件学习
## 3.1 实例一

CMakeLists.txt:
```
cmake_minimum_required(VERSION 3.0)

project(SOLIDERFIRE)                             # 项目名为SOLIDERFIRE

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")  # -Wall：输出警告的信息
                                                 # "${CMAKE_CXX_FLAGS} -Wall"表示在原有的CMAKE_CXX_FLAGS后添加-Wall

set(CMAKE_BUILD_TYPE Debug)    # 让输出的可执行文件是可debug的

include_directories(${CMAKE_SOURCE_DIR}/include)

add_executable(my_cmake_exe main.cpp src/Gun.cpp src/Solider.cpp)  # 对main.cpp、src/Gun.cpp和src/Solider.cpp三个cpp文件进行编译
```


## 3.2 实例2
```
cmake_minimum_required(VERSION 3.0)

set(SOURCE_FILES main.c)

project(TEST2)                             # 项目名为SOLIDERFIRE

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")  # -Wall：输出警告的信息
# "${CMAKE_CXX_FLAGS} -Wall"表示在原有的CMAKE_CXX_FLAGS后添加-Wall

set(CMAKE_BUILD_TYPE Debug)    # 让输出的可执行文件是可debug的

include_directories(${CMAKE_SOURCE_DIR}/ffmpeg/include)

link_directories(
		${CMAKE_SOURCE_DIR}/ffmpeg/lib/    # CMakeLists.txt中似乎不需要-l用来指定编译时具体需要什么库
)

add_executable(my_cmake_exe avframe.c avpacket.c  main.c )  # 对avframe.c avpacket.c  main.c 三个cpp文件进行编译

target_link_libraries(my_cmake_exe avcodec avutil m) # 指定运行时需要连接的库
```


## 3.3 实例三
可以对下面实例中，不懂的函数或变量进行百度，并进行注释，从而达到学习的目的。【现在懒得学，以后再说吧。】
```
cmake_minimum_required(VERSION 2.6)
project(pro)
add_definitions(-std=c++11)  # CmakeList支持c++11的方式有两种：
                             # SET(CMAKE_CXX_FLAGS "-std=c++11")
                             # add_definitions(-std=c++11)

option(CUDA_USE_STATIC_CUDA_RUNTIME OFF)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Debug)
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/workspace)

# 如果你是不同显卡，请设置为显卡对应的号码参考这里：https://developer.nvidia.com/zh-cn/cuda-gpus#compute
set(CUDA_GEN_CODE "-gencode=arch=compute_75,code=sm_75")

# 如果你的opencv找不到，可以自己指定目录
set(OpenCV_DIR   "/data/datav/expstation/lean/opencv4.2.0/lib/cmake/opencv4/")

set(CUDA_DIR     "/data/sxai/lean/cuda-10.2")
set(CUDNN_DIR    "/data/sxai/lean/cudnn8.2.2.26")
set(TENSORRT_DIR "/data/sxai/lean/TensorRT-8.0.1.6-cuda10.2-cudnn8.2")

# set(CUDA_DIR     "/data/sxai/lean/cuda-10.2")
# set(CUDNN_DIR    "/data/sxai/lean/cudnn7.6.5.32-cuda10.2")
# set(TENSORRT_DIR "/data/sxai/lean/TensorRT-7.0.0.11")

# set(CUDA_DIR     "/data/sxai/lean/cuda-11.1")
# set(CUDNN_DIR    "/data/sxai/lean/cudnn8.2.2.26")
# set(TENSORRT_DIR "/data/sxai/lean/TensorRT-7.2.1.6")

find_package(CUDA REQUIRED)
find_package(OpenCV)

include_directories(
    ${PROJECT_SOURCE_DIR}/src
    ${OpenCV_INCLUDE_DIRS}
    ${CUDA_DIR}/include
    ${TENSORRT_DIR}/include
    ${CUDNN_DIR}/include
)

# 切记，protobuf的lib目录一定要比tensorRT目录前面，因为tensorRTlib下带有protobuf的so文件
# 这可能带来错误
link_directories(
    ${TENSORRT_DIR}/lib
    ${CUDA_DIR}/lib64
    ${CUDNN_DIR}/lib
)

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -O0 -Wfatal-errors -pthread -w -g")
set(CUDA_NVCC_FLAGS "${CUDA_NVCC_FLAGS} -std=c++11 -O0 -Xcompiler -fPIC -g -w ${CUDA_GEN_CODE}")
file(GLOB_RECURSE cpp_srcs ${PROJECT_SOURCE_DIR}/src/*.cpp)
file(GLOB_RECURSE c_srcs ${PROJECT_SOURCE_DIR}/src/*.c)
file(GLOB_RECURSE cuda_srcs ${PROJECT_SOURCE_DIR}/src/*.cu)
cuda_add_library(cucodes SHARED ${cuda_srcs})

add_executable(pro ${cpp_srcs} ${c_srcs})

# 如果提示插件找不到，请使用dlopen(xxx.so, NOW)的方式手动加载可以解决插件找不到问题
target_link_libraries(cucodes nvinfer nvonnxparser)
target_link_libraries(cucodes cuda cublas cudart cudnn)
target_link_libraries(pro ${OpenCV_LIBS})
target_link_libraries(pro cucodes)

add_custom_target(
    run
    DEPENDS pro
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/workspace
    COMMAND ./pro
)
```


gcc中的-Wl,-rpath对应于cmake中的哪个东西？？

参考：https://www.bilibili.com/video/BV1fy4y1b7TC、微信公众号：VSCode、bilibili ：xiaobing1016
