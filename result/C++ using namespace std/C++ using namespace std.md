原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522350.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h3><a id="1namespaceusing_0"></a>1.namespace和using</h3> 
<p>C＋＋标准程序库中的所有标识符都被定义于一个名为std的namespace中。<br> 由于namespace的概念，使用C＋＋标准程序库的任何标识符时，可以有三种选择：<br> 1、直接指定标识符。例如std::ostream而不是ostream。完整语句如下：<br> std::cout &lt;&lt; std::hex&lt;&lt; 3.4&lt;&lt; std::endl;<br> 2、使用using关键字。<br> using std::cout;<br> using std::endl;<br> 以上程序可以写成<br> cout &lt;&lt; std::hex&lt;&lt; 3.4&lt;&lt; endl;<br> 3、最方便的就是使用using namespace std;<br> 例如：<br> #include <br> #include <br> #include <br> using namespace std;<br> 这样命名空间std内定义的所有标识符都有效（曝光）。就好像它们被声明为全局变量一样。那么以上语句可以如下写:<br> cout &lt;&lt; hex&lt;&lt; 3.4&lt;&lt; endl;</p> 
<h3><a id="2namespace_18"></a>2.自定义的名空间（namespace）</h3> 
<pre><code class="prism language-cpp"><span class="token comment">//#include &lt;conio.h&gt;</span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;iostream&gt;</span></span>
<span class="token keyword">namespace</span> car <span class="token comment">// 名空间的定义</span>
<span class="token punctuation">{<!-- --></span>
  <span class="token keyword">int</span> model<span class="token punctuation">;</span>
  <span class="token keyword">int</span> length<span class="token punctuation">;</span>
  <span class="token keyword">int</span> width<span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">namespace</span> plane
<span class="token punctuation">{<!-- --></span>
  <span class="token keyword">int</span> model<span class="token punctuation">;</span>
  <span class="token keyword">namespace</span> size <span class="token comment">// 名空间的嵌套</span>
  <span class="token punctuation">{<!-- --></span>
    <span class="token keyword">int</span> length<span class="token punctuation">;</span>
    <span class="token keyword">int</span> width<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>



<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
  
  plane<span class="token operator">::</span>size<span class="token operator">::</span>length<span class="token operator">=</span><span class="token number">70</span><span class="token punctuation">;</span>
  std<span class="token operator">::</span>cout<span class="token operator">&lt;&lt;</span><span class="token string">"the length of plane is "</span><span class="token operator">&lt;&lt;</span>plane<span class="token operator">::</span>size<span class="token operator">::</span>length<span class="token operator">&lt;&lt;</span><span class="token string">"m."</span><span class="token operator">&lt;&lt;</span>std<span class="token operator">::</span>endl<span class="token punctuation">;</span>
  <span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>参考：<a href="https://blog.csdn.net/quyafeng2011/article/details/68921750">链接1</a><br> <a href="https://blog.csdn.net/weixin_40597170/article/details/79827221">链接2</a></p>
                