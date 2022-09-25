原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522385.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>参考：https://bbs.csdn.net/topics/397173456<br> 现象：当全拼输入2~3个汉字时，会被强行打断，然后就无法继续输入(也无法切换中英文)，并且汉字下会有下划线。<br> 解决方法：<br> 1.点击菜单 “Help | Edit Custom VM options…”<br> 2.添加 -Drecreate.x11.input.method=true 到最后一行<br> 3.重启IDEA</p>
                