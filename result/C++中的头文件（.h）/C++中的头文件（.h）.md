原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522351.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h2><a id="1_0"></a>1.定义</h2> 
<p>头文件是扩展名为 .h 的文件，头文件也是C++的源代码，头文件中包含了 C++中函数、类、对象等的声明和宏定义，它可以被多个源文件通过#include引用共享。</p> 
<h2><a id="2_2"></a>2.使用头文件原因</h2> 
<p>C++中有“单一定义”规则，即一个对象只能被定义一次，如果在一个源文件中定义了一个函数，其他的源文件想要使用这个函数就需要在使用前声明一下这个函数，在编译结束之后，编译器链接的时候再去查找这些函数的定义。<br> 故要使用其他文件中定义的函数、类、对象（变量）时，需要对函数、类、对象进行声明。这些声明文件一般放在一个头文件中，这样只要通过#include就可以一下引入所有的声明。当然也可以在头文件中定义宏。<br> 自定义的头文件，使用#include"头文件.h"。对于标准库头文件的包含使用#include&lt;头文件.h&gt;</p> 
<h2><a id="3_6"></a>3.编译过程中的头文件</h2> 
<p>C++代码的编译主要通过以下几个过程：预编译-&gt;编译-&gt;汇编-&gt;链接【可参考：<a href="https://blog.csdn.net/qq_42775938/article/details/122346013">链接</a>(建议先看此链接，再看下面内容)】，最后生成可执行文件。<br> 在预编译阶段，编译器将#include"头文件.h"替换成“头文件.h”中具体的声明内容。<br> 在链接阶段，编译器查找声明对象的定义。</p> 
<h3><a id="31_10"></a>3.1.预编译阶段，头文件被替换</h3> 
<p>我们看一个简单的例子，下面是一个头文件CA.h</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">ifndef</span> <span class="token expression">CA_H</span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">define</span> <span class="token macro-name">CA_H</span></span>
 
<span class="token keyword">int</span> <span class="token function">Fun</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">endif</span></span>
</code></pre> 
<p>头文件中的函数、类、对象（变量）必须在一个源文件有进行定义，这里在A.cpp中进行定义。<br> A.cpp：</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">"CA.h"</span></span>
<span class="token keyword">int</span> <span class="token function">Fun</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
	<span class="token keyword">return</span> <span class="token number">1</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>B.cpp中引用头文件：</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">"CA.h"</span></span>
 
<span class="token keyword">int</span> <span class="token function">Fun1</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
	<span class="token keyword">return</span> <span class="token function">Fun</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">{<!-- --></span>
	<span class="token keyword">return</span> <span class="token function">Fun1</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>预编译命令：</p> 
<pre><code class="prism language-bash">g++ -E B.cpp -o B.i
</code></pre> 
<p>经过预处理后， B.i：</p> 
<pre><code class="prism language-cpp"># <span class="token number">1</span> <span class="token string">"B.cpp"</span>
# <span class="token number">1</span> <span class="token string">"&lt;built-in&gt;"</span>
# <span class="token number">1</span> <span class="token string">"&lt;command-line&gt;"</span>
# <span class="token number">1</span> <span class="token string">"/usr/include/stdc-predef.h"</span> <span class="token number">1</span> <span class="token number">3</span> <span class="token number">4</span>
# <span class="token number">1</span> <span class="token string">"&lt;command-line&gt;"</span> <span class="token number">2</span>
# <span class="token number">1</span> <span class="token string">"B.cpp"</span>
# <span class="token number">1</span> <span class="token string">"CA.h"</span> <span class="token number">1</span>



<span class="token keyword">int</span> <span class="token function">Fun</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
# <span class="token number">2</span> <span class="token string">"B.cpp"</span> <span class="token number">2</span>

<span class="token keyword">int</span> <span class="token function">Fun1</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
 <span class="token keyword">return</span> <span class="token function">Fun</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">{<!-- --></span>
 <span class="token keyword">return</span> <span class="token function">Fun1</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>可以看到，B.cpp中的头文件#include "CA.h"都被CA.h中的具体内容所代替。<br> 【注】“＃”是注释</p> 
<h3><a id="32_75"></a>3.2.使用头文件</h3> 
<pre><code class="prism language-bash">g++ A.cpp B.cpp -o main
</code></pre> 
<p>B.cpp中通过头文件引入的东西，会在A.cpp中自动找到。</p> 
<h2><a id="4_80"></a>4.如何写头文件</h2> 
<p>参考：<a href="https://blog.csdn.net/lyanliu/article/details/2195632">链接</a><br> 在写头文件时需要注意，在开头和结尾处必须按照如下样式加上预编译语句（如下）<br> Circle.h：</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">ifndef</span> <span class="token expression">CIRCLE_H</span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">define</span> <span class="token macro-name">CIRCLE_H</span></span>

 <span class="token comment">// 你的代码写在这里</span>

<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">endif</span></span>
</code></pre> 
<p>#ifndef代表没有定义CIRCLE_H时，才能进入if。进入if之后，第一步就是执行#define CIRCLE_H来定义CIRCLE_H。这样做以后，即使重复引入头文件，也不会重复执行if中的东西。<br> 至于CIRCLE_H这个名字实际上是无所谓的，你叫什么都行，只要符合规范都行。原则上来说，非常建议把它写成这种形式，因为比较容易和头文件的名字对应。<br> 下面举个最简单的例子来描述一下，咱就求个圆面积。<br> 第1步，建立一个空工程（以在VS2003环境下为例）。<br> 第2步，在头文件的文件夹里新建一个名为Circle.h的头文件，它的内容如下：</p> 
<pre><code class="prism language-cpp"> <span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">ifndef</span> <span class="token expression">CIRCLE_H</span></span>
 <span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">define</span>  <span class="token macro-name">CIRCLE_H</span></span>

 <span class="token keyword">class</span>  <span class="token class-name">Circle</span>
 <span class="token punctuation">{<!-- --></span>
<span class="token keyword">private</span><span class="token operator">:</span>
    <span class="token keyword">double</span> r<span class="token punctuation">;</span><span class="token comment">//半径</span>
<span class="token keyword">public</span><span class="token operator">:</span>
    <span class="token function">Circle</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span><span class="token comment">//构造函数</span>
    <span class="token function">Circle</span><span class="token punctuation">(</span><span class="token keyword">double</span> R<span class="token punctuation">)</span><span class="token punctuation">;</span><span class="token comment">//构造函数</span>
    <span class="token keyword">double</span> <span class="token function">Area</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span><span class="token comment">//求面积函数</span>
<span class="token punctuation">}</span> <span class="token punctuation">;</span>

 <span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">endif</span></span>
</code></pre> 
<p>在头文件里，并不写出函数的具体实现。<br> 第3步，要给出Circle类的具体实现，因此，在源文件夹里新建一个Circle.cpp的文件，它的内容如下：</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span>  <span class="token string">" Circle.h "</span></span>

<span class="token class-name">Circle</span><span class="token double-colon punctuation">::</span><span class="token function">Circle</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
 <span class="token punctuation">{<!-- --></span>
    <span class="token keyword">this</span><span class="token operator">-&gt;</span>r<span class="token operator">=</span><span class="token number">5.0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token class-name">Circle</span><span class="token double-colon punctuation">::</span><span class="token function">Circle</span><span class="token punctuation">(</span> <span class="token keyword">double</span>  R<span class="token punctuation">)</span>
 <span class="token punctuation">{<!-- --></span>
    <span class="token keyword">this</span><span class="token operator">-&gt;</span>r<span class="token operator">=</span>R<span class="token punctuation">;</span>
<span class="token punctuation">}</span>

 <span class="token keyword">double</span>  <span class="token class-name">Circle</span><span class="token double-colon punctuation">::</span> <span class="token function">Area</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
 <span class="token punctuation">{<!-- --></span>
    <span class="token keyword">return</span> <span class="token number">3.14</span><span class="token operator">*</span>r<span class="token operator">*</span>r<span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>一般实现Circle.h的cpp文件取名为Circle.cpp<br> 最后，我们建一个main.cpp来测试我们写的Circle类，它的内容如下：</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span>  <span class="token string">&lt; iostream &gt;</span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span>  <span class="token string">" Circle.h "</span></span>
 <span class="token keyword">using</span>   <span class="token keyword">namespace</span>  std<span class="token punctuation">;</span>

 <span class="token keyword">int</span>  <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
 <span class="token punctuation">{<!-- --></span>
    Circle <span class="token function">c</span><span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    cout<span class="token operator">&lt;&lt;</span><span class="token string">"Area="</span><span class="token operator">&lt;&lt;</span>c<span class="token punctuation">.</span><span class="token function">Area</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">&lt;&lt;</span>endl<span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token number">1</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>运行命令：</p> 
<pre><code class="prism language-bash">g++ Circle.cpp main.cpp -o main
./main
</code></pre> 
<h2><a id="5Chh_153"></a>5.C++头文件有.h和没有.h</h2> 
<p>iostream.h是非标准头文件，iostream是标准头文件形式。iostream.h时代没有名词空间，即所有库函数包括头文件iostream.h都声明在全局域。为了体现结构层次，c++标准委员会引入了名词空间这一概念，并把所有库函数声明由全局域改到了名词空间std。iostream.h里面定义的所有类以及对象都是在全局空间里，所以可以直接使用cout，但如果你用iostream，就不能直接使用cout了，iostream里面所定义的东西都在标准命名空间std里面，所以你必须加上 using namespace std才能使用cout。<br> 故而，<br> 在早些时候，这两种头文件是等价：<br> #include&lt;iostream.h&gt; // 这个现在已经不支持了<br> 和<br> #include <br> using namespace std;<br> 现在标准的C++头文件没有.h扩展名，将以前的C的头文件转化为C++的头文件后，可以加上c的前缀表示来自于c，例如cmath就是由math,h变来。<br> 注意：c语言的string.h变为cstring，和c++的string是两个完全不同的东西。</p> 
<h2><a id="6hpp_166"></a>6.后缀为.hpp的文件</h2> 
<p>后缀为.hpp的文件一般提供程序使用的接口。</p> 
<p>我们公司和另一家软件公司合作，这样就必然要互相提供一些软件的信息（比如一些类，它到底是要做什么的），可是在提供这些信息的同时我们又不像让对方知道我们这些类的具体实现，毕竟这些是我们公司的算法核心和心血啊。所以这个时候就可以把类的接口（这个类是要做什么的）放在*.hpp文件中，而具体类的实现放在 .cpp文件。这时候我们只要给对方公司.hpp文件就行了。这样既提供了必要的信息，又保护了我们的核心代码。</p> 
<p>参考：<a href="https://blog.csdn.net/ddllrrbb/article/details/84729366">链接1</a><br> <a href="https://blog.csdn.net/quyafeng2011/article/details/68921750">链接2</a><br> <a href="https://www.cnblogs.com/galoishelley/p/3844281.html">链接3</a><br> <a href="https://blog.csdn.net/hmd3394969/article/details/114162657">链接4</a><br> <a href="https://blog.csdn.net/u013921430/article/details/79288554">链接5</a><br> <a href="https://zhuanlan.zhihu.com/p/387773355">链接6</a></p>
                