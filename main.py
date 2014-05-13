#!/usr/bin/env python
#encoding=utf-8


import os
import sys
import time

from Queue import Queue
from optparse import OptionParser

from  threadpool import ThreadPool 
from bar import Bar
from customer import Customer 
from bbq import BBQ

#命令行参数解析#
'''
参数说明：
-p 指定取餐人数
-t 指定人员间隔,单位分钟
-n 时间缩小的倍数(为了快速模拟，将时间等比例缩小)
-h 帮助文档
'''
def  parseoption():
        
        helpInfo = '%%prog %s' % "-p count -t interval time -n Multiple number,example: -p 8 -t 0 -n 1"
        optParser = OptionParser(usage = helpInfo)
        optParser.add_option("-p",dest="p",default=1,type="int",help="The count of person,default:1")
        optParser.add_option("-t",dest="mid",default=0,type="int",help="The interval time(minutes),default:0")
        optParser.add_option("-n",dest="mul",default=1,type="int",help="The multiple number,default:1")
        
        (options,args) = optParser.parse_args()
       
        return options
        
'''
规整化时间
将秒转换为 X小时x分X秒格式
'''
def f(t):
    
    hours = 0
    min = 0
    sec = 0
    t = int(t)
    
    min = t/60
    sec = t%60
    hours = min/60
    min = min%60
    
    return "%sH:%sM:%sS" % (hours,min,sec)
    
    
if __name__=='__main__':
        
        ##解析命令行参数##
        time.clock()
        options = parseoption()
        
        #print options.p,options.mid
        #exit()
        
        mul = options.mul
        p = options.p
        mid = options.mid*60.0/mul
        

        ##创建20个吧台#
        Bars = [ Bar(10.0/mul) for x in xrange(20)]
        
        ##创建一个烧烤架##
        Bbq = BBQ(t=3.0*60/mul,count=8)
        
        ##创建顾客##
        customer_list = []
        for x in xrange(p):

            customer_list.append(Customer(Bars,Bbq))
            time.sleep(mid) #代表顾客之间的间隔
        
        '''
    循环等待每个顾客取材完毕
    '''
        TotalWaitBarTime = 0
        TotalWaitBBQTime = 0
        TotalWaitTime = 0
        i = 0
        print 
        while True:
        
            for c in customer_list:
          
                if c.isAlive():
                    continue
                else:
                    i += 1
                    print "No.",i,"customer gone!"
                    TotalWaitBarTime += c.WaitBarTime
                    TotalWaitBBQTime += c.WaitBBQTime
                    TotalWaitTime += c.TotalWaitTime
                    customer_list.remove(c)
            if len(customer_list) == 0:
                TotalWaitBarTime = TotalWaitBarTime*mul
                TotalWaitBBQTime = TotalWaitBBQTime*mul
                TotalWaitTime = TotalWaitTime*mul
                print ""
                print "Ttoal waiting Bar time:",f(TotalWaitBarTime)
                print "Total waiting BBQ time:",f(TotalWaitBBQTime)
                print "Total waiting time:",f(TotalWaitTime)
                print ""
                print "Average waiting Bar time:",f(TotalWaitBarTime/p)
                print "Average waiting BBQ time:",f(TotalWaitBBQTime/p)
                print "Average waiting time:",f(TotalWaitTime/p)
                #print TotalWaitBarTime,TotalWaitTime,TotalWaitBBQTime
                exit()
                    
              
                