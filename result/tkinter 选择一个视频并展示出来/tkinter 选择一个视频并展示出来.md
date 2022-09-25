原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522394.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h3><a id="1_0"></a>1.选择视频文件</h3> 
<pre><code>from tkinter.filedialog import askdirectory,askopenfilename
from tkinter import *

def selectPath():
    path_ = askopenfilename()
    path.set(path_)

root = Tk()
path = StringVar()
Label(root,text = "目标路径:").grid(row = 0, column = 0)
Entry(root, textvariable = path).grid(row = 0, column = 1) 
Button(root, text = "路径选择", command = selectPath).grid(row = 0, column = 2)

root.mainloop()
</code></pre> 
<h3><a id="2_18"></a>2、展示视频</h3> 
<pre><code>from tkinter import *

import camera as camera
import cv2
from PIL import Image, ImageTk

def video_play():
    while video.isOpened():
        ret, frame = video.read()  # 读取照片
        # print('读取成功')
        if ret == True:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # 转换颜色使播放时保持原有色彩
            current_image = Image.fromarray(img).resize((540, 320))  # 将图像转换成Image对象
            imgtk = ImageTk.PhotoImage(image=current_image)
            movieLabel.imgtk = imgtk
            movieLabel.config(image=imgtk)
            movieLabel.update()  # 每执行以此只显示一张图片，需要更新窗口实现视频播放

video = cv2.VideoCapture('1.mp4')  # 使用opencv打开本地视频文件
root = Tk()
root.title('视频播放案例')
Label(root,text = "视频播放案例'").grid(row = 0, column = 0)
movieLabel = Label(root)  # 创建一个用于播放视频的label容器

movieLabel.grid(row = 1, column = 0,padx=10, pady=10)

video_play()  # 调用video_play实现视频播放

mainloop()
camera.release()
cv2.destroyAllWindonws()
</code></pre> 
<h3><a id="3__53"></a>3、 选择一个视频并展示出来</h3> 
<pre><code>from tkinter.filedialog import askdirectory,askopenfilename
from tkinter import *

import camera as camera
import cv2
from PIL import Image, ImageTk



def selectPath():
    path_ = askopenfilename()
    path.set(path_)

    video_path = path_
    if video_path[-3:] == "mp4":
        video = cv2.VideoCapture(video_path)
        while video.isOpened():
            ret, frame = video.read()  # 读取照片
            # print('读取成功')
            if ret == True:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # 转换颜色使播放时保持原有色彩
                current_image = Image.fromarray(img).resize((540, 320))  # 将图像转换成Image对象
                imgtk = ImageTk.PhotoImage(image=current_image)
                movieLabel.imgtk = imgtk
                movieLabel.config(image=imgtk)
                movieLabel.update()  # 每执行以此只显示一张图片，需要更新窗口实现视频播放

root = Tk()
path = StringVar()

# layout
Label(root,text = "目标路径:").grid(row = 0, column = 0)
Entry(root, textvariable = path).grid(row = 0, column = 1)
Button(root, text = "路径选择", command = selectPath).grid(row = 0, column = 2)

movieLabel = Label(root)  # 创建一个用于播放视频的label容器
movieLabel.grid(row = 1, column = 0,padx=10, pady=10)


mainloop()
camera.release()
cv2.destroyAllWindonws()
</code></pre>
                