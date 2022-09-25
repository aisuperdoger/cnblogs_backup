原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522383.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>参考<a href="https://www.cnblogs.com/leiben/archive/2012/06/05/2536508.html">链接</a></p> 
<h2><a id="OpenCL_1"></a>一、OpenCL中的一些函数</h2> 
<p>OpenCL的Kernel相当于CUDA的device<br> OpenCL的Work-item相当于CUDA的thread<br> OpenCL的Work-group相当于CUDA的block<br> OpenCL的ND-Range相当于CUDA的grid</p> 
<p>get_global_id(dim) ：CUDA中需要计算线程的id，而在opencl中线程id直接通过这个函数直接获取<br> get_global_size(dim)：线程总数量</p> 
<p>get_group_id(dim)：dim可以为0，1，2，分别代表CUDA中的blockIdx.x、blockIdx.y、blockIdx.z<br> get_num_groups(dim)：<br> get_local_id(dim)：dim可以为0，1，2，分别代表CUDA中的threadIdx.x、threadIdx.y、threadIdx.z<br> get_local_size(dim)</p> 
<h2><a id="_15"></a>二、内存模型：</h2> 
<p><img src="https://img-blog.csdnimg.cn/f5a2b0f0294e4634aad616efa9a6b9d8.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_9,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 箭头表示可以访问。所有的workItem都可以读Global Memory的数据。我们在利用opencl写并行函数的时候，可以看到函数的形参是类似这样定义的：__global int *C，这就代表C所指向的地方是Global Memory。</p> 
<h2><a id="opencl_18"></a>三、opencl编程实践</h2> 
<p>opencl需要包含头文件：#include&lt;CL/cl.h&gt;<br> 这里新建一个Vadd.cl文件，用于保存__kernel函数的相关代码。然后在testOpenCL.cpp中建立环境和调用Vadd.cl文件中的__kernel函数。<br> 实现矩阵乘法（参考：<a href="https://blog.csdn.net/c602273091/article/details/45418129">矩阵乘法</a>）：<br> Vadd.cl中代码如下：</p> 
<pre><code class="prism language-cpp">__kernel <span class="token keyword">void</span> <span class="token function">matrix_mult</span><span class="token punctuation">(</span>
	<span class="token keyword">const</span> <span class="token keyword">int</span> Ndim<span class="token punctuation">,</span>
	<span class="token keyword">const</span> <span class="token keyword">int</span> Mdim<span class="token punctuation">,</span>
	<span class="token keyword">const</span> <span class="token keyword">int</span> Pdim<span class="token punctuation">,</span>
	__global <span class="token keyword">const</span> <span class="token keyword">float</span><span class="token operator">*</span> A<span class="token punctuation">,</span>
	__global <span class="token keyword">const</span> <span class="token keyword">float</span><span class="token operator">*</span> B<span class="token punctuation">,</span>
	__global <span class="token keyword">float</span><span class="token operator">*</span> C<span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
	<span class="token keyword">int</span> i <span class="token operator">=</span> <span class="token function">get_global_id</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">int</span> j <span class="token operator">=</span> <span class="token function">get_global_id</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">int</span> k<span class="token punctuation">;</span>
	<span class="token keyword">float</span> tmp<span class="token punctuation">;</span>

	<span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token punctuation">(</span>i <span class="token operator">&lt;</span> Ndim<span class="token punctuation">)</span> <span class="token operator">&amp;&amp;</span> <span class="token punctuation">(</span>j <span class="token operator">&lt;</span> Mdim<span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>
		tmp <span class="token operator">=</span> <span class="token number">0.0</span><span class="token punctuation">;</span>
		<span class="token keyword">for</span> <span class="token punctuation">(</span>k <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> k <span class="token operator">&lt;</span> Pdim<span class="token punctuation">;</span> k<span class="token operator">++</span><span class="token punctuation">)</span>
			tmp <span class="token operator">+=</span> A<span class="token punctuation">[</span>i<span class="token operator">*</span>Pdim <span class="token operator">+</span> k<span class="token punctuation">]</span> <span class="token operator">*</span> B<span class="token punctuation">[</span>k<span class="token operator">*</span>Mdim <span class="token operator">+</span> j<span class="token punctuation">]</span><span class="token punctuation">;</span>
		C<span class="token punctuation">[</span>i<span class="token operator">*</span>Mdim <span class="token operator">+</span> j<span class="token punctuation">]</span> <span class="token operator">=</span> tmp<span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre> 
<p>testOpenCL.cpp中代码如下：</p> 
<pre><code class="prism language-cpp"><span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;CL/cl.h&gt;</span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;stdio.h&gt;</span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;stdlib.h&gt;</span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;time.h&gt;</span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;iostream&gt;</span></span>
<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">include</span> <span class="token string">&lt;fstream&gt;</span></span>

<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">define</span> <span class="token macro-name">NWITEMS</span> <span class="token expression"><span class="token number">6</span></span></span>

<span class="token macro property"><span class="token directive-hash">#</span><span class="token directive keyword">pragma</span> <span class="token expression"><span class="token function">comment</span> <span class="token punctuation">(</span>lib<span class="token punctuation">,</span></span><span class="token string">"OpenCL.lib"</span><span class="token expression"><span class="token punctuation">)</span></span></span>

<span class="token comment">//把文本文件读入一个 string 中</span>
<span class="token keyword">int</span> <span class="token function">convertToString</span><span class="token punctuation">(</span><span class="token keyword">const</span> <span class="token keyword">char</span> <span class="token operator">*</span>filename<span class="token punctuation">,</span> std<span class="token operator">::</span>string<span class="token operator">&amp;</span> s<span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
	size_t size<span class="token punctuation">;</span>
	<span class="token keyword">char</span><span class="token operator">*</span> str<span class="token punctuation">;</span>
	std<span class="token operator">::</span>fstream <span class="token function">f</span><span class="token punctuation">(</span>filename<span class="token punctuation">,</span> <span class="token punctuation">(</span>std<span class="token operator">::</span>fstream<span class="token operator">::</span>in <span class="token operator">|</span> std<span class="token operator">::</span>fstream<span class="token operator">::</span>binary<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>f<span class="token punctuation">.</span><span class="token function">is_open</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
	<span class="token punctuation">{<!-- --></span>
		size_t fileSize<span class="token punctuation">;</span>
		f<span class="token punctuation">.</span><span class="token function">seekg</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> std<span class="token operator">::</span>fstream<span class="token operator">::</span>end<span class="token punctuation">)</span><span class="token punctuation">;</span>
		size <span class="token operator">=</span> fileSize <span class="token operator">=</span> <span class="token punctuation">(</span>size_t<span class="token punctuation">)</span>f<span class="token punctuation">.</span><span class="token function">tellg</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
		f<span class="token punctuation">.</span><span class="token function">seekg</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> std<span class="token operator">::</span>fstream<span class="token operator">::</span>beg<span class="token punctuation">)</span><span class="token punctuation">;</span>
		str <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token keyword">char</span><span class="token punctuation">[</span>size <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
		<span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>str<span class="token punctuation">)</span>
		<span class="token punctuation">{<!-- --></span>
			f<span class="token punctuation">.</span><span class="token function">close</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
			<span class="token keyword">return</span> <span class="token constant">NULL</span><span class="token punctuation">;</span>
		<span class="token punctuation">}</span>
		f<span class="token punctuation">.</span><span class="token function">read</span><span class="token punctuation">(</span>str<span class="token punctuation">,</span> fileSize<span class="token punctuation">)</span><span class="token punctuation">;</span>
		f<span class="token punctuation">.</span><span class="token function">close</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
		str<span class="token punctuation">[</span>size<span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token string">'\0'</span><span class="token punctuation">;</span>
		s <span class="token operator">=</span> str<span class="token punctuation">;</span>
		<span class="token keyword">delete</span><span class="token punctuation">[</span><span class="token punctuation">]</span> str<span class="token punctuation">;</span>
		<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
	<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"Error: Failed to open file %s\n"</span><span class="token punctuation">,</span> filename<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> <span class="token number">1</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{<!-- --></span>
	cl_uint status<span class="token punctuation">;</span>
	cl_platform_id platform<span class="token punctuation">;</span>

	<span class="token comment">//创建平台对象</span>
	status <span class="token operator">=</span> <span class="token function">clGetPlatformIDs</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>platform<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	cl_device_id device<span class="token punctuation">;</span>
	<span class="token comment">//创建 GPU 设备</span>
	<span class="token function">clGetDeviceIDs</span><span class="token punctuation">(</span>platform<span class="token punctuation">,</span> CL_DEVICE_TYPE_GPU<span class="token punctuation">,</span>
		<span class="token number">1</span><span class="token punctuation">,</span>
		<span class="token operator">&amp;</span>device<span class="token punctuation">,</span>
		<span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token comment">//创建context</span>
	cl_context context <span class="token operator">=</span> <span class="token function">clCreateContext</span><span class="token punctuation">(</span><span class="token constant">NULL</span><span class="token punctuation">,</span>
		<span class="token number">1</span><span class="token punctuation">,</span>
		<span class="token operator">&amp;</span>device<span class="token punctuation">,</span>
		<span class="token constant">NULL</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token comment">//创建命令队列</span>
	cl_command_queue commandQueue <span class="token operator">=</span> <span class="token function">clCreateCommandQueue</span><span class="token punctuation">(</span>context<span class="token punctuation">,</span>
		device<span class="token punctuation">,</span>
		CL_QUEUE_PROFILING_ENABLE<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">if</span> <span class="token punctuation">(</span>commandQueue <span class="token operator">==</span> <span class="token constant">NULL</span><span class="token punctuation">)</span>
		<span class="token function">perror</span><span class="token punctuation">(</span><span class="token string">"Failed to create commandQueue for device 0."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">//建立要传入从机的数据</span>
	<span class="token comment">/********  创建内核和内存对象 ********/</span>

	<span class="token keyword">const</span> <span class="token keyword">int</span> Ndim <span class="token operator">=</span> <span class="token number">4</span><span class="token punctuation">;</span>
	<span class="token keyword">const</span> <span class="token keyword">int</span> Mdim <span class="token operator">=</span> <span class="token number">3</span><span class="token punctuation">;</span>
	<span class="token keyword">const</span> <span class="token keyword">int</span> Pdim <span class="token operator">=</span> <span class="token number">4</span><span class="token punctuation">;</span>
	<span class="token keyword">int</span> szA <span class="token operator">=</span> Ndim <span class="token operator">*</span> Pdim<span class="token punctuation">;</span>
	<span class="token keyword">int</span> szB <span class="token operator">=</span> Pdim <span class="token operator">*</span> Mdim<span class="token punctuation">;</span>
	<span class="token keyword">int</span> szC <span class="token operator">=</span> Ndim <span class="token operator">*</span> Mdim<span class="token punctuation">;</span>

	<span class="token keyword">float</span> <span class="token operator">*</span>A<span class="token punctuation">;</span>
	<span class="token keyword">float</span> <span class="token operator">*</span>B<span class="token punctuation">;</span>
	<span class="token keyword">float</span> <span class="token operator">*</span>C<span class="token punctuation">;</span>

	A <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token keyword">float</span> <span class="token operator">*</span><span class="token punctuation">)</span><span class="token function">malloc</span><span class="token punctuation">(</span>szA <span class="token operator">*</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	B <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token keyword">float</span> <span class="token operator">*</span><span class="token punctuation">)</span><span class="token function">malloc</span><span class="token punctuation">(</span>szB <span class="token operator">*</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	C <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token keyword">float</span> <span class="token operator">*</span><span class="token punctuation">)</span><span class="token function">malloc</span><span class="token punctuation">(</span>szC <span class="token operator">*</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">int</span> i<span class="token punctuation">,</span> j<span class="token punctuation">;</span>
	<span class="token keyword">for</span> <span class="token punctuation">(</span>i <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> i <span class="token operator">&lt;</span> szA<span class="token punctuation">;</span> i<span class="token operator">++</span><span class="token punctuation">)</span>
		A<span class="token punctuation">[</span>i<span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span>i <span class="token operator">+</span> <span class="token number">1.0</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">for</span> <span class="token punctuation">(</span>i <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> i <span class="token operator">&lt;</span> szB<span class="token punctuation">;</span> i<span class="token operator">++</span><span class="token punctuation">)</span>
		B<span class="token punctuation">[</span>i<span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span>i <span class="token operator">+</span> <span class="token number">1.0</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">//创建三个 OpenCL 内存对象，并把buf1 的内容通过隐式拷贝的方式</span>
	<span class="token comment">//拷贝到clbuf1, buf2 的内容通过显示拷贝的方式拷贝到clbuf2</span>
	cl_mem memObjects<span class="token punctuation">[</span><span class="token number">3</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">{<!-- --></span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">0</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
	memObjects<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token function">clCreateBuffer</span><span class="token punctuation">(</span>context<span class="token punctuation">,</span> CL_MEM_READ_ONLY <span class="token operator">|</span> CL_MEM_COPY_HOST_PTR<span class="token punctuation">,</span>
		<span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token operator">*</span> szA<span class="token punctuation">,</span> A<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	memObjects<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token function">clCreateBuffer</span><span class="token punctuation">(</span>context<span class="token punctuation">,</span> CL_MEM_READ_ONLY <span class="token operator">|</span> CL_MEM_COPY_HOST_PTR<span class="token punctuation">,</span>
		<span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token operator">*</span> szB<span class="token punctuation">,</span> B<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	memObjects<span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token function">clCreateBuffer</span><span class="token punctuation">(</span>context<span class="token punctuation">,</span> CL_MEM_READ_WRITE <span class="token operator">|</span> CL_MEM_COPY_HOST_PTR<span class="token punctuation">,</span>
		<span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token operator">*</span> szC<span class="token punctuation">,</span> C<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>memObjects<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span> <span class="token operator">==</span> <span class="token constant">NULL</span> <span class="token operator">||</span> memObjects<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span> <span class="token operator">==</span> <span class="token constant">NULL</span> <span class="token operator">||</span> memObjects<span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">]</span> <span class="token operator">==</span> <span class="token constant">NULL</span><span class="token punctuation">)</span>
		<span class="token function">perror</span><span class="token punctuation">(</span><span class="token string">"Error in clCreateBuffer.\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">const</span> <span class="token keyword">char</span> <span class="token operator">*</span> filename <span class="token operator">=</span> <span class="token string">"Vadd.cl"</span><span class="token punctuation">;</span>
	std<span class="token operator">::</span>string sourceStr<span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">convertToString</span><span class="token punctuation">(</span>filename<span class="token punctuation">,</span> sourceStr<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>status<span class="token punctuation">)</span>
		cout <span class="token operator">&lt;&lt;</span> status <span class="token operator">&lt;&lt;</span> <span class="token string">"  !!!!!!!!"</span> <span class="token operator">&lt;&lt;</span> endl<span class="token punctuation">;</span>
	<span class="token keyword">const</span> <span class="token keyword">char</span> <span class="token operator">*</span> source <span class="token operator">=</span> sourceStr<span class="token punctuation">.</span><span class="token function">c_str</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	size_t sourceSize<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">{<!-- --></span> <span class="token function">strlen</span><span class="token punctuation">(</span>source<span class="token punctuation">)</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
	<span class="token comment">//创建程序对象</span>
	cl_program program <span class="token operator">=</span> <span class="token function">clCreateProgramWithSource</span><span class="token punctuation">(</span>
		context<span class="token punctuation">,</span>
		<span class="token number">1</span><span class="token punctuation">,</span>
		<span class="token operator">&amp;</span>source<span class="token punctuation">,</span>
		sourceSize<span class="token punctuation">,</span>
		<span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token comment">//编译程序对象</span>
	status <span class="token operator">=</span> <span class="token function">clBuildProgram</span><span class="token punctuation">(</span>program<span class="token punctuation">,</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>device<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>status<span class="token punctuation">)</span>
		cout <span class="token operator">&lt;&lt;</span> status <span class="token operator">&lt;&lt;</span> <span class="token string">"  !!!!!!!!"</span> <span class="token operator">&lt;&lt;</span> endl<span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">!=</span> <span class="token number">0</span><span class="token punctuation">)</span>
	<span class="token punctuation">{<!-- --></span>
		<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"clBuild failed:%d\n"</span><span class="token punctuation">,</span> status<span class="token punctuation">)</span><span class="token punctuation">;</span>
		<span class="token keyword">char</span> tbuf<span class="token punctuation">[</span><span class="token number">0x10000</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
		<span class="token function">clGetProgramBuildInfo</span><span class="token punctuation">(</span>program<span class="token punctuation">,</span> device<span class="token punctuation">,</span> CL_PROGRAM_BUILD_LOG<span class="token punctuation">,</span> <span class="token number">0x10000</span><span class="token punctuation">,</span> tbuf<span class="token punctuation">,</span>
			<span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
		<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"\n%s\n"</span><span class="token punctuation">,</span> tbuf<span class="token punctuation">)</span><span class="token punctuation">;</span>
		<span class="token comment">//return −1;</span>
	<span class="token punctuation">}</span>

	<span class="token comment">//创建 Kernel 对象</span>
	cl_kernel kernel <span class="token operator">=</span> <span class="token function">clCreateKernel</span><span class="token punctuation">(</span>program<span class="token punctuation">,</span> <span class="token string">"matrix_mult"</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">//设置 Kernel 参数</span>
	cl_int clnum <span class="token operator">=</span> NWITEMS<span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">clSetKernelArg</span><span class="token punctuation">(</span>kernel<span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">int</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>Ndim<span class="token punctuation">)</span><span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">clSetKernelArg</span><span class="token punctuation">(</span>kernel<span class="token punctuation">,</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">int</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>Mdim<span class="token punctuation">)</span><span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">clSetKernelArg</span><span class="token punctuation">(</span>kernel<span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">,</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">int</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>Pdim<span class="token punctuation">)</span><span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">clSetKernelArg</span><span class="token punctuation">(</span>kernel<span class="token punctuation">,</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span>cl_mem<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>memObjects<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">clSetKernelArg</span><span class="token punctuation">(</span>kernel<span class="token punctuation">,</span> <span class="token number">4</span><span class="token punctuation">,</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span>cl_mem<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>memObjects<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">clSetKernelArg</span><span class="token punctuation">(</span>kernel<span class="token punctuation">,</span> <span class="token number">5</span><span class="token punctuation">,</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span>cl_mem<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>memObjects<span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>status<span class="token punctuation">)</span>
		cout <span class="token operator">&lt;&lt;</span> <span class="token string">"参数设置错误"</span> <span class="token operator">&lt;&lt;</span> endl<span class="token punctuation">;</span>

	<span class="token comment">//执行 kernel</span>
	size_t global<span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
	cl_event prof_event<span class="token punctuation">;</span>
	cl_ulong ev_start_time <span class="token operator">=</span> <span class="token punctuation">(</span>cl_ulong<span class="token punctuation">)</span><span class="token number">0</span><span class="token punctuation">;</span>
	cl_ulong ev_end_time <span class="token operator">=</span> <span class="token punctuation">(</span>cl_ulong<span class="token punctuation">)</span><span class="token number">0</span><span class="token punctuation">;</span>
	<span class="token keyword">double</span> rum_time<span class="token punctuation">;</span>
	global<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">(</span>size_t<span class="token punctuation">)</span>Ndim<span class="token punctuation">;</span>
	global<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">(</span>size_t<span class="token punctuation">)</span>Mdim<span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">clEnqueueNDRangeKernel</span><span class="token punctuation">(</span>commandQueue<span class="token punctuation">,</span> kernel<span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">,</span>
		global<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>prof_event<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>status<span class="token punctuation">)</span>
		cout <span class="token operator">&lt;&lt;</span> <span class="token string">"执行内核时错误"</span> <span class="token operator">&lt;&lt;</span> endl<span class="token punctuation">;</span>
	<span class="token function">clFinish</span><span class="token punctuation">(</span>commandQueue<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">//读取时间</span>
	status <span class="token operator">=</span> <span class="token function">clGetEventProfilingInfo</span><span class="token punctuation">(</span>prof_event<span class="token punctuation">,</span> CL_PROFILING_COMMAND_QUEUED<span class="token punctuation">,</span>
		<span class="token keyword">sizeof</span><span class="token punctuation">(</span>cl_ulong<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>ev_start_time<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	status <span class="token operator">=</span> <span class="token function">clGetEventProfilingInfo</span><span class="token punctuation">(</span>prof_event<span class="token punctuation">,</span> CL_PROFILING_COMMAND_END<span class="token punctuation">,</span>
		<span class="token keyword">sizeof</span><span class="token punctuation">(</span>cl_ulong<span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token operator">&amp;</span>ev_end_time<span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>status<span class="token punctuation">)</span>
		<span class="token function">perror</span><span class="token punctuation">(</span><span class="token string">"读取时间的时候发生错误\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	rum_time <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token keyword">double</span><span class="token punctuation">)</span><span class="token punctuation">(</span>ev_end_time <span class="token operator">-</span> ev_start_time<span class="token punctuation">)</span><span class="token punctuation">;</span>
	cout <span class="token operator">&lt;&lt;</span> <span class="token string">"执行时间为:"</span> <span class="token operator">&lt;&lt;</span> rum_time <span class="token operator">&lt;&lt;</span> endl<span class="token punctuation">;</span>

	<span class="token comment">//数据拷回 host 内存</span>
	status <span class="token operator">=</span> <span class="token function">clEnqueueReadBuffer</span><span class="token punctuation">(</span>commandQueue<span class="token punctuation">,</span> memObjects<span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">]</span><span class="token punctuation">,</span> CL_TRUE<span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span>
		<span class="token keyword">sizeof</span><span class="token punctuation">(</span><span class="token keyword">float</span><span class="token punctuation">)</span><span class="token operator">*</span> szC<span class="token punctuation">,</span> C<span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">,</span> <span class="token constant">NULL</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>status<span class="token punctuation">)</span>
		<span class="token function">perror</span><span class="token punctuation">(</span><span class="token string">"读回数据的时候发生错误\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">//结果显示</span>
	<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"\nArray A:\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">for</span> <span class="token punctuation">(</span>i <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> i <span class="token operator">&lt;</span> Ndim<span class="token punctuation">;</span> i<span class="token operator">++</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>
		<span class="token keyword">for</span> <span class="token punctuation">(</span>j <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> j <span class="token operator">&lt;</span> Pdim<span class="token punctuation">;</span> j<span class="token operator">++</span><span class="token punctuation">)</span>
			<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"%.3f\t"</span><span class="token punctuation">,</span> A<span class="token punctuation">[</span>i<span class="token operator">*</span>Pdim <span class="token operator">+</span> j<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
		<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
	<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"\nArray B:\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">for</span> <span class="token punctuation">(</span>i <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> i <span class="token operator">&lt;</span> Pdim<span class="token punctuation">;</span> i<span class="token operator">++</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>
		<span class="token keyword">for</span> <span class="token punctuation">(</span>j <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> j <span class="token operator">&lt;</span> Mdim<span class="token punctuation">;</span> j<span class="token operator">++</span><span class="token punctuation">)</span>
			<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"%.3f\t"</span><span class="token punctuation">,</span> B<span class="token punctuation">[</span>i<span class="token operator">*</span>Mdim <span class="token operator">+</span> j<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
		<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
	<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"\nArray C:\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">for</span> <span class="token punctuation">(</span>i <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> i <span class="token operator">&lt;</span> Ndim<span class="token punctuation">;</span> i<span class="token operator">++</span><span class="token punctuation">)</span> <span class="token punctuation">{<!-- --></span>
		<span class="token keyword">for</span> <span class="token punctuation">(</span>j <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> j <span class="token operator">&lt;</span> Mdim<span class="token punctuation">;</span> j<span class="token operator">++</span><span class="token punctuation">)</span>
			<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"%.3f\t"</span><span class="token punctuation">,</span> C<span class="token punctuation">[</span>i<span class="token operator">*</span>Mdim <span class="token operator">+</span> j<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
		<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"\n"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>

	cout <span class="token operator">&lt;&lt;</span> endl<span class="token punctuation">;</span>

	<span class="token keyword">if</span> <span class="token punctuation">(</span>A<span class="token punctuation">)</span>
		<span class="token function">free</span><span class="token punctuation">(</span>A<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>B<span class="token punctuation">)</span>
		<span class="token function">free</span><span class="token punctuation">(</span>B<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>C<span class="token punctuation">)</span>
		<span class="token function">free</span><span class="token punctuation">(</span>C<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">//删除 OpenCL 资源对象</span>
	<span class="token function">clReleaseMemObject</span><span class="token punctuation">(</span>memObjects<span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token function">clReleaseMemObject</span><span class="token punctuation">(</span>memObjects<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token function">clReleaseMemObject</span><span class="token punctuation">(</span>memObjects<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token function">clReleaseProgram</span><span class="token punctuation">(</span>program<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token function">clReleaseCommandQueue</span><span class="token punctuation">(</span>commandQueue<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token function">clReleaseContext</span><span class="token punctuation">(</span>context<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token function">system</span><span class="token punctuation">(</span><span class="token string">"pause"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre>
                