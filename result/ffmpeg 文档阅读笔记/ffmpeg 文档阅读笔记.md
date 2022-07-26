原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/06/05/16344239.html
提交日期：Sun, 05 Jun 2022 08:19:00 GMT
博文内容：
# 1.ffmpeg简介
## 1.1.命令格式
```
ffmpeg [global_options] {[input_file_options] -i input_url} ... {[output_file_options] output_url} ...
```
-i：指定输入。输入可以是视频文件、网络流、音视频设备等。可以使用-i指定任意数量的输入。
输出：命令行上任意不能被解释成选项的东西，都被认为是输出。可以有任意数量的输出。
-map：一条ffmpeg命令中，可能有多个输入和输出。-map指定哪个输入对应哪个输出。如果没有使用-map进行指定，那么会使用默认的方法进行指定

-i后面跟索引，索引值从0开始。2:3代表第三个输入文件的第四个流。【不懂？？】

ffmpeg的每个选项按顺序对输入进行操作，即选项对输入进行操作的结果，送给下一个选项进行操作，故ffmpeg的选项的顺序很重要。全局选项（例如 verbosity level）是个例外，全局选项的位置不重要，但是一般放在最前面。

选项都只应用于最先遇到的文件。

## 1.2.ffmpeg的处理流程
```
 _______              ______________
|       |            |              |
| input |  demuxer   | encoded data |   decoder
| file  | ---------> | packets      | -----+
|_______|            |______________|      |
                                           v
                                       _________
                                      |         |
                                      | decoded |
                                      | frames  |
                                      |_________|
 ________             ______________       |
|        |           |              |      |
| output | <-------- | encoded data | <----+
| file   |   muxer   | packets      |   encoder
|________|           |______________|

```
使用libavformat库读取输入文件，获取到encoded data packets。When there are multiple input files, ffmpeg tries to keep them synchronized by tracking lowest timestamp on any active input stream.【这句英文看不懂】
decoder产生未压缩的帧（(raw video/PCM audio/...），然后可以进行filtering




# 2.Filtering

使用libavfilter库中的filter对decoder产生未压缩的帧进行处理，多个filter形成一个filter graph。filter分为simple和complex


## 2.1.Simple filtergraphs
Simple filtergraphs结构如下：
```
 _________                        ______________
|         |                      |              |
| decoded |                      | encoded data |
| frames  |\                   _ | packets      |
|_________| \                  /||______________|
             \   __________   /
  simple     _\||          | /  encoder
  filtergraph   | filtered |/
                | frames   |
                |__________|
```

通过-vf和-af分别指定视频和音频的filter



## 2.2. Complex filtergraphs
Complex filtergraphs结构如下
```
 _________
|         |
| input 0 |\                    __________
|_________| \                  |          |
             \   _________    /| output 0 |
              \ |         |  / |__________|
 _________     \| complex | /
|         |     |         |/
| input 1 |---->| filter  |\
|_________|     |         | \   __________
               /| graph   |  \ |          |
              / |         |   \| output 1 |
 _________   /  |_________|    |__________|
|         | /
| input 2 |/
|_________|

```
通过-lavfi指定Complex filtergraphs，-lavfi是一个全局选项


# 3.Stream copy

-codec copy 复制原始的编码规则，过程如下：
```
 _______              ______________            ________
|       |            |              |          |        |
| input |  demuxer   | encoded data |  muxer   | output |
| file  | ---------> | packets      | -------> | file   |
|_______|            |______________|          |________|

```
可以看到略过了decode和encode阶段



# Stream selection

-map：应该是用于控制哪个输入映射到哪个输出

-vn / -an / -sn / -dn分别使得视频、音频、字幕和数据流不输出


不采取-map时，自动采取什么样的流选择（从哪个输入映射到哪个输出称为流选择）

流包括视频、音频、字幕和数据（video, audio, subtitle and data streams）

没有-map时，默认采取以下措施：
检查输出格式是否包含video, audio，subtitles

选择视频中最高分辨率的视频
选择通道最多的音频
选择第一个字幕，并返回一个警告
参数相同时，选择索引最低的流
数据流不会被自动选择，需要使用-map指定


当-map被使用的时，输出文件就只包含-map指定的流。filtergraph outputs是个例外，

complex filtergraph output streams with unlabeled pads都会被添加到第一个输出文件中。 This will lead to a fatal error if the stream type is not supported by the output format. In the absence of the map option, the inclusion of these streams leads to the automatic stream selection of their types being skipped. If map options are present, these filtergraph streams are included in addition to the mapped streams.（看不懂）

Complex filtergraph output streams with labeled pads必须被map一次且只能一次


Stream handling独立于流选择，除了下面的字幕描述
Stream handling通过设置选项-codec实现`

stream selection之后，进行Stream handling

没有-codec选项，将使用the output file muxer的默认encoder



An exception exists for subtitles. If a subtitle encoder is specified for an output file, the first subtitle stream found of any type, text or image, will be included. ffmpeg does not validate if the specified encoder can convert the selected stream or if the converted stream is acceptable within the output format. This applies generally as well: when the user sets an encoder manually, the stream selection process cannot check if the encoded stream can be muxed into the output file. If it cannot, ffmpeg will abort and all output files will fail to be processed.（看不懂，为什么都没有实例说明，这他妈时官方文档吗？？？）



```bash
假设输入文件如下：
input file 'A.avi'
      stream 0: video 640x360
      stream 1: audio 2 channels

input file 'B.mp4'
      stream 0: video 1920x1080
      stream 1: audio 2 channels
      stream 2: subtitles (text)
      stream 3: audio 5.1 channels
      stream 4: subtitles (text)

input file 'C.mkv'
      stream 0: video 1280x720
      stream 1: audio 2 channels
      stream 2: subtitles (image)

命令：
ffmpeg -i A.avi -i B.mp4 out1.mkv out2.wav -map 1:a -c:a copy out3.mov

out1.mkv是Matroska container file，可以包含视频、音频和字幕文件。
    For video, it will select stream 0 from B.mp4, which has the highest resolution among all the input video streams.
    For audio, it will select stream 3 from B.mp4, since it has the greatest number of channels.
    For subtitles, it will select stream 2 from B.mp4, which is the first subtitle stream from among A.avi and B.mp4.

out2.wav：accepts only audio streams, so only stream 3 from B.mp4 is selected.
    
out3.mov
    -map 1:a   1代表选择第二个输入文件B.mp4;   a代表选择B.mp4中的所有音频文件。

out1.mkv和out2.wav使用了输出格式默认的编码器
out3.mov使用了copy到的编码器
```
