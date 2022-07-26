原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/05/16445936.html
提交日期：Tue, 05 Jul 2022 04:00:00 GMT
博文内容：

在执行makefile文件时，出现如下错误：
```
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFReadDirectory@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFWriteEncodedStrip@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFIsTiled@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFOpen@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFReadEncodedStrip@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFSetField@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFWriteScanline@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFGetField@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFScanlineSize@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFWriteDirectory@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFSetWarningHandler@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFSetErrorHandler@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFReadEncodedTile@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFReadRGBATile@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFClose@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFRGBAImageOK@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFClientOpen@LIBTIFF_4.0’未定义的引用
/home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so：对‘TIFFReadRGBAStrip@LIBTIFF_4.0’未定义的引用
```
查找libopencv_imgcodecs.so的依赖：
```
ldd /home/zwl/software/opencv4.2/lib/libopencv_imgcodecs.so
        linux-vdso.so.1 (0x00007fff9c1f0000)
        libopencv_imgproc.so.4.2 => /home/zwl/software/opencv4.2/lib/libopencv_imgproc.so.4.2 (0x00007f1a4e0cc000)
        libjpeg.so.8 => /usr/lib/x86_64-linux-gnu/libjpeg.so.8 (0x00007f1a4de64000)
        libpng16.so.16 => /usr/lib/x86_64-linux-gnu/libpng16.so.16 (0x00007f1a4dc32000)
        libtiff.so.5 => /usr/lib/x86_64-linux-gnu/libtiff.so.5 (0x00007f1a4d9ba000)
        libopencv_core.so.4.2 => /home/zwl/software/opencv4.2/lib/libopencv_core.so.4.2 (0x00007f1a4d34f000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f1a4d132000)
        libstdc++.so.6 => /usr/lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f1a4cda9000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f1a4ca0b000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f1a4c7f3000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f1a4c5d4000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1a4c1e3000)
        liblzma.so.5 => /lib/x86_64-linux-gnu/liblzma.so.5 (0x00007f1a4bfbd000)
        libjbig.so.0 => /usr/lib/x86_64-linux-gnu/libjbig.so.0 (0x00007f1a4bdaf000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f1a4bbab000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007f1a4b9a3000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f1a4ee11000)
```
从libtiff.so.5 => /usr/lib/x86_64-linux-gnu/libtiff.so.5 (0x00007f1a4d9ba000)可看出：libopencv_imgcodecs.so依赖libtiff.so.5，且libtiff.so.5在目录 /usr/lib/x86_64-linux-gnu/下。
也就是说libopencv_imgcodecs.so库会去目录 /usr/lib/x86_64-linux-gnu/下查找依赖libtiff.so.5

然后我发现我用-L指定的目录$(python_path)/lib下也有库libtiff，这就是问题所在：
libopencv_imgcodecs.so首先会去目录$(python_path)/lib下查找库libtiff，然后就找到了libtiff，但是由于版本不一致，就会出现上面的错误。

解决方法：让libopencv_imgcodecs.so先去查找目录 /usr/lib/x86_64-linux-gnu/，而不是目录$(python_path)/lib，即在-L $(python_path)/lib前加上-L /usr/lib/x86_64-linux-gnu/，即：
-L /usr/lib/x86_64-linux-gnu/ -L $(python_path)/lib


出现以上错误，是由于版本不一致导致的。