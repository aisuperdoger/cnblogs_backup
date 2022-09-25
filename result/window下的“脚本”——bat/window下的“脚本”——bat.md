原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522416.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <pre><code>for %%i in (*.mp4) do ffmpeg -i %%i -r 2 -f image2 output^\%%i_frame_%%010d.bmp
pause
</code></pre> 
<p>本代码循环执行命令“ffmpeg -i %%i -r 2 -f image2 output^%%i_frame_%%010d.bmp”<br> 上面这个命令存储在名为“run.bat”的文件中</p>
                