原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522405.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h2><a id="1_Virtualenv_0"></a>1. Virtualenv创建虚拟环境</h2> 
<h3><a id="11_1"></a>1.1创建环境:</h3> 
<pre><code>sudo apt install python3-virtualenv    	# 安装 virtualenv 
virtualenv -p /usr/bin/python3.5 myVENV 
</code></pre> 
<ul><li>/usr/bin/python3.5：是python语言版本的路径。在window下python语言版本的路径要加上后缀exe，如E:\studySoftware\python39\python.exe</li><li>myVENV：是虚拟环境的名称。</li></ul> 
<h3><a id="12__8"></a>1.2 激活环境：</h3> 
<pre><code>myVENV\Scripts\activate  			# windows下激活
source myVENV\bin\activate		# linux下激活			
</code></pre> 
<p>然后我们可以看到命令行多了一个前缀“myVENV”，如下图所示：<br> <img src="https://img-blog.csdnimg.cn/64c5f9d84875421da4c4447735150068.png" alt="在这里插入图片描述"><br> 此后我们执行pip install xx等操作都只是对我们建立的虚拟环境产生影响。</p> 
<h2><a id="2_conda_16"></a>2. conda创建虚拟环境</h2> 
<p>参考视频：https://www.bilibili.com/video/av74281036/<br> 打开anaconda Prompt</p> 
<pre><code>conda create -n pytorch python=3.6 # 创建名为pytorch的虚拟环境
conda activate pytorch # 激活环境
conda remove -n pytorch --all # 移除环境
</code></pre> 
<p>激活以后前缀改变了：<br> <img src="https://img-blog.csdnimg.cn/img_convert/32ebb7934d2417d1c77d20aaa14b63f8.png" alt="image-20210506085306549"><br> 以上安装的环境会出现在anaconda安装目录的envs目录下：<br> <img src="https://img-blog.csdnimg.cn/img_convert/c75ffcaf50454d0d41799e9c008fe084.png" alt="image-20210506091818386"></p>
                