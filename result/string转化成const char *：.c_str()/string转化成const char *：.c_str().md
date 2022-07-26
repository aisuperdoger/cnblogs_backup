原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/25/16516505.html
提交日期：Mon, 25 Jul 2022 02:15:00 GMT
博文内容：
string result_path = "images/" + labels + "/image" + s1 + ".jpg";
FILE *file = fopen(result_path.c_str(), "r")