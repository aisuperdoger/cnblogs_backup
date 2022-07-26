原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16243136.html
提交日期：Sat, 07 May 2022 08:41:00 GMT
博文内容：
# 1.ubuntu安装redis
安装
```
sudo apt update
sudo apt install redis-server
```
一旦安装完成，Redis 服务将会自动启动。想要检查服务的状态，输入下面的命令：
```
sudo systemctl status redis-server
```
你应该看到下面这些：
```
 redis-server.service - Advanced key-value store
     Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2020-06-06 20:03:08 UTC; 10s ago
```
# 2.配置 Redis 远程访问
打开 Redis 配置文件：
```
sudo vim /etc/redis/redis.conf
```
如果找不到/etc/redis/redis.conf，请参考[链接](https://blog.csdn.net/qq_39552993/article/details/113433319)
定位到以bind 127.0.0.1 ::1开头的一行，并且将它注释。
如果你的服务器有局域网 IP，并且你想要 Redis 从局域网可以访问 Redis，在这一行后面加上服务器局域网 IP 地址，如下：
```
# bind 127.0.0.1 ::1
bind 192.168.154.130 ::1 #  192.168.154.130为本服务器IP
```
保存这个文件，并且重启 Redis 服务，使应用生效：
```
sudo systemctl restart redis-server
```
下一步，你将需要配置你的防火墙，允许网络流量通过 TCP 端口6379。
通常你想要允许从一个指定 IP 地址或者一个指定 IP 范围来访问 Redis 服务器。例如，想要允许从192.168.121.0/24的连接，运行下面的命令：
```
sudo ufw allow proto tcp from 192.168.121.0/24 to any port 6379
```
确保你的防火墙被配置仅仅接受来自受信任 IP 的连接。
此时，你应该可以从远程位置通过 TCP 连接到 Redis 的 6379 端口。
想要验证所有设置都设置好了，你可以尝试使用redis-cli从你的远程机器上 ping 一下 Redis 服务器。
```
redis-cli -h <REDIS_IP_ADDRESS> ping
```
这个命令将会返回一个响应：PONG

参考：[链接](https://developer.aliyun.com/article/764565#:~:text=Redis%205.0%20%E8%A2%AB%E5%8C%85%E5%90%AB%E5%9C%A8%E9%BB%98%E8%AE%A4%E7%9A%84%20Ubuntu%2020.04%20%E8%BD%AF%E4%BB%B6%E6%BA%90%E4%B8%AD%E3%80%82%20%E6%83%B3%E8%A6%81%E5%AE%89%E8%A3%85%E5%AE%83%EF%BC%8C%E4%BB%A5%20root,%E8%BA%AB%E4%BB%BD%E8%BF%90%E8%A1%8C%E4%B8%8B%E9%9D%A2%E7%9A%84%E5%91%BD%E4%BB%A4%EF%BC%9A%20sudo%20apt%20update%20sudo%20apt%20install%20redis-server)
# 3.redis的基本使用
## 3.1.远程登录命令：
```
redis-cli -h 192.168.154.130 -p 6379 -a "mypass"   # 192.168.154.130为服务器IP，mypass为登录密码
```
## 3.2.Redis支持五种数据类型
Redis支持五种数据类型：string（字符串），hash（哈希），list（列表），set（集合）及zset(sorted set：有序集合)。
###3.2.1.Redis 字符串(String)
Redis 字符串(String)：就是添加一个key，以及一个字符串类型的value


###3.2.2.哈希(Hash)
哈希(Hash)：每一个key下，可以创建多个<field,value>
每个 hash 可以存储 $2^{32} - 1$ 键值对（40多亿）【这是指<field,value>的个数为$2^{32} - 1$吗？】
```
HMSET runoobkey name "redis tutorial" description "redis basic commands for caching"
```
key为runoobkey，<field,value>有<name,"redis tutorial" >、<description,"redis basic commands for caching">


###3.2.3.Redis 列表(List)
Redis 列表(List)：每一个key下，可以创建多个字符串。按照插入顺序排序。


###3.2.4.Redis 集合(Set)
每一个key下，可以创建多个字符串。无序排列，成员唯一。



###3.2.5.Redis 有序集合(sorted set)
Redis 有序集合和集合一样也是 string 类型元素的集合,且不允许重复的成员。
不同的是每个元素都会关联一个 double 类型的分数。redis 正是通过分数来为集合中的成员进行从小到大的排序。
有序集合的成员是唯一的,但分数(score)却可以重复。
集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 O(1)。 集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)。

我把菜鸟教程里的东西抄一遍也没有意义，所以这里知识粗略总结自己的理解。具体可以参考[菜鸟教程](https://www.runoob.com/redis/redis-tutorial.html)。菜鸟教程对各种命令进行了中文的总结，需要的时候，查阅就行。
当然我们也可以直接查阅官网的[命令手册](https://redis.io/commands/)，官方文档对每个命令所举的例子很好。

redis常用的可视化软件为Redis Desktop Manager，不过好像要钱。



# 问题：
redis如何用于保存关系型数据库的数据
redis不能使用sql？？


NoSQL(NoSQL = Not Only SQL )，意即“不仅仅是SQL”。NoSQL数据库的产生就是为了解决大规模数据集合多重数据种类带来的挑战，尤其是大数据应用难题，包括超大规模数据的存储。redis是属于NoSQL的。
为什么mysql不行，NoSQL就可以解决大数据应用问题。
NoSQL：这些类型的数据存储不需要固定的模式，无需多余操作就可以横向扩展。【这里的固定模式指mysql数据库中的什么？横向扩展又是指什么？】
