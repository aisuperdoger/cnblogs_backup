原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522432.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <p>来自百度知道：<br> 　　在使用git 对源代码进行push到gitHub时可能会出错，信息如下<br><br> 　　此时很多人会尝试下面的命令把当前分支代码上传到master分支上。<br> 　　$ git push -u origin master<br> 　　但依然没能解决问题<br><br> 　　出现错误的主要原因是github中的README.md文件不在<a href="https://www.baidu.com/s?wd=%E6%9C%AC%E5%9C%B0%E4%BB%A3%E7%A0%81&amp;tn=SE_PcZhidaonwhc_ngpagmjz&amp;rsv_dl=gh_pc_zhidao">本地代码</a>目录中<br><br> 　　可以通过如下命令进行代码合并【注：pull=fetch+merge]<br> 　　git pull --rebase origin master<br><br> 　　执行上面代码后可以看到<a href="https://www.baidu.com/s?wd=%E6%9C%AC%E5%9C%B0%E4%BB%A3%E7%A0%81&amp;tn=SE_PcZhidaonwhc_ngpagmjz&amp;rsv_dl=gh_pc_zhidao">本地代码</a>库中多了README.md文件</p>
                