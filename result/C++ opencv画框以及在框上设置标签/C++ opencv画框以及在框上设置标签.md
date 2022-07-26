原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/11/16466816.html
提交日期：Mon, 11 Jul 2022 08:18:00 GMT
博文内容：

```
int baseline = 0;
string label_string = "labels....";

// 框出图像中的某个物体。cv::Point(a,b)，其中a是相对于图片左边的距离，b是相对于图片上边的距离
cv::rectangle(image, cv::Point(left, top), cv::Point(right, bottom), cv::Scalar(0, 0, 255));   

// text_size中存储文本的宽高；baseline是基线y-相对于最底部文本的基线坐标【我也看不太懂baseline是什么？】
cv::Size text_size = cv::getTextSize(label_string, FONT_HERSHEY_SIMPLEX, 0.4, 1, &baseline);   

// 给文本填充背景颜色。虽然我也看不太懂baseline是什么，但是你把下面的baseline去掉看看效果，就大概知道baseline是个什么了
cv::rectangle(image, cv::Point(left, top - text_size.height - baseline), cv::Point(left+ text_size.width, top), cv::Scalar(255, 0, 255), -1);  

// 添加文字标签
cv::putText(image, label_string, cv::Point(left, top - baseline), FONT_HERSHEY_SIMPLEX, 0.4, cv::Scalar(0, 255, 255));
```
		