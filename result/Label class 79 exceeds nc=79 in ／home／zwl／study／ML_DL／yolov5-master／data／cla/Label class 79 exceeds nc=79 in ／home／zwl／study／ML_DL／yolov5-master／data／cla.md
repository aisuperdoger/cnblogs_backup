原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/17/16282597.html
提交日期：Tue, 17 May 2022 14:01:00 GMT
博文内容：

错误：
Label class 79 exceeds nc=79 in /home/zwl/study/ML_DL/yolov5-master/data/cla
解决：
txt格式的labels每个种类标的是有序号的，序号从0开始以此递增。
我出现错误的原因是：有79个类，但序号却是从0到21，23到79，缺少了22。
故将序号改为0~79就行了
参考：[此链接的评论区](https://blog.csdn.net/qq_45714906/article/details/120528631)