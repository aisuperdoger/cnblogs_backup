原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522411.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>参考：https://blog.csdn.net/yuanlulu/article/details/79818599</p> 
<p>https://blog.csdn.net/sinat_17196995/article/details/57946708</p> 
<p>https://zhuanlan.zhihu.com/p/391396206</p> 
<p>两个标注文件：</p> 
<h2><a id="det_8"></a><strong>det目录:</strong></h2> 
<p>det目录下只有一个det.txt文件，每行一个标注，代表一个检测的物体。</p> 
<p>内容摘抄为：</p> 
<pre><code>1,-1,1359.1,413.27,120.26,362.77,2.3092,-1,-1,-1
1,-1,571.03,402.13,104.56,315.68,1.5028,-1,-1,-1
1,-1,650.8,455.86,63.98,193.94,0.33276,-1,-1,-1
1,-1,721.23,446.86,41.871,127.61,0.27401,-1,-1,-1
1,-1,454.06,434.36,97.492,294.47,0.20818,-1,-1,-1
1,-1,1254.6,446.72,33.822,103.47,0.14776,-1,-1,-1
1,-1,1301.1,237.38,195.98,589.95,0.051818,-1,-1,-1
.....
</code></pre> 
<p>其格式为：</p> 
<pre><code>&lt;frame&gt;, &lt;id&gt;, &lt;bb_left&gt;, &lt;bb_top&gt;, &lt;bb_width&gt;, &lt;bb_height&gt;, &lt;conf&gt;, &lt;x&gt;, &lt;y&gt;, &lt;z&gt; 
</code></pre> 
<p>每行10个数字，第一个代表第几帧，第二个代表轨迹编号（在这个文件里总是为-1）</p> 
<p>bb开头的4个数代表物体框的左上角坐标及长宽。conf代表置信度，最后3个是MOT3D用到的内容，2D检测总是为-1.</p> 
<p>总结：有用的字段主要是frame， bb_left, bb_top, bb_width, bb_height, conf</p> 
<h2><a id="gt_37"></a><strong>gt目录:</strong></h2> 
<p>这个目录下有一个gt.txt文件，内容和上面的det.txt很像。内容摘抄如下：</p> 
<pre><code>1,1,912,484,97,109,0,7,1
2,1,912,484,97,109,0,7,1
3,1,912,484,97,109,0,7,1
4,1,912,484,97,109,0,7,1
5,1,912,484,97,109,0,7,1
6,1,912,484,97,109,0,7,1
7,1,912,484,97,109,0,7,1
.......
</code></pre> 
<p>第一个值含义同上，第二个值为目标运动轨迹的ID号，第三个到第六个值的同上，第七个值为目标轨迹是否进入考虑范围内的标志，0表示忽略，1表示active。第八个值为该轨迹对应的目标种类，第九个值为box的visibility ratio，表示目标运动时被其他目标box包含/覆盖或者目标之间box边缘裁剪情况。</p> 
<h2><a id="seqinfoini_54"></a><strong>seqinfo.ini文件</strong></h2> 
<p>内容摘抄如下：</p> 
<pre><code>[Sequence]
name=MOT16-02
imDir=img1
frameRate=30
seqLength=600
imWidth=1920
imHeight=1080
imExt=.jpg
</code></pre> 
<p>主要介绍视频的帧率、分辨率等基本信息。</p>
                