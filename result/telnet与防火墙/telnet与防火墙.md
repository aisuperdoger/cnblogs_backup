原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522346.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>Telnet 命令通常用来远程登录，是TCP/IP协议族中的一员。<br> Telnet 命令还可以作为别的用途，比如确定远程服务的状态，比如确定远程服务器的某个端口是否能访问。<br> 默认情况下，Telnet 在端口 23 上运行。如果您的系统上正在运行任何防火墙，请确保启用必要的端口：</p> 
<pre><code class="prism language-bash"><span class="token function">sudo</span> ufw allow 23
<span class="token function">sudo</span> ufw reload
<span class="token function">sudo</span> ufw <span class="token function">enable</span>
</code></pre> 
<p>telnet 命令的一般格式如下：</p> 
<pre><code class="prism language-bash">telnet <span class="token punctuation">[</span>hostname/ipaddress<span class="token punctuation">]</span> <span class="token punctuation">[</span>port number<span class="token punctuation">]</span>
</code></pre> 
<p>下面的示例命令测试在IP为192.168.77.21的服务器的端口 153上是否开启了监听：</p> 
<pre><code class="prism language-bash">telnet 192.168.77.21 153
</code></pre> 
<p>输出：</p> 
<pre><code class="prism language-bash">Trying 192.168.77.21<span class="token punctuation">..</span>.
Connected to 192.168.77.21.
Escape character is <span class="token string">'^]'</span><span class="token keyword">.</span>
</code></pre> 
<p>参考：<a href="https://www.cnblogs.com/qichunlin/p/8877983.html">链接</a><br> <a href="https://www.yundongfang.com/Yun71091.html#:~:text=Telnet%20%E9%80%9A%E5%B8%B8%E5%9C%A8%20TCP%20%E7%AB%AF%E5%8F%A3%2023%20%E4%B8%8A%E4%BE%A6%E5%90%AC%E7%94%A8%E6%88%B7%E7%9A%84%E6%89%80%E6%9C%89%E8%AF%B7%E6%B1%82%EF%BC%8C%E4%BD%86%E6%82%A8%E5%8F%AF%E4%BB%A5%E7%9B%B8%E5%BA%94%E5%9C%B0%E6%9B%B4%E6%94%B9%E5%AE%83%E3%80%82%20%E6%AD%A5%E9%AA%A4%201.,%E4%B8%8A%20%E5%AE%89%E8%A3%85%20Telnet%20%E3%80%82%20%E9%BB%98%E8%AE%A4%E6%83%85%E5%86%B5%E4%B8%8B%EF%BC%8CTelnet%20%E5%9C%A8%20Ubuntu%20%E5%9F%BA%E7%A1%80%E5%AD%98%E5%82%A8%E5%BA%93%E4%B8%AD%E5%8F%AF%E7%94%A8%E3%80%82">链接</a></p>
                