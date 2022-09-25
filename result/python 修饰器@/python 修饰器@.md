原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522390.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>参考：https://www.liaoxuefeng.com/wiki/1016959663602400/1017451662295584<br> 装饰器让函数在不需要做任何代码变动的前提下增加额外功能</p> 
<pre><code># 不带参数的修饰器
import functools

def log(func):
    @functools.wraps(func) # 防止依赖函数签名的代码执行出错
    def wrapper(*args, **kw): # 这两个参数代表任意参数
        print('call %s():' % func.__name__) # 日志
        return func(*args, **kw)
    return wrapper
    
@log		# 给now添加打印日志的修饰符
def now():
    print('2015-3-25')	
</code></pre> 
<p>log函数的功能是给now函数添加一个日志。</p> 
<pre><code># 带参数的修饰器
import functools

def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
</code></pre>
                