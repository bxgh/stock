# -*- coding:utf-8 -*-
# use sched to timing
import sched
import FbDownQxftp   #大富翁全息分笔数据下载任务
import datetime,time,os,shutil
from datetime import datetime as dt

schedule = sched.scheduler(time.time, time.sleep)
# 被周期性调度触发的函数
def execute_Close(inc): #循环收盘任务
    closeNow = time.localtime(time.time()) 
    closeDay=time.strftime("%Y%m%d", closeNow)     
    ExcFunc.MarketClose(closeDay)
    schedule.enter(86400, 0, execute_Close, (86400,))  # 86400=24小时

def execute_open(inc): #循环开盘任务
    ExcFunc.MarketOpen()
    schedule.enter(86400, 0, execute_open, (86400,))  # 86400=24小时    
 
 
def ontimer(incOpen,incClose):  #任务调度
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(incClose, 0, execute_Close, (incClose,))
    schedule.enter(incOpen, 0, execute_open, (incOpen,))
    schedule.run() 

if __name__ == '__main__':
    now = time.localtime(time.time())  
    year = int(time.strftime("%Y", now))  
    month = int(time.strftime("%m", now)) 
    day = int(time.strftime("%d", now))
    today=time.strftime("%Y%m%d", now) 
    now=datetime.datetime.now()    

    schedOpenTime0=datetime.datetime(year,month,day,8,00)    #设置开盘初始化时间，当天8:00
    schedOpenTime1=datetime.datetime(year,month,day+1,8,00)  #设置开盘初始化时间次日8:00
    schedCloseTime0=datetime.datetime(year,month,day,16,15)    #设置大富翁全息数据ftp下载时间，当天16:15
    schedCloseTime1=datetime.datetime(year,month,day+1,16,15)    #设置次日ftp下载时间，次日16:15

    if now>schedOpenTime0 :
        incOpen=(schedOpenTime1-now).seconds     #启动开盘时间
    else :
        incOpen=(schedOpenTime0-now).seconds

    if now>schedCloseTime0 :
        incClose=(schedCloseTime1-now).seconds #启动日线收盘时间
    else :
        incClose=(schedCloseTime0-now).seconds 

    ExcFunc=FbDownQxftp.FenBi()    #分笔数据实例
    if ExcFunc.baseFunc.isTradeDay==1  : #是否交易日
        ExcFunc.MarketOpen()                
        ontimer(incOpen,incClose) # incOpen：开盘初始化 incKdayClose：日线收盘作业