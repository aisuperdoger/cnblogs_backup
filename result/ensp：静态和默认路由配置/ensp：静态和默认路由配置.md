原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522426.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <p>用到的命令：</p> 
<ol><li>静态路由设置，形如：ip route-static 10.0.13.0 24 10.0.23.3</li><li>备用静态路由设置，形如：ip route-static 10.0.13.0 24 10.0.12.1 preference 80</li><li>跟踪数据包，所经过的路径，形如：Tracet 10.0.13.3</li><li>默认路由配置，形如：ip route-static 0.0.0.0 24 10.0.13.3</li><li>查看路由表：display ip routing-table</li><li>查看端口的简要情况：display ip interface brief</li><li>查看当前的配置情况：display current-configuration</li><li>关闭端口：shutdown</li><li>删除配置的静态路由，形如：undo ip route-static 10.0.13.0 24 10.0.23.3</li><li>删除所有静态路由：undo ip route-static all</li><li>返回上一级：quit；返回用户视图：return</li><li>配置回环接口：interface loopback 0</li></ol>
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p>
                