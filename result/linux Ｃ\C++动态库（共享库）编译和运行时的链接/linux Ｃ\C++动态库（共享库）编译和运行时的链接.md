原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/28/16320965.html
提交日期：Sat, 28 May 2022 08:26:00 GMT
博文内容：
#　0.C\C++动态库（共享库）编译和运行时的链接简介

库文件在编译（静态库和共享库）和运行（仅限于使用共享库的程序）时被使用，在使用之前肯定需要在一些搜索路径下查找库文件，看库文件是否存在，搜索路径是在系统中进行设置的。一般Linux系统把/lib和/usr/lib这两个目录作为默认的库搜索路径，所以使用这两个目录中的库时不需要进行设置搜索路径即可直接使用。对于处于默认库搜索路径之外的库，需要将库的位置添加到库的搜索路径之中。

**搜索路径分为两种，分别为编译时搜索路径和运行时搜索路径。**
- 添加编译时搜索路径的方式：pkg-config和LIBRARY_PATH。LIBRARY_PATH只用添加编译时的搜索路径，pkg-config可以用于添加编译时的搜索路径和头文件所在路径。程序的编译阶段，还可以通过-L参数添加编译时的搜索路径。

- 添加运行时搜索路径的方式：LD_LIBRARY_PATH和ldconfig。还可以通过-Wl,-rpath参数添加运行时的搜索路径。

-L和-Wl,-rpath设置的路径将被优先搜索。

&nbsp;

**下面是对编译时库的查找与运行时库的查找做一个简单的比较：**

1）编译时查找的是静态库或动态库， 而运行时，查找的是动态库；

2）编译时可以用-L、pkg-config、LIBRARY_PATH指定查找路径， 而运行时可以用-Wl,rpath、修改/etc/ld.so.conf、LD_LIBRARY_PATH指定查找路径

3）编译时用的链接器是ld，而运行时用的链接器是/lib/ld-linux.so.2

4）编译时与运行时都会查找默认路径/lib、/usr/lib

5）编译时还有一个默认路径/usr/local/lib，而运行时不会默认查找该路径；

说明： -Wl,rpath选项虽然是在编译时传递的，但是其实是工作在运行时。其本身其实也不算是gcc的一个选项，而是ld的选项，gcc只不过是一个包装器而已。我们可以执行man ld来进一步了解相关信息


下面介绍一下这几种链接方式。













# 1./etc/ld.so.conf和ldconfig

在/etc/ld.so.conf文件中添加库的搜索路径，将库文件的绝对路径直接写进/etc/ld.so.conf文件中就OK了，一行一个。比如：
```
/usr/X11R6/lib
/usr/local/lib
/opt/lib
```
我们也可以在/etc/ld.so.conf.d目录下建立xxxx.conf，然后再在xxxx.conf中添加以上内容。可以这样做的原因是：/etc/ld.so.conf文件中通过“include /etc/ld.so.conf.d/*.conf”包含了目录ld.so.conf.d下的所有.conf文件。

在/etc/ld.so.conf添加路径以后，需要使用/sbin/ldconfig更新一下，才会生效。原因如下：为了加快程序执行时对共享库的定位速度，避免使用搜索路径查找共享库的低效率，所以是直接读取库列表文件/etc/ld.so.cache的方式从中进行搜索。/etc/ld.so.cache是一个非文本的数据文件，不能直接编辑，需要使用/sbin/ldconfig命令更新/etc/ld.so.cache（ldconfig命令要以root权限执行）。


# 2.LD_LIBRARY_PATH

修改/etc/ld.so.conf文件的方式需要 root 权限，以改变 /etc/ld.so.conf 文件并执行 /sbin/ldconfig 命令。而且，当系统重新启动后，所有的基于 GTK2 的程序在运行时都将使用新安装的 GTK+ 库。不幸的是，由于 GTK+ 版本的改变，这有时会给应用程序带来兼容性的问题，造成某些程序运行不正常。为了避免出现上面的这些情况，在 GTK+ 及其依赖库的安装过程中对于库的搜索路径的设置将采用修改LD_LIBRARY_PATH的方式进行。这种设置方式不需要 root 权限，设置也简单：
```
export LD_LIBRARY_PATH=/opt/gtk/lib:$LD_LIBRARY_PATH
```
上述命令设置了/opt/gtk/lib为程序运行时的搜索路径。

LIBRARY_PATH和LD_LIBRARY_PATH差不多，LIBRARY_PATH的设置命令如下：
```
export LIBRARY_PATH=/opt/gtk/lib:$LIBRARY_PATH
```
上述命令设置了/opt/gtk/lib为程序编译时的搜索路径。


#3.Linux中pkg-config
请直接参考：[链接](https://blog.csdn.net/newchenxf/article/details/51750239)，下面做简要的总结：

在源代码**编译**时，pkg-config可用于查询某个库文件所依赖的头文件和库文件所在位置。为了让pkg-config可以得到一个库的信息，就要求库的提供者提供一个.pc文件。如：
``` 
gcc -o test test.c pkg-config --libs --cflags opencv.0 #　--cflags一般用于指定头文件，--libs一般用于指定库文件。
```
上述命令执行时，pkg-config默认会到/usr/lib/pkconfig/目录下去寻找opencv.pc文件。然而假如我们安装了一个库，其生成的.pc文件并不在这个默认目录中的话，pkg-config就找不到了。此时我们需要通过PKG_CONFIG_PATH环境变量来指定pkg-config去哪些地方去寻找.pc文件。我们可以通过如下命令来设置PKG_CONFIG_PATH环境变量：
```
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig/
```
这样pkg-config就会在/usr/local/lib/pkgconfig/目录下寻找.pc文件了。
另外还需要注意的是,上述环境变量的设置只对当前的终端窗口有效。为了让其永久生效，我们可以将上述命令写入/etc/.bashrc或者/home/chenxf/.bashrc的文件末尾。





# 4. -L和-Wl,rpath，以及实战
-Wl,-rpath选项的作用就是指定程序运行时的库搜索目录，是一个链接选项，生效于设置的环境变量之前(LD_LIBRARY_PATH)。下面我们通过一个例子来说明：
项目的结构：
```
├── add.c
├── add.h
└── main.c
```
```
// add.h
int add(int i, int j);
 
// add.c
#include "add.h"
 
int add(int i, int j)
{
	return i + j;
}
 
// main.c
#include <stdio.h>
#include <stdlib.h>
#include "add.h"
 
int main(int argc, char *argv[]) 
{
	printf("1 + 2 = %d\n", add(1, 2));
	return 0;
}
```
add.h和add.c用于生成一个so库，实现了一个简单的加法，main.c中引用共享库计算1 + 2。
编译：
```
# 编译共享库
gcc add.c -fPIC -shared -o libadd.so  # -fPIC：生成位置无关目标代码，适用于动态连接；
                                      # -shared：生成一个共享库文件；
# 编译主程序
gcc main.c -ladd -o app      # ladd相当于libadd.so的简写
/usr/bin/ld: cannot find -ladd
collect2: error: ld returned 1 exit status
```
可以看到编译时无法找到库libadd.so，此时可以通过设置pkg-config、LIBRARY_PATH和-L的方式添加编译时的搜索路径（任选一种）:
-L方式：
```
gcc main.c -L . -ladd -o app  # "-L ."代表编译阶段在当前目录下查找库
```
LIBRARY_PATH方式：
```
export  LIBRARY_PATH=/home/server/projects/test/test4:$LIBRARY_PATH
gcc main.c  -ladd -o app
```
/home/server/projects/test/test4请替换成自己的libadd.so所在目录

pkg-config方式【感觉比较麻烦，有时间再来写】

编译好后运行程序：
```
./app
输出：
./app: error while loading shared libraries: libadd.so: cannot open shared object file: No such file or directory

ldd app   # ldd用于查看app依赖的库文件
        linux-vdso.so.1 (0x00007fffb1751000)
        libadd.so => not found
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1f2d5ed000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f1f2d7f5000)
```
可以看到， libadd.so这个库没有找到。这是因为我们上面只添加了编译时库文件的搜索路径，并没有添加运行时的搜索路径，添加运行时的搜索路径的方式有LD_LIBRARY_PATH、ldconfig和-Wl,-rpath（任选一种）：
-Wl,-rpath方式：
```
gcc -Wl,-rpath=`pwd` main.c -L. -ladd -o app # pwd代表当前路径
                                             # "-L ."代表链接阶段在当前目录下查找库
                                             # -Wl,-rpath代表运行时，在哪里找库。
./app
输出：
1 + 2 = 3
```
LD_LIBRARY_PATH方式：
```
export LD_LIBRARY_PATH=/home/server/projects/test/test4:$LD_LIBRARY_PATH
./app
输出：
1 + 2 = 3
```
/home/server/projects/test/test4请替换成自己的libadd.so所在目录

ldconfig方式：
```
sudo vim /etc/ld.so.conf  # 在/etc/ld.so.conf中添加目录/home/server/projects/test/test4
sudo /sbin/ldconfig
```
/home/server/projects/test/test4请替换成自己的libadd.so所在目录








# 5.运行时搜索路径的搜索顺序
Linux程序在运行时对动态链接库的搜索顺序如下：

1） 在编译目标代码时所传递的动态库搜索路径（注意，这里指的是通过-Wl,rpath=<path1>:<path2>选项传递的运行时动态库搜索路径，而不是通过-L选项传递的编译时的搜索路径）

例如：
```
gcc -Wl,-rpath,/home/arc/test,-rpath,/lib/,-rpath,/usr/lib/,-rpath,/usr/local/lib test.c
或者
gcc -Wl,-rpath=/home/arc/test:/lib/:/usr/lib/:/usr/local/lib test.c
```

2） 环境变量LD_LIBRARY_PATH指定的动态库搜索路径；

3） 配置文件/etc/ld.so.conf中所指定的动态库搜索路径(更改/etc/ld.so.conf之后，一定要执行命令ldconfig，该命令会将/etc/ld.so.conf文件中所有路径下的库载入内存）;

4） 默认的动态库搜索路径/lib；

5） 默认的动态库搜索路径/usr/lib;









# 6.gcc编译头文件查找路径
对于#include ""，预处理器首先在当前目录查找，如果没找到，就按系统设置目录列表查找头文件。
对于#include<>，预处理器按系统设置目录列表查找头文件。我们常用 -I添加头文件的查找目录。预处理器的查找顺序为：当前目录——>-I设定目录——>系统设置目录。
您还可以使用 -nostdinc 选项阻止预处理器搜索任何默认系统头目录。当您编译操作系统内核或其他不使用标准 C 库工具或标准 C 库本身的程序时，这很有用。

除此之外，我们还可以通过相应的环境变量来指定头文件的搜索路径：
```
export C_INCLUDE_PATH=XXXX:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=XXX:$CPLUS_INCLUDE_PATH
```
可以将以上代码添加到/etc/profile末尾。


# 7.gcc编译选项
```
-I：编译程序按照-I指定的路进去搜索头文件
-L：指定的路径会被优先搜索
-l：-L用于指定库所在的目录，-l用于指定具体的库。
```
注意：-l event指定的是所有库名称中含有“libevent”字串的库。有时“-l event”也写成“-levent”。

下面是一个编译实例：
```
g++ main.cpp -Wl,-rpath=`../lib`  -L ../lib  -l opencv_core -l opencv_imgproc -l opencv_videoio -l opencv_imgcodecs -l opencv_highgui -I ../include/opencv4 -o app 

-Wl,-rpath：指定运行时在哪里找库
-L：指定库目录
-l：指定具体的库文件。即使有了-L，也需要设置-l
-I：指定了头文件所在的目录
```





from：[链接](https://blog.csdn.net/chen_jianjian/article/details/123890413)
