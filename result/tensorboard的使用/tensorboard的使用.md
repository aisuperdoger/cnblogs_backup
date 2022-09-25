原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522399.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>TensorBoard 是 TensorFlow提供的一组可视化工具（a suite of visualization tools），可以帮助开发者方便的理解、调试、优化TensorFlow 程序</p> 
<pre><code>from torch.utils.tensorboard import SummaryWriter
import numpy as np
from PIL import Image

writer = SummaryWriter("logs")
image_path = "img.png"
img_PIL = Image.open(image_path)
img_array = np.array(img_PIL)
print(type(img_array))
print(img_array.shape)

writer.add_image("train", img_array, 1, dataformats='HWC')
# y = 2x
for i in range(100):
    writer.add_scalar("y=2x", 3*i, i)

writer.close()
</code></pre> 
<pre><code># 命令行中执行以下代码，启动tensorboard
tensorboard --logdir=logs # logs是运行上面程序后生成的
</code></pre>
                