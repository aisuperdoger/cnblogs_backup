原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522361.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>C++的main函数可以没有输入参数，也可以有输入参数，而且只能有两个参数，习惯上coding如下：</p> 
<pre><code class="prism language-cpp"> <span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token keyword">int</span> argc<span class="token punctuation">,</span> <span class="token keyword">char</span><span class="token operator">*</span> argv<span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span> 或者 <span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token keyword">int</span> argc<span class="token punctuation">,</span> <span class="token keyword">char</span><span class="token operator">*</span><span class="token operator">*</span> argv<span class="token punctuation">)</span>
</code></pre> 
<p>其中，argc = argument count ：表示传入main函数的数组元素个数，为int类型，而 argv = argument vector ：表示传入main函数的指针数组，为char**类型。第一个数组元素argv[0]是程序名称，并且包含程序所在的完整路径。argc至少为1，即argv数组至少包含程序名。<br> 　 一般编译器默认使用argc和argv两个名称作为main函数的参数，但这两个参数如此命名并不是必须的，你可以使用任何符合C++语言命名规范的变量名，但要保证第一个参数类型为int型，第二个参数为char**型。<br> 　 由于main函数不能被其他函数调用，因此不可能在程序内部取得实际值。main函数的参数值是从操作系统命令行上获取的。在window系统中，假如编译链接成的可执行文件为my_project.exe，则在命令提示符(快捷键windows+R，输入cmd)中，键入如下命令(可执行文件 参数 参数 参数 …)：</p> 
<pre><code class="prism language-cpp">my_project<span class="token punctuation">.</span>exe jisongxie <span class="token number">1996</span>
</code></pre> 
<p>将会传递三个参数给main函数，第一个argv[0]是前面提到的文件名，第二个argv[1]是"jisongxie"，第三个argv[2]是“1996”。同理，可以传入更多的参数。在ubuntu系统中，可以通过终端进行相同的操作。<br> 　　传入的参数数组类型为char *字符串类型，可以通过atoi，atof函数进行类型的转换。<br> 　　1、atoi，即ascii to integer，把字符串转换成int<br> 　　2、atof，即ascii to float，把字符串转换成double<br> 　　3、atol，即ascii to long int，把字符串转换成long int<br> 　　4、atoll，即ascii to long long int，把字符串转换成long long int<br> 　　例如上述输入的1996，可以得到如下：</p> 
<pre><code class="prism language-cpp"><span class="token keyword">int</span> year <span class="token operator">=</span> <span class="token function">atoi</span><span class="token punctuation">(</span>argv<span class="token punctuation">[</span><span class="token number">2</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>  <span class="token comment">// year = 1996</span>
</code></pre> 
<p>因此，通过上述的命令行输入以及程序里面的类型转换，可以通过命令行窗口传入值(字符串和数字)到程序中运行。</p> 
<p>参考：<a href="https://www.cnblogs.com/jisongxie/p/7892366.html">链接</a></p>
                