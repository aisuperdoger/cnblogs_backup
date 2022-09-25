原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522422.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <pre class="has"><code class="language-html"> 1，“ { % if verified %}
        &lt;em&gt;你通过了验证&lt;/em&gt;
    { % else % }
        &lt;em&gt;密码或账号打错了&lt;/em&gt;
    { % endif % }” 被直接打印出来？
解决方法：将“{”和“%”的之间的空格去掉</code></pre>
                