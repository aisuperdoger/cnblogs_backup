原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/08/05/16553436.html
提交日期：Fri, 05 Aug 2022 02:12:00 GMT
博文内容：
下面语句g++无法编译通过，但是gcc可以。
```
void *vptr
char *ptr;
ptr = vptr;
```