原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522360.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>ctrl-z: 挂起在命令行窗口运行的进程，而并非结束进程，用户可以在命令行窗口中输入fg/bg来让进程继续执行。<br> 输入fg：在前台执行（在当前命令行窗口执行），此时可以使用ctrl-z再次挂起该进程<br> 输入bg：在后台执行（在当前命令行窗口看不到执行过程），<br> 一个比较常用的功能：正在使用vi编辑一个文件时，需要执行shell命令查询一些需要的信息，可以使用ctrl-z挂起vi，等执行 完shell命令后再使用fg恢复vi继续编辑你的文件（当然，也可以在vi中使用！command方式执行shell命令，但是没有该方法方便）。</p> 
<p>参考：https://blog.csdn.net/mylizh/article/details/38385739</p>
                