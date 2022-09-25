原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522374.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h3><a id="1_0"></a>1.不同系统定义不同</h3> 
<p>size_t 的全称应该是size type，就是说size_t是用来记录数据大小无符号整型。size_t的真实类型与操作系统有关。<br> 在32位架构中被普遍定义为：</p> 
<pre><code class="prism language-cpp"><span class="token keyword">typedef</span>   <span class="token keyword">unsigned</span> <span class="token keyword">int</span> size_t<span class="token punctuation">;</span>
</code></pre> 
<p>而在64位架构中被定义为：</p> 
<pre><code class="prism language-cpp"><span class="token keyword">typedef</span>  <span class="token keyword">unsigned</span> <span class="token keyword">long</span> size_t<span class="token punctuation">;</span>
</code></pre> 
<p>size_t在32位架构上是4字节，在64位架构上是8字节，在不同架构上进行编译时需要注意这个问题。而int在不同架构下都是4字节，与size_t不同；且int为带符号数，size_t为无符号数。</p> 
<h2><a id="2size_tsizeof_12"></a>2.size_t常与sizeof配合使用</h2> 
<p>size_t 的全称应该是size type，就是说size_t是用来记录数据大小无符号整型。所以size_t最经常与sizeof配合使用，如：</p> 
<pre><code class="prism language-cpp">size_t size <span class="token operator">=</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span>i<span class="token punctuation">)</span><span class="token punctuation">;</span> 
</code></pre> 
<p>我的理解是，在64位系统中数据i可能占用字节数会更多，所以需要将size_t定义为unsigned long。在32位系统中数据i可能占用字节数会少一些，所以需要将size_t定义为unsigned int。这样使得，同样都是使用size_t但所表示大小不同，size_t会依据系统的具体定义进行调整，即size_t代表的值会更加地符合系统的实际。</p> 
<h3><a id="3_18"></a>3.注意点</h3> 
<p>在编译的过程中size_t类型的a值会被编译他的补码。所以在使用size_t类型数据的过程中尤其要注意，特别是在逻辑表达式中使用到该类型，稍不注意可能带来很严重的后果。<br> 注：正数的补码：与原码相同；负数的补码：符号位为1，其余位为该数绝对值的原码按位取反，然后整个数加1。</p> 
<p>参考：<br> <a href="https://blog.csdn.net/JIEJINQUANIL/article/details/50981834">链接1</a><br> <a href="https://blog.csdn.net/qq_41598072/article/details/84924997">链接2</a><br> <a href="https://www.zhihu.com/question/24773728">链接3</a></p>
                