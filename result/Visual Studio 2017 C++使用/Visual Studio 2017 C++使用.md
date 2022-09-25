原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522349.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>参考：<a href="https://www.bilibili.com/video/BV1zs411u7vp?spm_id_from=333.999.0.0">链接</a><br> <a href="https://www.bilibili.com/video/BV1Cs411A7Mi?spm_id_from=333.999.0.0">链接</a><br> 本博客是以上两个视频的笔记</p> 
<h2><a id="1_3"></a>1.安装</h2> 
<p>只选下面这个就可以<br> <img src="https://img-blog.csdnimg.cn/5dc6df210b5647da93dcc7df516ec5ca.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 安装详情,自行百度</p> 
<h2><a id="2__7"></a>2 项目建立流程</h2> 
<h3><a id="21__8"></a>2.1 新建项目</h3> 
<p><img src="https://img-blog.csdnimg.cn/91c38ffaafae425ba527daa22c1d5fa4.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 我们将项目名称设为Test，解决方案名称设为Code。一个解决方案中可以建立多个项目。每一个项目都可以转化成一个exe或dll文件。<br> 点击确定以后出现下图窗口：<br> <img src="https://img-blog.csdnimg.cn/ef761cc3db7446b592e980ab2e71ccd9.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_14,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 点击确定以后就成功建立了项目。<br> 在视图菜单下可以找到解决方案资源管理器，通过解决方案资源管理器可以看到解决方案下的项目文件，如下图所示：<img src="https://img-blog.csdnimg.cn/ef814977c5944e07b71227720393a455.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 右击“源文件”可添加cpp文件。</p> 
<h3><a id="22_SDL_16"></a>2.2 安全开发生命周期（SDL）检查</h3> 
<p>为了项目开发更加的安全，用VS开发C++程序默认进行安全开发生命周期（SDL）检查，这就会有一些以前常用的东西报错，如下面代码就会报错：</p> 
<pre><code class="prism language-cpp"><span class="token macro property">#<span class="token directive keyword">include</span><span class="token string">&lt;stdio.h&gt;</span></span>

<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>
	<span class="token keyword">int</span> m<span class="token punctuation">;</span>
	<span class="token function">scanf</span><span class="token punctuation">(</span><span class="token string">"%d"</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>m<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>编译（生成目录下面有一个编译按钮）一下，出现如下错误：</p> 
<pre><code class="prism language-bash">This <span class="token keyword">function</span> or variable may be unsafe. Consider using scanf_s instead. 
To disable deprecation, use _CRT_SECURE_NO_WARNINGS.
See online <span class="token function">help</span> <span class="token keyword">for</span> details.
</code></pre> 
<p>通过上面那串英文，我们可以得出以下两种解决方案：</p> 
<pre><code class="prism language-cpp"><span class="token comment">// 修改scanf为scanf_s。scanf_s才遵循SDL，更安全。</span>
<span class="token macro property">#<span class="token directive keyword">include</span><span class="token string">&lt;stdio.h&gt;</span></span>

<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>
	<span class="token keyword">int</span> m<span class="token punctuation">;</span>
	<span class="token function">scanf</span><span class="token punctuation">(</span><span class="token string">"%d"</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>m<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>或</p> 
<pre><code class="prism language-cpp"><span class="token comment">// 定义一个宏_CRT_SECURE_NO_WARNINGS。此宏的意思是说本cpp文件不进行SDL检查，请不要再报错了</span>
<span class="token macro property">#<span class="token directive keyword">define</span> _CRT_SECURE_NO_WARNINGS</span>
<span class="token macro property">#<span class="token directive keyword">include</span><span class="token string">&lt;stdio.h&gt;</span></span>

<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>
	<span class="token keyword">int</span> m<span class="token punctuation">;</span>
	<span class="token function">scanf</span><span class="token punctuation">(</span><span class="token string">"%d"</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>m<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>如果这个宏要在项目的很多文件中使用，一般会将宏定义在项目中，从而防止宏的重定义。定义过程如下：<br> <img src="https://img-blog.csdnimg.cn/a452338869c74a439b2570a4007bfaf2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 右击项目Test，选择属性。<br> 在配置上选择当前活动的项目。<br> 然后按照上图点击编辑，然后将宏_CRT_SECURE_NO_WARNINGS复制上去，结果如下所示，然后点击确定。<br> <img src="https://img-blog.csdnimg.cn/7dc3366724cb44f493860ddd2f68743b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 关闭SDL检查的方法是：项目-&gt;属性-&gt;C/C+±&gt;SDL检查，选测否，就可以将其关闭了</p> 
<h2><a id="3__66"></a>3 其他</h2> 
<h3><a id="31_VS_67"></a>3.1 帮助文档与重新选择需要下载的VS组件</h3> 
<p>点击相应函数，再点击F1就可跳转到此函数的帮助文档中了。这个文档是通过浏览器打开的，如果需要下载帮助文档的组件，过程如下：<br> 右击VS2017，点击更改<br> <img src="https://img-blog.csdnimg.cn/56585b35c3254a07b80bfc10fde70344.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 单个组件下勾选Help Viewer，然后点击修改<br> <img src="https://img-blog.csdnimg.cn/deefd48981bf4f3497c4581caa0f6ef8.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"></p> 
<p><img src="https://img-blog.csdnimg.cn/8cbc2b0ddbab4edba8dc33530dee5820.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 然后出现：<br> <img src="https://img-blog.csdnimg.cn/92a303745e9242c8b0c302ad97d887d3.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 点击添加，添加成功后，点击更新<br> 然后就可以在如下地方搜索函数的使用方法<br> <img src="https://img-blog.csdnimg.cn/3648a18742774732ac8e3d1e4da9686b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"></p> 
<h3><a id="32__80"></a>3.2 解决方案中的多个项目</h3> 
<p>右击项目，选择设为启动项，就可以调试和运行相应的项目，如下图所示<br> <img src="https://img-blog.csdnimg.cn/a9c345727c2e4eeb98ba21b371f8d151.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_11,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"></p> 
<h3><a id="33__84"></a>3.3 解决方案的目录结构</h3> 
<p><img src="https://img-blog.csdnimg.cn/d00b2cbec64940e7b3eb4f971b97a326.png" alt="在这里插入图片描述"><br> .vs：存放一些缓存内容<br> Debug：存放Debug和x86下的exe等文件（下面有介绍）<br> Test和Test2是两个项目文件，项目文件的目录结构如下：<br> <img src="https://img-blog.csdnimg.cn/f670edb3a45e442dbfbc84f446103ff3.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_17,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 可以看到，除了cpp文件和头文件，还有一些vs创建的与项目相关的文件。其中Debug和Release是编译时候的中间文件，即编译时产生的obj【注：C++是先将cpp文件编译乘obj文件，再将obj文件链接成exe文件】<br> 项目中的中间文件Debug和Release、解决方案里面的Debug和Release，还有.vs文件都是可以删除的，将这些文件删除以后再发给别人，别人还是可以成功运行这个程序的。<br> exe文件的生成：点击生成解决方案可生成.exe文件，生成解决方案是可以通过如下选项进行选择的：<br> <img src="https://img-blog.csdnimg.cn/b227138302ae42d2a87a921bfa554f99.png" alt="在这里插入图片描述"><br> 可以选择Debug、Release和x86、x64。如果选择的是Debug和x86，那么就会在解决方案的目录下的Debug目录中生成exe等文件。如果选择的是Release和x86，那么就会在解决方案的目录下生成一个名为Release的文件夹用于存放exe等文件。<br> 如果选择的是x64，那么就会在解决方案的目录下生成一个名为x64的文件夹用于存放Debug和Release。<br> 这里的x86和x64应该是代表此exe文件可以在哪个种系统中运行。<br> vs中的程序有debug和release两个版本，程序员可以对Debug版进行调试，Release版是给用户使用的，用户一般不在发布版本上进行调试。debug程序通常比release程序要慢，尤其是处理视频方便release要比debug快很多。<br> debug跟release在初始化变量时所做的操作是不同的，debug是将每个字节位都赋成0xcc， 而release的赋值近似于随机。如果你的程序中的某个变量没被初始化就被引用，就很有可能出现异常：用作控制变量将导致流程导向不一致；用作数组下标将会使程序崩溃；更加可能是造成其他变量的不准确而引起其他的错误。所以在<strong>声明变量后马上对其初始化一个默认的值是最简单有效的办法</strong>，否则项目大了你找都没地方找。代码存在错误在debug方式下可能会忽略而不被察觉到。debug方式下数组越界也大多不会出错，在release中就暴露出来了，这个找起来就比较难了。【参考<a href="https://blog.csdn.net/gxiaob/article/details/9045085">链接</a>】</p> 
<h3><a id="34_Win32Win32_100"></a>3.4 Win32控制台（控制台应用）与Win32项目（桌面应用程序）</h3> 
<p><img src="https://img-blog.csdnimg.cn/17288b5027244e12bc03878d7c567f10.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> Win32控制台（控制台应用）是一个只有输入输出的黑框框<br> Win32项目（桌面应用程序）是可以添加按钮等控件的程序</p> 
<h3><a id="35__exe_104"></a>3.5 发布exe文件</h3> 
<p>直接发送解决方案目录中的Release文件夹下的exe文件给别人，则会因为别人电脑里没有相应的运行库而无法成功运行程序。解决方法如下：<br> 方法一：将项目的运行库修改为“多线程(/MT)”。<br> <img src="https://img-blog.csdnimg.cn/16c9af9ecf3742d799bd24b9eaa7b5b6.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 此时生成的Release版的exe文件中是包含运行库的<br> 方法二：让想要运行你的程序的人安装相应的运行库，运行库的名字一般为Visual C++ Redistributable for Visual Studio 20xx。可以在<a href="https://visualstudio.microsoft.com/zh-hans/downloads/">链接</a>中找到。这个运行库可以在你没有安装Visual Studio 20xx的条件下，运行用Visual Studio 20xx编写的exe文件。<br> <img src="https://img-blog.csdnimg.cn/ca0997d96ca24c63879fa889e61c428a.png" alt="在这里插入图片描述"></p> 
<p>上面的发布方法不适用于MFC程序。MFC：利用微软提供的C++组件类创建界面</p> 
<h3><a id="36__113"></a>3.6 调试</h3> 
<p>请选择Debug模式下进行调试<br> <img src="https://img-blog.csdnimg.cn/bf0018dd88764c54982490f45b2f1abb.png" alt="在这里插入图片描述"><br> 调试下的开始调试和本地Windows调试器是一个东西<br> 逐语句：一条语句一条语句执行， 会进入函数<br> 逐过程：不会进入函数<br> 断点：程序执行到断点会暂停，点击继续后会执行到下一个断点<br> 条件断点：点击下图的螺丝，就可以设置条件断点。<br> <img src="https://img-blog.csdnimg.cn/3be8cff73163482bb9f0bbc99a2d48e5.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_12,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 下面设置条件断点：当a等于10000时程序暂停<br> <img src="https://img-blog.csdnimg.cn/5b7dc34aa16a42768633e35ba93af19c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_14,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 在调试目录下还有很多用于调试的功能，如调用堆栈和监视<br> <img src="https://img-blog.csdnimg.cn/a09a52852abb4616ac498ee01bbe79ee.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 在调用堆栈中，我们可以查看被调用函数的相关信息，如下：</p> 
<p><img src="https://img-blog.csdnimg.cn/c3edb38d8349499fa95f2ca96fe7be3b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_12,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 在监视中，我们可以输入想要查询的变量，从而得到该变量此时的值为多少。下图查询a此时的值为10<br> <img src="https://img-blog.csdnimg.cn/104a097da0f242598339f25df6208a36.png" alt="在这里插入图片描述"></p> 
<h3><a id="37__131"></a>3.7 代码分发方式</h3> 
<ol><li>源码：头文件+源文件</li><li>动态库：头文件(可选)+LIB文件(可选)+DLL 文件</li><li>静态库：头文件+LIB文件<br> <img src="https://img-blog.csdnimg.cn/5a5b8461e3fe4291af08150667f133f4.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> <img src="https://img-blog.csdnimg.cn/be946ea5423c48cdb8f8862fd20b39d7.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"></li></ol> 
<h4><a id="371_LIB_137"></a>3.7.1 静态库配置方法（头文件+LIB文件）</h4> 
<p>方法一：在代码的开头添加如下代码：</p> 
<pre><code class="prism language-cpp"><span class="token macro property">#<span class="token directive keyword">include</span><span class="token string">"头文件的绝对路径"</span></span>
<span class="token macro property">#<span class="token directive keyword">pragma</span> comment(lib, "lib文件的绝对路径")</span>
</code></pre> 
<p>方法二：在项目的属性里面配置，如下：<br> 配置头文件：<br> <img src="https://img-blog.csdnimg.cn/bb230e68a54f4e64a7c0d6d585de320a.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 将头文件所在目录放进附加包含目录中。注意不要把头文件都放进去。<br> 配置lib文件：<br> <img src="https://img-blog.csdnimg.cn/8ff6eda4e6644eda82e0792288bb6608.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 将lib文件所在目录放进附加包含目录中。注意不要把lib文件都放进去。然后在添加lib文件，如下：<br> <img src="https://img-blog.csdnimg.cn/540735cc8afb4142a6c7c84e5f375625.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 配置好了，以后下面有个确定是需要点的，不然配置不会保存<br> 配置的时候，注意下面两个要匹配好<br> <img src="https://img-blog.csdnimg.cn/5143d85c2347466f8a1198fbf6bd9619.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"></p> 
<h4><a id="372_LIBDLL__155"></a>3.7.2 动态库配置方法（头文件(可选)+LIB文件(可选)+DLL 文件）</h4> 
<p>头文件(可选)+LIB文件(可选) 和静态库配置方法一样，这里就不再赘述。<br> DLL文件的配置方法为：将DLL文件放在和exe文件同一个路径下就可以了</p> 
<h3><a id="38__159"></a>3.8 动态库的建立</h3> 
<p>参考：https://www.bilibili.com/video/BV1hE411Y7vd?spm_id_from=333.999.0.0，不想写了，心累。。。</p>
                