# -*- coding:utf-8 -*-
# use sched to timing
import time,datetime
import os
import sched
import stockFunction
 
 
# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)
 
 
# 被周期性调度触发的函数
def execute_kdayClose(inc): #循环日线收盘任务
    closeNow = time.localtime(time.time()) 
    closeDay=time.strftime("%Y%m%d", closeNow) 
    # mskday.kdayClose()
    mskday.kday_close(closeDay)
    schedule.enter(86400, 0, execute_kdayClose, (86400,))  # 86400=24小时

def execute_open(inc): #循环日线开盘任务
    mskday.MarketOpen()
    schedule.enter(86400, 0, execute_open, (86400,))  # 86400=24小时    
 
 
def ontimer(incOpen,incKdayClose):  #任务调度
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(incKdayClose, 0, execute_kdayClose, (incKdayClose,))
    schedule.enter(incOpen, 0, execute_open, (incOpen,))
    schedule.run()
 
 
# 每60秒查看下网络连接情况
if __name__ == '__main__':
    now = time.localtime(time.time())  
    year = int(time.strftime("%Y", now))  
    month = int(time.strftime("%m", now)) 
    day = int(time.strftime("%d", now))
    today=time.strftime("%Y%m%d", now)
    print(now)
    
    now=datetime.datetime.now()    
    schedOpenTime0=datetime.datetime(year,month,day,8)    #设置开盘初始化时间，当天8:00
    schedOpenTime1=datetime.datetime(year,month,day+1,8)  #设置开盘初始化时间次日8:00
    schedKdayCloseTime0=datetime.datetime(year,month,day,20,15)    #设置日线收盘时间，当天16:30
    schedKdayCloseTime1=datetime.datetime(year,month,day+1,20,15)    #设置日线收盘时间，次日16:30

    if now>schedOpenTime0 :
      incOpen=(schedOpenTime1-now).seconds     #启动开盘时间
    else :
      incOpen=(schedOpenTime0-now).seconds

    if now>schedKdayCloseTime0 :
      incKdayClose=(schedKdayCloseTime1-now).seconds #启动日线收盘时间
    else :
      incKdayClose=(schedKdayCloseTime0-now).seconds  

    print(incKdayClose)     

    mskday = stockFunction.MSSQL(host="192.168.151.213", user="toshare1", pwd="toshare1", db="kday_qfq",myOrms="mysql")  
    mskday.MarketOpen()
    ontimer(incOpen,incKdayClose)
