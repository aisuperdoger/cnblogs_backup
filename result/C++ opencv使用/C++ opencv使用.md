原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/24/16307407.html
提交日期：Tue, 24 May 2022 14:10:00 GMT
博文内容：
# 安装
请参考：[C++ opencv安装和使用](https://blog.csdn.net/weixin_44796670/article/details/115900538)

通过以下命令，将opencv安装到指定目录中：
```
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/home/ubuntu1/test_c++/opencv  ..
```
将C++ opencv安装到指定目录下以后，可以看到有四个目录bin、include、lib 和 share,分别包含了可执行文件、头文件、库文件和cmake配置文件。在这里,我们只需用到 include 和 lib 这两个文件夹,
  


为什么在OpenCV 3.x和OpenCV 4.x中都有有一个opencv2文件夹？
基于C的OpenCV是API v1，基于C ++的OpenCV是API v2。库版本现在为3.x或4.x，但它们仍使用相同的基于C ++的API。因此，OpenCV构建仍将其头文件保存在opencv2文件夹中。也就是说opencv2代表此库用于C++。


lib中各个库都代表什么？什么时候需要引入什么库？？？


# 使用

只能保存avi，mp4格式编码方式有点迷


```
// 画框cv::rectangle(图片,左上点,右上点,框的颜色);
cv::rectangle(image, cv::Point(400, 400), cv::Point(450, 450), cv::Scalar(0, 0, 255));
```

opencv读取图片：
```
//main.cpp

#include <opencv2/opencv.hpp>
#include<iostream>

int main(int argc, char const *argv[])
{
    cv::VideoCapture cap;
    cap.open("human.mp4");

    if (!cap.isOpened())
        return 0;


  
    cv::Mat frame;
    while(1) {
        cap >> frame;
        if (frame.empty())
            break;
        cv::imshow("hello", frame);
        cv::waitKey(50);
    }
    cap.release();

    return 0;
}
```
使用g++进行编译：
```
g++ main.cpp -Wl,-rpath=./opencv/lib -L ./opencv/lib  -l opencv_core -l opencv_imgproc -l opencv_videoio -l opencv_imgcodecs -l opencv_highgui -I ./opencv/include/opencv4 -o app 

-Wl,-rpath：运行阶段，在这个目录下查找库文件
-L：编译阶段，在这个目录下查找库文件
-l：-L指向目录，-l指向具体的库。
-I：指向头文件所在目录
命令具体可参考：https://www.cnblogs.com/codingbigdog/p/16320965.html
```
