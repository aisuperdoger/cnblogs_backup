原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522408.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <hr> 
<h2><a id="typoracopyimagesto__img_1"></a>typora-copy-images-to: 评价指标_img</h2> 
<h1><a id="1MAP_4"></a><strong>1.MAP</strong></h1> 
<p>参考：https://www.bilibili.com/video/BV1ez4y1X7g2</p> 
<p>https://www.zhihu.com/search?type=content&amp;q=map</p> 
<p>https://www.bilibili.com/video/BV1zE411u7Vw?from=search&amp;seid=10424710946648558529</p> 
<h2><a id="11__12"></a><strong>1.1 一些名词的解释</strong></h2> 
<ul><li>TP: IoU&gt;0.5的检测框数量（同一Ground Truth只计算一次）。（检测出来且正确的框）</li><li>FP: IoU&lt;=0.5的检测框，或者是检测到同一个GT的多余检测框的数量。（误检的框）</li><li>FN: 没有检测到的GT的数量。（没检测出来的真实框）</li></ul> 
<p>P代表检测出的框，T代表后面哪个字母是否正确。</p> 
<p>bbox中IOU最大且大于0.5的那个框是TP；在bbox中的其他框为FP；</p> 
<p>Precision： TP / (TP + FP)，TP除以检测到的所有框，查准率（1-误检率）。检测到的所有框中，检测正确的有多少。</p> 
<p>Recall：TP / (TP + FN)，TP除以GT的总数量，查全率（1-漏检率）。真实框中被检测到的有多少。</p> 
<h2><a id="12_MAP_26"></a><strong>1.2 MAP</strong></h2> 
<h3><a id="121_AP_28"></a><strong>1.2.1 AP产生的原因</strong></h3> 
<p>置信度：除了IOU外，如果框的置信度小于设定的置信度的TP和FP，我们是不考虑进去的。</p> 
<p>随着置信度的变化，precision和recall的变化。如果precision和recall一直都很大，那么P-R的曲线所围成的面积就会趋于一。所以可以通过P-R的曲线所围成的面积来评价模型的好坏。而AP就是P-R的曲线所围成的面积</p> 
<p>mAP：mean Average Precision, 即各类别 AP 的平均值。</p> 
<h3><a id="122_PrecisionRecall_36"></a><strong>1.2.2 计算Precision和Recall</strong></h3> 
<p>假设我们有 7 张图片（Images1-Image7），这些图片共有 15 个GT（绿色的框）以及 24 个预测边框（红色的框，A-Y 编号表示，并且有一个置信度值）</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/61645c1a3cfdeb0d9872ea53526162d5.png" alt="image-20210904165334795"></p> 
<p>IOU_thred=0.3，结果如下：</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/dede726a9e0fc809c1153485f03943d6.png" alt="image-20210904165426912"></p> 
<p>​ 根据置信度从大到小排序所有的预测框，然后就可以计算 Precision 和 Recall 的值，见下表。（需要记住一个叫<strong>累加的概念，就是下图的 ACC TP 和 ACC FP</strong>）</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/182d5d643519b807918d7e8236e41bbb.png" alt="image-20210904165509442"></p> 
<p>不同置信度下的Precision和Recall：</p> 
<ul><li>标号为 1 的 Precision 和 Recall 的计算方式：Precision=TP/(TP+FP)=1/(1+0)=1，Recall=TP/(TP+FN)=TP/(all ground truths)=1/15=0.0666</li><li>标号 2：Precision=TP/(TP+FP)=1/(1+1)=0.5，Recall=TP/(TP+FN)=TP/(all ground truths)=1/15=0.0666</li><li>标号 3：Precision=TP/(TP+FP)=2/(2+1)=0.6666，Recall=TP/(TP+FN)=TP/(all ground truths)=2/15=0.1333</li><li>其他的依次类推</li></ul> 
<p>然后就可以绘制出 P-R 曲线</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/f76e49d2b9d0c68b1461fd92684e0166.png" alt="image-20210904183050249"></p> 
<h3><a id="123_AP_63"></a><strong>1.2.3 计算AP的两种方法</strong></h3> 
<p>1.VOC2010及以后的方法计算AP的方法</p> 
<p>上图中，Recall相同时，只取Precision最大的那一个点，其他的删掉。</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/442daae909264a49ee21f6dc60758173.png" alt="image-20210904183131789"></p> 
<p>AP为红色区域，AP=(0.0666-0)*1+(0.1333-0.0666)*0.6666+(0.2-0.1333)*0.3+(0.2666-0.2)*0.3333+(0.3333-0.2666)*0.3846+(0.4-0.3333)*0.4285+(0.4666-0.4)*0.3043</p> 
<p>2.VOC2010之前的方法</p> 
<p><strong>Recall</strong>取 11 个点 <strong>[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]，然后分别取每个点以后最大的Precision，如Recall=&gt;0.4中最大的Precision为0.4285</strong></p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/e8e8f455d828c813cbe593080597cc36.png" alt="image-20210904183424480"></p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/84fd264006dc7b477bede4ef31ec4ce4.png" alt="image-20210904183248662"></p> 
<h3><a id="124_COCO_83"></a><strong>1.2.4 COCO中的评价指标：</strong></h3> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/2470d16fe98d2593681096b11b46f6da.png" alt="image-20210904183742716"></p> 
<p>在这个表中，COCO设置了不同的IOU、max和大小得出不同的MAP值，下面是一个实例：</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/6b92abe41ede429c76d8edf23d0d1027.png" alt="image-20210904183931434"></p>
                