原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522371.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h3><a id="1_0"></a>1.基本使用</h3> 
<p>grep：查找哪个文件中有字符串A，并将A对应文件和A所在行打印出来。<br> 如：</p> 
<pre><code class="prism language-cpp"># 查找满足条件的文件
grep include <span class="token operator">*</span>cpp    # 查找以cpp结尾的文件中有哪些文件是包含字符串include，以及打印include所在行
输出如下：
test2<span class="token punctuation">.</span>cpp<span class="token operator">:</span>#include<span class="token operator">&lt;</span>iostream<span class="token operator">&gt;</span>
test<span class="token punctuation">.</span>cpp<span class="token operator">:</span>#include<span class="token operator">&lt;</span>iostream<span class="token operator">&gt;</span>
</code></pre> 
<pre><code class="prism language-cpp"># 查找目录下所有文件
grep <span class="token operator">-</span>r include <span class="token punctuation">.</span><span class="token operator">/</span>	 # 查找当前目录下所有包含字符串include的文件以及打印include所在行 
输出如下：
<span class="token punctuation">.</span><span class="token operator">/</span>test<span class="token punctuation">.</span>i<span class="token operator">:</span># <span class="token string">"/usr/include/c++/9/iostream"</span> 
<span class="token punctuation">.</span><span class="token operator">/</span>test<span class="token punctuation">.</span>i<span class="token operator">:</span># <span class="token string">"/usr/include/c++/9/iostream"</span>
</code></pre> 
<pre><code class="prism language-cpp"># 查找不包含某字符的文件及其对应行
grep <span class="token operator">-</span>v include <span class="token operator">*</span>cpp<span class="token operator">*</span> # 查找文件名包含cpp的文件中不包含include的行
输出如下：
test2<span class="token punctuation">.</span>cpp<span class="token operator">:</span><span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">{<!-- --></span>
test2<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	std<span class="token double-colon punctuation">::</span>cout <span class="token operator">&lt;&lt;</span> <span class="token string">"/*"</span><span class="token punctuation">;</span>
test2<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	std<span class="token double-colon punctuation">::</span>cout <span class="token operator">&lt;&lt;</span> <span class="token string">"*/"</span><span class="token punctuation">;</span>
test2<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	<span class="token comment">// std: :cout &lt;&lt; /* "*/" */;</span>
test2<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	<span class="token comment">// std: :cout &lt;&lt; /* "*/" /* "/*" */;</span>
test2<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
test2<span class="token punctuation">.</span>cpp<span class="token operator">:</span><span class="token punctuation">}</span>
test<span class="token punctuation">.</span>cpp<span class="token operator">:</span><span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">{<!-- --></span>
test<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	std<span class="token double-colon punctuation">::</span>cout <span class="token operator">&lt;&lt;</span> <span class="token string">"/*"</span><span class="token punctuation">;</span>
test<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	std<span class="token double-colon punctuation">::</span>cout <span class="token operator">&lt;&lt;</span> <span class="token string">"*/"</span><span class="token punctuation">;</span>
test<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	<span class="token comment">// std: :cout &lt;&lt; /* "*/" */;</span>
test<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	<span class="token comment">// std: :cout &lt;&lt; /* "*/" /* "/*" */;</span>
test<span class="token punctuation">.</span>cpp<span class="token operator">:</span>	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
test<span class="token punctuation">.</span>cpp<span class="token operator">:</span><span class="token punctuation">}</span>
</code></pre> 
<pre><code class="prism language-cpp"># 总结：
$ grep <span class="token string">"被查找的字符串"</span> 文件名 # 从文件内容查找匹配指定字符串的行
$ grep –r <span class="token string">"被查找的字符串"</span> 目录名 # 查找目录下所有文件有哪些文件的哪些行满足条件
$ grep –e <span class="token string">"正则表达式"</span> 文件名 # 从文件内容查找与正则表达式匹配的行
$ grep –i <span class="token string">"被查找的字符串"</span> 文件名 # 查找时不区分大小写
$ grep <span class="token operator">-</span>c <span class="token string">"被查找的字符串"</span> 文件名 # 查找匹配的行数
$ grep –v <span class="token string">"被查找的字符串"</span> 文件名 从文件内容查找不匹配指定字符串的行
</code></pre> 
<h3><a id="2__47"></a>2. |的使用</h3> 
<p>某查询命令｜grep “被查找的字符串”：中间的|功能是把上一条命令的输出，作为下一条命令的参数，如：</p> 
<pre><code class="prism language-cpp">ps <span class="token operator">-</span>ef <span class="token operator">|</span>grep java
其中ps <span class="token operator">-</span>ef输出所有进程的状态
grep java代表在ps <span class="token operator">-</span>ef输出的文本中查找java这个字段
如果连续使用 <span class="token operator">|</span> grep xxx ，就相当于 一层层的过滤筛选。 比如 ps <span class="token operator">-</span>ef <span class="token operator">|</span> grep java <span class="token operator">|</span>grep jenkins <span class="token operator">|</span>grep httpPort

再如：
ls <span class="token punctuation">.</span><span class="token operator">/</span> <span class="token operator">|</span> grep bash
查找ls输出的信息中是否含有带字符串bash
</code></pre> 
<h3><a id="3_59"></a>3.其他</h3> 
<p>sudo grep -r -i pypi.douban.com / # 从根目录开始找含有pypi.douban.com的文件</p> 
<p>参考：https://blog.csdn.net/auccy/article/details/79376680</p>
                