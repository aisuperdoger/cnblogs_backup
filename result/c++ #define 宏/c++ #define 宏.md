原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522348.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h3><a id="1define__1"></a>1.#define 宏的使用：</h3> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">define</span> <span class="token macro-name">PI</span> <span class="token expression"><span class="token number">3.1415926</span> </span><span class="token comment">// 把程序中出现的PI全部换成3.1415926</span></span>
</code></pre> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">define</span> <span class="token macro-name function">S</span><span class="token expression"><span class="token punctuation">(</span>a<span class="token punctuation">,</span>b<span class="token punctuation">)</span> a<span class="token operator">*</span>b </span><span class="token comment">// area=S(3,2)；第一步被换为area=a*b; ，第二步被换为area=3*2;</span></span>
</code></pre> 
<pre><code class="prism language-cpp"><span class="token comment">// 实参如果是表达式容易出问题</span>

<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">define</span> <span class="token macro-name function">S</span><span class="token expression"><span class="token punctuation">(</span>r<span class="token punctuation">)</span> r<span class="token operator">*</span>r</span></span>

area<span class="token operator">=</span><span class="token function">S</span><span class="token punctuation">(</span>a<span class="token operator">+</span>b<span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">// 第一步换为area=r*r;,第二步被换为area=a+b*a+b;</span>
<span class="token comment">//正确的宏定义是 #define S(r) ((r)*(r))</span>
</code></pre> 
<p>更具体可见<a href="https://www.cnblogs.com/zhizhiyu/p/10155614.html">链接</a></p> 
<h3><a id="2undef_20"></a>2.#undef使用</h3> 
<p>undef用于取消宏定义</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;stdio.h&gt;</span>  </span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">define</span> <span class="token macro-name">PI</span> <span class="token expression"><span class="token number">3.14</span>  </span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">undef</span> <span class="token expression">PI  </span></span>
<span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>  
   <span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"%f"</span><span class="token punctuation">,</span>PI<span class="token punctuation">)</span><span class="token punctuation">;</span>  
<span class="token punctuation">}</span>
</code></pre> 
<p>执行上面示例代码，得到以下结果</p> 
<pre><code class="prism language-bash">Compile Time Error: <span class="token string">'PI'</span> undeclared
</code></pre> 
<p>参考<a href="https://www.yiibai.com/cprogramming/c-preprocessor-undef.html">链接</a></p>
                