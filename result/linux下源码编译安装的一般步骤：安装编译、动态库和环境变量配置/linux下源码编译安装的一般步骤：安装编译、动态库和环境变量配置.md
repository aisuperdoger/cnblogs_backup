原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/28/16321101.html
提交日期：Sat, 28 May 2022 08:55:00 GMT
博文内容：
# 1.安装

(./configure）–＞ 编译（sudo make） –＞ 安装（sudo make install）。

1.配置：这是编译源代码的第一步，通过 ./configure 命令完成（图形化可以用cmake-gui来配置）。执行此步以便为编译源代码作准备。常用的选项有 --prefix=PREFIX，用以指定程序的安装位置。更多的选项可通过 --help 查询。也有某些程序无需执行此步。
2.编译：一旦配置通过，可即刻使用 make 指令来执行源代码的编译过程。视软件的具体情况而定，编译所需的时间也各有差异，我们所要做的就是耐心等候和静观其变。此步虽然仅下简单的指令，但有时候所遇到的问题却十分复杂。较常碰到的情形是程序编译到中途却无法圆满结束。此时，需要根据出错提示分析以便找到应对之策。
3.安装：如果编译没有问题，那么执行 sudo make install 就可以将程序安装到系统中了。

例子：
```
//0.有时候需要先安装依赖库
//1.解压缩
tar -zxf nagios-4.0.2.tar.gz  
//2.进入目录
cd nagios-4.0.2
//3.配置
./configure --prefix=/usr/local/nagios     
//4.编译
make -j4
//5.安装
make install
```
参考：[链接](https://blog.csdn.net/qq_38455499/article/details/118465821)

# 2.配置
## 2.1.动态库配置
使用--prefix指定安装目录后，运行所需的动态库也会被安装在这个目录下。当程序运行时，linux系统不会去这个目录下查找动态库，那么程序就会由于缺少动态库而无法运行，一般会出现如下错误：error while loading shared libraries。
为了让linux系统找到动态库所在路径，必须做如下操作：
```
在/etc/ld.so.conf中添加动态库所在路径，或在/etc/ld.so.conf.d目录下建立xxxx.conf，然后再在xxxx.conf中添加动态库所在路径【xxxx随便什么都可以】
命令行输入：sudo /sbin/ldconfig
```

参考[链接](https://www.cnblogs.com/codingbigdog/p/16320965.html)

## 2.2.环境变量配置
在ubuntu系统中，经常会遇到修改环境变量的需要，修改的方式有三种，区别在于生效的范围：当前终端、当前用户、所有用户
- 1.在命令行窗口内执行如下命令export PATH=$PATH:<你的要加入的路径>，只对当前终端有效，执行命令后立即生效

- 2.在~目录下修改.bashrc 隐藏文件，添加如下语句 export PATH=<你要加入的路径1>:<你要加入的路径2>: ...... :$PATH，只对当前用户有效，需要重新打开命令行窗口生效。下面是一个实例：
```
sudo vim ~/.bashrc

# 在文件末尾添加两行
export PATH=$PATH:/home/lorien/work/media/ffmpeg/install/bin
export LD_LIBRARY_PATH=/home/lorien/work/media/ffmpeg/install/lib

source ~/.bashrc
```
- 3.在~目录下还有一个.profile隐藏文件，和.bashrc类似，但是该文件在用户登录时候被读取执行，所以需要重启生效。

- 4.在/etc目录下修改profile文件，添加如下语句export PATH=<你要加入的路径>:$PATH，对所有用户有效，需要重启或者执行source /etc/profile命令使得立即生效

下面是一个实例：
```
# 加入全局环境变量路径：
dxb@dxb-virtual-machine:~$ sudo vi /etc/profile
在文件中加入以下内容:
export PATH="/usr/local/ffmpeg/bin:$PATH"  
# PATH="/usr/local/ffmpeg/bin:$PATH"表示在$PATH前添加"/usr/local/ffmpeg/bin:"，然后将整体返回给$PATH

然后保存并运行source /etc/profile
每个新开的终端都需要输入source /etc/profile以后，才能直接运行软件。

重启以后，新开的终端不用运行source /etc/profile，就可以直接运行软件。
```

参考：[链接](https://blog.csdn.net/weixin_40571066/article/details/123257988)
