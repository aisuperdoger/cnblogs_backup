原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/17/16282625.html
提交日期：Tue, 17 May 2022 14:09:00 GMT
博文内容：
# 1.launch.json
新建launch.json，内容如下：

```
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "pythonPath":"/usr/bin/python3",
            "args":[
                
            ],
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}

```
【注】打开哪个文件，就会运行哪个文件。故运行文件A时，记得要打开文件A，然后再点运行。
