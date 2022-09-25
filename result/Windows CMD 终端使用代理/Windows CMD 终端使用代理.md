原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522388.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>https://www.cnblogs.com/duchaoqun/p/11854744.html</p> 
<pre><code># 使用 http 类型代理
set http_proxy=http://127.0.0.1:8484
set https_proxy=http://127.0.0.1:8484

# 使用 socks 类型代理
netsh winhttp set proxy proxy-server="socks=127.0.0.1:8484" bypass-list="localhost"
netsh winhttp show proxy
netsh winhttp reset proxy

# 使用 socks 类型代理
set http_proxy=socks5://127.0.0.1:8484
set https_proxy=socks5://127.0.0.1:8484
</code></pre>
                