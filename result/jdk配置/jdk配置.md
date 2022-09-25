原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522434.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <p>1，安装JDK 选择安装目录 安装过程中会出现两次 安装提示 。第一次是安装 jdk ，第二次是安装 jre 。建议两个都安装在同一个java文件夹中的不同文件夹中。（不能都安装在java文件夹的根目录下，jdk和jre安装在同一文件夹会出错）</p> 
<p>如图为正确做法：</p> 
<p><a href="http://jingyan.baidu.com/album/6dad5075d1dc40a123e36ea3.html?picindex=1"><img alt="JDK安装与环境变量配置" class="has" src="https://imgsa.baidu.com/exp/w=500/sign=261eb1c31d950a7b75354ec43ad0625c/6a63f6246b600c33ed52343d1a4c510fd9f9a118.jpg"></a></p> 
<p>2.安装完JDK后配置环境变量 &nbsp;计算机→属性→高级系统设置→高级→环境变量</p> 
<p>系统变量→新建 JAVA_HOME 变量 。</p> 
<p>变量值填写jdk的安装目录（本人是 E:\Java\jdk1.7.0)</p> 
<p>3.系统变量→寻找 Path 变量→编辑</p> 
<p>在变量值最后输入&nbsp;%JAVA_HOME%\bin（注意原来Path的变量值末尾有没有;号，如果没有，先输入；号再输入上面的代码）（注意原来Path的变量值末尾以“\”结尾的，就直接添加）</p> 
<p>4.新建 classpath 环境变量 ，classpath=.;%JAVA_HOME%\lib;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\tools.jar</p>
                