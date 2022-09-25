原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/08/08/16563106.html
提交日期：Mon, 08 Aug 2022 11:04:00 GMT
博文内容：
```
#include <iostream>
#include <bitset>

using namespace std;

int main()
{
    unsigned char bits = 0xff;
    auto bits2 = bits << 8;

    if (typeid(bits2) == typeid(int))  // bits2被提升为int类型
    {
        cout << (bitset<32> (bits << 8));  // 转化为32位的int类型数据，并以二进制格式进行输出
    }
}
```