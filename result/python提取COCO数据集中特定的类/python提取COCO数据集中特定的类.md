原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522345.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <pre><code class="prism language-cpp"><span class="token keyword">import</span> <span class="token module">os</span>
from shutil <span class="token keyword">import</span> <span class="token module">copyfile</span><span class="token punctuation">,</span>move

src_path <span class="token operator">=</span> <span class="token char">'./labels/train2017/'</span>  # 标签
img_path <span class="token operator">=</span> <span class="token char">'./images/train2017/'</span>  # 图像
dst_label_path <span class="token operator">=</span> <span class="token char">'./traffic_train_coco/labels/'</span>
dst_img_path <span class="token operator">=</span> <span class="token char">'./traffic_train_coco/images/'</span>
cls_id <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token char">'79'</span><span class="token punctuation">]</span>  # 牙刷

labels <span class="token operator">=</span> os<span class="token punctuation">.</span><span class="token function">listdir</span><span class="token punctuation">(</span>src_path<span class="token punctuation">)</span>
labels<span class="token punctuation">.</span><span class="token function">sort</span><span class="token punctuation">(</span><span class="token punctuation">)</span>

<span class="token keyword">for</span> label in labels<span class="token operator">:</span>
    <span class="token keyword">if</span> label<span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span> <span class="token operator">!=</span> <span class="token char">'t'</span><span class="token operator">:</span>
        <span class="token keyword">continue</span>
    # 存标签
    tmp <span class="token operator">=</span> <span class="token number">0</span>
    <span class="token keyword">for</span> line in <span class="token function">open</span><span class="token punctuation">(</span>src_path <span class="token operator">+</span> <span class="token char">'/'</span> <span class="token operator">+</span> label<span class="token punctuation">)</span><span class="token operator">:</span>
        str_list <span class="token operator">=</span> line<span class="token punctuation">.</span><span class="token function">split</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
        # 被选类别的标签
        <span class="token keyword">for</span> i in <span class="token function">range</span><span class="token punctuation">(</span><span class="token function">len</span><span class="token punctuation">(</span>cls_id<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token operator">:</span>
            <span class="token keyword">if</span> str_list<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span> <span class="token operator">==</span> cls_id<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token operator">:</span>
                # 改成自己的标签，这里是数组下标
                tmp <span class="token operator">=</span><span class="token number">1</span>
                <span class="token keyword">break</span>
    # 没有被选类别
    <span class="token keyword">if</span> tmp <span class="token operator">==</span> <span class="token number">0</span><span class="token operator">:</span>
        <span class="token keyword">continue</span>
    # 新的标签文件
    <span class="token function">move</span><span class="token punctuation">(</span>src_path <span class="token operator">+</span> <span class="token char">'/'</span> <span class="token operator">+</span> label<span class="token punctuation">,</span> dst_label_path <span class="token operator">+</span> <span class="token char">'/'</span> <span class="token operator">+</span> label<span class="token punctuation">)</span>
    <span class="token macro property"><span class="token directive-hash">#</span> <span class="token directive keyword">copyfile</span><span class="token expression"><span class="token punctuation">(</span>src_path <span class="token operator">+</span> </span><span class="token char">'/'</span> <span class="token expression"><span class="token operator">+</span> label<span class="token punctuation">,</span> dst_label_path <span class="token operator">+</span> </span><span class="token char">'/'</span> <span class="token expression"><span class="token operator">+</span> label<span class="token punctuation">)</span></span></span>

    image <span class="token operator">=</span> label<span class="token punctuation">[</span><span class="token operator">:</span><span class="token operator">-</span><span class="token number">4</span><span class="token punctuation">]</span> <span class="token operator">+</span> <span class="token char">'.jpg'</span>
    # 拷贝有被选类别的图片
    <span class="token function">move</span><span class="token punctuation">(</span>img_path <span class="token operator">+</span> <span class="token char">'/'</span> <span class="token operator">+</span> image<span class="token punctuation">,</span> dst_img_path <span class="token operator">+</span> image<span class="token punctuation">)</span>
    <span class="token macro property"><span class="token directive-hash">#</span> <span class="token directive keyword">copyfile</span><span class="token expression"><span class="token punctuation">(</span>img_path <span class="token operator">+</span> </span><span class="token char">'/'</span> <span class="token expression"><span class="token operator">+</span> image<span class="token punctuation">,</span> dst_img_path <span class="token operator">+</span> image<span class="token punctuation">)</span></span></span>


</code></pre> 
<p>参考：<a href="https://blog.csdn.net/ManiacLook/article/details/121951887">链接</a></p>
                