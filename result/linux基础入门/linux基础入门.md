原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522369.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h3><a id="1_0"></a>1.文件和目录管理</h3> 
<pre><code class="prism language-cpp">创建：mkdir
删除：rm
删除非空目录：rm <span class="token operator">-</span>rf file目录
删除日志 rm <span class="token operator">*</span>log <span class="token punctuation">(</span>等价<span class="token operator">:</span> $find <span class="token punctuation">.</span><span class="token operator">/</span> <span class="token operator">-</span>name “<span class="token operator">*</span>log” <span class="token operator">-</span>exec rm <span class="token punctuation">{<!-- --></span><span class="token punctuation">}</span> <span class="token punctuation">;</span><span class="token punctuation">)</span>
移动：mv
复制：cp source_dir  dest_dir <span class="token punctuation">(</span>复制目录：cp <span class="token operator">-</span>r source_dir  dest_dir<span class="token punctuation">)</span>
显示当前路径<span class="token operator">:</span> pwd
</code></pre> 
<h3><a id="2_11"></a>2.性能监控</h3> 
<pre><code class="prism language-cpp">$ps <span class="token operator">-</span>ef	 # 查询正在运行的进程信息，常与grep结合使用，如：
$ps <span class="token operator">-</span>ef <span class="token operator">|</span> grep colin115  # 查询归属于用户colin115的进程
$pgrep <span class="token operator">-</span>l re  # 查询进程名中含有re的进程
$kill PID	# 杀死进程
</code></pre> 
<pre><code class="prism language-cpp">$top	# 显示进程信息，并实时更新。输入以下内容得到相应结果：
i：使top不显示任何闲置或者僵死进程。
P：根据CPU使用百分比大小进行排序。
M：根据驻留内存大小进行排序。
</code></pre> 
<h3><a id="3_24"></a>3.网络工具</h3> 
<p>netstat</p> 
<pre><code class="prism language-cpp">netstat <span class="token operator">-</span>a		# 列出所有端口
netstat <span class="token operator">-</span>at		# 列出所有 tcp 端口
netstat <span class="token operator">-</span>l		# 列出所有有监听的服务状态
$netstat <span class="token operator">-</span>antp <span class="token operator">|</span> grep <span class="token number">6379</span>	# 查看<span class="token number">6379</span>端口情况
</code></pre> 
<h3><a id="4_33"></a>4.用户与组</h3> 
<pre><code class="prism language-cpp">$useradd <span class="token operator">-</span>m username # 创建了<span class="token operator">/</span>home<span class="token operator">/</span>username目录和相应用户
$passwd username	 # 给用户设置密码
$userdel <span class="token operator">-</span>r username # 删除用户并且删除<span class="token operator">/</span>home<span class="token operator">/</span>username目录
$su userB 			 # 切换用户
$groups				 # 查看用户所在组
$usermod <span class="token operator">-</span>G groupNmame username # 一个用户可以属于多个组，将用户加入到组
$usermod <span class="token operator">-</span>g groupName username  # 变更用户所属的根组<span class="token punctuation">(</span>将用加入到新的组，并从原有的组中除去）
</code></pre> 
<h3><a id="5_43"></a>5.文件访问权限</h3> 
<h5><a id="51_44"></a>5.1查看权限</h5> 
<p>使用ls -l可查看文件的属性字段，文件属性字段总共有10个字母组成，第一个字母表示文件类型，如果这个字母是一个减号”-”,则说明该文件是一个普通文件。字母”d”表示该文件是一个目录，字母”d”,是dirtectory(目录)的缩写。 后面的9个字母为该文件的权限标识，3个为一组，分别表示文件所属用户、用户所在组、其它用户的读写和执行权限；</p> 
<pre><code class="prism language-cpp">ls <span class="token operator">-</span>l 文件<span class="token operator">/</span>目录		# 查看文件的权限，如
<span class="token punctuation">[</span><span class="token operator">/</span>home<span class="token operator">/</span>weber#<span class="token punctuation">]</span>ls <span class="token operator">-</span>l <span class="token operator">/</span>etc<span class="token operator">/</span>group
<span class="token operator">-</span>rwxrw<span class="token operator">-</span>r<span class="token operator">--</span> colin king <span class="token number">725</span> <span class="token number">2013</span><span class="token operator">-</span><span class="token number">11</span><span class="token operator">-</span><span class="token number">12</span> <span class="token number">15</span><span class="token operator">:</span><span class="token number">37</span> <span class="token operator">/</span>home<span class="token operator">/</span>colin<span class="token operator">/</span>a
</code></pre> 
<p>表示这个文件对文件拥有者colin这个用户可读写、可执行；对colin所在的组（king）可读可写；对其它用户只可读；</p> 
<h4><a id="52_53"></a>5.2修改文件权限</h4> 
<pre><code class="prism language-cpp">字母法：
$chmod <span class="token function">userMark</span><span class="token punctuation">(</span><span class="token operator">+</span><span class="token operator">|</span><span class="token operator">-</span><span class="token punctuation">)</span>PermissionsMark
userMark取值：
u：用户
g：组
o：其它用户
a：所有用户
PermissionsMark取值：
r<span class="token operator">:</span>读
w：写
x：执行
如：
$chmod a<span class="token operator">+</span>x main         对所有用户给文件main增加可执行权限
$chmod g<span class="token operator">+</span>w blogs        对组用户给文件blogs增加可写权限
数字法：
使用三个数表示权限，第一位指定文件拥有者的权限，第二位指定组权限，
第三位指定其他用户的权限，每位通过<span class="token function">4</span><span class="token punctuation">(</span>读<span class="token punctuation">)</span>、<span class="token function">2</span><span class="token punctuation">(</span>写<span class="token punctuation">)</span>、<span class="token function">1</span><span class="token punctuation">(</span>执行<span class="token punctuation">)</span>三种数值的和来确定权限。
如<span class="token function">6</span><span class="token punctuation">(</span><span class="token number">4</span><span class="token operator">+</span><span class="token number">2</span><span class="token punctuation">)</span>代表有读写权，<span class="token function">7</span><span class="token punctuation">(</span><span class="token number">4</span><span class="token operator">+</span><span class="token number">2</span><span class="token operator">+</span><span class="token number">1</span><span class="token punctuation">)</span>有读、写和执行的权限。如：
$chmod <span class="token number">740</span> main     将main的用户权限设置为rwxr<span class="token operator">--</span><span class="token operator">--</span><span class="token operator">-</span>

更改文件或目录的拥有者：
$chown username 文件或目录
$chown <span class="token operator">-</span>R weber server<span class="token operator">/</span>  # 将server目录下的所有文件的拥有者都变为weber
</code></pre> 
<h3><a id="ubuntu_79"></a>ubuntu目录结构</h3> 
<p>1、/：目录属于根目录，是所有目录的绝对路径的起始点，Ubuntu 中的所有文件和目录都在跟目录下。<br> 2、/etc（存放配置文件）：绝大多数系统和相关服务的配置文件都保存在这里，这个目录的内容一般只能由管理员进行修改。像密码文件、设置网卡信息、环境变量的设置等都在此目录中。此目录的 rcn.d 目录中存放不同启动级别所启动的服务，network 目录放置网卡的配置信息等。<br> 3、/home（每个用户都在这个目录下建立一个目录）：系统默认的用户家目录，新增用户账号时，用户的家目录都存放在此目录下，~表示当前用户的家目录，~test表示用户test的家目录。建议单独分区，并设置较大的磁盘空间，方便用户存放数据<br> 4、/bin :此目录中放置了所有用户能够执行的命令。<br> 5、/sbin：此目录中放置了一般是只有系统管理有才能执行的命令。<br> 6、/dev：存放linux系统下的设备文件，<strong>访问该目录下某个文件，相当于访问某个设备</strong>，常用的是挂载光驱mount /dev/cdrom /mnt。<br> 7、/mnt：此目录主要是作为挂载点使用。（不是很明白？？）<br> 8、/usr：此目录包含了所有的命令、说明文件、程序库等，此目录下有很多重要的目录，常见的有：/usr/local 这个目录包含管理员自己安装的程序；/usr/share 包含文件的帮助文件；/usr/bin 和/usr/sbin 包含了所有的命令（这里应该指的是非root用户可以使用的命令）。<br> 9、/var：包含了日志文件、计划性任务和邮件等内容。<br> 10、/lib：包含了系统的函数库文件。<br> 11、/lost+found：包含了系统修复时的回复文件。<br> 12、/tmp：包含了临时的文件。一般用户或正在执行的程序临时存放文件的目录,任何人都可以访问,重要数据不可放置在此目录下<br> 13、/boot：系统的内核所在地，也是启动分区。<strong>放置linux系统启动时用到的一些文件</strong>。/boot/vmlinuz为linux的内核文件，以及/boot/gurb。建议单独分区，分区大小100M即可<br> 14、/media：主要用于挂载多媒体设备。（应该是指在此建立对应设备的相应文件）<br> 15、/root：系统管理员的宿主目录。<br> 参考：<a href="https://www.cnblogs.com/hf8051/p/5074903.html#:~:text=ubuntu%20--%20%E7%B3%BB%E7%BB%9F%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84,1%E3%80%81/%EF%BC%9A%E7%9B%AE%E5%BD%95%E5%B1%9E%E4%BA%8E%E6%A0%B9%E7%9B%AE%E5%BD%95%EF%BC%8C%E6%98%AF%E6%89%80%E6%9C%89%E7%9B%AE%E5%BD%95%E7%9A%84%E7%BB%9D%E5%AF%B9%E8%B7%AF%E5%BE%84%E7%9A%84%E8%B5%B7%E5%A7%8B%E7%82%B9%EF%BC%8CUbuntu%20%E4%B8%AD%E7%9A%84%E6%89%80%E6%9C%89%E6%96%87%E4%BB%B6%E5%92%8C%E7%9B%AE%E5%BD%95%E9%83%BD%E5%9C%A8%E8%B7%9F%E7%9B%AE%E5%BD%95%E4%B8%8B%E3%80%82%202%E3%80%81/etc%EF%BC%9A%E6%AD%A4%E7%9B%AE%E5%BD%95%E9%9D%9E%E5%B8%B8%E9%87%8D%E8%A6%81%EF%BC%8C%E7%BB%9D%E5%A4%A7%E5%A4%9A%E6%95%B0%E7%B3%BB%E7%BB%9F%E5%92%8C%E7%9B%B8%E5%85%B3%E6%9C%8D%E5%8A%A1%E7%9A%84%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E9%83%BD%E4%BF%9D%E5%AD%98%E5%9C%A8%E8%BF%99%E9%87%8C%EF%BC%8C%E8%BF%99%E4%B8%AA%E7%9B%AE%E5%BD%95%E7%9A%84%E5%86%85%E5%AE%B9%E4%B8%80%E8%88%AC%E5%8F%AA%E8%83%BD%E7%94%B1%E7%AE%A1%E7%90%86%E5%91%98%E8%BF%9B%E8%A1%8C%E4%BF%AE%E6%94%B9%E3%80%82%20">链接</a></p> 
<h3><a id="7_96"></a>7.其他</h3> 
<pre><code class="prism language-cpp">sudo passwd root 	# Ubuntu创建root用户
$uname <span class="token operator">-</span>a 			# 查看系统版本
$lsb_release <span class="token operator">-</span>a 	# 查看系统版本，排列整齐地显示
wget url	# 下载文件
Ctl<span class="token operator">-</span>U   删除光标到行首的所有字符
Ctl<span class="token operator">-</span>W   删除当前光标到前边的最近一个空格之间的字符
</code></pre> 
<p>参考：<a href="https://linuxtools-rst.readthedocs.io/zh_CN/latest/index.html">链接</a></p>
                