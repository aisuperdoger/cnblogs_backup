原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522424.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <p>1，&nbsp; HDLC，它是一种ISO标准数据链路层协议，用于封装同步串行链路上的数据。（同步串行链路什么意思，封装有是什么意思？封装什么）。</p> 
<p>2,HDLC传送的信息单位为帧（帧是什么意思？？）。它是面向比特的同步数据链路层协议（？？面向比特流？？）。其最大的特点是不需要数据必须是规定的字符集，对任何一种比特流，均可以实现透明的传输。</p> 
<p>3，HDLC具有如下特点（HDLC是什么都不知道，下面这些话一句都不理解）：</p> 
<p style="margin-left:0pt;">1、协议不依赖于任何一种字符编码集；</p> 
<p style="margin-left:0pt;">2、数据报文可透明传输，用于透明传输的“0比特插入法”易于硬件实现；</p> 
<p style="margin-left:0pt;">3、全双工通讯，不必等待确认可连续发送数据，有较高的数据链路传输效率；</p> 
<p style="margin-left:0pt;">4、所有帧均采用CRC校验，对信息帧进行顺序编号，可防止漏收或重收，传输可靠性高；</p> 
<p style="margin-left:0pt;">5、传输控制功能与处理功能分离，具有较大的灵活性和较完善的控制功能。</p> 
<p style="margin-left:0pt;">标准HDLC协议族中的协议都是运行于同步串行线路之上。</p> 
<p>&nbsp;</p> 
<p>4，下面对HDLC帧的介绍（什么狗屁不通，我都不知道HDLC是什么鬼）</p> 
<p style="margin-left:0pt;">HDLC的完整的帧由标志字段（F）、地址字段（A）、控制字段（C）、信息字段（I）、帧校验序列字段（FCS）等组成。</p> 
<p style="margin-left:0pt;">标志字段（F）</p> 
<p style="margin-left:0pt;">标志字段为01111110的比特模式，用以标志帧的开始与结束，也可以作为帧与帧之间的填充字符。</p> 
<p style="margin-left:0pt;">地址字段（A）</p> 
<p style="margin-left:0pt;">地址字段携带的是地址信息。</p> 
<p style="margin-left:0pt;">控制字段（C）</p> 
<p style="margin-left:0pt;">控制字段用于构成各种命令及响应，以便对链路进行监视与控制。发送方主节点或组合节点利用控制字段来通知被寻址的从节点或组合节点执行约定的操作；相反，从节点用该字段作为对命令的响应，报告已经完成的操作或状态的变化。</p> 
<p style="margin-left:0pt;">信息字段（I）</p> 
<p style="margin-left:0pt;">&nbsp;&nbsp;信息字段可以是任意的二进制比特串，长度未作限定，其上限由FCS字段或通讯节点的缓冲容量来决定，目前国际上用得较多的是1000-2000比特，而下限可以是0，即无信息字段。但是监控帧中不能有信息字段。</p> 
<p style="margin-left:0pt;">帧校验序列字段（FCS）</p> 
<p style="margin-left:0pt;">&nbsp;帧检验序列字段可以使用16位CRC，对两个标志字段之间的整个帧的内容进行校验。</p> 
<p>5，？？？？什么鬼啊</p> 
<p style="margin-left:0pt;">&nbsp;HDLC有信息帧（I帧）、监控帧（S帧）和无编号帧（U帧）3种不同类型的帧。</p> 
<p style="margin-left:0pt;">&nbsp;</p> 
<p style="margin-left:0pt;">信息帧（I帧）</p> 
<p style="margin-left:0pt;">信息帧用于传送有效信息或数据，通常简称为I帧。</p> 
<p style="margin-left:0pt;">监控帧（S帧）</p> 
<p style="margin-left:0pt;">监控帧用于差错控制和流量控制，通常称为S帧。S帧的标志是控制字段的前两个比特位为“10”。S帧不带信息字段，只有6个字节即48个比特。</p> 
<p style="margin-left:0pt;">无编号帧（U帧）</p> 
<p style="margin-left:0pt;">无编号帧简称U帧。U帧用于提供对链路的建立、拆除以及多种控制功能。</p> 
<p style="margin-left:0pt;">&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p><img alt="" class="has" height="153" src="https://img-blog.csdnimg.cn/20191118203248954.png" width="799"></p> 
<p>1，PPP提供了一个在点到点链路上传输多协议数据包的标准方法，是目前广泛应用的数据链路层点到点通信协议。</p> 
<p>（我对这句话的理解：ppp是广域网协议，而广域网协议使用来连接不通的局域网的，而不同的局域网采用的协议可能是不同的，而“PPP提供了一个在点到点链路上传输多协议数据包的标准方法”的意思就是让使用不同协议的局域网相互通信）</p> 
<p>&nbsp;</p> 
<p>2，PPP协议在TCP/IP协议栈中位于数据链路层，是目前应用最广泛的点到点链路层协议。 PPP协议通常用于串行链路、ATM链路和SDH链路上，封装和发送IP数据包。</p> 
<p>（我对这句话的理解：数据链路层就是对网络层数据的封装，屏蔽网络层之间的差异。从这个意义上我们就可以理解ppp的帧与mac帧的区别，ppp帧屏蔽了局域网之间的差异，使得数据可以无差异地在局域网间传输，而Mac帧是帮助数据更好地在局域网间传输。在这个结论下，我们理解下面的ppp的三个组件就比较容易了）</p> 
<p>2.1PPP的三个协议组件：</p> 
<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td> <p>组件名称</p> </td><td> <p>作用</p> </td></tr><tr><td> <p>数据封装方式</p> </td><td> <p>定义封装多协议数据包的方法</p> </td></tr><tr><td> <p>链路控制协议</p> <p>Link&nbsp;Control&nbsp;Protocol</p> </td><td> <p>定义建立、协商和测试数据链路层连接的方法</p> </td></tr><tr><td> <p>网络层控制协议</p> <p>Network&nbsp;Control&nbsp;Protocol</p> </td><td> <p>包含一组协议，用于对不同的网络层协议进行连接建立和参数协商</p> </td></tr></tbody></table>
<p style="margin-left:0pt;">PPP共定义了三个协议组件，分别是数据封装方式，链路控制协议（Link Control Protocol，LCP）和网络层控制协议（Network Control Protocol，NCP）。</p> 
<p style="margin-left:0pt;">数据封装方式定义了如何封装多种类型的上层协议数据包。</p> 
<p style="margin-left:0pt;">为了能适应多种多样的链路类型，PPP定义了链路控制协议LCP。LCP可以自动检测链路环境，如是否存在环路；协商链路参数，如最大数据包长度，使用何种认证协议等等。与其他数据链路层协议相比，PPP协议的一个重要特点是可以提供认证功能，链路两端可以协商使用何种认证协议并实施认证过程，只有认证成功才会建立连接。这个特点使PPP协议适合运营商用来接入分散的用户。</p> 
<p style="margin-left:0pt;">PPP定义了一组网络层控制协议NCP，每一个协议对应一种网络层协议，用于协商网络层地址等参数，例如IPCP用于协商控制IP，IPXCP用于协商控制IPX协议等。</p> 
<p style="margin-left:0pt;">&nbsp;</p> 
<p style="margin-left:0pt;">&nbsp;</p> 
<p style="margin-left:0pt;">2.2&nbsp; PPP数据帧的封装方式用于区别不同上层协议的数据包。PPP封装方式非常简单，只包含三个字段。</p> 
<p style="margin-left:0pt;">Protocol：协议域，长度为两个字节，标识此PPP数据帧中封装的协议类型，如IP数据包，LCP，NCP等等。常用取值示例如图所示。</p> 
<p style="margin-left:0pt;">Information：信息域，被PPP封装的数据，例如LCP数据，NCP数据，网络层数据包等。此字段的长度是可变的。</p> 
<p style="margin-left:0pt;">Padding：填充域。用于填充信息域。</p> 
<p style="margin-left:0pt;">Padding字段和Information字段两个字段的最大总长度称为PPP的最大接收单元（Maximum Receive Unit，MRU），MRU默认为1500字节。</p> 
<p style="margin-left:0pt;">当Information字段的长度小于MRU时，可以使用Padding字段将长度填充至MRU以方便发送和接收，也可以不进行填充，即Padding字段是可选的。</p> 
<p style="margin-left:0pt;">3，</p> 
<p style="margin-left:0pt;"><img alt="" class="has" height="311" src="https://img-blog.csdnimg.cn/20191118203338781.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNzc1OTM4,size_16,color_FFFFFF,t_70" width="790"></p> 
<p style="margin-left:0pt;">PPP数据帧不能直接在链路上传输，在不同的链路上传输PPP数据帧需要不同的额外封装和控制机制。</p> 
<p style="margin-left:0pt;">在串行链路上传送PPP数据帧遵循HDLC标准。</p> 
<p style="margin-left:0pt;">Flag：数据帧开始和结束的界定标志，取值为二进制“01111110”。</p> 
<p style="margin-left:0pt;">Address：地址，固定为全“1”。由于PPP设计为点到点通信协议，因此不需要寻址机制，只是使用全“1”表示接收端。</p> 
<p style="margin-left:0pt;">Control：控制字段。HDLC可以使用此字段实现数据传输和控制命令的有序传输。在PPP中，此字段取值为0x03，表示使用不计数数据传输，是最简单的一种工作机制。</p> 
<p style="margin-left:0pt;">&nbsp;</p> 
<p>&nbsp;</p>
                