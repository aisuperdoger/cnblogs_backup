原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522387.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h1><a id="_0"></a>遇到的错误</h1> 
<p>在源码安装pytorch时，我的cuda的版本时11.4，所以按照官方的安装指南是需要magma-cuda114，而此时magma-cuda114还没发布。<br> 所以我的方法是<br> 卸载驱动、CUDA和CUDNN（具体自己百度）。然后选择对应cuda版本为11.3的显卡驱动，然后安装cuda11.3和相应的CUDNN。<br> 说明：显卡的驱动可以用较低版本的。</p> 
<h1><a id="1_6"></a>1.安装驱动</h1> 
<p>参考：https://www.mlzhilu.com/archives/ubuntu2004%E5%AE%89%E8%A3%85nvidia%E6%98%BE%E5%8D%A1%E9%A9%B1%E5%8A%A8</p> 
<h2><a id="11__8"></a>1.1 驱动下载</h2> 
<p>我需要安装cuda11.3，所以需要选择相应版本的驱动<br> 从<a href="https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html">这里</a>可以看到cuda和驱动之间的版本对应关系<br> 从<a href="https://www.nvidia.com/en-us/geforce/drivers/">这里</a>可以下载各种版本的驱动<br> 最好将下载完的驱动放在~目录下，别问为什么，听我的就对了</p> 
<h2><a id="12__13"></a>1.2 安装前的准备</h2> 
<p>1.安装lightdm</p> 
<pre><code>sudo apt-get update
sudo apt install -y lightdm
</code></pre> 
<p>弹出来一个选项，选择lightdm就行<br> 2.停止lightdm桌面服务</p> 
<pre><code>sudo service lightdm stop
</code></pre> 
<p>3.设置一下root账户密码</p> 
<pre><code>sudo passwd root
</code></pre> 
<p>然后输入密码<br> 4.首先查看你有没有安装gcc</p> 
<pre><code>gcc --version
</code></pre> 
<p>如果没有安装gcc一般make也没安装，这时需要安装一下gcc和make</p> 
<pre><code>sudo apt install gcc 
sudo apt install make
</code></pre> 
<p>5.删除自带驱动</p> 
<pre><code>sudo apt purge nvidia*
sudo apt-get autoremove
</code></pre> 
<p>6.禁用自带的nouveau nvidia驱动</p> 
<pre><code>sudo gedit /etc/modprobe.d/blacklist.conf 
</code></pre> 
<p>在最后添加如下内容</p> 
<pre><code>blacklist nouveau  
options nouveau modeset=0 
</code></pre> 
<p>然后保存退出。</p> 
<pre><code>sudo update-initramfs -u	# 更新
sudo reboot	# 重启
</code></pre> 
<p>重启之后显示是黑屏，此时按ctrl+alt+F1或ctrl+alt+F2,进入命令行，然后登录<br> 7.重启后查看是否已经将自带的驱动屏蔽了，输入以下代码</p> 
<pre><code>lsmod | grep nouveau
</code></pre> 
<p>没有结果输出，则表示屏蔽成功</p> 
<h2><a id="13__69"></a>1.3 安装驱动</h2> 
<p>cd到你下载的显卡驱动的目录<br> 执行：</p> 
<pre><code>sudo chmod a+x NVIDIA-Linux-x86_64-465.31.run
sudo ./NVIDIA-Linux-x86_64-465.31.run -no-x-check -no-nouveau-check -no-opengl-files
# -no-x-check:安装时关闭X服务
# -no-nouveau-check: 安装时禁用nouveau
# -no-opengl-files:只安装驱动文件，不安装OpenGL文件
</code></pre> 
<p>然后会弹出来一个窗口，根据提示进行操作<br> 最后重启，然后输入nvidia-smi会显示驱动和cuda的版本信息，说明驱动安装成功</p> 
<h1><a id="2_cuda_82"></a>2 安装cuda</h1> 
<p>参考：https://bbs.huaweicloud.com/blogs/detail/210271<br> 1.cuda下载安装<br> 从<a href="https://developer.nvidia.com/cuda-toolkit-archive">这里</a>下载对应版本的cuda，这里选择runfile(local)进行安装<br> <img src="https://img-blog.csdnimg.cn/9437586afce049779f6ec21f9003ba46.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 运行如下命令：</p> 
<pre><code>wget https://developer.download.nvidia.com/compute/cuda/11.3.1/local_installers/cuda_11.3.1_465.19.01_linux.run
sudo sh cuda_11.3.1_465.19.01_linux.run
</code></pre> 
<p>然后会弹出来一个窗口，按空格取消第一个选项，因为我们安装过驱动了，不要安装了。最后选择安装即可<br> 2.环境配置（两种方式）</p> 
<pre><code>修改home目录下的.bashrc文件（ 修改home目录下的.bashrc文件，只针对当前用户）

cd ~          # 切换回home目录
gedit .bashrc      # 修改.bashrc文件

# add cuda path    # 在文件末尾添加路径
export PATH="/usr/local/cuda-11.0/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-11.0/lib64:$LD_LIBRARY_PATH"  

:wq   # 退出保存
</code></pre> 
<pre><code>修改profile文件，针对所有用户

sudo vim /etc/profile    # 修改/etc/profile文件

# add cuda path  # 文件末尾增加以下两行代码
export PATH="/usr/local/cuda-11.0/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-11.0/lib64:$LD_LIBRARY_PATH" 

:wq   # 退出保存
</code></pre> 
<p>目录注意改成自己的</p> 
<pre><code>立即生效（或重启服务器生效）

source .bashrc   
 
或

source /etc/profile
</code></pre> 
<p>3.验证安装成功 nvcc -V (注意 是大V)，结果如下<br> <img src="https://img-blog.csdnimg.cn/fd623c6031f445faac8034c980f50680.png" alt="在这里插入图片描述"></p> 
<h1><a id="3_cudnn_133"></a>3. cudnn安装</h1> 
<p>下载cudnn：https://developer.nvidia.com/zh-cn/cudnn<br> 在链接中选择“Library for Linux”<br> 然后执行以下命令</p> 
<pre><code>sudo cp cuda/include/cudnn*.h    /usr/local/cuda/include      注意，解压后的文件夹名称为cuda ,将对应文件复制到 /usr/local中的cuda内
sudo cp cuda/lib64/libcudnn*    /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h   /usr/local/cuda/lib64/libcudnn*

</code></pre> 
<p>判断是否安装成功：</p> 
<pre><code>cat /usr/local/cuda-11.3/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
</code></pre> 
<p>如果没有反应就说明安装失败</p> 
<h1><a id="4pytorch_149"></a>4.源码安装pytorch</h1> 
<p>直接参考pytorch.org中的源码安装就行</p>
                