原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/22/16506475.html
提交日期：Fri, 22 Jul 2022 09:21:00 GMT
博文内容：
可以用少量字总结的就总结一下，如果不行，就只写一下有什么知识

练习答案：https://github.com/applenob/Cpp_Primer_Practice



1.main()函数return的是0，则表示成功；非零表示各种错误类型

不同编译器规定c++源文件的后缀不同，可能是cc,cpp,cp等

UNIX可执行文件后缀为.out，可以没有后缀；windows可执行文件后缀为.exe

ubuntu中直接输入a.out是无法找到可执行文件，需要执行./a.out通过“./”告诉系统可执行文件所在目录。

在命令行中运行完可执行文件后，可以使用echo输出main函数返回的值





2.cin和cout是两个对象，<<是一个运算符。

cerr和clog也是两个输出对象，分别用于输出错误和日志

程序员常常在调试时添加打印语句。这类语句应该保证“一直”刷新流，即cout都应该以<<std::endl结尾。否则，如果程序崩溃，输出可能还留在缓冲区中，此时我们以为某位置没有输出，其实是输出了，只是留在了缓冲区中。这就会导致导致关于程序崩溃位置的错误推断。

<<可以输出不同类型数据，是因为定义了不同版本的<<运算符来处理不同类型的数据。





3.while(std::cin>>value)中std::cin>>value返回的是一个std::cin对象，当对象是文件结束符（或输入错误）时while循环结束。

文件结束符：windows下为ctrl+z或Enter，linux（或MAC os x）下为ctrl+d。

常见错误类型：syntax error（如忘写分号）、type error（int型被字符串进行赋值）、declaration error（名字拼写错误、忘写std::）

修改一部分代码就重新编译调试一次，因为后面很多错误可能只是由前面修改的错误引起的。

类就是一种自定义的数据类型

**标准库的头文件使用#include<>**，非标准库的头文件（自己写的头文件）使用include""。

./test.out <text.txt> text2.txt：代表使用cin的地方从text.txt中读取内容，使用cout的地方将内容输出到text2.txt中





4.空类型（void）：当函数不返回任何值时使用空类型作为返回类型。

不同机器上数据类型（又称算术类型）占用的比特不同，但c++规定了各类型的最小尺寸。

wchar：存放扩展字符；char16_t、char32_t：存放Unicode字符

每个地址上可以存放的比特数称为字节，一个字节一般是八个比特；CPU一次性处理的数据大小称为字，**64位计算机指的是字的大小为8个字节。**

char用signed char或unsigned char来实现，不同的编译器实现的方式不同；所以如果实在必须将char当成整型来用，指明使用的是signed char还是unsigned char。

数值范围int无法表示，一般直接使用long long；浮点运算一般使用double，不使用float。





5.类型转换

类型转换：如char转int——就是将char变量对应的二进制码解读成int。

给**无符号数**赋值超过表示范围时，结果是初始值对无符号类型可表示的数值的个数取模后的**余数**。给**有符号数赋值**超过表示范围时，结果为**未定义**，此时程序可能出现不可预知的风险。

**int和无符号数相加**时，int变量会被转换成**无符号数**。如果此时int变量是负数，则直接将此负数对应的二进制补码解读成原码；

无符号相减得到的结果如果是负数：如u2-u1为负数，则u2-u1=u2+(-u1)，其中-u1的机器码为补码，这里的补码解读为原码。

**for(unsigned u=10;u>=0;- -u)**中当u=-1时，u实际为4294967295。及其解决方法。

**切勿混用带符号类型和无符号**类型进行运算





6.字面值常量

字面值常量：就是告诉你整数、浮点数、字符串等需要怎么表示

八进制：0开头；十六进制：0x或0X开头

默认情况下，十进制字面值是带符号数，八进制和十六进制字面值既可能是带符号的也可能是无符号的。

十进制字面值是利用“int、long、long long”中一个来装载的。具体选的是可容纳此字面值的最小类型来装载。

八进制和十六进制字面值是利用“int、unsigned int、long、unsigned Iong、Iong long和unsigned long long ”中一个来装载的。具体选的是可容纳此字面值的最小类型来装载。

浮点数默认使用**double**来装载。3.14159E0或3.14159e0中的E0或e0代表乘以10的0次方

我们还可以自己选择利用哪个类型来装载，只需要利用**字面值后添加相应的后缀**即可，如42ULL代表42这个数用unsigned long long来装载。如果指定的装载类型太小，编译器会自动用其他更大的类型来装



由单引号括起来的一个字符称为char型字面值，双引号括起来的零个或多个字符则构成字符串型字面值。

**字符串**字面值是由**字符数组**来装载的，编译器在每个字符串的**结尾**处添加一一个**空字符('\0')**， 因此，**字符串字**
**面值的实际长度要比它的内容多1。**

多行字符串实际会被当成一行字符串。

**给字面值添加前缀**来指明用什么类型装在字符或字符串，如L’a’代表用wchar_t装载字符a





7.变量

变量可以当成内置的对象

string在std命名空间中被定义

初始化的含义是创建变量时赋予其一个初始值，而赋值的含义是把对象的当前值擦除，而以一个新值来替代。

列表初始化：int a={0}或int a{0}。如果我们使用列表初始化且初始值存在丢失信息的风险，则编译器将报错（如**int a{1.111}中的.111会丢失**）

**函数体外**定义的变量对应的机器码会**默认初始化为零**。**函数体内**定义的变量可能会初始化成**没有意义的数或者为未定义**。
一个未被初始化的内置类型变量的值是**未定义的**（还有，给有符号数赋值超过表示范围时，结果也为未定义），如果试图拷贝或以其他形式访问此未定义变量将引发错误。这句话没看懂？？？

为了安全**建议初始化每一个内置类型的变量**

声明：告诉了程序这个变量的存在，但未申请内存。定义：申请了内存。

声明：在变量前面添加extern，如extern int a;

一个文件如**果想使用别处定义的名字**则必须包含对那个**名字的声明**。

变量能且只能被定义一次。但是**可以被多次声明**。

**函数内部**不能声明变量

**显式初始化的声明即成为定义。**“extern int val = 1; ”为定义

**函数的声明是函数**头，也可以在函数头左边加上extern。函数声明的形参可以只写类型，而不写形参的名称。

c++中**不能使用标识符**：不能**连续**出现**两个下划线**；不能以**下划线紧连大写**字母开头；定义在**函数体外**的标识符**不能以下划线开头**。

**变量名**一般用**小写**字母，如index；用户自定义的**类名**一般以**大写字母开头**，如Sales_item;标识符由多个单词组成时，单词之间用下划线隔开或除第一个单词外的其他单词都大写。

不用把**定义**都放在开头，**放在使用的地方的附近**（注意不要重复定义）

cout<<**::reused**;表示访问**全局变量**reused

8.引用就是别名，**引用上的任何改变都是对原变量的改变**。int &a=b;

引用必须初始化；无法更改绑定对象；引用只能绑定在对象上，不能绑定在字面值上

引用的作用：函数fun(int &a)传入实参a时，不需要复制一份a，而直接传入a本身。函数fun(int a)传入实参a时，需要复制一份a。

指针：存储对象的地址。由于引用不是对象，只是别名，所以没有指向引用的指针。利用取地址符&取引用地址时，取到的是引用指向变量的地址。

无效指针：最常见的是，指针所指的内存单元被释放了，此时指针就变为了无效指针，**不遗留任何无效指针总是最好的实践方式。**

如果p是个指针，则\*p代表访问p所指向对象。

空指针：int *p=nullptr;int *p=0;int *p=NULL;

其中NULL是预处理变量，在预处理阶段会被替换成零

把**int变量直接赋给指针是错误的操作**，**即使int变量的值恰好等于0也不行**

建议**所有指针都要进行初始化**

指针一般写成这样：**int \*p**，而不写成int\* p。再如：int* p1, p2; // **p1是指向int的指针，p2是int**

指向指针的引用：给指针取别名，如int *&r=p，从右往左读，首先读到&，代表r是一个引用，其余部分代表r是什么类型数据的引用，即int指针的引用



9、const int k=9;定义一个不可改变的常量，k必须在定义的时候就**初始化**，任何在k上的操作都**不可以修改k**的值

**非常量引用不可以指向一个常量对象；常量引用可以指向一个非常量对象**

在初始化常量引用时允许用任意表达式作为初始值，只要该表达式的结果能转换成引用的类型即可，如**const int &ri = dval ;其中dval为double类型**，此时ri绑定的是一个临时常量而不是dval。而下面这个却是错误的：**int &ri = dval ;其中dval为double类型**。为什么普通引用不可以绑定到临时常量上呢？答：因为一般需要修改dval时，才会使用普通引用。所以如果普通引用被绑定在临时变量上了，就不可以修改dval了

const int *ri = dval ;其中dval为int类型，即dval可以不是const int。dval为int类型时，应该和上面一样：ri实际是绑定了一个临时变量

const指针：指针本身为常量。

int \*const E=&e;const代表E本身是一个常量，int \*代表这个常量是int类型指针。const double \*const pip=\&pi;const代表pip是一个常量，const double \*代表这个常量是double常量类型指针

指针本身是一个常量并不意味着不能通过指针修改其所指对象的值。

顶层const( top-level const)表示本身是个常量，底层const (low-level const)表示指针或引用所指的对象是一个常量。

常量表达式：值不会改变并且在编译过程就能得到计算结果的表达式。如当表达式中含有函数时，计算结果是在运行的时候才能得到。常量表达式在后面会用到。

C++11中判断是否为常量表达式的方法是将表达式赋给constexpr变量。constexpr变量：constexpr int a = A，编译器会验证A是否为常量表达式。

constexpr指针：只能存放地址固定的对象的地址。如一般函数体内的对象（变量）一般不能由constexpr指向（但有例外，例外是啥呢？？？？），函数体内可以。

constexpr const int  \*p=&i; // p是常量指针，指向整型常量i
constexpr int \*p1=&j;// p1是常量指针，指向整数j

10、

取别名:

​		typedef int *p;  // p为int *的别名

​		typedef int p;   // p为int的别名

​		using SI = Sales_ item;  // SI为Sales_ item的别名

​		typedef char *pstring;
​		const pstring cstr = 0; // cstr是指向char的常量指针

​		const char *cstr = 0; // cstr是指向char类型常量的指针

auto item = val1 + val2; // auto推断出val1+val2为类型A，并将item定义成类型A。等号自然是将val1+val2的值，赋给了item。

auto也能在一条语句中声明多个变量以及其注意点

auto a = i; // i是一个引用。auto获取的是i所指对象的类型，而不是获取到引用类型。

auto会忽略顶层const，底层const会被保留下来。

使用auto获取引用类型和顶层const的方法

不能为非常量引用绑定字面值，可以为常量引用绑定字面值。

设置一个类型为auto的引用时，初始值中的顶层常量属性仍然保留。

auto不能确定基本数据类型是什么而导致的错误



decltype：只返回表达式的类型，返回表达式的值（即不用表达式的值进行初始化）

decltype(ci) x=2; \\\ 获取ci的类型A，将x定义成类型A并初始化为2；

decltype处理项层const和引用的方式与auto有些许不同。如果decltype使用的表达式是一个变量，则decltype返回该变量的类型(包括顶层const和引用在内):

需要指出的是，引用从来都作为其所指对象的同义词出现，只有用在decltype处是一个例外。

如果decltype使用的表达式不是一个变量时，则decltype返回表达式结果对应的类型【具体见原文】

如果表达式的内容是解引用操作，则decltype将得到引用类型。

切记: decltype ( (variable)) (注意是双层括号)的结果永远是引用，而decltype (variable)结果只有当生variable本身就是一个引用时才是引用。



使用struct自定义数据结构（类）【struct使用方法和class相似，不需要再看了 】

C++11新标准规定，可以为数据成员提供一个类内初始值

头文件的编写

类名一般和头文件名一样

头文件通常包含那些只能被定义一次的实体，如类、const和constexpr变量(

通过#ifndef和文件保护符防止头文件的重复引用。通常文件保护符的名字和类名有关





接下来看第三章







重载：相同函数名，不同形参

重写：子类对父类中相同函数（函数名、形参和返回值都相同）的覆盖

空的形参列表的两种表示：void f();或void f(void);。void f(void)是为了和C语言兼容

void函数不返回任何值。函数的返回类型不能是数组类型或函数类型，但可以是指向数组或函数的指针。



goto语句：goto label;代表跳转到代码label:所在的位置

# 异常处理
异常处理：throw在try中抛出异常，根据异常的不同选择不同的catch块。

多层函数调用中，出现异常，程序会一层一层的往上寻找对应的catch语句，找不到就终止程序。
catch块中一般进行内存释放等清理操作。
大多数常见的类都是定义在标准库中的，所以调用的时候，都要带std::，如std::runtime_error。
如果异常类型有一个字符串初始值，则what()返回字符串。
具体见原文和[链接](https://www.cnblogs.com/codingbigdog/p/16505862.html)



# 函数指针
将函数名替换成(*pf)就生成了一个函数指针pf。
函数名当成一个值使用时，该函数名被当成地址。
函数指针作为形参
函数指针作为返回值




# 智能指针
智能指针不用自己释放内存，只要没有指针指向内存了，就会自动释放。
shared ptr允许多个指针指向同一个对象
unique_ ptr则“独占”所指向的对象。
标准库还定义了一个名为weak_ ptr的伴随类，它是一种弱引用，指向shared ptr所管理的对象。这三种类型都定义在memory头文件中。
shared_ptr创建出对象，而对象当然有相应的方法可以调用，如返回对象被引用的次数。
make_shared用于动态分配内存并初始化
接下来看404





# IO库
cout<<：代表向对象cout写入内容，<<代表写入的意思
三大IO类：
- iostream针对IO流
- fstream针对文件
- sstream针对string类型
类型ifstream和istringstream都继承自istream。类型ofstream和ostringstream都继承自ostream。所以对istream和ostream进行的操作，对其他两类型也可以。





# 位运算符












# 其他：

补码运算：正数为原码本身，负数为原码取反加一









# 问题：

2.取模运算？答：[链接](https://blog.csdn.net/qq_42775938/article/details/122696829)

3.int转无符号数的规则是什么？

4.为什么说初始化和赋值是两个完全不同的操作，是因为一个使用构造函数，另一个使用别的东西吗？？

5.constexpr变量的变量到底有什么作用？

6.“2.2.1”中有一个问题？ 