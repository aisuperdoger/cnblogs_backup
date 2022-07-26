原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/28/16320965.html
提交日期：Sat, 28 May 2022 08:26:00 GMT
博文内容：
首先我们大致看一下以下五个问题:
**1.pkg-config是什么？**
在源代码编译时，pkg-config可用于查询已安装的库的使用接口

**2.动态库（共享库）和静态库的区别是什么？**
区别：1、静态库的扩展名一般为“.a”或“.lib”；动态库的扩展名一般为“.so”或“.dll”。2、静态库在编译时会直接整合到目标程序中，编译成功的可执行文件可独立运行；动态库在编译时不会放到连接的目标程序中，即可执行文件无法单独运行。
可参考这篇[文章](https://blog.csdn.net/m0_61745661/article/details/123597887)，写得很好

**3.linux扩展名没有作用？**
Linux不根据扩展名判断文件类型，而是根据文件的内容来判断。所以扩展名的作用是帮助人来识别文件，对于Linux系统本身来说没有什么用处。
.sh结尾表示是shell脚本文件，但是不以.sh结尾的文件也可以是可执行的shell脚本（比如/etc/init.d中的脚本），因为它们的文件开头都有#!/bin/sh这一行




**4.make进行编译以后不就生成了可执行文件，make install进行了什么操作？**
类 UNIX 系统的软件，有些不需要安装，执行可执行文件就可以直接用了。
有些软件需要将配置文件、资源文件复制到相应的位置才能运行，如动态链接库的软件需要更新动态链接库缓存，否则会因为找不到刚刚编译出来的动态链接库而出错，等等。

**5.linux下源码安装的一般流程**
请参考[链接](https://blog.csdn.net/weixin_42732867/article/details/104789431)




# 1.Linux中pkg-config
## 1.1.pkg-config简介
pkg-config用于指明第三方头文件和库文件的位置。为了让pkg-config可以得到一个库的信息，就要求库的提供者提供一个.pc文件。
如：
``` 
gcc -o test test.c `pkg-config --libs --cflags glib-2.0` #　--cflags一般用于指定头文件，--libs一般用于指定库文件。
```
pkg-config默认会到/usr/lib/pkconfig/目录下去寻找glib-2.0.pc文件。然而假如我们安装了一个库，其生成的.pc文件并不在这个默认目录中的话，pkg-config就找不到了。此时我们需要通过PKG_CONFIG_PATH环境变量来指定pkg-config还应该在哪些地方去寻找.pc文件。

我们可以通过如下命令来设置PKG_CONFIG_PATH环境变量：
```
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig/
```
这样pkg-config就会在/usr/local/lib/pkgconfig/目录下寻找.pc文件了。
另外还需要注意的是,上述环境变量的设置只对当前的终端窗口有效。为了让其永久生效，我们可以将上述命令写入到/etc/bash.bashrc等文件中，以方便后续使用。



##　1.2.pkg-config与LD_LIBRARY_PATH
pkg-config与LD_LIBRARY_PATH的主要工作阶段：
- pkg-config: 编译时、 链接时
- LD_LIBRARY_PATH: 链接时、 运行时

pkg-config主要是在编译时会用到其来查找对应的头文件、链接库等；而LD_LIBRARY_PATH环境变量则在 链接时 和 运行时 会用到。程序编译出来之后，在程序加载执行时也会通过LD_LIBRARY_PATH环境变量来查询所需要的库文件。




##　1.3.LD_LIBRARY_PATH及ldconfig
下面我们来讲述一下LD_LIBRARY_PATH及ldconfig命令：
库文件在链接（静态库和共享库）和运行（仅限于使用共享库的程序）时被使用，其搜索路径是在系统中进行设置的。一般Linux系统把/lib和/usr/lib这两个目录作为默认的库搜索路径，所以使用这两个目录中的库时不需要进行设置搜索路径即可直接使用。对于处于默认库搜索路径之外的库，需要将库的位置添加到库的搜索路径之中。设置库文件的搜索路径有下列两种方式，可任选其中一种使用：

- 在环境变量LD_LIBRARY_PATH中指明库的搜索路径
- 在/etc/ld.so.conf文件中添加库的搜索路径

将自己可能存放库文件的路径都加入到/etc/ld.so.conf中是明智的选择。添加方法也及其简单，将库文件的绝对路径直接写进/etc/ld.so.conf文件中就OK了，一行一个。比如：
```
/usr/X11R6/lib
/usr/local/lib
/opt/lib
```
我们也可以在/etc/ld.so.conf.d目录下建立xxxx.conf，然后再在xxxx.conf中添加以上内容。可以这样做的原因是：/etc/ld.so.conf文件中通过“include /etc/ld.so.conf.d/*.conf”包含了目录ld.so.conf.d下的所有.conf文件。



需要注意的是：第二种搜索路径的设置方式对于程序链接时的库（包括共享库和静态库）的定位已经足够了。但是对于使用了共享库的程序的执行还是不够的，这是因为为了加快程序执行时对共享库的定位速度，避免使用搜索路径查找共享库的低效率，所以是直接读取库列表文件/etc/ld.so.cache的方式从中进行搜索。/etc/ld.so.cache是一个非文本的数据文件，不能直接编辑，它是根据/etc/ld.so.conf中设置的搜索路径由/sbin/ldconfig命令将这些搜索路径下的共享库文件集中在一起而生成的（ldconfig命令要以root权限执行）。因此为了保证程序执行时对库的定位，在/etc/ld.so.conf中进行了库搜索路径的设置之后，还必须要运行/sbin/ldconfig命令更新/etc/ld.so.cache文件之后才可以。

ldconfig，简单的说，它的作用就是将/etc/ld.so.conf列出的路径下的库文件缓存到/etc/ld.so.cache以供使用。因此当安装完一些库文件（例如刚安装好glib)，或者修改ld.so.conf增加新的库路径之后，需要运行一下/sbin/ldconfig使所有的库文件都被缓存到ld.so.cache中。如果没有这样做，即使库文件明明就在/usr/lib下的，也是不会被使用的，结果在编译过程中报错。

前面已经说明过了，库搜索路径的设置有两种方式：在环境变量 LD_LIBRARY_PATH 中设置以及在 /etc/ld.so.conf 文件中设置。其中，第二种设置方式需要 root 权限，以改变 /etc/ld.so.conf 文件并执行 /sbin/ldconfig 命令。而且，当系统重新启动后，所有的基于 GTK2 的程序在运行时都将使用新安装的 GTK+ 库。不幸的是，由于 GTK+ 版本的改变，这有时会给应用程序带来兼容性的问题，造成某些程序运行不正常。为了避免出现上面的这些情况，在 GTK+ 及其依赖库的安装过程中对于库的搜索路径的设置将采用第一种方式进行。这种设置方式不需要 root 权限，设置也简单：
```
export LD_LIBRARY_PATH=/opt/gtk/lib:$LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH
```

在程序链接时，对于库文件（静态库和共享库）的搜索路径，除了上面的设置方式之外，还可以通过-L参数显示指定。因为用-L设置的路径将被优先搜索，所以在链接的时候通常都会以这种方式直接指定要链接的库的路径。




# 2.Linux下链接库的路径顺序
##  2.1.运行时链接库的搜索顺序
Linux程序在运行时对动态链接库的搜索顺序如下：

1） 在编译目标代码时所传递的动态库搜索路径（注意，这里指的是通过-Wl,rpath=<path1>:<path2>或-R选项传递的运行时动态库搜索路径，而不是通过-L选项传递的）

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

## 2.2.编译时与运行时动态库查找的比较
下面是对编译时库的查找与运行时库的查找做一个简单的比较：

1）编译时查找的是静态库或动态库， 而运行时，查找的是动态库；

2）编译时可以用-L指定查找路径，或者用环境变量LIBRARY_PATH， 而运行时可以用-Wl,rpath或者-R选项，或者修改/etc/ld.so.conf，或者设置环境变量LD_LIBRARY_PATH;

3）编译时用的链接器是ld，而运行时用的链接器是/lib/ld-linux.so.2

4）编译时与运行时都会查找默认路径/lib、/usr/lib

5）编译时还有一个默认路径/usr/local/lib，而运行时不会默认查找该路径；

说明： -Wl,rpath选项虽然是在编译时传递的，但是其实是工作在运行时。其本身其实也不算是gcc的一个选项，而是ld的选项，gcc只不过是一个包装器而已。我们可以执行man ld来进一步了解相关信息



# 3.gcc使用-Wl,-rpath
-Wl,-rpath选项的作用就是指定程序运行时的库搜索目录，是一个链接选项，生效于设置的环境变量之前(LD_LIBRARY_PATH)。下面我们通过一个例子来说明：
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
add.h和add.c用于生成一个so库，实现了一个简单的加法，main.c中引用共享库计算1 + 2：
```
# 编译共享库
gcc add.c -fPIC -shared -o libadd.so  # -fPIC：生成位置无关目标代码，适用于动态连接；
                                      # -shared：生成一个共享库文件；
# 编译主程序
gcc main.c -L . -ladd -o app  # ladd应该相当于libadd.so的简写
                              # "-L ."代表链接阶段在当前目录下查找库
```
编译好后运行：
```
./app
输出：
./app: error while loading shared libraries: libadd.so: cannot open shared object file: No such file or directory
```
可以看到， libadd.so这个库没有找到。这是因为-L指定的是编译时从哪里找动态库，我们还需要使用-Wl,rpath选项指定运行时从哪个目录下找动态库之后：
```
gcc -Wl,-rpath=`pwd` main.c -L. -ladd -o app # pwd代表当前路径
                                             # "-L ."代表链接阶段在当前目录下查找库
                                             # -Wl,-rpath代表运行时，在哪里找库。
./app
输出：
1 + 2 = 3
```
依赖库的查找路径就找到了，程序能正常运行。

用ldd查看C++程序的依赖库【参考：[用ldd查看C++程序的依赖库](https://blog.csdn.net/csfreebird/article/details/9200469)】：
```
ldd -v  app
输出：
linux-vdso.so.1 (0x00007ffd619b7000)
libadd.so => ./libadd.so (0x00007f9e216ca000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f9e214c7000)
/lib64/ld-linux-x86-64.so.2 (0x00007f9e216d6000)

Version information:
./app:
        libc.so.6 (GLIBC_2.2.5) => /lib/x86_64-linux-gnu/libc.so.6
/lib/x86_64-linux-gnu/libc.so.6:
        ld-linux-x86-64.so.2 (GLIBC_2.3) => /lib64/ld-linux-x86-64.so.2
        ld-linux-x86-64.so.2 (GLIBC_PRIVATE) => /lib64/ld-linux-x86-64.so.2
```

下面我们再来看一下生成的可执行文件app，执行如下命令：
```
readelf app -d
```
输出：
```
Dynamic section at offset 0xe08 contains 26 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libadd.so]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
 0x000000000000000f (RPATH)              Library rpath: [/root/test]
 0x000000000000000c (INIT)               0x400578
 0x000000000000000d (FINI)               0x400784
 0x0000000000000019 (INIT_ARRAY)         0x600df0
 0x000000000000001b (INIT_ARRAYSZ)       8 (bytes)
 0x000000000000001a (FINI_ARRAY)         0x600df8
 0x000000000000001c (FINI_ARRAYSZ)       8 (bytes)
 0x000000006ffffef5 (GNU_HASH)           0x400298
 0x0000000000000005 (STRTAB)             0x400408
 0x0000000000000006 (SYMTAB)             0x4002d0
 0x000000000000000a (STRSZ)              189 (bytes)
 0x000000000000000b (SYMENT)             24 (bytes)
 0x0000000000000015 (DEBUG)              0x0
 0x0000000000000003 (PLTGOT)             0x601000
 0x0000000000000002 (PLTRELSZ)           96 (bytes)
 0x0000000000000014 (PLTREL)             RELA
 0x0000000000000017 (JMPREL)             0x400518
 0x0000000000000007 (RELA)               0x400500
 0x0000000000000008 (RELASZ)             24 (bytes)
 0x0000000000000009 (RELAENT)            24 (bytes)
 0x000000006ffffffe (VERNEED)            0x4004e0
 0x000000006fffffff (VERNEEDNUM)         1
 0x000000006ffffff0 (VERSYM)             0x4004c6
 0x0000000000000000 (NULL)               0x0
```
可以看到是在编译后的程序中包含了库的搜索路径。

我们还经常见到-Wl,rpath-link
-Wl,rpath-link是设置编译链接时候的顺序，例如app运行依赖libadd.so，但是libadd.so又依赖libadd_ex.so，rpath-link就是指定libadd_ex.so的路径。和-Wl,rpath相比工作的时间不同，一个在链接期间，一个在运行期间。




# 4.gcc编译头文件查找路径
对于#include ""，预处理器首先在当前目录查找，如果没找到，就按系统设置目录列表查找头文件。
对于#include<>，预处理器按系统设置目录列表查找头文件。我们常用 -I添加头文件的查找目录。预处理器的查找顺序为：当前目录——>-I设定目录——>系统设置目录。
您还可以使用 -nostdinc 选项阻止预处理器搜索任何默认系统头目录。当您编译操作系统内核或其他不使用标准 C 库工具或标准 C 库本身的程序时，这很有用。

除此之外，我们还可以通过相应的环境变量来指定头文件的搜索路径：
```
export C_INCLUDE_PATH=XXXX:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=XXX:$CPLUS_INCLUDE_PATH
```
可以将以上代码添加到/etc/profile末尾。


#gcc编译选项
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
