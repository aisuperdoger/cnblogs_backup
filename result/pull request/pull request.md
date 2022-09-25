原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522342.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>“Pull Request 是一种通知机制。<br> 你修改了他人的代码，将你的修改通知原来的作者，希望他合并你的修改，这就是 Pull Request。”</p> 
<p>假设要pull request的库为https://github.com/usernameA/repository<br> 1.fork原仓库<br> 首先你需要对库repository进行fork。假设fork以后，仓库repository在你的github中的地址为https://github.com/mynameA/repository<br> 2.修改代码，并上传到远程仓库<br> 执行：</p> 
<pre><code class="prism language-bash"><span class="token function">git</span> clone https://github.com/mynameA/repository  <span class="token comment"># 将仓库从你的github克隆下来</span>
创建分支feature、修改、add、commit、merge
<span class="token function">git</span> push -u origin feature  <span class="token comment"># 第一次需要指明origin和feature，以后只需要输入git push就相当于git push -u origin feature </span>
</code></pre> 
<p>3.执行pull request<br> 在https://github.com/mynameA/repository中创建pull request，如下：<br> <img src="https://img-blog.csdnimg.cn/d22a6cb0a298455db26083e6bcb3ef58.png" alt="在这里插入图片描述"></p> 
<p>选择将mynameA/repository的哪个分支merge到usernameA/repository的哪个分支，如下：<br> <img src="https://img-blog.csdnimg.cn/f7abfcee833445e19f20e36426b8aea5.png" alt="在这里插入图片描述"></p> 
<p><strong>说明1：</strong></p> 
<pre><code class="prism language-bash"><span class="token function">git</span> push -u origin master  
相当于 
<span class="token function">git</span> branch --set-upstream-to<span class="token operator">=</span>origin/master master // 将远程仓库origin的master分支与本地仓库master分支关联 
加 
<span class="token function">git</span> push origin master
</code></pre> 
<p><strong>说明2：</strong><br> 在我们push前，应该让本地仓库和https://github.com/usernameA/repository保持同步，而不是和https://github.com/mynameA/repository保持同步，执行下面命令：</p> 
<pre><code class="prism language-bash"><span class="token function">git</span> remote <span class="token function">add</span> remoteA https://github.com/usernameA/repository <span class="token comment">#　将远程库添加进来，命名为remoteA</span>
<span class="token function">git</span> fetch remoteA   <span class="token comment">#　获取远程库中的最新更改</span>
<span class="token function">git</span> merge remoteA/master <span class="token comment"># 合并远程的最新代码到本分支</span>
</code></pre> 
<p>git pull remoteA/master:feature # 合并仓库remoteA中的master到本地仓库的feature分支中<br> git pull = git fetch 和 git merge<br> 命令格式如下：<br> git pull &lt;远程主机名&gt; &lt;远程分支名&gt;:&lt;本地分支名&gt;</p> 
<p>参考：<a href="https://blog.csdn.net/dwx_top/article/details/119574394">pull request</a><br> <a href="https://www.bilibili.com/video/BV1s3411g7PS">git、github 保姆级教程入门，工作和协作必备技术，github提交pr - pull request</a></p>
                