#encoding=utf-8
#!/usr/bin/env python

import os
import sys
import time
from threading import Thread 
from Queue import Queue
from  threadpool import ThreadPool 

'''
烧烤架子
采用线程池，线程数代表可同时处理的份数。
t: 每份的处理时间，单位:秒
count:可同时处理的份数
''' 
       
class BBQ(object): 

        def __init__(self,t=180,count=8):
		
                
            
            self.time = float(t)
            self.count = int(count)
            
            self.ThreadPool = ThreadPool(self.count)
        
        '''
    实际处理烧烤任务的函数
    '''
        def handle(self,task):
            
            time.sleep(self.time)#模拟烧烤时间
            try:
                task[0] = True
            except:
                pass
            return 
         
        '''
    添加一个烧烤任务
    task格式:[True/False],
    True代表处理完成
    False 代表等待处理
    '''
        def addTask(self,task):
        
            self.ThreadPool.addTask(self.handle,task)