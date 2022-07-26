原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/06/24/16409963.html
提交日期：Fri, 24 Jun 2022 10:55:00 GMT
博文内容：

**大部分在 crontab 计划任务中都会年到未尾带 >/dev/null 2>&1,是什么意思呢？**

\>是重定向
/dev/null 代表空设备文件
1 表示stdout标准输出,系统默认值是1,所以 ">/dev/null" 等同于 "1>/dev/null"
2 表示stderr标准错误
& 表示等同于的意思,2>&1,表示2的输出重定向等同于1

整句的意思就是标准输出重定向到空设备文件,也就是不输出任何信息到终端,标准错误输出重定向等同于标准输出,因为之前标准输出已经重定向到了空设备文件,所以标准错误输出也重定向到空设备文件

运行脚本的时候有些错误不想让它显示，就输出到/dev/null
 

**command > file 2>file 与 command > file 2>&1 有什么区别呢?**

command > file 2>file 的意思是将命令所产生的标准输出信息,和错误的输出信息送到file 中.command > file 2>file 这样的写法,stdout和stderr都直接送到file中, file会被打开两次,这样stdout和stderr会互相覆盖,这样写相当使用了FD1和FD2两个同时去抢占file 的管道.
而command >file 2>&1 这条命令就将stdout直接送向file, stderr 继承了FD1管道后,再被送往file,此时,file 只被打开了一次,也只使用了一个管道FD1,它包括了stdout和stderr的内容.
从IO效率上,前一条命令的效率要比后面一条的命令效率要低,所以在编写shell脚本的时候,较多的时候我们会用command > file 2>&1 这样的写法.

**所以在添加crontab命令时，无论命令是否有输出，最好都加上输出重定向到文件或者/dev/null中。如下**

*/5 * * * * /root/XXXX.sh &>/dev/null 2>&1

/dev/null 代表空设备文件

\> 代表重定向到哪里，例如：echo "123" > /home/123.txt

1 表示stdout标准输出，系统默认值是1，所以">/dev/null"等同于"1>/dev/null"

2 表示stderr标准错误

& 表示等同于的意思，2>&1，表示2的输出重定向等同于1

那么>/dev/null 2>&1的意思就是：

标准输出重定向到空设备文件,也就是不输出任何信息到终端,标准错误输出重定向等同于标准输出,因为之前标准输出已经重定向到了空设备文件,所以标准错误输出也重定向到空设备文件。

 

示例:

每天早上6点 
0 6 * * * echo "Good morning." >> /tmp/test.txt //注意单纯echo，从屏幕上看不到任何输出，因为cron把任何输出都email到root的信箱了。

每两个小时 
0 */2 * * * echo "Have a break now." >> /tmp/test.txt 

好文要顶 关注我 收藏该文  


参考：[链接](https://www.cnblogs.com/gyrgyr/p/11367843.html)