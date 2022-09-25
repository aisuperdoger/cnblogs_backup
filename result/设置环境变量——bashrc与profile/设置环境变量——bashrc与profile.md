原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522368.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>bashrc与profile都用于保存用户的环境信息，bashrc用于交互式non-loginshell，而profile用于交互式login shell。（这句我没看懂）</p> 
<p>/etc/profile，/etc/bashrc 是系统全局环境变量设定<br> ~/.profile，~/.bashrc用户目录下的私有环境变量设定</p> 
<p>当登入系统获得一个shell进程时，其读取环境设置脚本分为三步:<br> 1.首先读入的是全局环境变量设置文件/etc/profile，然后根据其内容读取额外的文档，如/etc/profile.d和/etc/inputrc<br> 2.读取当前登录用户Home目录下的文件~/.bash_profile，其次读取~/.bash_login，最后读取~/.profile，这三个文档设定基本上是一样的，读取有优先关系<br> 3.读取~/.bashrc<br> ~/.profile与~/.bashrc的区别:</p> 
<ul><li>这两者都具有个性化定制功能</li><li>~/.profile可以设定本用户专有的路径，环境变量，等，它只能登入的时候执行一次</li><li>~/.bashrc也是某用户专有设定文档，可以设定路径，命令别名，每次shell script的执行都会使用它一次</li></ul>
                