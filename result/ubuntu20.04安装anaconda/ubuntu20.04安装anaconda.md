原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522389.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>1.下载anaconda：https://www.anaconda.com/products/individual#linux<br> 2.使用以下命令安装</p> 
<pre><code>bash Anaconda3-5.3.1-Linux-x86_64.sh
</code></pre> 
<p>一路yes就行。<br> 在~/.bashrc中添加</p> 
<pre><code>export PATH=/home/usrname/anaconda3/bin:$PATH
</code></pre> 
<p>然后输入以下命令</p> 
<pre><code>source ~/.bashrc
</code></pre> 
<p>3.判断是否安装成功</p> 
<pre><code>conda info		
</code></pre> 
<p>4.激活anaconda，出现base前缀。想要去掉(base)，参考这个连接https://blog.csdn.net/Just_youHG/article/details/104686642#commentBox</p>
                