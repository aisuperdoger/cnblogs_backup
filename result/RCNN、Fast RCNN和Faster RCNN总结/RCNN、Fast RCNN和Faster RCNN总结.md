原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522417.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>参考：https://www.bilibili.com/video/BV1af4y1m7iL?p=1</p> 
<h1><a id="1RCNNRegionCNN_4"></a>1.RCNN（Region-CNN）</h1> 
<h2><a id="11_RCNN_5"></a>1.1 RCNN的总述</h2> 
<p>1.得到候选框：通过Selective Search算法在每张图片中生成1k~2k的候选区域。<font color="red">ss算法具体如何实现？</font><br> 2.特征提取：将候选框中的图片缩放成227x227，然后通过包含CNN的神经网络对每个候选区域进行特征提取，并拉直成一维向量<br> 3.SVM分类：将一维向量送入SVM分类器中预测属于各个类的概率，然后利用非极大值抑制剔除一些建议框<br> 4.修正候选区域：利用回归器修正候选区域位置</p> 
<h2><a id="12_RCNN_11"></a>1.2 RCNN的细节详述</h2> 
<h3><a id="121__13"></a>1.2.1 特征提取</h3> 
<p>​ 将2000个候选区域都缩放到227x227pixel，接着将每个候选区域输入事先训练好的AlexNet CNN网络，每个候选区域获取4096维的特征，从而得到2000×4096维矩阵。 <font color="red">如何缩放？</font></p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/71a3513a44586e9e9d12d349a6c41f87.png" alt="image-20210819102205544"></p> 
<h3><a id="122_SVM_19"></a>1.2.2 <strong>SVM分类</strong></h3> 
<p>​ 将2000×4096维特征与20个SVM组成的权值矩阵4096×20相乘（<font color="red">不需要映射到高维上面的吗？</font>）， 获得2000×20维矩阵表示每个建议框是某个目标类别的得分。分别对上述2000×20维矩阵中每一列即每一类进行<strong>非极大值抑制</strong>剔除一些建议框，得到该列即该类中得分最高的一些建议框。</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/56bfb974e2bfdb7ba9dc458116d374f4.png" alt="image-20210819111426165"></p> 
<p>使用20个SVM的原因：这里是假设有二十个类别。而SVM是一个二分类，所以20个SVM就可以进行20个分类.</p> 
<h3><a id="123__27"></a>1.2.3 非极大值抑制剔除建议框</h3> 
<p>​ 选出每一类（列）中SVM得分最高的建议框A，然后计算A和其他建议框的IOU值。假设A和B的IOU值大于给定阈值，这就说明A和B重合过多，就剔除B。因为重合过多就说明A和B实际框住的是同一个物体，但是A的得分高，效果更好，故保留A剔除B。当阈值的设置合适时，就可以保证每个物体上只有一个框。每一行只保留得分最高的类别，此类别就是框住的类别。</p> 
<p>存在的问题：</p> 
<ul><li>当两物体之间的距离很近且给定的阈值太小时，那么容易导致两个物体中有一个物体的框被剔除掉（漏检）</li><li>不能保证每个物体都有框（漏检）</li><li>如果A框到没有物体的地方或A与其他框的重合不多，就会导致A被保留下来(误检)</li></ul> 
<h3><a id="124__37"></a>1.2.4 修正候选区域</h3> 
<p>​ 对NMS处理后剩余的建议框进一步筛选。接着分别用20个回归器对上述20个类别中剩余的建议框进行回</p> 
<p>归操作，最终得到每个类别的修正后的得分最高的 bounding box。 <font color="red">如何进行回归操作呢</font>？</p> 
<p>如下图，黄色框口P表示建议框Region Proposal， 绿色窗口G表示实际框Ground Truth，红色窗口</p> 
<p>表示Region Proposal进行回归后的预测窗口，可以用 最小二乘法解决的线性回归问题。</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/4f4f44a9f000a0a2200fe5f999a4ba56.png" alt="image-20210819153520861"></p> 
<h2><a id="13_RCNN_51"></a>1.3 RCNN存在的问题</h2> 
<p>1.测试速度慢： 测试一张图片约53s(CPU)。用Selective Search算法 提取候选框用时约2秒，一张图像内<strong>候选框之间存在大</strong> <strong>量重叠</strong>，提取特征操作冗余。</p> 
<p>2.训练速度慢： 过程及其繁琐</p> 
<p>3.训练所需空间大： 对于SVM和bbox（bounding box）回归训练，需要从每个图像中的每个目标候选框提取特征，并写入磁盘。对于非常深的网络（ <font color="red">和网络深浅有什么关系？</font>），如VGG16，从VOC07 训练集上的5k张图像上提取的特征需要数百GB的存储空间。</p> 
<h1><a id="2Fast_RCNN_59"></a>2.Fast RCNN</h1> 
<h2><a id="21_Fast_RCNN_61"></a>2.1 Fast RCNN的总述</h2> 
<p>1.得到候选框：利用ss算法（Selective Search）在一张图像生成1K~2K个候选区域，随机选取64个候选区域</p> 
<p>2.特征提取：将整张图像输入网络得到相应的<strong>特征图</strong>，将SS算法生成的候选框投影到特征图上获得相应的<strong>特征矩阵</strong></p> 
<p>3.一个神经网络进行分类和生成bbox的回归参数：将每个特征矩阵通过ROI pooling层缩放到<strong>7x7大小的特征图</strong>，接着将特征图展平通过一系列全连接层得到目标所属的类别和bbox的回归参数 。（ROI:Region of Interest）</p> 
<p>Fast RCNN与RCNN区别：RCNN中是输入特征区域对应的图像（227x227）得到相应的特征向量，然后将特征向量输入到SVM进行分类、利用回归器修正候选区域位置</p> 
<h2><a id="22_Fast_RCNN_71"></a>2.2 Fast RCNN的细节详述</h2> 
<h3><a id="221__73"></a>2.2.1 候选区域选取</h3> 
<p>​ 随机选取候选区域：在Fast RCNN中并没有使用所有的候选框，而是随机从正样本和负样本拿出总共64个。正样本是指候选框与真实值之间的IOU值大于0.5。负样本是指候选框与真实值之间的IOU值在[0.1,0.5)，且是从IOU最大的开始采样（先采样正样本，其余的从负样本的最大IOU开始取，总共取64个）。</p> 
<h3><a id="222_ROI_pooling_77"></a>2.2.2 ROI pooling层缩放</h3> 
<p>​ 首先将每个候选框的特征图分割成7*7，总共49块，然后对每一块进行max pooling（每块中取像素最大的点）。</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/5594e392cc7edac9dae907d2541610ed.png" alt="image-20210820010149951"></p> 
<p>注：特征图肯定不是上图那个样子，这里只是为了方便而这么画的</p> 
<h3><a id="223bbox_85"></a>2.2.3.分类器和bbox回归器</h3> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/d0e5a05c7aa9b0e34d40561dd46c4686.png" alt="image-20210820011003487"></p> 
<p>上图中除了上面标注FCs以外的所有长方体块都是表示图像的矩阵。</p> 
<p>从上图可知，</p> 
<ul><li> <p>首先将整张图片输入进行特征提取的到特征图。</p> </li><li> <p>然后将候选框在特征图中框出的区域输入到ROI pooling层中，得到7*7的矩阵。</p> </li><li> <p>再将7*7矩阵展平以后输入到两个全连接层中得到ROI feature vector。</p> </li><li> <p>然后将ROI feature vector分别输入到两个不同的全连接层得到分类的结果和bbox的回归参数。输出分类结果的部分就叫分类器，输出bbox回归参数的就叫做bbox回归器。</p> </li></ul> 
<p><strong>分类器</strong>：输出N+1个类别的概率（N为检测目标的种类, 1为背景）共N+1个节点 。N+1个概率相加的结果为1。</p> 
<p><strong>bbox回归器</strong>：输出对应N+1个类别的候选边界框回归参数(d<sub>x</sub>, d<sub>y</sub>, d<sub>w</sub>, d<sub>h</sub>),即输出共(N+1)x4个节点。利用这些参数就可以计算出最终的预测框，计算公式如下：<font color="red">一个候选框预测出N+1个预测框吗？答：分类器得出此候选框属于哪一类，bbox回归器得出此候选框的此类的最终预测框</font></p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/f0f3ff5ae3ef0c0aa2e9c77b90eb6264.png" alt="image-20210824152026231"></p> 
<p>这里的d<sub>x</sub>§是d<sub>x</sub>的意思。</p> 
<p>解释以下第一个公式<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         
          G
         
         
          x
         
        
        
         ^
        
       
       
        =
       
       
        
         P
        
        
         w
        
       
       
        
         d
        
        
         x
        
       
       
        (
       
       
        P
       
       
        )
       
       
        +
       
       
        
         P
        
        
         x
        
       
      
      
       \widehat{G_x}=P_wd_x(P)+P_x
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.07333em; vertical-align: -0.15em;"></span><span class="mord accent"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.92333em;"><span class="" style="top: -3em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord"><span class="mord mathdefault">G</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span><span class="svg-align" style="top: -3.68333em;"><span class="pstrut" style="height: 3em;"></span><span class="" style="height: 0.24em;">
           <svg width="100%" height="0.24em" viewBox="0 0 1062 239" preserveAspectRatio="none">
            <path d="M529 0h5l519 115c5 1 9 5 9 10 0 1-1 2-1 3l-4 22
c-1 5-5 9-11 9h-2L532 67 19 159h-2c-5 0-9-4-11-9l-5-22c-1-6 2-12 8-13z"></path>
           </svg></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.13889em;">P</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: -0.13889em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight" style="margin-right: 0.02691em;">w</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mord"><span class="mord mathdefault">d</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mopen">(</span><span class="mord mathdefault" style="margin-right: 0.13889em;">P</span><span class="mclose">)</span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.222222em;"></span></span><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.13889em;">P</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: -0.13889em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>：这里的就是利用参数<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         d
        
        
         x
        
       
       
        (
       
       
        P
       
       
        )
       
      
      
       d_x(P)
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mord"><span class="mord mathdefault">d</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mopen">(</span><span class="mord mathdefault" style="margin-right: 0.13889em;">P</span><span class="mclose">)</span></span></span></span></span>和<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         P
        
        
         w
        
       
      
      
       P_w
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.13889em;">P</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: -0.13889em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight" style="margin-right: 0.02691em;">w</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>来调节<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         P
        
        
         x
        
       
      
      
       P_x
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.13889em;">P</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: -0.13889em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>使其变得更加准确。可以更加准确的原因是最终的预测框会与真实框进行比较，然后调节参数<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         d
        
        
         x
        
       
      
      
       d_x
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.84444em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault">d</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>，使得这个参数可以调节预测框去接近真实框。<font color="red">是这个公式，而不是其他的，作者是怎么得出这个公式的？？</font></p> 
<h3><a id="224__115"></a>2.2.4 损失函数</h3> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/16a5cf58faf3898d26bba913a76518a3.png" alt="image-20210824155245323"></p> 
<p><font color="red">这里的v是是什么意思，我不太明白?</font></p> 
<p>L<sub>cls</sub>(p,u) = - logp<sub>u</sub>，这里的P<sub>u</sub>代表预测类别为u的概率</p> 
<p><span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml">
     
      
       
        
         
          L
         
         
          l
         
        
        
         o
        
        
         c
        
        
         (
        
        
         
          t
         
         
          u
         
        
        
         ,
        
        
         v
        
        
         )
        
        
         =
        
        
         
          ∑
         
         
          
           i
          
          
           ∈
          
          
           
            {
           
           
            x
           
           
            ,
           
           
            y
           
           
            ,
           
           
            w
           
           
            ,
           
           
            h
           
           
            }
           
          
         
        
        
         s
        
        
         m
        
        
         o
        
        
         o
        
        
         t
        
        
         
          h
         
         
          
           L
          
          
           1
          
         
        
        
         (
        
        
         
          t
         
         
          i
         
         
          u
         
        
        
         −
        
        
         
          v
         
         
          i
         
        
        
         )
        
       
       
         L_loc(t^u,v) = \sum_{i\in {\{x,y,w,h\}}}smooth_{L_1}(t_i^u-v_i)
       
      
     </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mord"><span class="mord mathdefault">L</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.336108em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight" style="margin-right: 0.01968em;">l</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mord mathdefault">o</span><span class="mord mathdefault">c</span><span class="mopen">(</span><span class="mord"><span class="mord mathdefault">t</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.714392em;"><span class="" style="top: -3.113em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">u</span></span></span></span></span></span></span></span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathdefault" style="margin-right: 0.03588em;">v</span><span class="mclose">)</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 2.56601em; vertical-align: -1.51601em;"></span><span class="mop op-limits"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.05001em;"><span class="" style="top: -1.80899em; margin-left: 0em;"><span class="pstrut" style="height: 3.05em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathdefault mtight">i</span><span class="mrel mtight">∈</span><span class="mord mtight"><span class="mopen mtight">{<!-- --></span><span class="mord mathdefault mtight">x</span><span class="mpunct mtight">,</span><span class="mord mathdefault mtight" style="margin-right: 0.03588em;">y</span><span class="mpunct mtight">,</span><span class="mord mathdefault mtight" style="margin-right: 0.02691em;">w</span><span class="mpunct mtight">,</span><span class="mord mathdefault mtight">h</span><span class="mclose mtight">}</span></span></span></span></span><span class="" style="top: -3.05em;"><span class="pstrut" style="height: 3.05em;"></span><span class=""><span class="mop op-symbol large-op">∑</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 1.51601em;"><span class=""></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathdefault">s</span><span class="mord mathdefault">m</span><span class="mord mathdefault">o</span><span class="mord mathdefault">o</span><span class="mord mathdefault">t</span><span class="mord"><span class="mord mathdefault">h</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.328331em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathdefault mtight">L</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.317314em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714286em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2501em;"><span class=""></span></span></span></span></span></span><span class="mopen">(</span><span class="mord"><span class="mord mathdefault">t</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.714392em;"><span class="" style="top: -2.453em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span><span class="" style="top: -3.113em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">u</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.247em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mbin">−</span><span class="mspace" style="margin-right: 0.222222em;"></span></span><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.03588em;">v</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.311664em;"><span class="" style="top: -2.55em; margin-left: -0.03588em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mclose">)</span></span></span></span></span></span>：就是两框之间的差距</p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        s
       
       
        m
       
       
        o
       
       
        o
       
       
        t
       
       
        
         h
        
        
         
          L
         
         
          1
         
        
       
       
        (
       
       
        x
       
       
        )
       
       
        =
       
       
        
         {
        
        
         
          
           
            
             
              0.5
             
             
              
               x
              
              
               2
              
             
             
              ,
             
            
           
          
          
           
            
             
              i
             
             
              f
             
             
              ∣
             
             
              x
             
             
              ∣
             
             
              &lt;
             
             
              1
             
            
           
          
         
         
          
           
            
             
              ∣
             
             
              x
             
             
              ∣
             
             
              −
             
             
              0.5
             
             
              ,
             
            
           
          
          
           
            
             
              o
             
             
              t
             
             
              h
             
             
              e
             
             
              r
             
             
              w
             
             
              i
             
             
              s
             
             
              e
             
            
           
          
         
        
       
      
      
       smooth_{L_1}(x)= \left\{ \begin{array}{lr} 0.5x^2, &amp; if |x|&lt;1 \\ |x|-0.5, &amp; otherwise \end{array} \right.
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.0001em; vertical-align: -0.2501em;"></span><span class="mord mathdefault">s</span><span class="mord mathdefault">m</span><span class="mord mathdefault">o</span><span class="mord mathdefault">o</span><span class="mord mathdefault">t</span><span class="mord"><span class="mord mathdefault">h</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.328331em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathdefault mtight">L</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.317314em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714286em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.2501em;"><span class=""></span></span></span></span></span></span><span class="mopen">(</span><span class="mord mathdefault">x</span><span class="mclose">)</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 2.40003em; vertical-align: -0.95003em;"></span><span class="minner"><span class="mopen delimcenter" style="top: 0em;"><span class="delimsizing size3">{<!-- --></span></span><span class="mord"><span class="mtable"><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-l"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">0</span><span class="mord">.</span><span class="mord">5</span><span class="mord"><span class="mord mathdefault">x</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mpunct">,</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">∣</span><span class="mord mathdefault">x</span><span class="mord">∣</span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mbin">−</span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">5</span><span class="mpunct">,</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="arraycolsep" style="width: 0.5em;"></span><span class="col-align-r"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.45em;"><span class="" style="top: -3.61em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord mathdefault">i</span><span class="mord mathdefault" style="margin-right: 0.10764em;">f</span><span class="mord">∣</span><span class="mord mathdefault">x</span><span class="mord">∣</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">&lt;</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mord">1</span></span></span><span class="" style="top: -2.41em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord mathdefault">o</span><span class="mord mathdefault">t</span><span class="mord mathdefault">h</span><span class="mord mathdefault">e</span><span class="mord mathdefault" style="margin-right: 0.02778em;">r</span><span class="mord mathdefault" style="margin-right: 0.02691em;">w</span><span class="mord mathdefault">i</span><span class="mord mathdefault">s</span><span class="mord mathdefault">e</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.95em;"><span class=""></span></span></span></span></span><span class="arraycolsep" style="width: 0.5em;"></span></span></span><span class="mclose nulldelimiter"></span></span></span></span></span></span></p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         v
        
        
         x
        
       
       
        =
       
       
        
         
          
           G
          
          
           x
          
         
         
          −
         
         
          
           P
          
          
           x
          
         
        
        
         
          P
         
         
          w
         
        
       
      
      
       v_x=\frac{G_x-P_x}{P_w}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.58056em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.03588em;">v</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: -0.03588em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 1.33353em; vertical-align: -0.4451em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.888431em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathdefault mtight" style="margin-right: 0.13889em;">P</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.164543em;"><span class="" style="top: -2.357em; margin-left: -0.13889em; margin-right: 0.0714286em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mathdefault mtight" style="margin-right: 0.02691em;">w</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.4101em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathdefault mtight">G</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.164543em;"><span class="" style="top: -2.357em; margin-left: 0em; margin-right: 0.0714286em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span><span class="mbin mtight">−</span><span class="mord mtight"><span class="mord mathdefault mtight" style="margin-right: 0.13889em;">P</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.164543em;"><span class="" style="top: -2.357em; margin-left: -0.13889em; margin-right: 0.0714286em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.143em;"><span class=""></span></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.4451em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span></span></span></span></span>：<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         G
        
        
         x
        
       
      
      
       G_x
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault">G</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">x</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>为真实框对应的x</p> 
<p>[u=&gt;1]：方括号内的条件满足则为1，不满足则为0。当u=0时表示背景，而当u为其他大于一的数时表示类别标签。也就是说当框内的东西为背景时，是没有边界框回归损失，因为背景可没有被框住。</p> 
<p><a href="https://www.cnblogs.com/wangguchangqing/p/12021638.html">损失函数的理解可以参考这个</a></p> 
<h2><a id="23_Fast_RCNNRCNN_141"></a>2.3 Fast RCNN与RCNN框架之间的对比</h2> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/489ddff9bc684add9224b21d38cc71fa.png" alt="image-20210824194543724"></p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/d0c921600ade60591eab5d9a2426310b.png" alt="image-20210824194507042"></p> 
<p>Fast RCNN特征提取、分类、参数回归都融合成在了一个CNN网络中了，而RCNN分成了三个部分。</p> 
<h1><a id="3Faster_RCNN_151"></a>3.Faster RCNN</h1> 
<p>​ 同样使用VGG16作为网络的backbone(主干)，推理速度在GPU上达到5fps(包括候选区域的生成)，准确率也有进一步的提升。</p> 
<p>Faster RCNN=Fast RCNN+RPN</p> 
<h2><a id="31_Faster_RCNN_157"></a>3.1 Faster RCNN的总述</h2> 
<p>1.得到候选框：将整张图像输入conv层得到特征图，将特征图输入到RPN中得到候选框</p> 
<p>2.特征提取：将RPN生成的候选框投影到特征图上获得相应的<strong>特征矩阵</strong></p> 
<p>3.一个神经网络进行分类和生成bbox的回归参数：将每个特征矩阵通过ROI pooling层缩放到<strong>7x7大小的特征图</strong>，接着将特征图展平通过一系列全连接层得到目标所属的类别和bbox的回归参数 。（ROI:Region of Interest）</p> 
<p>Faster RCNN与Fast RCNN的区别：Faster RCNN利用RPN获取候选框。Fast RCNN利用ss算法获取候选框。</p> 
<p>下图是Faster RCNN的整体架构</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/1e4558424a77f750de73c88b8e0c4969.png" alt="image-20210824210043488"></p> 
<h2><a id="32_RPNRegion_Proposal_Network_173"></a>3.2 RPN(Region Proposal Network)</h2> 
<h3><a id="321_RPN_175"></a>3.2.1 RPN的构成</h3> 
<p>​ RPN的作用是筛选出可能会有目标的框”。RPN是用一个全卷积网络来实现的，可以与检测网络共享整幅图像的卷积特征，从而产生几乎无代价的区域推荐。</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/910fc8802fea1182d41050c74679f2b1.png" alt="image-20210824210323801"></p> 
<p>​ <strong>图中右边的解释</strong>：sliding window（滑动窗口）在 conv feature map（特征图）滑动。每滑动到一个区域，输出一个一维的向量（256个元素）。将这个一维向量分别输入到两个全连接层中，分别产生2k个score和4k个coordinate。下面对上面这句话进行补充解释：</p> 
<p>​ <strong>一维向量的生成</strong>：一维向量有256个元素，这是因为特征图是由ZF生成的，ZF生成的特征图有256个channel。如果特征图是由VGG16生成的话，特征图就有512个channel，此时一维向量就有512个元素。一维向量的生成过程为：利用256或512个3*3的conv（步长为1，padding为全零填充）在特征图上滑动，从而生成一个和特征图shape一致的图，这个图的每一个像素点下的256或512个channel都代表一个上面提到的一维向量。每个一维向量都预测出k个anchor box（论文种k=9）。</p> 
<p>​ <strong>9个anchor box</strong>：k代表k个anchor box，anchor boxes指的是以滑动窗口中心点对应原始图像上的中心点为中心的一些框。k一般为9，即9种anchor box。9种anchor box：anchor box的大小有{<!-- --><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        12
       
       
        
         8
        
        
         2
        
       
       
        ,
       
       
        25
       
       
        
         6
        
        
         2
        
       
       
        ,
       
       
        51
       
       
        
         2
        
        
         2
        
       
      
      
       128^2,256^2,512^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.00855em; vertical-align: -0.19444em;"></span><span class="mord">1</span><span class="mord">2</span><span class="mord"><span class="mord">8</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">2</span><span class="mord">5</span><span class="mord"><span class="mord">6</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">5</span><span class="mord">1</span><span class="mord"><span class="mord">2</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>}三种，anchor box的宽高比例有{1:1,1:2,2:1}三种。所以在每个位置（每个滑动窗口）在原图上都对应3*3=9个anchor（作者说这些是经验所得）。下面是9个anchor的示意图：</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/fa28b9e42dd8a548a952249acef7e7ed.png" alt="image-20210825095139040"></p> 
<p>​ 那么问题来了！ZF感受野是 171 ，VGG感受野是 228 （感受野：特征图的一个像素点对应原图多大一块），对于VGG来说，输入网络的一维向量只能代表原图中<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        22
       
       
        
         8
        
        
         2
        
       
      
      
       228^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.814108em; vertical-align: 0em;"></span><span class="mord">2</span><span class="mord">2</span><span class="mord"><span class="mord">8</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>大小的面积，而在预测到的anchor中有两种面积是大于<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        22
       
       
        
         8
        
        
         2
        
       
      
      
       228^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.814108em; vertical-align: 0em;"></span><span class="mord">2</span><span class="mord">2</span><span class="mord"><span class="mord">8</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>，分别为：{<!-- --><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        25
       
       
        
         6
        
        
         2
        
       
       
        ,
       
       
        51
       
       
        
         2
        
        
         2
        
       
      
      
       256^2,512^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.00855em; vertical-align: -0.19444em;"></span><span class="mord">2</span><span class="mord">5</span><span class="mord"><span class="mord">6</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">5</span><span class="mord">1</span><span class="mord"><span class="mord">2</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>}。为什么可以通过面积小的预测出面积大的区域呢？答：比如你看到一个物体的一部分就可以猜出这个物体是什么。</p> 
<p>​ <strong>anchor box的两个预测值</strong>：每个anchor box有两个score，分别表示anchor box中为背景的概率和anchor box中为目标的概率，两个score相加不一定为一。每个anchor box有四个coordinate，这四个coordinate是anchor box的回归参数(d<sub>x</sub>, d<sub>y</sub>, d<sub>w</sub>, d<sub>h</sub>)，通过(d<sub>x</sub>, d<sub>y</sub>, d<sub>w</sub>, d<sub>h</sub>)将anchor box调整成proposal（候选框）。</p> 
<p>​ score和coordinate的形成：利用2k个1*1的卷积核对256-d进行卷积，从而使得每一个像素点对应的一维向量都输出2k个score。利用4k个1*1的卷积核对256-d进行卷积，从而使得每一个像素点对应的一维向量都输出4k个coordinate。<font color="red">这里的score核coordinate为什么是对应的？明明是通过两个不同的全连接层生成的？</font></p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/1749f113620cadfe7252bcbeff0fca26.png" alt="image-20210825152538419"></p> 
<p>​ <strong>候选框最终的确定（举例）</strong>：对于一张1000x600x3的图像，大约有60x40x9=20k个anchor，忽略跨越边界的anchor以后，剩下约6k个anchor。将6k个anchor通过(d<sub>x</sub>, d<sub>y</sub>, d<sub>w</sub>, d<sub>h</sub>)调整成6k个proposal（候选框）。候选框之间存在大量重叠，基于候选框的<em>cls</em>得分，采用非极大值抑制剔除重叠框，IoU设为0.7，这样每张图片只剩2k个候选框。</p> 
<h3><a id="322_RPN_199"></a>3.2.2 RPN的训练与损失函数</h3> 
<p><strong>训练RPN过程中的数据采样</strong>：在一张图片中所有的anchor中采样256个anchor，这256个anchor中有128个正样本和128个负样本。如果正样本不足128个，就用负样本填充，如正样本有100个，那负样本就有156个。</p> 
<p>正样本：i)样本与gt的IOU大于0.7。ii)样本是与gt相交中IOU最大的</p> 
<p>负样本：与所有的gt的IOU都小于0.3的样本</p> 
<p><strong>RPN的损失函数</strong>：</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/fadab1d5a8f3da950f69fd3c7779a789.png" alt="image-20210825162314584"></p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         p
        
        
         i
        
       
      
      
       p_i
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.625em; vertical-align: -0.19444em;"></span><span class="mord"><span class="mord mathdefault">p</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.311664em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>表示第i个anchor中真实标签的score，如某一个anchor的目标和背景的score分别为0.9和0.2，若anchor中是背景，那么<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         p
        
        
         i
        
       
       
        =
       
       
        −
       
       
        l
       
       
        n
       
       
        0.2
       
      
      
       p_i=-ln0.2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.625em; vertical-align: -0.19444em;"></span><span class="mord"><span class="mord mathdefault">p</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.311664em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 0.77777em; vertical-align: -0.08333em;"></span><span class="mord">−</span><span class="mord mathdefault" style="margin-right: 0.01968em;">l</span><span class="mord mathdefault">n</span><span class="mord">0</span><span class="mord">.</span><span class="mord">2</span></span></span></span></span>。</p> 
<p>各个参数的意义：</p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         p
        
        
         i
        
        
         ∗
        
       
      
      
       p^*_i
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.94736em; vertical-align: -0.258664em;"></span><span class="mord"><span class="mord mathdefault">p</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.688696em;"><span class="" style="top: -2.44134em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mbin mtight">∗</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.258664em;"><span class=""></span></span></span></span></span></span></span></span></span></span>当为正样本时为 1，当为负样本时为 0。</p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         t
        
        
         i
        
       
      
      
       t_i
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.76508em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault">t</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.311664em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>表示预测第 i个anchor的边界框回归参数。</p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         t
        
        
         i
        
        
         ∗
        
       
      
      
       t^*_i
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.94736em; vertical-align: -0.258664em;"></span><span class="mord"><span class="mord mathdefault">t</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.688696em;"><span class="" style="top: -2.44134em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mbin mtight">∗</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.258664em;"><span class=""></span></span></span></span></span></span></span></span></span></span>表示第i个anchor对应的gt的边界框回归参数。</p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         N
        
        
         
          c
         
         
          l
         
         
          s
         
        
       
      
      
       N_{cls}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.10903em;">N</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.336108em;"><span class="" style="top: -2.55em; margin-left: -0.10903em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathdefault mtight">c</span><span class="mord mathdefault mtight" style="margin-right: 0.01968em;">l</span><span class="mord mathdefault mtight">s</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>表示一个min-batch中的所有样本数量，即一次采样的数量，即256。</p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         N
        
        
         
          r
         
         
          e
         
         
          g
         
        
       
      
      
       N_{reg}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.969438em; vertical-align: -0.286108em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.10903em;">N</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.151392em;"><span class="" style="top: -2.55em; margin-left: -0.10903em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathdefault mtight" style="margin-right: 0.02778em;">r</span><span class="mord mathdefault mtight">e</span><span class="mord mathdefault mtight" style="margin-right: 0.03588em;">g</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.286108em;"><span class=""></span></span></span></span></span></span></span></span></span></span>表示特征图上像素点的个数，约2400个。</p> 
<p>补充解释：</p> 
<p>为了简单，经常将<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        λ
       
       
        
         1
        
        
         
          N
         
         
          
           r
          
          
           e
          
          
           g
          
         
        
       
      
      
       \lambda\frac{1}{N_{reg}}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.38743em; vertical-align: -0.54232em;"></span><span class="mord mathdefault">λ</span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.845108em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathdefault mtight" style="margin-right: 0.10903em;">N</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.164543em;"><span class="" style="top: -2.357em; margin-left: -0.10903em; margin-right: 0.0714286em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight"><span class="mord mathdefault mtight" style="margin-right: 0.02778em;">r</span><span class="mord mathdefault mtight">e</span><span class="mord mathdefault mtight" style="margin-right: 0.03588em;">g</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.281886em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.54232em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span></span></span></span></span>令成<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         1
        
        
         
          N
         
         
          
           c
          
          
           l
          
          
           s
          
         
        
       
      
      
       \frac{1}{N_{cls}}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.29597em; vertical-align: -0.45086em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.845108em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight"><span class="mord mathdefault mtight" style="margin-right: 0.10903em;">N</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.3448em;"><span class="" style="top: -2.34877em; margin-left: -0.10903em; margin-right: 0.0714286em;"><span class="pstrut" style="height: 2.5em;"></span><span class="sizing reset-size3 size1 mtight"><span class="mord mtight"><span class="mord mathdefault mtight">c</span><span class="mord mathdefault mtight" style="margin-right: 0.01968em;">l</span><span class="mord mathdefault mtight">s</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.151229em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.45086em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span></span></span></span></span>，因为两者差不多。</p> 
<p><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         L
        
        
         
          c
         
         
          l
         
         
          s
         
        
       
      
      
       L_{cls}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault">L</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.336108em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathdefault mtight">c</span><span class="mord mathdefault mtight" style="margin-right: 0.01968em;">l</span><span class="mord mathdefault mtight">s</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>为softmax cross entropy，而不是BInary cross entropy，即某一个anchor的目标和背景的score分别为0.9和0.2。若anchor中是目标，那么<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         p
        
        
         i
        
       
       
        =
       
       
        −
       
       
        l
       
       
        n
       
       
        0.9
       
      
      
       p_i=-ln0.9
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.625em; vertical-align: -0.19444em;"></span><span class="mord"><span class="mord mathdefault">p</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.311664em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 0.77777em; vertical-align: -0.08333em;"></span><span class="mord">−</span><span class="mord mathdefault" style="margin-right: 0.01968em;">l</span><span class="mord mathdefault">n</span><span class="mord">0</span><span class="mord">.</span><span class="mord">9</span></span></span></span></span>。</p> 
<p>如果这里<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         L
        
        
         
          c
         
         
          l
         
         
          s
         
        
       
      
      
       L_{cls}
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault">L</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.336108em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathdefault mtight">c</span><span class="mord mathdefault mtight" style="margin-right: 0.01968em;">l</span><span class="mord mathdefault mtight">s</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>为BInary cross entropy时，每个anchor只需要一个score而不是两个。假设当背景的score为0.2时，就可以推断出目标的score为0.8。若anchor中是目标，则<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         p
        
        
         i
        
       
       
        =
       
       
        −
       
       
        l
       
       
        n
       
       
        0.8
       
      
      
       p_i=-ln0.8
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.625em; vertical-align: -0.19444em;"></span><span class="mord"><span class="mord mathdefault">p</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.311664em;"><span class="" style="top: -2.55em; margin-left: 0em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathdefault mtight">i</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 0.77777em; vertical-align: -0.08333em;"></span><span class="mord">−</span><span class="mord mathdefault" style="margin-right: 0.01968em;">l</span><span class="mord mathdefault">n</span><span class="mord">0</span><span class="mord">.</span><span class="mord">8</span></span></span></span></span>。</p> 
<p>这里的边界框回归损失和Fast RCNN中的是一样的。</p> 
<h2><a id="33_Faster_RCNN_237"></a>3.3 Faster RCNN的损失函数</h2> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/f054257bb75b0ba8938305a86be630df.png" alt="image-20210825192047433"></p> 
<p>与Fast RCNN的损失函数完全一致。</p> 
<h2><a id="34_Faster_RCNN_243"></a>3.4 Faster R-CNN的训练过程</h2> 
<p>原论文中采用分别训练RPN以及Fast R-CNN的方法 <font color="red">看不懂！！</font>：</p> 
<p>(1)利用ImageNet预训练分类模型初始化前置卷积网络层参数，并开始单独训练RPN网络参数；</p> 
<p>(2)固定RPN网络独有的卷积层以及全连接层参数，再利用ImageNet预训练分类模型初始化前置卷积网络参数，并利用RPN 网络生成的目标建议框去训练Fast RCNN网络参数。</p> 
<p>(3)固定利用Fast RCNN训练好的前置卷积网络层参数，去微调RPN网络独有的卷积层以及全连接层参数。</p> 
<p>(4)同样保持固定前置卷积网络层参数，去微调Fast RCNN网络的全连接层参数。最后RPN网络与Fast RCNN网络共享前置卷积网络层参数，构成一个统一网络。</p> 
<p>现在一般不采用原论文的方式，而直接采用RPN Loss+ Fast R-CNN Loss的联合训练方法 。</p> 
<h2><a id="35_Faster_RCNNFast_RCNNRCNN_257"></a>3.5 Faster RCNN、Fast RCNN与RCNN框架之间的对比</h2> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/0cb919096639eb2b1a793180e822da8b.png" alt="image-20210825193050416"></p> 
<p>Fast RCNN特征提取、分类、参数回归都融合成在了一个CNN网络中了，而RCNN分成了三个部分。</p> 
<p>Faster RCNN进一步将所有过程都融入了CNN中。</p> 
<h2><a id="_267"></a>小知识补充：</h2> 
<h3><a id="_269"></a>计算感受野</h3> 
<p>计算Faster RCNN中ZF网络feature map 中3x3滑动窗口在原图中感受野的大小。<font color="red">为什么这么计算呢？</font></p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/168b7721a4faf75bac8f55788610822d.png" alt="image-20210825103950358"></p> 
<h3><a id="1x1_275"></a>1x1卷积核</h3> 
<p>1x1卷积核改变输出通道数（channels），而不改变输出的宽度和高度。1x1卷积的作用是减少或增加channel的数量（降维\升维、跨通道信息交互。（<a href="https://zhuanlan.zhihu.com/p/40050371">参考此链接</a>）</p> 
<h1><a id="4_FPNFeature_Pyramid_Networks_279"></a>4. FPN(Feature Pyramid Networks)</h1> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/d20ba222afb15d9327ece00b1eb869d9.png" alt="image-20210828141402246"></p> 
<p>（a）将图片缩放到不同的大小，并将对不同大小的图片进行预测。此种方法要进行多次预测，效率很低。</p> 
<p>（b）通过backbone（主干网络）得到最终的特征图，然后在特征图上进行预测，此种方法就是Fast RCNN中用到的方法。此种方法对小目标的预测效果不佳，这是因为大目标占有的像素点比较多，小目标占有的像素点比较少，即小目标对特征图的形成起到的作用比较小，即特征图中包含较少的小目标的信息。</p> 
<p>（c）对每一层产生的特征图进行预测，和SDD算法类似</p> 
<p>（d）对不同的特征图进行融合，也就是FPN。下图是FPN网络的一些细节。</p> 
<p><img src="https://img-blog.csdnimg.cn/img_convert/9a25383c68cf8eaec112af6eeeb8657f.png" alt="image-20210828143249233"></p> 
<p>​ 可以看到，FPN将每一层的特征图都经过256个1*1的卷积核变成channel为256的特征图。然后上层的特征图通过上采样使得特征图的shape和下层的特征图的shape一样，最后两特征图的对应位置直接相加，从而实现融合。P2到P5的特征图用于Fast RCNN，P2到P6用于RPN。（Faster RCNN=Fast RCNN+RPN）</p> 
<p>​ Fast RCNN进行预测：对不同大小的目标采用不同的特征图进行预测，目标较小就使用较底层的特征图。因为较底层的特征图中小目标的信息损失没那么严重。这里的目标指的就是RPN得到候选框。通过以下公式得到此目标（候选框里的内容）需要利用哪个特征图进行预测：</p> 
<p>​ <span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        k
       
       
        =
       
       
        ⌊
       
       
        
         k
        
        
         0
        
       
       
        +
       
       
        l
       
       
        o
       
       
        
         g
        
        
         2
        
       
       
        (
       
       
        
         
          
           w
          
          
           h
          
         
        
        
         244
        
       
       
        )
       
       
        ⌋
       
      
      
       k=\lfloor k_0+log_2(\frac{\sqrt {wh}}{244}) \rfloor
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.69444em; vertical-align: 0em;"></span><span class="mord mathdefault" style="margin-right: 0.03148em;">k</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mopen">⌊</span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.03148em;">k</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.301108em;"><span class="" style="top: -2.55em; margin-left: -0.03148em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">0</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.222222em;"></span></span><span class="base"><span class="strut" style="height: 1.39549em; vertical-align: -0.345em;"></span><span class="mord mathdefault" style="margin-right: 0.01968em;">l</span><span class="mord mathdefault">o</span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.03588em;">g</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.301108em;"><span class="" style="top: -2.55em; margin-left: -0.03588em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mopen">(</span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.05049em;"><span class="" style="top: -2.655em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">2</span><span class="mord mtight">4</span><span class="mord mtight">4</span></span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.394em;"><span class="pstrut" style="height: 3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord sqrt mtight"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.937845em;"><span class="svg-align" style="top: -3em;"><span class="pstrut" style="height: 3em;"></span><span class="mord mtight" style="padding-left: 0.833em;"><span class="mord mathdefault mtight" style="margin-right: 0.02691em;">w</span><span class="mord mathdefault mtight">h</span></span></span><span class="" style="top: -2.89785em;"><span class="pstrut" style="height: 3em;"></span><span class="hide-tail mtight" style="min-width: 0.853em; height: 1.08em;">
                   <svg width="400em" height="1.08em" viewBox="0 0 400000 1080" preserveAspectRatio="xMinYMin slice">
                    <path d="M95,702c-2.7,0,-7.17,-2.7,-13.5,-8c-5.8,-5.3,-9.5,
-10,-9.5,-14c0,-2,0.3,-3.3,1,-4c1.3,-2.7,23.83,-20.7,67.5,-54c44.2,-33.3,65.8,
-50.3,66.5,-51c1.3,-1.3,3,-2,5,-2c4.7,0,8.7,3.3,12,10s173,378,173,378c0.7,0,
35.3,-71,104,-213c68.7,-142,137.5,-285,206.5,-429c69,-144,104.5,-217.7,106.5,
-221c5.3,-9.3,12,-14,20,-14H400000v40H845.2724s-225.272,467,-225.272,467
s-235,486,-235,486c-2.7,4.7,-9,7,-19,7c-6,0,-10,-1,-12,-3s-194,-422,-194,-422
s-65,47,-65,47z M834 80H400000v40H845z"></path>
                   </svg></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.102155em;"><span class=""></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.345em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mclose">)</span><span class="mclose">⌋</span></span></span></span></span></p> 
<p>​ <span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        
         k
        
        
         0
        
       
       
        =
       
       
        4
       
      
      
       k_0=4
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.84444em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.03148em;">k</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.301108em;"><span class="" style="top: -2.55em; margin-left: -0.03148em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">0</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 0.64444em; vertical-align: 0em;"></span><span class="mord">4</span></span></span></span></span>,w和h是候选框的宽和高，k指的是特征图P的下标。</p> 
<p>​ RPN生成候选框：上一章中的Faster RCNN是在一个特征图上预测不同大小的anchor，但是在FPN中是在不同的特征图上预测不同大小的anchor，即P2到P6分别预测{<!-- --><span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        3
       
       
        
         2
        
        
         2
        
       
       
        ,
       
       
        6
       
       
        
         4
        
        
         2
        
       
       
        ,
       
       
        12
       
       
        
         8
        
        
         2
        
       
       
        ,
       
       
        25
       
       
        
         6
        
        
         2
        
       
       
        ,
       
       
        51
       
       
        
         2
        
        
         2
        
       
      
      
       32^2,64^2,128^2,256^2,512^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 1.00855em; vertical-align: -0.19444em;"></span><span class="mord">3</span><span class="mord"><span class="mord">2</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">6</span><span class="mord"><span class="mord">4</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">1</span><span class="mord">2</span><span class="mord"><span class="mord">8</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">2</span><span class="mord">5</span><span class="mord"><span class="mord">6</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">5</span><span class="mord">1</span><span class="mord"><span class="mord">2</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>}，就是P2对应<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        3
       
       
        
         2
        
        
         2
        
       
      
      
       32^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.814108em; vertical-align: 0em;"></span><span class="mord">3</span><span class="mord"><span class="mord">2</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>、P3对应<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        6
       
       
        
         4
        
        
         2
        
       
      
      
       64^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.814108em; vertical-align: 0em;"></span><span class="mord">6</span><span class="mord"><span class="mord">4</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>……。每一尺寸都对应三个比例，即{1:2,1:1,2:1}，如P2对应<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        3
       
       
        
         2
        
        
         2
        
       
      
      
       32^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.814108em; vertical-align: 0em;"></span><span class="mord">3</span><span class="mord"><span class="mord">2</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>，<span class="katex--inline"><span class="katex"><span class="katex-mathml">
    
     
      
       
        3
       
       
        
         2
        
        
         2
        
       
      
      
       32^2
      
     
    </span><span class="katex-html"><span class="base"><span class="strut" style="height: 0.814108em; vertical-align: 0em;"></span><span class="mord">3</span><span class="mord"><span class="mord">2</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.814108em;"><span class="" style="top: -3.063em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span></span></span>又分为{1:2,1:1,2:1}。</p> 
<h1><a id="_307"></a>思考题</h1> 
<p>我对为什么这些人能想到这些优化和方法的理解？？</p>
                