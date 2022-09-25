原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522362.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>使用char类型的数组保存字符串。每个字符串都需要以’\0’结尾，所以字符串数组的长度最小等于字符个数+1<br> 三种等价的初始化方式：</p> 
<pre><code class="prism language-cpp"><span class="token keyword">char</span> str<span class="token punctuation">[</span><span class="token number">12</span><span class="token punctuation">]</span><span class="token operator">=</span><span class="token punctuation">{<!-- --></span><span class="token string">'H'</span><span class="token punctuation">,</span><span class="token string">'e'</span><span class="token punctuation">,</span><span class="token string">'l'</span><span class="token punctuation">,</span><span class="token string">'l'</span><span class="token punctuation">,</span><span class="token string">'o'</span><span class="token punctuation">,</span><span class="token string">','</span><span class="token punctuation">,</span><span class="token string">'W'</span><span class="token punctuation">,</span><span class="token string">'o'</span><span class="token punctuation">,</span><span class="token string">'r'</span><span class="token punctuation">,</span><span class="token string">'l'</span><span class="token punctuation">,</span><span class="token string">'d'</span><span class="token punctuation">,</span><span class="token string">'\0'</span><span class="token punctuation">}</span><span class="token punctuation">;</span> <span class="token comment">// 初始化列表</span>
<span class="token keyword">char</span> str1<span class="token punctuation">[</span><span class="token number">12</span><span class="token punctuation">]</span><span class="token operator">=</span><span class="token string">"Hello,World"</span><span class="token punctuation">;</span> <span class="token comment">// 指定字符数组长度,字符串末尾隐含设为'\0'</span>
<span class="token keyword">char</span> str2<span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token operator">=</span><span class="token string">"Hello,World"</span><span class="token punctuation">;</span>   <span class="token comment">// 未指定字符数组长度,字符串末尾隐含设为'\0'</span>
</code></pre> 
<p>当然还可以使用string定义字符串，这里不赘述。</p> 
<p>参考：https://blog.csdn.net/shizheng_Li/article/details/105752490</p>
                