原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/17/16282619.html
提交日期：Tue, 17 May 2022 14:06:00 GMT
博文内容：
Linux下端口被占用（例如端口3000），关掉端口占用的进程的方法：
```
# 查询进程号
# netstat -tln | grep 8090
sudo lsof -i:8090
# 杀死进程
sudo kill -9 进程号
```