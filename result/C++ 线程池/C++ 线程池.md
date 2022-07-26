原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/05/18/16286717.html
提交日期：Wed, 18 May 2022 14:47:00 GMT
博文内容：
创建几个线程用于处理任务，这些线程暂时不销毁，从而减少线程创建和销毁所需的时间。
将任务放进任务队列中，线程从任务队列中取任务。
这是生成者和消费者模型，需要考虑互斥与同步的问题。实现所需内容如下：
- 一个锁：用于线程互斥访问任务队列
- 两个条件变量：1.当任务队列满时不能添加任务  2.队列中有任务才能取
- 循环队列：用循环队列实现任务队列

实现所需函数如下
```
pthread_cond_wait：等待条件变量满足后，继续执行下面程序
pthread_cond_signal：随机给某一个等待在条件变量的线程发送信号。
pthread_cond_broadcast：给所有等待在等待条件变量的线程发送信号
```
# 1.**epoll加线程池的实现：**
头文件threadpoolsimple.h：
```
#ifndef _THREADPOOL_H
#define _THREADPOOL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>
#include "sys/epoll.h"
#include "wrap.h"

typedef struct _PoolTask // 代表一个任务。用一个PoolTask数组构造任务队列
{
    int tasknum;//模拟任务编号
    void *arg;//回调函数参数
    void (*task_func)(void *arg);//任务的回调函数
    int fd;
    int epfd;
    struct epoll_event *evs;

}PoolTask ;

typedef struct _ThreadPool // 线程池
{
    int max_job_num;	//最大任务个数
    int job_num;		//实际任务个数
    PoolTask *tasks;	//任务队列数组的首地址
    int job_push;		//入队位置
    int job_pop;		// 出队位置

    int thr_num;		//线程池内线程个数
    pthread_t *threads;	//线程池内线程数组
    int shutdown;		//是否关闭线程池
    pthread_mutex_t pool_lock;	//线程池的锁
    pthread_cond_t empty_task;//任务队列为空的条件
    pthread_cond_t not_empty_task;//任务队列不为空的条件

}ThreadPool;

void create_threadpool(int thrnum,int maxtasknum);//创建线程池--thrnum  代表线程个数，maxtasknum 最大任务个数
void destroy_threadpool(ThreadPool *pool);//摧毁线程池
//void addtask(ThreadPool *pool);//添加任务到线程池
void addtask(ThreadPool *pool,int fd,struct epoll_event *evs);
void taskRun(void *arg);	//任务回调函数

#endif
```

```
//简易版线程池
#include "threadpoolsimple.h"

ThreadPool *thrPool = NULL;

int beginnum = 1000;

void *thrRun(void *arg)
{
    //printf("begin call %s-----\n",__FUNCTION__);
    ThreadPool *pool = (ThreadPool*)arg;
    int taskpos = 0;//任务位置
    PoolTask *task = (PoolTask *)malloc(sizeof(PoolTask));

    while(1)
	{
        //获取任务，先要尝试加锁
        pthread_mutex_lock(&thrPool->pool_lock);

		//无任务并且线程池不是要摧毁
        while(thrPool->job_num <= 0 && !thrPool->shutdown ) // 当pool->not_empty_task为1时，循环退出，并在下面代码中销毁线程
		{
			//如果没有任务，线程会阻塞
            pthread_cond_wait(&thrPool->not_empty_task,&thrPool->pool_lock);
        }
        
        if(thrPool->job_num)
		{
            //有任务需要处理
            taskpos = (thrPool->job_pop++) % thrPool->max_job_num;  // 从循环队列中取任务
            //printf("task out %d...tasknum===%d tid=%lu\n",taskpos,thrPool->tasks[taskpos].tasknum,pthread_self());
			//为什么要拷贝？避免任务被修改，生产者会添加任务
            memcpy(task,&thrPool->tasks[taskpos],sizeof(PoolTask));
            task->arg = task;
            thrPool->job_num--;
            //task = &thrPool->tasks[taskpos];
            pthread_cond_signal(&thrPool->empty_task);// empty_task加一，代表任务队列空余空间增加一
        }

        if(thrPool->shutdown)
		{
            //代表要摧毁线程池，此时线程退出即可
            //pthread_detach(pthread_self());//临死前分家
            pthread_mutex_unlock(&thrPool->pool_lock);
            free(task);
			pthread_exit(NULL);
        }

        //释放锁
        pthread_mutex_unlock(&thrPool->pool_lock);
        printf("001\n");
        task->task_func(task->arg);//执行回调函数
        printf("002\n");
    }
    
    //printf("end call %s-----\n",__FUNCTION__);
}

//创建线程池
void create_threadpool(int thrnum,int maxtasknum)
{
    printf("begin call %s-----\n",__FUNCTION__);
    thrPool = (ThreadPool*)malloc(sizeof(ThreadPool));

    thrPool->thr_num = thrnum;
    thrPool->max_job_num = maxtasknum;
    thrPool->shutdown = 0;//是否摧毁线程池，1代表摧毁
    thrPool->job_push = 0;//任务队列添加的位置
    thrPool->job_pop = 0;//任务队列出队的位置
    thrPool->job_num = 0;//初始化的任务个数为0

    thrPool->tasks = (PoolTask*)malloc((sizeof(PoolTask)*maxtasknum));//申请最大的任务队列

    //初始化锁和条件变量
    pthread_mutex_init(&thrPool->pool_lock,NULL);
    pthread_cond_init(&thrPool->empty_task,NULL);
    pthread_cond_init(&thrPool->not_empty_task,NULL);

    int i = 0;
    thrPool->threads = (pthread_t *)malloc(sizeof(pthread_t)*thrnum);//申请n个线程id的空间
	
	pthread_attr_t attr;
	pthread_attr_init(&attr);
	pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
    for(i = 0;i < thrnum;i++)
	{
        pthread_create(&thrPool->threads[i],&attr,thrRun,(void*)thrPool);//创建多个线程
    }
    //printf("end call %s-----\n",__FUNCTION__);
}
//摧毁线程池
void destroy_threadpool(ThreadPool *pool)
{
    pool->shutdown = 1;// 标志位设为1 
    pthread_cond_broadcast(&pool->not_empty_task);// 给所有阻塞在pool->not_empty_task上的线程发信号

    int i = 0;
    for(i = 0; i < pool->thr_num ; i++)
	{
        pthread_join(pool->threads[i],NULL);  // 这个代码没有必要
    }

    pthread_cond_destroy(&pool->not_empty_task);
    pthread_cond_destroy(&pool->empty_task);
    pthread_mutex_destroy(&pool->pool_lock);

    free(pool->tasks);
    free(pool->threads);
    free(pool);
}

//添加任务到线程池
void addtask(ThreadPool *pool,int fd,struct epoll_event *evs)
{
    //printf("begin call %s-----\n",__FUNCTION__);
    pthread_mutex_lock(&pool->pool_lock);

	//实际任务总数大于最大任务个数则阻塞等待(等待任务被处理)
    while(pool->max_job_num <= pool->job_num)
	{
        pthread_cond_wait(&pool->empty_task,&pool->pool_lock);
    }

    int taskpos = (pool->job_push++)%pool->max_job_num;
    //printf("add task %d  tasknum===%d\n",taskpos,beginnum);
    pool->tasks[taskpos].tasknum = beginnum++;
    pool->tasks[taskpos].arg = (void*)&pool->tasks[taskpos];
    pool->tasks[taskpos].task_func = taskRun;
    pool->tasks[taskpos].fd = fd;
     pool->tasks[taskpos].evs = evs;
    pool->job_num++;

    pthread_mutex_unlock(&pool->pool_lock);

    pthread_cond_signal(&pool->not_empty_task);// not_empty_task加一，代表任务增加一
    //printf("end call %s-----\n",__FUNCTION__);
}

//任务回调函数
void taskRun(void *arg)
{
    printf("003\n");
    PoolTask *task = (PoolTask*)arg;
     char buf[1024]="";
    int n = Read(task->fd , buf,sizeof(buf));
    if(n == 0 )
        {
         close(task->fd);//关闭cfd
        epoll_ctl(task->epfd,EPOLL_CTL_DEL,task->fd,task->evs);//将cfd上树
            printf("client close\n");
        }
    else if(n> 0)
        {
         printf("%s\n",buf );
         Write(task->fd ,buf,n);

        }
 printf("004\n");
   
}


int main()
{
    create_threadpool(3,20);
    int i = 0;
    //创建套接字,绑定
    int lfd = tcp4bind(8000,NULL);
    //监听
    listen(lfd,128);
    //创建树
    int epfd = epoll_create(1);
    struct epoll_event ev,evs[1024];
    ev.data.fd = lfd;
    ev.events = EPOLLIN;//监听读事件
    //将ev上树
    epoll_ctl(epfd,EPOLL_CTL_ADD,lfd,&ev);
    while(1)
    {
        int nready = epoll_wait(epfd,evs,1024,-1);
        if(nready < 0)
            perr_exit("err");
        else if(nready == 0)
            continue;
        else if(nready > 0 )
        {
            for(int i=0;i<nready;i++)
            {
                if(evs[i].data.fd == lfd && evs[i].events & EPOLLIN)//如果是lfd变化,并且是读事件。这个处理很快，所以就不放进任务队列里面了
                {
                        struct sockaddr_in cliaddr;
                        char buf_ip[16]="";
                        socklen_t len  = sizeof(cliaddr);
                        int cfd = Accept(lfd,(struct sockaddr *)&cliaddr,&len);
                        printf("client ip=%s port=%d\n",inet_ntop(AF_INET,
                        &cliaddr.sin_addr.s_addr,buf_ip,sizeof(buf_ip)),
                        ntohs(cliaddr.sin_port));
                        ev.data.fd = cfd;//cfd上树
                        ev.events = EPOLLIN;//监听读事件
                        epoll_ctl(epfd,EPOLL_CTL_ADD,cfd,&ev);//将cfd上树

                }
                else if(evs[i].events & EPOLLIN)//普通的读事件
                {
                    printf("###########1\n");
                    addtask(thrPool,evs[i].data.fd,&evs[i]);
                     printf("###########2\n");
                    // char buf[1024]="";
                    // int n = Read(evs[i].data.fd , buf,sizeof(buf));
                    // if(n <= 0 )
                    // {
                    //     close(evs[i].data.fd);//关闭cfd
                    //     epoll_ctl(epfd,EPOLL_CTL_DEL,evs[i].data.fd,&evs[i]);//将cfd上树
                    //     printf("client close\n");
                    // }
                    // else
                    // {
                    //     printf("%s\n",buf );
                    //     Write(evs[i].data.fd ,buf,n);

                    // }


                }


            }



        }


    }
    close(lfd);

   
    destroy_threadpool(thrPool);

    return 0;
}
```
# 2.复杂版的线程池实现
头文件threadpool.h：
```
#ifndef __THREADPOOL_H_
#define __THREADPOOL_H_

typedef struct threadpool_t threadpool_t;

/**
 * @function threadpool_create
 * @descCreates a threadpool_t object.
 * @param thr_num  thread num
 * @param max_thr_num  max thread size
 * @param queue_max_size   size of the queue.
 * @return a newly created thread pool or NULL
 */
threadpool_t *threadpool_create(int min_thr_num, int max_thr_num, int queue_max_size);

/**
 * @function threadpool_add
 * @desc add a new task in the queue of a thread pool
 * @param pool     Thread pool to which add the task.
 * @param function Pointer to the function that will perform the task.
 * @param argument Argument to be passed to the function.
 * @return 0 if all goes well,else -1
 */
int threadpool_add(threadpool_t *pool, void*(*function)(void *arg), void *arg);

/**
 * @function threadpool_destroy
 * @desc Stops and destroys a thread pool.
 * @param pool  Thread pool to destroy.
 * @return 0 if destory success else -1
 */
int threadpool_destroy(threadpool_t *pool);

/**
 * @desc get the thread num
 * @pool pool threadpool
 * @return # of the thread
 */
int threadpool_all_threadnum(threadpool_t *pool);

/**
 * desc get the busy thread num
 * @param pool threadpool
 * return # of the busy thread
 */
int threadpool_busy_threadnum(threadpool_t *pool);

#endif

```
```
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <errno.h>
#include "threadpool.h"

#define DEFAULT_TIME 10                 /*10s检测一次*/
#define MIN_WAIT_TASK_NUM 10            /*如果queue_size > MIN_WAIT_TASK_NUM 添加新的线程到线程池*/ 
#define DEFAULT_THREAD_VARY 10          /*每次创建和销毁线程的个数*/
#define true 1
#define false 0

// 代表一个任务
typedef struct 
{
    void *(*function)(void *);          /* 函数指针，回调函数 */
    void *arg;                          /* 上面函数的参数 */
} threadpool_task_t;                    /* 各子线程任务结构体 */

/* 描述线程池相关信息 */
struct threadpool_t 
{
    pthread_mutex_t lock;               /* 用于锁任务队列 */    
    pthread_mutex_t thread_counter;     /* 记录忙状态线程个数的锁 -- busy_thr_num */

    pthread_cond_t queue_not_full;      /* 当任务队列满时，添加任务的线程阻塞，等待此条件变量 */
    pthread_cond_t queue_not_empty;     /* 任务队列里不为空时，通知等待任务的线程 */
  
    pthread_t *threads;                 /* 存放线程池中每个线程的tid。数组 */
    pthread_t adjust_tid;               /* 存管理线程tid */
    threadpool_task_t *task_queue;      /* 任务队列(数组首地址) */

    int min_thr_num;                    /* 线程池最小线程数 */
    int max_thr_num;                    /* 线程池最大线程数 */
    int live_thr_num;                   /* 当前存活线程个数 */
    int busy_thr_num;                   /* 忙状态线程个数 */
    int wait_exit_thr_num;              /* 要销毁的线程个数 */

    int queue_front;                    /* task_queue队头下标 */
    int queue_rear;                     /* task_queue队尾下标 */
    int queue_size;                     /* task_queue队中实际任务数 */
    int queue_max_size;                 /* task_queue队列可容纳任务数上限 */

    int shutdown;                       /* 标志位，线程池使用状态，true或false */
};

void *threadpool_thread(void *threadpool);

void *adjust_thread(void *threadpool);

int is_thread_alive(pthread_t tid);
int threadpool_free(threadpool_t *pool);

//threadpool_create(3,100,100);  
threadpool_t *threadpool_create(int min_thr_num, int max_thr_num, int queue_max_size)
{
    int i;
    threadpool_t *pool = NULL;
    do 
	{
        if((pool = (threadpool_t *)malloc(sizeof(threadpool_t))) == NULL) 
		{  
            printf("malloc threadpool fail");
            break;                                      /*跳出do while。相当于使用了go to,直接跳转到下面的位置*/
        }

        pool->min_thr_num = min_thr_num;
        pool->max_thr_num = max_thr_num;
        pool->busy_thr_num = 0;
        pool->live_thr_num = min_thr_num;               /* 活着的线程数 初值=最小线程数 */
        pool->wait_exit_thr_num = 0;
        pool->queue_size = 0;                           /* 有0个任务 */
        pool->queue_max_size = queue_max_size;
        pool->queue_front = 0;
        pool->queue_rear = 0;
        pool->shutdown = false;                         /* 不关闭线程池 */

        /* 根据最大线程上限数， 给工作线程数组开辟空间, 并清零 */
        pool->threads = (pthread_t *)malloc(sizeof(pthread_t)*max_thr_num); 
        if (pool->threads == NULL) 
		{
            printf("malloc threads fail");
            break;
        }
        memset(pool->threads, 0, sizeof(pthread_t)*max_thr_num);

        /* 队列开辟空间 */
        pool->task_queue = (threadpool_task_t *)malloc(sizeof(threadpool_task_t)*queue_max_size);
        if (pool->task_queue == NULL) 
		{
            printf("malloc task_queue fail\n");
            break;
        }

        /* 初始化互斥琐、条件变量 */
        if (pthread_mutex_init(&(pool->lock), NULL) != 0
                || pthread_mutex_init(&(pool->thread_counter), NULL) != 0
                || pthread_cond_init(&(pool->queue_not_empty), NULL) != 0
                || pthread_cond_init(&(pool->queue_not_full), NULL) != 0)
        {
            printf("init the lock or cond fail\n");
            break;
        }

		//启动工作线程
		pthread_attr_t attr;
		pthread_attr_init(&attr);
		pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
        for (i = 0; i < min_thr_num; i++) 
		{
            pthread_create(&(pool->threads[i]), &attr, threadpool_thread, (void *)pool);/*pool指向当前线程池*/
            printf("start thread 0x%x...\n", (unsigned int)pool->threads[i]);
        }

		//创建管理者线程，用于根据任务的多少，动态地增加和减少线程的数量
        pthread_create(&(pool->adjust_tid), &attr, adjust_thread, (void *)pool);

        return pool;

    } while (0);

	/* 前面代码调用失败时,释放poll存储空间 */
    threadpool_free(pool);

    return NULL;
}

/* 向线程池中 添加一个任务 */
//threadpool_add(thp, process, (void*)&num[i]);   /* 向线程池中添加任务 process: 小写---->大写*/

int threadpool_add(threadpool_t *pool, void*(*function)(void *arg), void *arg)
{
    pthread_mutex_lock(&(pool->lock));

    /* ==为真，队列已经满， 调wait阻塞 */
    while ((pool->queue_size == pool->queue_max_size) && (!pool->shutdown)) 
	{
        pthread_cond_wait(&(pool->queue_not_full), &(pool->lock));
    }

    if (pool->shutdown) 
	{
        pthread_cond_broadcast(&(pool->queue_not_empty));
        pthread_mutex_unlock(&(pool->lock));
        return 0;
    }

    /* 清空 工作线程 调用的回调函数 的参数arg */
    if (pool->task_queue[pool->queue_rear].arg != NULL) 
	{
        pool->task_queue[pool->queue_rear].arg = NULL;
    }

    /*添加任务到任务队列里*/
    pool->task_queue[pool->queue_rear].function = function;
    pool->task_queue[pool->queue_rear].arg = arg;
    pool->queue_rear = (pool->queue_rear + 1) % pool->queue_max_size;       /* 队尾指针移动, 模拟环形 */
    pool->queue_size++;

    /*添加完任务后，队列不为空，唤醒线程池中 等待处理任务的线程*/
    pthread_cond_signal(&(pool->queue_not_empty));
    pthread_mutex_unlock(&(pool->lock));

    return 0;
}

/* 线程池中各个工作线程 */
void *threadpool_thread(void *threadpool)
{
    threadpool_t *pool = (threadpool_t *)threadpool;
    threadpool_task_t task;

    while (true) 
	{
        /* Lock must be taken to wait on conditional variable */
        /*刚创建出线程，等待任务队列里有任务，否则阻塞等待任务队列里有任务后再唤醒接收任务*/
        pthread_mutex_lock(&(pool->lock));

        /*queue_size == 0 说明没有任务，调 wait 阻塞在条件变量上, 若有任务，跳过该while*/
        while ((pool->queue_size == 0) && (!pool->shutdown)) 
		{  
            printf("thread 0x%x is waiting\n", (unsigned int)pthread_self());
            pthread_cond_wait(&(pool->queue_not_empty), &(pool->lock));//暂停到这

            /*清除指定数目的空闲线程，如果要结束的线程个数大于0，结束线程*/
            if (pool->wait_exit_thr_num > 0) 
			{
                pool->wait_exit_thr_num--;

                /*如果线程池里线程个数大于最小值时可以结束当前线程*/
                if (pool->live_thr_num > pool->min_thr_num) 
				{
                    printf("thread 0x%x is exiting\n", (unsigned int)pthread_self());
                    pool->live_thr_num--;
                    pthread_mutex_unlock(&(pool->lock));
					//pthread_detach(pthread_self());
                    pthread_exit(NULL);
                }
            }
        }

        /*如果指定了true，要关闭线程池里的每个线程，自行退出处理---销毁线程池*/
        if (pool->shutdown) 
		{
            pthread_mutex_unlock(&(pool->lock));
            printf("thread 0x%x is exiting\n", (unsigned int)pthread_self());
            //pthread_detach(pthread_self());
            pthread_exit(NULL);     /* 线程自行结束 */
        }

        /*从任务队列里获取任务, 是一个出队操作*/
        task.function = pool->task_queue[pool->queue_front].function;
        task.arg = pool->task_queue[pool->queue_front].arg;

        pool->queue_front = (pool->queue_front + 1) % pool->queue_max_size;       /* 出队，模拟环形队列 */
        pool->queue_size--;

        /*通知可以有新的任务添加进来*/
        pthread_cond_broadcast(&(pool->queue_not_full));

        /*任务取出后，立即将 线程池琐 释放*/
        pthread_mutex_unlock(&(pool->lock));

        /*执行任务*/ 
        printf("thread 0x%x start working\n", (unsigned int)pthread_self());
        pthread_mutex_lock(&(pool->thread_counter));                            /*忙状态线程数变量琐*/
        pool->busy_thr_num++;                                                   /*忙状态线程数+1*/
        pthread_mutex_unlock(&(pool->thread_counter));

        (*(task.function))(task.arg);                                           /*执行回调函数任务*/
        //task.function(task.arg);                                              /*执行回调函数任务*/

        /*任务结束处理*/ 
        printf("thread 0x%x end working\n", (unsigned int)pthread_self());
        pthread_mutex_lock(&(pool->thread_counter));
        pool->busy_thr_num--;                                       /*处理掉一个任务，忙状态数线程数-1*/
        pthread_mutex_unlock(&(pool->thread_counter));
    }

    pthread_exit(NULL);
}

/* 管理线程 */
void *adjust_thread(void *threadpool)
{
    int i;
    threadpool_t *pool = (threadpool_t *)threadpool;
    while (!pool->shutdown) 
	{

        sleep(DEFAULT_TIME);                                    /*定时 过一段时间就对线程增加或减少一次*/

        pthread_mutex_lock(&(pool->lock));
        int queue_size = pool->queue_size;                      /* 任务数 */
        int live_thr_num = pool->live_thr_num;                  /* 存活的线程数 */
        pthread_mutex_unlock(&(pool->lock));

        pthread_mutex_lock(&(pool->thread_counter));
        int busy_thr_num = pool->busy_thr_num;                  /* 忙着的线程数 */
        pthread_mutex_unlock(&(pool->thread_counter));

        /* 创建新线程 算法： 任务数大于最小线程池个数（不应该任务数大于不忙的线程时才增加吗？）, 且存活的线程数少于最大线程个数时 如：30>=10 && 40<100*/
        if (queue_size >= MIN_WAIT_TASK_NUM && live_thr_num < pool->max_thr_num) 
		{
            pthread_mutex_lock(&(pool->lock));  
            int add = 0;

            /*一次增加 DEFAULT_THREAD 个线程*/
            for (i = 0; i < pool->max_thr_num && add < DEFAULT_THREAD_VARY
                    && pool->live_thr_num < pool->max_thr_num; i++) 
			{
                if (pool->threads[i] == 0 || !is_thread_alive(pool->threads[i])) // 查找数组pool->threads中可用的位置 
				// pool->threads[i] == 0代表pool->threads[i]没存线程号；
				// !is_thread_alive(pool->threads[i])为真代表存储的线程已死
				{
                    pthread_create(&(pool->threads[i]), NULL, threadpool_thread, (void *)pool);
                    add++;
                    pool->live_thr_num++;
                }
            }

            pthread_mutex_unlock(&(pool->lock));
        }

        /* 销毁多余的空闲线程 算法：忙线程X2 小于 存活的线程数 且 存活的线程数 大于 最小线程数时*/
        if ((busy_thr_num * 2) < live_thr_num  &&  live_thr_num > pool->min_thr_num) 
		{
            /* 一次销毁DEFAULT_THREAD个线程, 隨機10個即可 */
            pthread_mutex_lock(&(pool->lock));
            pool->wait_exit_thr_num = DEFAULT_THREAD_VARY;      /* 要销毁的线程数 设置为10 */
            pthread_mutex_unlock(&(pool->lock));

            for (i = 0; i < DEFAULT_THREAD_VARY; i++) 
			{
                /* 通知处在空闲状态的线程, 他们会自行终止*/
                pthread_cond_signal(&(pool->queue_not_empty));
            }
        }
    }

    return NULL;
}

int threadpool_destroy(threadpool_t *pool)
{
    int i;
    if (pool == NULL) 
	{
        return -1;
    }
    pool->shutdown = true;

    /*先销毁管理线程*/
    //pthread_join(pool->adjust_tid, NULL);

    for (i = 0; i < pool->live_thr_num; i++) 
	{
        /*通知所有的空闲线程*/
        pthread_cond_broadcast(&(pool->queue_not_empty));
    }

    /*for (i = 0; i < pool->live_thr_num; i++) 
	{
        pthread_join(pool->threads[i], NULL);
    }*/

    threadpool_free(pool);

    return 0;
}

int threadpool_free(threadpool_t *pool)
{
    if (pool == NULL) 
	{
        return -1;
    }

    if (pool->task_queue) 
	{
        free(pool->task_queue);
    }

    if (pool->threads) 
	{
        free(pool->threads);
        pthread_mutex_lock(&(pool->lock));
        pthread_mutex_destroy(&(pool->lock));
        pthread_mutex_lock(&(pool->thread_counter));
        pthread_mutex_destroy(&(pool->thread_counter));
        pthread_cond_destroy(&(pool->queue_not_empty));
        pthread_cond_destroy(&(pool->queue_not_full));
    }

    free(pool);
    pool = NULL;

    return 0;
}

int threadpool_all_threadnum(threadpool_t *pool)
{
    int all_threadnum = -1;

    pthread_mutex_lock(&(pool->lock));
    all_threadnum = pool->live_thr_num;
    pthread_mutex_unlock(&(pool->lock));

    return all_threadnum;
}

int threadpool_busy_threadnum(threadpool_t *pool)
{
    int busy_threadnum = -1;

    pthread_mutex_lock(&(pool->thread_counter));
    busy_threadnum = pool->busy_thr_num;
    pthread_mutex_unlock(&(pool->thread_counter));

    return busy_threadnum;
}

int is_thread_alive(pthread_t tid)
{
    int kill_rc = pthread_kill(tid, 0);     //发0号信号，测试线程是否存活
    if (kill_rc == ESRCH) 
	{
        return false;
    }

    return true;
}

/*测试*/ 

#if 1
/* 线程池中的线程，模拟处理业务 */
void *process(void *arg)
{
    printf("thread 0x%x working on task %d\n ",(unsigned int)pthread_self(),*(int *)arg);
    sleep(1);
    printf("task %d is end\n", *(int *)arg);

    return NULL;
}

int main(void)
{
    /*threadpool_t *threadpool_create(int min_thr_num, int max_thr_num, int queue_max_size);*/
    threadpool_t *thp = threadpool_create(3,100,100);   /*创建线程池，池里最小3个线程，最大100，队列最大100*/
    printf("pool inited");

    //int *num = (int *)malloc(sizeof(int)*20);
    int num[20], i;
    for (i = 0; i < 20; i++) 
	{
        num[i]=i;
        printf("add task %d\n",i);
        threadpool_add(thp, process, (void*)&num[i]);   /* 向线程池中添加任务 */
    }

    sleep(10);                                          /* 等子线程完成任务 */
    threadpool_destroy(thp);

    return 0;
}

#endif
```
