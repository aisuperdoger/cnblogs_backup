原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522406.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>1.for循环：</p> 
<pre><code>for i in $(ls ./zz) 				# 列出zz目录下的所有文件 
do
		echo hello${i%.*}  	# ${}让变量i可以和字符串hello进行拼接
										# %后面跟需要截取掉的部分，其他截取方法请参考https://blog.csdn.net/zzddada/article/details/120739198
										# .*代表截取掉.和.后面的所有部分
done	
</code></pre>
                