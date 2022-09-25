原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522347.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>先看下面一段代码：</p> 
<pre><code class="prism language-cpp"><span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;iostream&gt;</span></span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;csignal&gt;</span></span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;unistd.h&gt;</span></span>
 
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>
 
<span class="token keyword">void</span> <span class="token function">signalHandler</span><span class="token punctuation">(</span> <span class="token keyword">int</span> signum <span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
    cout <span class="token operator">&lt;&lt;</span> <span class="token string">"Interrupt signal ("</span> <span class="token operator">&lt;&lt;</span> signum <span class="token operator">&lt;&lt;</span> <span class="token string">") received.\n"</span><span class="token punctuation">;</span>
 
    <span class="token comment">// 清理并关闭</span>
    <span class="token comment">// 终止程序  </span>
   <span class="token function">exit</span><span class="token punctuation">(</span>signum<span class="token punctuation">)</span><span class="token punctuation">;</span>  
 
<span class="token punctuation">}</span>
 
<span class="token keyword">int</span> main <span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
    <span class="token comment">// 注册信号 SIGINT 和信号处理程序</span>
    <span class="token function">signal</span><span class="token punctuation">(</span>SIGINT<span class="token punctuation">,</span> signalHandler<span class="token punctuation">)</span><span class="token punctuation">;</span>  
 
    <span class="token keyword">while</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">{<!-- --></span>
       cout <span class="token operator">&lt;&lt;</span> <span class="token string">"Going to sleep...."</span> <span class="token operator">&lt;&lt;</span> endl<span class="token punctuation">;</span>
       <span class="token function">sleep</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
 
    <span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>signal(SIGINT, signalHandler); 代表当程序检测到SIGINT信号的时候，执行signalHandler函数。SIGINT信号是程序终止(interrupt)信号，故当你按ctrl+c时，就相当于释放了程序终止(interrupt)信号，就会自动调用signalHandler函数。<br> signal(registered signal, signal handler)这个函数接收两个参数：第一个参数是代表了信号的编号；第二个参数是一个指向信号处理函数的指针。有以下几种信号编号：<br> <img src="https://img-blog.csdnimg.cn/041c8e66d3d242e0ae01cb7c703bb258.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_13,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 参考：<a href="https://www.runoob.com/cplusplus/cpp-signal-handling.html">链接</a></p>
                