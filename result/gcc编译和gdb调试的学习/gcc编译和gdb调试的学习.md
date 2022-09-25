原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522376.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h3><a id="gccg_0"></a>gcc与g++基本用法</h3> 
<p>GCC编译流程分为四个步骤： 编译预处理、编译、汇编和链接<br> <img src="https://img-blog.csdnimg.cn/e74e63cd6ae24614bf893b5e1e8192ad.png" alt="在这里插入图片描述"><br> gcc最基本的用法是∶gcc [options] [filenames]<br> 使用gcc可以让源文件编译停在上述四个编译步骤的某一步，具体如下：</p> 
<ul><li> <p>预编译（Pre-Processing）<br> 预编译是在程序被编译之前为编译器所做的一些准备工作，主要是 <strong>拷贝包含的头文件到源程序文件、把宏替换成具体的数</strong>和处理条件编译。我们使用-E选项来使得GCC编译器在完成预处理后停止执行。<br> g++ -E test.cpp -o test.i</p> </li><li> <p>编译（Compiling）<br> 在这个阶段中，GCC编译器首先要 检查代码的规范性，<strong>有无语法错误</strong>，检查无误后再将代码<strong>翻译成汇编语言</strong>。 我们使用-S选项来使得GCC编译器只将输入的文件编译成汇编代码，而不再进一步处理。<br> g++ -S test.cpp -o test.s 或<br> g++ -S test.i -o test.s</p> </li><li> <p>汇编（Assembling）<br> 汇编阶段就是把编译阶段生成的 .s文件转换成<strong>目标文件</strong>。在此可使用选项-c来生成.o的<strong>二进制目标代码</strong>。<br> g++ -c test.cpp -o test.o 或<br> g++ -c test.s -o test.o</p> </li><li> <p>链接（Linking）<br> 在成功编译后，就进入了链接阶段。所谓链接就是把 <strong>前面生成的目标文件及所用到的库函数链接成一个可执行文件</strong>。<br> g++ test.cpp -o test.out 或<br> g++ test.o -o test.out</p> </li><li> <p>编译过程总结：预编译——》代码无错误时，翻译成汇编语言（编译）——》翻译成二进制代码（汇编）——》将汇编得到的目标文件及所用到的库函数链接成一个可执行文件（链接）</p> </li><li> <p>命令总结<br> -o：指定生成的输出文件的名字，默认为a.out；-E：仅执行编译预处理；-S：将C代码转换为汇编代码；- wall：显示警告信息；-c：仅执行编译操作，不进行连接操作。</p> </li></ul> 
<p>g++使用规则和gcc一样。gcc和g++两者都可以编译c和cpp文件，但存在差异。gcc在编译cpp时语法按照c来编译但默认不能链接到c++的库（gcc默认链接c库，g++默认链接c++库）。g++编译.c和.cpp文件都统一按cpp的语法规则来编译。所以一般编译c用gcc，编译c++用g++。</p> 
<h3><a id="gdb_26"></a>gdb调试</h3> 
<p>编译：g++ -g test.cpp -o test.out<br> 调试：gdb test.out<br> 调试命令说明：<br> 以后再来补充。。。。。。。<br> https://blog.csdn.net/u013525455/article/details/52813637</p> 
<p>调试方法好像有查看调用栈，这时什么意思？C++查看调用栈？？<br> 怎么查看呢？<br> C++调试方法？？》</p> 
<h3><a id="_38"></a>其他</h3> 
<p>1.如果没有给出可执行文件的名字，gcc将生成一个名为a.out的文件<br> 2. 在Linux系统中，可执行文件没有统一的后缀，系统从文件的属性来区分可执行文件和不可执行文件。而gcc则通过后缀来区别输入文件的类别。</p> 
<p>参考：<br> gcc和g++：<br> https://blog.csdn.net/yang_quan_yang/article/details/80996032<br> https://blog.csdn.net/qq_42475711/article/details/85224010<br> gdb调试：<br> https://blog.csdn.net/u013525455/article/details/52813637</p>
                