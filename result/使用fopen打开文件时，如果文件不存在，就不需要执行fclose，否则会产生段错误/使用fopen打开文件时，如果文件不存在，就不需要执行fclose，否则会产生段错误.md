原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/24/16514423.html
提交日期：Sun, 24 Jul 2022 05:59:00 GMT
博文内容：
使用fopen打开文件时，如果文件不存在，就不需要执行fclose，否则会产生段错误，如下：
```
// test.cpp  
#include <stdio.h>

int main() {
    FILE *outfp_ = NULL;
    outfp_ = fopen("output.h264", "rb");
    if (outfp_ == NULL ){
      fclose(outfp_);
    }
}
```
由于output.h264文件不存在，那么上述代码就会产生段错误，执行过程如下：
```
g++ test.cpp 
./a.out 
Segmentation fault (core dumped)
```