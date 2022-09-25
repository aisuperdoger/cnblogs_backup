原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522415.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>1.视频转图片:</p> 
<pre><code>ffmpeg -i 1.mp4 -r 5 -f image2 .\output\1_frame_%05d.bmp
</code></pre> 
<p>"-r 5"代表一秒中抽取五帧<br> “ image2”代表图片的类型，<br> “%05d”代表五位的数，如“00001”<br> 输出图片的后缀不一定要为bmp，也可以为png，这都是无损提取。而输出的图片为jpg时，输出的图片就是压缩过后的。</p> 
<p>2.图片转视频：</p> 
<pre><code>ffmpeg -f image2 -framerate 25 -i "img%05d.bmp" -b:v 25313k C:\123\222.mp4
</code></pre> 
<p>“ -framerate 25”：代表一秒25帧，<br> “-b:v 25313k ”：代表视频所需的码率为25313k</p> 
<p>码率的获取：<br> 在利用ffmpeg将视频变为图片完成的时候，会得到bitrate，如下图：<img src="https://img-blog.csdnimg.cn/d3f3a6063c4f4b71bdd7a4b27a871119.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAcXFfNDI3NzU5Mzg=,size_20,color_FFFFFF,t_70,g_se,x_16" alt="在这里插入图片描述"><br> 将码率设为和原视频一致，那么由图片得到的视频也会和原视频的播放效果类似。</p> 
<p>3.批量重命名<br> 在图片转视频时，图片的命名应该是一样的，只有编号不一样，如aa1.bmp，所以需要对所有图片进行重命名。依次键入下面命令<br> CTRL+A：全选<br> F2：重命名为aa.bmp<br> CTRL+enter：将所有图片按顺序命名成"aa (1).bmp"、“aa (2).bmp”…………<br> 此时图片转视频的命令变为：</p> 
<pre><code>ffmpeg -f image2 -framerate 25 -i "aa (%d).bmp" -b:v 25313k C:\123\222.mp4
</code></pre> 
<p>因为批量重命名后aa与后面的编号之间有空格，所以命令中的aa (%d).bmp必须用双引号括起来。</p> 
<p>注意：这里不管是视频转图片，还是图片转视频，都会导致画质少量的损失。</p>
                