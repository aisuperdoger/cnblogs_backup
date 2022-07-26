原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/01/16433421.html
提交日期：Fri, 01 Jul 2022 01:30:00 GMT
博文内容：
C++ opencv保存mp4文件
```
cv::VideoWriter w_cap("re_video.mp4", VideoWriter::fourcc('m', 'p', '4', 'v'), rate, cv::Size(width, height));
// VideoWriter::fourcc('m', 'p', '4', 'v')中的mp4v都要小写才不会报错，操!
```