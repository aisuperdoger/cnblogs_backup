原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/07/16243162.html
提交日期：Sat, 07 May 2022 08:48:00 GMT
博文内容：
#　1.查看标准库源码
在Windows系统中，visual studio默认使用的是微软C++编译器（MSVC），当然你可以修改visual studio使用何种编译器。
我是用的是visual studio 2017，它把C++标准库的源码放在了Visual Studio2017\VC\Tools\MSVC\14.16.27023\include下。其他在visual studio 2017中查看源码的方法请参考[使用Visual Studio查看系统库的源码结构](https://blog.csdn.net/qq_40946921/article/details/89266735)


#　2.list不能使用::sort
标准库提供的全局::sort()算法所使用的迭代器必须是随机访问迭代器（Random Access Iterator）。
链表list的迭代器不支持随机访问，无法使用全局::sort()算法进行排序。
vector和deque的迭代器支持随机访问，可使用全局::sort()算法进行排序。
注：随机访问指的就是直接first+N，便可以得到第N个元素的地址，因为这些相邻元素是按顺序连续存储的。


#　3.面向对象和泛型编程的区别？
面向对象编程（OOP，Object-Oriented Programming）：将数据data和操作method相关联。
泛型编程（GP，Generic Programming）：将数据data和操作method相分离。

采用泛型编程的优点：
- 容器（Containers）和算法（Algorithms）可各自独立实现，提供统一的对外接口即可，两者以迭代器（Iterator）作为桥梁。
- 算法（Algorithms）通过迭代器（Iterator）确定操作范围，并通过迭代器（Iterator）获取和使用容器（Containers）元素。


模板的相关知识，请参考：[C++ 模板](https://www.jianshu.com/p/710acc3d5fc1)


# 4.allcator
即使学会了利用allocator，也不建议去使用它。使用new和malloc就可以。但是需要了解它。【都不要去使用它，那了解它干嘛？？】
C++的内存分配函数的底层都是调用了malloc和free，malloc和free再根据不同的操作系统类型(Windows，Linux，Unix等)底层的系统API来获取内存和释放内存。
malloc分配的内存中不止用来存数据，也存储一些额外的数据（如分配出去的空间大小）。如果分配次数越多，那么内存中数据越零散，这些额外的数据开销就越大。所以一个优秀的分配器，应当尽可能的让这些额外的空间占比更小，让速度更快。

GC2.9的alloc分配器的优化思路：malloc分配的内存中不止用来存数据，也存储一些额外的数据（如分配出去的空间大小）。但是因为同一个容器而言，它的内置类型应当是相同的。所以对于容器的分配器，我们可以对此作出优化。









本小节候捷也没有具体讲，等我看完内存管理，再来补充这一节吧，若想提前学习的，请参考：https://blog.csdn.net/weixin_45067603/article/details/122770539



#5.深度探索list
迭代器++是找到下一个元素，迭代器－－是找到上一个元素。在双向链表list中，我们可以知道下一个元素就是next所指元素，上一个元素就是prev所指元素。
list的迭代器的++操作，就会访问list节点对应的next指针。也就是说list的迭代器的++与指针的++不一样，后者只是地址的增加，而迭代器会根据具体迭代器类型执行不同的“++”操作，迭代器是相当于一个智能指针。


list<int>::iterator a;这里的::是什么意思？？


源码探究：为什么下面这个是倒序？？——学会看源码
```
//使用迭代器倒序输出list容器中的元素
	for (std::list<double>::iterator it = values.begin(); it != values.end();++it) {
		std::cout << *it << " ";
	}
	return 0;
```


参考：[【学习笔记】C++STL和泛型编程-侯捷](https://blog.csdn.net/newson92/article/details/122164204)
