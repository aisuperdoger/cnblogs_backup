原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522379.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h1><a id="_0"></a>一、预备知识—程序的内存分配</h1> 
<p>一个由C/C++编译的程序占用的内存分为以下几个部分<br> 1、栈区（stack）— 由编译器自动分配释放 ，存放函数的参数值，局部变量的值等。其操作方式类似于数据结构中的栈。<br> 2、堆区（heap） — 一般由程序员分配释放， 若程序员不释放，程序结束时<strong>可能</strong>由OS回收 。注意它与数据结构中的堆是两回事，分配方式倒是类似于链表，呵呵。 如使用new分配的空间，最后需要delete释放空间。<br> 3、全局区（静态区）（static）—，全局变量和静态变量的存储是放在一块的，初始化的全局变量和静态变量在一块区域， 未初始化的全局变量和未初始化的静态变量在相邻的另一块区域。 - 程序结束后由系统释放。<br> 4、文字常量区 —常量字符串就是放在这里的。程序结束后由系统释放<br> 5、程序代码区—存放函数体的二进制代码。</p> 
<h1><a id="_7"></a>二、例子程序</h1> 
<p>这是一个前辈写的，非常详细</p> 
<pre><code class="prism language-cpp"><span class="token comment">//main.cpp    </span>
  <span class="token keyword">int</span>   a   <span class="token operator">=</span>   <span class="token number">0</span><span class="token punctuation">;</span>   <span class="token comment">// 全局初始化区    </span>
  <span class="token keyword">char</span>   <span class="token operator">*</span>p1<span class="token punctuation">;</span>   <span class="token comment">// 全局未初始化区    </span>
  <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>    
  <span class="token punctuation">{<!-- --></span>    
  <span class="token keyword">int</span>   b<span class="token punctuation">;</span>   <span class="token comment">// 栈    </span>
  <span class="token keyword">char</span>   s<span class="token punctuation">[</span><span class="token punctuation">]</span>   <span class="token operator">=</span>   <span class="token string">"abc"</span><span class="token punctuation">;</span>   <span class="token comment">// 栈    </span>
  <span class="token keyword">char</span>   <span class="token operator">*</span>p2<span class="token punctuation">;</span>   <span class="token comment">// 栈    </span>
  <span class="token keyword">char</span>   <span class="token operator">*</span>p3   <span class="token operator">=</span>   <span class="token string">"123456"</span><span class="token punctuation">;</span>  <span class="token comment">//  123456/0在常量区，p3在栈上。    </span>
  <span class="token keyword">static</span>   <span class="token keyword">int</span>   c   <span class="token operator">=</span><span class="token number">0</span>；<span class="token comment">// 全局（静态）初始化区    </span>
  p1   <span class="token operator">=</span>   <span class="token punctuation">(</span><span class="token keyword">char</span>   <span class="token operator">*</span><span class="token punctuation">)</span><span class="token function">malloc</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">)</span><span class="token punctuation">;</span>    
  p2   <span class="token operator">=</span>   <span class="token punctuation">(</span><span class="token keyword">char</span>   <span class="token operator">*</span><span class="token punctuation">)</span><span class="token function">malloc</span><span class="token punctuation">(</span><span class="token number">20</span><span class="token punctuation">)</span><span class="token punctuation">;</span>  <span class="token comment">// 分配得来得10和20字节的区域就在堆区。    </span>
  <span class="token function">strcpy</span><span class="token punctuation">(</span>p1<span class="token punctuation">,</span>   <span class="token string">"123456"</span><span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">// 123456/0放在常量区，编译器可能会将它与p3所指向的"123456" 优化成一个地方。    </span>
  <span class="token punctuation">}</span>    
</code></pre> 
<h1><a id="_25"></a>二、堆和栈的理论知识</h1> 
<h2><a id="21_26"></a>2.1申请方式</h2> 
<p>stack:<br> 由系统自动分配。 例如，声明在函数中一个局部变量 int b; 系统自动在栈中为b开辟空 间<br> heap:<br> 需要程序员自己申请，并指明大小，在c中malloc函数<br> 如p1 = (char *)malloc(10);<br> 在C++中用new运算符<br> 如p2 = new char[10];<br> 但是注意p1、p2本身是在栈中的。</p> 
<h2><a id="22____36"></a>2.2 申请后系统的响应</h2> 
<p>栈：只要栈的剩余空间大于所申请空间，系统将为程序提供内存，否则将报异常提示栈溢 出。<br> 堆：首先应该知道操作系统有一个记录空闲内存地址的链表，当系统收到程序的申请时， 会遍历该链表，寻找第一个空间大于所申请空间的堆结点，然后将该结点从空闲结点链表 中删除，并将该结点的空间分配给程序，另外，对于大多数系统，会在这块内存空间中的 首地址处记录本次分配的大小，这样，代码中的delete语句才能正确的释放本内存空间。 另外，由于找到的堆结点的大小不一定正好等于申请的大小，系统会自动的将多余的那部分重新放入空闲链表中。</p> 
<h2><a id="23__39"></a>2.3 申请大小的限制</h2> 
<p>栈：在Windows下,栈是向低地址扩展的数据结构，是一块连续的内存的区域。这句话的意 思是栈顶的地址和栈的最大容量是系统预先规定好的，在WINDOWS下，栈的大小是2M（也有的说是1M，总之是一个编译时就确定的常数），如果申请的空间超过栈的剩余空间时，将 提示overflow。因此，能从栈获得的空间较小。<br> 堆：堆是向高地址扩展的数据结构，是不连续的内存区域。这是由于系统是用链表来存储的空闲内存地址的，自然是不连续的，而链表的遍历方向是由低地址向高地址。堆的大小受限于计算机系统中有效的虚拟内存。由此可见，堆获得的空间比较灵活，也比较大。</p> 
<h2><a id="24__42"></a>2.4 申请效率的比较：</h2> 
<p>栈由系统自动分配，速度较快。但程序员是无法控制的。<br> 堆是由new分配的内存，一般速度比较慢，而且容易产生内存碎片,不过用起来最方便. 另外，在WINDOWS下，最好的方式是用VirtualAlloc分配内存，他不是在堆，也不是在栈是 直接在进程的地址空间中保留一块内存，虽然用起来最不方便。但是速度快，也最灵活。</p> 
<h2><a id="25__45"></a>2.5 堆和栈中的存储内容</h2> 
<p>栈： 在函数调用时，第一个进栈的是主函数中后的下一条指令（函数调用语句的下一条可执行语句）的地址，然后是函数的各个参数，在大多数的C编译器中，参数是由右往左入栈的，然后是函数中的局部变量。注意静态变量是不入栈的。当本次函数调用结束后，局部变量先出栈，然后是参数，最后栈顶指针指向最开始存的地址，也就是主函数中的下一条指令，程序由该点继续运行。<br> 堆：一般是在堆的头部用一个字节存放堆的大小。堆中的具体内容由程序员安排。</p> 
<h2><a id="26__49"></a>2.6 存取效率的比较</h2> 
<pre><code class="prism language-cpp"><span class="token keyword">char</span>   s1<span class="token punctuation">[</span><span class="token punctuation">]</span>   <span class="token operator">=</span>   <span class="token string">"aaaaaaaaaaaaaaa"</span><span class="token punctuation">;</span>    
<span class="token keyword">char</span>   <span class="token operator">*</span>s2   <span class="token operator">=</span>   <span class="token string">"bbbbbbbbbbbbbbbbb"</span><span class="token punctuation">;</span>    
</code></pre> 
<p>aaaaaaaaaaa是在运行时刻赋值的；<br> 而bbbbbbbbbbb是在编译时就确定的；<br> 但是，在以后的存取中，在栈上的数组比指针所指向的字符串(例如堆)快。<br> 比如：</p> 
<pre><code class="prism language-cpp"> <span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span>    </span>
  <span class="token keyword">void</span>   <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>    
  <span class="token punctuation">{<!-- --></span>    
  <span class="token keyword">char</span>   a   <span class="token operator">=</span>   <span class="token number">1</span><span class="token punctuation">;</span>    
  <span class="token keyword">char</span>   c<span class="token punctuation">[</span><span class="token punctuation">]</span>   <span class="token operator">=</span>   <span class="token string">"1234567890"</span><span class="token punctuation">;</span>    
  <span class="token keyword">char</span>   <span class="token operator">*</span>p   <span class="token operator">=</span><span class="token string">"1234567890"</span><span class="token punctuation">;</span>    
  a   <span class="token operator">=</span>   c<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">;</span>    
  a   <span class="token operator">=</span>   p<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">;</span>    
  <span class="token keyword">return</span><span class="token punctuation">;</span>    
  <span class="token punctuation">}</span>    
</code></pre> 
<p>对应的汇编代码<br> 10: a = c[1];<br> 00401067 8A 4D F1 mov cl,byte ptr [ebp-0Fh]<br> 0040106A 88 4D FC mov byte ptr [ebp-4],cl<br> 11: a = p[1];<br> 0040106D 8B 55 EC mov edx,dword ptr [ebp-14h]<br> 00401070 8A 42 01 mov al,byte ptr [edx+1]<br> 00401073 88 45 FC mov byte ptr [ebp-4],al<br> 第一种在读取时直接就把字符串中的元素读到寄存器cl中，而第二种则要先把指针值读到 edx中，再根据edx读取字符，显然慢了。</p> 
<h1><a id="_27__81"></a># 2.7 小结：</h1> 
<table><thead><tr><th>栈</th><th>堆</th></tr></thead><tbody><tr><td>由编译器自动分配释放 ，存放函数的参数值，局部变量的值等。从系统提供的内存区域分配。栈区比较小（2M左右）。在函数调用时，第一个进栈的是主函数中后的下一条指令。</td><td>由程序员分配释放，如使用new分配的空间，最后需要delete释放空间。从记录空闲内存地址的链表中申请。堆的大小受限于计算机系统中有效的虚拟内存。 堆的头部用一个字节存放堆的大小。</td></tr><tr><td>分配速度快。运行时刻赋值，但读取时直接就把数据读到寄存器中。</td><td>分配速度较栈慢。编译时就确定，但读取时先把指针值读到 edx中，再根据edx读取字符。</td></tr></tbody></table>
                