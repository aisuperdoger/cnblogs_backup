原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/25/16516545.html
提交日期：Mon, 25 Jul 2022 02:21:00 GMT
博文内容：
```
time_t curr_time;
time(&curr_time);
char *curr_time2 = asctime(localtime(&curr_time));
regex pattern1(" "); // 规则一：匹配空格
regex pattern2("\n"); // 规则二：匹配换行
string s1 = regex_replace(regex_replace(curr_time2, pattern1, "_"), pattern2, "");
```