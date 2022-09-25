原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522410.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p><strong>PASCAL VOC2012数据集与制作自己的数据集</strong></p> 
<p>官网：https://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#devkit</p> 
<p>官网进不去的话，这个博客https://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#devkit中提到用这个镜像下载数据集https://pjreddie.com/projects/pascal-voc-dataset-mirror/</p> 
<p>PASCAL VOC2012数据集的具体介绍，可以google</p> 
<p>PASCAL VOC挑战赛，包括图像分类、目标识别、目标分割、动作识别这几个类别</p> 
<p>制作自己的数据集的软件主要有两种，分别为labelme和labellmg两种，labelme的标注文件json格式保存的，labellmg的标注文件是用xml格式保存的，labellmg中还有一个此照片标注难易的属性。labellmg的标注文件和PASCAL VOC数据集的格式完全一致。</p> 
<p>通过pip install labelme或pip install labellmg，即可安装对应的软件。它们的使用说明可以上github上查找进行查看</p>
                