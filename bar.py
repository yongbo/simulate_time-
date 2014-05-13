#encoding=utf-8
#!/usr/bin/env python

import os
import sys
import time
from threading import Thread 
from Queue import Queue

'''
一个吧台就是一个线程，
传入参数t代表排队取材料的时间
单位是秒
'''

class Bar(Thread):
        
	def __init__(self,t):
		
            Thread.__init__(self)
            
            self.setDaemon(True)
            
            '''
      取材料队列，格式如下[True/False,Lock],
      第一个参数代表是否处理完成，第二个
      锁每一个顾客一个独立的锁，一个顾客同时只能使用一个吧台
      '''
            self.WaitQueue = Queue() 
            
            #当前程序运行状态True为运行中,False为暂未运行
            self.state = False
            
            self.time = t
            
            self.start()
	
        '''
    排队取材料
    '''
        def addTask(self,task):
            
            self.WaitQueue.put(task)
        
        '''
    循环从队列中取出排队的人，sleep t秒
    置取材料成功标志位
    '''
        def run(self):
        
            self.state = True
            while True:
                
                try:
                    task = self.WaitQueue.get()
                    
                    #判断此顾客是否正在被其他吧台处理
                    #是则添加到队列末尾
                    if task[1].locked():
                        self.addTask(task)
                    else:
                        task[1].acquire()
                        time.sleep(self.time)#模拟取材料时间
                        task[0] = True
                        task[1].release()
                       
                        self.WaitQueue.task_done()
                except Exception,msg:
                    print msg
                    continue