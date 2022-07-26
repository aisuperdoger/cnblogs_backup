原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/08/16459838.html
提交日期：Fri, 08 Jul 2022 14:41:00 GMT
博文内容：
我的原因：
使用gcc  avframe.c avpacket.c  main.c -o main -I /home/ubuntu1/softwares/ffmpeg/include -L /home/ubuntu1/softwares/ffmpeg/lib/ -l avcodec -l avutil  -lm 生成可执行文件main，然后运行main的时候，发现运行时动态库找不到，原来是我忘记加-Wl,-rpath了。
此时加上-Wl,-rpath：gcc  avframe.c avpacket.c  main.c -o main -I /home/ubuntu1/softwares/ffmpeg/include -L /home/ubuntu1/softwares/ffmpeg/lib/ -l avcodec -l avutil  -lm -Wl,-rpath=/home/ubuntu1/softwares/ffmpeg/lib/，然后重新运行main。此时发现动态库还是找不到。
原因是因为前面运行的可执行文件main没有删除，要删除main以后，再重新进行编译。