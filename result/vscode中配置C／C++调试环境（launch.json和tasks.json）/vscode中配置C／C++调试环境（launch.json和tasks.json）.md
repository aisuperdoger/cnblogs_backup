原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/08/16459417.html
提交日期：Fri, 08 Jul 2022 11:09:00 GMT
博文内容：
# launch.json和tasks.json
## launch.json


launch.json中存放运行或者调试可执行文件时的配置：
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "g++.exe build and debug active file",
            "type": "cppdbg",
            "request": "launch",
            "program": "${fileDirname}\\${fileBasenameNoExtension}",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "/usr/bin/gdb",
            "setupCommands": [
                {
                    "description": "为 gdb 启用整齐打印",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "g++.exe build active file"
        }
    ]
}
```
首先使用cmake和make生成可调试的可执行文件，在launch.json中的program字段设置可执行文件所在位置，如设置program为：
```
"program": "${workspaceFolder}/build/my_cmake_exe"
// ${workspaceFolder}/build/my_cmake_exe代表在当前目录下的build文件夹中的可执行文件my_cmake_exe，是一个绝对路径。
```
配置好launch.json文件，我们就可以通过vscode的调试菜单对可执行文件进行调试了。


## tasks.json

tasks.json中存放生成可执行文件的命令：
```
{
    "version": "2.0.0",
    "options": {
        "cwd": "${workspaceFolder}/build"   // 进入本项目目录下的build文件夹下
    },
    "tasks": [
        {
            "type": "shell",
            "label": "cmake",          // 名字
            "command": "cmake",        // 执行cmake命令，参数为..
            "args": [
                ".."
            ]
        },
        {
            "label": "make",
            "group": {            // 不知道有什么用？
                "kind": "build",
                "isDefault": true
            },
            "command": "make",
            "args": [

            ]
        },
        {
            "label": "Build",
            "dependsOrder": "sequence", // 按列出的顺序执行任务依赖项
            "dependsOn":[
                "cmake",
                "make"
            ]
        }
    ]

}
```
在tasks.json中建立了三个任务，分别为Build、cmake和make，其中Build依赖cmake和make。Build任务的含义为：使用cmake和make生成可执行文件。
我们可以将launch.json中的preLaunchTask设置为"preLaunchTask": "Build"，那么在使用launch.json进行调试前，会先执行Build的任务。



launch.json和tasks.json的其他字段？？
