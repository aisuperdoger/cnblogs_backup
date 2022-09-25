原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522391.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p>参考：https://www.liaoxuefeng.com/wiki/1016959663602400/1017497232674368</p> 
<h2><a id="1__1"></a>1 类</h2> 
<p>在python中类其实就是一种数据类型，和int，list等没有区别，如每一个list对象都有方法append()。</p> 
<h2><a id="2_4"></a>2.私有变量</h2> 
<p>属性的名称前加上两个下划线__，就变成了一个私有变量（private），只有内部可以访问，外部不能访问。而外部要通过函数对私有变量进行访问，而此函数一般会对私有变量进行一定的保护，如：</p> 
<pre><code>class Student(object):
    ...

    def set_score(self, score):
        if 0 &lt;= score &lt;= 100:
            self.__score = score
        else:
            raise ValueError('bad score')
</code></pre> 
<p>本代码中修改私有变量__score时有一个判断“0 &lt;= score &lt;= 100”，这保证了私有变量的安全。<br> 有些时候，你会看到以一个下划线开头的实例变量名，比如_name，这样的实例变量外部是可以访问的，但是，按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”</p> 
<h2><a id="3_19"></a>3.多态</h2> 
<p>要理解多态，首先我们先看一段代码：</p> 
<pre><code>class Animal(object):
    def run(self):
        print('Animal is running...')

class Dog(Animal):
    def run(self):
        print('Dog is running...')

class Cat(Animal):
    def run(self):
        print('Cat is running...')

class Timer(object):
    def run(self):
        print('Start...')

def run_twice(animal):
    animal.run()
    animal.run()
    
run_twice(Animal())			###1
run_twice(Cat()) 				###2
run_twice(Timer())			###3
</code></pre> 
<p>多态：从###1和###2可以看出来，多态就是依赖Animal的对象作为参数的函数，可以输入Animal的子类的对象作为参数进行运行，而不需要修改函数中的代码。而Animal的子类中的方法run的实现细节可以千变万化，子类的实现可以千变万化这就是多态的功能。</p> 
<p>多态的原因：子类的对象之所以可以作为参数输入到run_twice()中，是因为Animal中有的东西，子类Cat也有（子类继承父类的所有东西，并且部分可以进行重写）。而在python中函数run_twice的形参animal是不用说明数据类型的，所以任何有run方法的类的对象，都可以输入到run_twice中，如###3。Java中函数run_twice的形参animal是需要说明数据类型的，所以只能输入形参对应的类的对象或子类的对象。</p> 
<p>Animal中的方法可以具体没有实现，只是return或print了适当的内容，具体的实现都留给了它的子类。</p> 
<h2><a id="4_52"></a>4.类与函数相比的优点</h2> 
<p>类的特点时封装、继承和多态。<br> 封装：将一个事物的属性和方法定义在一个类里<br> 继承：可以重写类中的方法，对方法的实现细节进行自定义或增加方法，如对数据库的读操作，就可以通过修改方法的实现细节从读取不同的数据库。<br> 多态：以父类作为形参的函数，子类也可以作为这个函数的形参，虽然子类中方法的实现细节与父类可能有所不同。</p> 
<h2><a id="5_58"></a>5.与类相关的方法</h2> 
<ol><li>isinstance(h, Husky) # 判断对象h是否为类Husky。即用来判断类型是否正确</li><li>类中定义的类似“<strong>xxx</strong>”这样的函数，都是有特殊用途的，如</li></ol> 
<pre><code>&gt;&gt;&gt; class MyDog(object):
...     def __len__(self):
...         return 100
...
&gt;&gt;&gt; dog = MyDog()
&gt;&gt;&gt; dog.__len__()		# 和len(dog)是等价的
100
&gt;&gt;&gt; len(dog)				# 在len()函数内部，它自动去调用该对象的__len__()方法
100
</code></pre> 
<p>3.hasattr(fp, ‘read’) # 判断fp对象中是否有方法或属性‘read’</p> 
<h2><a id="6_74"></a>6.类变量</h2> 
<pre><code>class Student(object):
    name = 'Student'
</code></pre> 
<p>name就是类变量</p> 
<pre><code>class Student(object):
    def __init__(self, name):
        self.name = name

s = Student()		
s.age = 18			# 为对象s创建了一个变量age，而不是为类创建了一个变量age
</code></pre> 
<p>self.name就是对象的变量。</p> 
<h2><a id="7_89"></a>7.类的高级用法</h2> 
<p>1.__slots__:允许实例添加的属性</p> 
<pre><code>class Student(object):
    __slots__ = ('name', 'age') # 只允许对Student实例添加name和age属性。
</code></pre> 
<p>__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用.除非在子类中也定义__slots__，这样，子类实例允许定义的属性就是自身的__slots__加上父类的__slots__<br> 2.@property:给属性值的设置添加限制</p> 
<pre><code>class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value): # 给属性值的设置添加限制.没有@score.setter时self._score就是只读变量
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value &lt; 0 or value &gt; 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

# 但是获取和设置属性值的时候用的是如下:
&gt;&gt;&gt; s = Student()
&gt;&gt;&gt; s.score = 60 # OK，实际转化为s.set_score(60)
&gt;&gt;&gt; s.score # OK，实际转化为s.get_score()
60
</code></pre> 
<p>这样我们就既对属性值的设置做了限制,同时也没有让属性值的获取和设置变得困难.<br> 3.元类</p>
                