原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/09/23/16723428.html
提交日期：Fri, 23 Sep 2022 09:13:00 GMT
博文内容：
我从P8开始看的。

# 面向对象的编程和基于对象的编程思想
muduo库不使用抽象类和虚函数作为接口，只暴露具体类，这就意味着muduo库不使用面向对象的编程思想，而使用基于对象的编程思想，以下说明两者的区别：
## 面向对象的编程思想

Thread.h：
```
#ifndef _THREAD_H_
#define _THREAD_H_

#include <pthread.h>

class Thread
{
public:
	Thread();

	// 由于要用到多态，所以这里析构函数设为虚函数。
	// 设为虚函数以后，使用父类指针访问的子类对象结束后，才会调用子类的析构函数，不然只会调用父类的析构函数。
	virtual ~Thread();

	void Start();
	void Join();

	void SetAutoDelete(bool autoDelete);

private:
	// 加了静态，就没有隐含的 this 指针了
	static void *ThreadRoutine(void *arg);
	// 纯虚函数
	virtual void Run() = 0; 
	pthread_t threadId_;
	bool autoDelete_;
};

#endif // _THREAD_H_
```

[C++中虚析构函数](https://blog.csdn.net/weicao1990/article/details/81911341)：设为虚析构函数以后，使用父类指针访问的子类对象结束后，才会调用子类的析构函数，不然只会调用父类的析构函数。

Thread.cpp：
```
#include "Thread.h"
#include <iostream>
using namespace std;


Thread::Thread() : autoDelete_(false)
{
	cout<<"Thread ..."<<endl;
}

Thread::~Thread()
{
	cout<<"~Thread ..."<<endl;
}

void Thread::Start()
{        
        // C++中类的普通成员函数不能作为 pthread_create的线程函数。
        // 所以ThreadRoutine可以设为静态成员函数，但不能是普通成员函数，所以ThreadRoutine也不能直接设为Run
	pthread_create(&threadId_, NULL, ThreadRoutine, this);
}

void Thread::Join()
{
	pthread_join(threadId_, NULL);
}

void* Thread::ThreadRoutine(void* arg)
{
	// static_cast 是强制类型转换为 Thread*
	Thread* thread = static_cast<Thread*>(arg); // static_cast<Thread*>(arg)得到的肯定是一个Thread的子类对象
                                                    // 而thread是父类指针，故这里使用到了多态，所以Run要设为virtual
	thread->Run(); //  ThreadRoutine中不能直接调用Run，因为 ThreadRoutine是静态成员函数，而Run是普通成员函数
	if (thread->autoDelete_)  // 本函数执行完毕，即线程执行完毕，就将对象delete掉
		delete thread;
	return NULL;
}

void Thread::SetAutoDelete(bool autoDelete)
{
	autoDelete_ = autoDelete;
}
```
[ C++中类的普通成员函数不能作为 pthread_create的线程函数](https://blog.csdn.net/hsd2012/article/details/51207585)，这篇文章说隐含传入的this指针与线程函数参数(void\*)不能匹配。但是我觉得它说的有问题，因为this和(void*)明显是匹配的。我觉得“C++中类的普通成员函数不能作为 pthread_create的线程函数”的主要原因是：普通成员函数由于要隐含传入this，所以它在实现上可能与pthread_create要求的函数有所区别，所以不能传入。

Thread_test.cpp：
```
#include "Thread.h"
#include <unistd.h>
#include <iostream>
using namespace std;

class TestThread : public Thread
{
	public:
		TestThread(int count) : count_(count)
		{
			cout<<"TestThread ..."<<endl;
		}

		~TestThread()
		{
			cout<<"~TestThread ..."<<endl;
		}

	private:
		void Run()
		{
			while (count_--)
			{
				cout<<"this is a test ..."<<endl;
				sleep(1);
			}
		}

		int count_;
};

int main(void)
{
	/*
	TestThread t(5);
	t.Start();

	t.Join();
	*/

	TestThread* t2 = new TestThread(5);
	t2->SetAutoDelete(true);
	t2->Start();
	t2->Join();

	return 0;
}

```



## 基于对象的编程思想