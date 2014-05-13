#encoding=utf-8
#!/usr/bin/env python

import os
import sys
import time
import random
from Queue import Queue
from threading import Thread,Lock 

'''
顾客类
传入参数:
Bars:吧台列表
BBQ:一个烧烤架
'''

class Customer(Thread):
        
	def __init__(self,Bars =[],BBQ=None):
		
                Thread.__init__(self)
                
                self.setDaemon(True)
                
		self.Bars = Bars
        
                self.BBQ = BBQ
        
		#当前程序运行状态
		self.state = False
                
                #分别表示等待吧台，烧烤架和总的时间，单位为秒
                self.WaitBarTime = 0
                self.WaitBBQTime = 0
                self.TotalWaitTime = 0
                
                self.start()
                    
        '''
    首先排队取材料，然后等待烧烤
    '''
        def run(self):
            self.state = True
            print "A customer come!"
            start = time.clock()
            
            if not self.Bars or not self.BBQ :
                return 
            
            #随机选择最多5个吧台的材料
            stuffs = random.sample([x for x in xrange(len(self.Bars))], min(5,len(self.Bars)))
            waitBar = []
            L = Lock()
            for stuff in stuffs:
                p = [False,L]
                waitBar.append(p)
                self.Bars[stuff].addTask(p)
           
            #等待取材料
            while True:
                flag = True
                for stuff in waitBar:
                    flag = flag and stuff[0]
                if flag:
                    break
            
            self.WaitBarTime = time.clock() - start
            
            #添加一个烧烤任务
            waitBBQ = [False]
            self.BBQ.addTask(waitBBQ)
            #等待烧烤完成
            while not waitBBQ[0]:
                time.sleep(0.1)
            
            self.WaitBBQTime = time.clock() - start - self.WaitBarTime
            self.TotalWaitTime = time.clock() - start
            return 