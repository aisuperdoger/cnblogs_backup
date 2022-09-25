原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522359.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h1><a id="0void_0"></a>0.void*简介</h1> 
<p>void*是一种特殊的指针类型，可用于存放任意对象的地址。</p> 
<pre><code class="prism language-cpp"><span class="token keyword">void</span> <span class="token operator">*</span>pv <span class="token operator">=</span><span class="token operator">&amp;</span>obj<span class="token punctuation">;</span> <span class="token comment">// obj 可以是任意类型的对象</span>
</code></pre> 
<p>void指针pv只保存了对象obj的首地址，并不知道obj是什么类型，所以通过pv无法取出obj。但是如果我们指明obj的类型，我们就可以取出obj对象。例子如下：</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;iostream&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>


<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>
	<span class="token keyword">int</span> b <span class="token operator">=</span> <span class="token number">1</span><span class="token punctuation">;</span>
	<span class="token keyword">void</span> <span class="token operator">*</span>a <span class="token operator">=</span> <span class="token operator">&amp;</span>b<span class="token punctuation">;</span>
	cout <span class="token operator">&lt;&lt;</span> a<span class="token operator">&lt;&lt;</span>endl<span class="token punctuation">;</span>			
	cout <span class="token operator">&lt;&lt;</span> <span class="token punctuation">(</span><span class="token keyword">int</span><span class="token operator">*</span><span class="token punctuation">)</span>a<span class="token operator">&lt;&lt;</span>endl<span class="token punctuation">;</span>  <span class="token comment">// 输出与cout &lt;&lt; a;一致</span>
	cout <span class="token operator">&lt;&lt;</span> <span class="token operator">*</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token keyword">int</span><span class="token operator">*</span><span class="token punctuation">)</span>a<span class="token punctuation">)</span><span class="token punctuation">;</span>    <span class="token comment">// 输出1。(int*)a将void指针强制转换为int类型，相当于指明了a为int型。</span>
	
	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

</code></pre> 
<h3><a id="1void_23"></a>1.void*作为函数形参</h3> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;stdio.h&gt;</span></span>

<span class="token keyword">int</span> <span class="token function">void_test</span><span class="token punctuation">(</span><span class="token keyword">void</span><span class="token operator">*</span> data<span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
    <span class="token keyword">int</span> num <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span>

    num <span class="token operator">=</span> <span class="token operator">*</span><span class="token punctuation">(</span><span class="token keyword">int</span><span class="token operator">*</span><span class="token punctuation">)</span>data<span class="token punctuation">;</span> 		<span class="token comment">// (int*)的作用是将data当成一个int指针（强制类型转换）</span>
    <span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"num = %d\n"</span><span class="token punctuation">,</span> num<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token punctuation">}</span>

<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
    <span class="token keyword">int</span> val<span class="token punctuation">;</span>

    val <span class="token operator">=</span> <span class="token number">123</span><span class="token punctuation">;</span>
    <span class="token function">void_test</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>val<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// 将以上代码编译并运行，输出结果为：</span>
<span class="token comment">// num = 123</span>
</code></pre> 
<h3><a id="2void_48"></a>2.void指针的加一操作</h3> 
<p>在ANSI中下面代码是错误的</p> 
<pre><code class="prism language-cpp"><span class="token keyword">void</span> <span class="token operator">*</span> pvoid<span class="token punctuation">;</span>
pvoid<span class="token operator">++</span><span class="token punctuation">;</span> <span class="token comment">//ANSI：错误</span>
pvoid <span class="token operator">+=</span> <span class="token number">1</span><span class="token punctuation">;</span> <span class="token comment">//ANSI：错误</span>
</code></pre> 
<p>GNU指定void *的算法操作与char *一致</p> 
<pre><code class="prism language-cpp"><span class="token keyword">void</span> <span class="token operator">*</span> pvoid<span class="token punctuation">;</span>
pvoid<span class="token operator">++</span><span class="token punctuation">;</span> <span class="token comment">//GNU：正确</span>
pvoid <span class="token operator">+=</span> <span class="token number">1</span><span class="token punctuation">;</span> <span class="token comment">//GNU：正确</span>
</code></pre> 
<p>为迎合ANSI标准，并提高程序的可移植性，我们可以这样编写实现同样功能的代码：</p> 
<pre><code class="prism language-cpp"><span class="token keyword">void</span> <span class="token operator">*</span> pvoid<span class="token punctuation">;</span>
<span class="token punctuation">(</span><span class="token keyword">char</span> <span class="token operator">*</span><span class="token punctuation">)</span>pvoid<span class="token operator">++</span><span class="token punctuation">;</span> <span class="token comment">//ANSI：正确；GNU：正确</span>
<span class="token punctuation">(</span><span class="token keyword">char</span> <span class="token operator">*</span><span class="token punctuation">)</span>pvoid <span class="token operator">+=</span> <span class="token number">1</span><span class="token punctuation">;</span> <span class="token comment">//ANSI：错误；GNU：正确</span>
</code></pre> 
<p>GNU和ANSI还有一些区别，总体而言，GNU较ANSI更“开放”，提供了对更多语法的支持。但是我们在真实设计时，还是应该尽可能地迎合ANSI标准。</p> 
<h3><a id="_69"></a>其他</h3> 
<p>如果函数的参数可以是任意类型指针，那么应声明其参数为void *<br> 典型的如内存操作函数memcpy和memset的函数原型分别为：</p> 
<pre><code class="prism language-cpp"><span class="token keyword">void</span> <span class="token operator">*</span> <span class="token function">memcpy</span><span class="token punctuation">(</span><span class="token keyword">void</span> <span class="token operator">*</span>dest<span class="token punctuation">,</span> <span class="token keyword">const</span> <span class="token keyword">void</span> <span class="token operator">*</span>src<span class="token punctuation">,</span> size_t len<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">void</span> <span class="token operator">*</span> <span class="token function">memset</span> <span class="token punctuation">(</span> <span class="token keyword">void</span> <span class="token operator">*</span> buffer<span class="token punctuation">,</span> <span class="token keyword">int</span> c<span class="token punctuation">,</span> size_t num <span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre> 
<p>参考：https://www.cnblogs.com/geekham/p/4225993.html</p>
                