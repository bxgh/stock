# -*- coding:utf-8 -*-
# use sched to timing
import sched
import FbDownQxftp   #大富翁全息分笔数据下载任务
import datetime,time,os,shutil
from datetime import datetime as dt

schedule = sched.scheduler(time.time, time.sleep)
timerType='fbqx'    ######设置任务类型，对应config.ini节点，读取相关设置
# 被周期性调度触发的函数
def execute_Close(inc): #循环收盘任务 
    closeDay=ExcFunc.conf.get(timerType,'closeDay')             
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
    ExcFunc=FbDownQxftp.FenBi(timerType)    #分笔数据实例
    getHisdata=ExcFunc.conf.get(timerType,'getHisdata') 
    today = ExcFunc.conf.get(timerType,'closeDay')   #config.in读取收盘日期
    year = int(today[0:4])  
    month = int(today[4:6]) 
    day = int(today[6:8])   

    openTime= ExcFunc.conf.get(timerType,'marketOpenTime')  #config.in读取开盘时间
    closeTime=ExcFunc.conf.get(timerType,'marketCloseTime') #config.in读取收盘时间      
    openTimehh=int(openTime[0:2])        #config.in读取开盘小时
    openTimemm=int(openTime[2:4])        #config.in读取开盘分钟
    closeTimehh=int(closeTime[0:2])
    closeTimemm=int(closeTime[2:4])    
    now=datetime.datetime.now()         #程序运行当前时间
    schedOpenTime0=datetime.datetime(year,month,day,openTimehh,openTimemm)    #设置开盘初始化时间，当天8:00
    schedOpenTime1=datetime.datetime(year,month,day+1,openTimehh,openTimemm)  #设置开盘初始化时间次日8:00
    schedCloseTime0=datetime.datetime(year,month,day,closeTimehh,closeTimemm)    #设置大富翁全息数据ftp下载时间，当天16:15
    schedCloseTime1=datetime.datetime(year,month,day+1,closeTimehh,closeTimemm)    #设置次日ftp下载时间，次日16:15

    if now>schedOpenTime0 :
        incOpen=(schedOpenTime1-now).seconds     #启动开盘时间
    else :
        incOpen=(schedOpenTime0-now).seconds

    if now>schedCloseTime0 :
        incClose=(schedCloseTime1-now).seconds   #启动收盘时间
    else :
        incClose=(schedCloseTime0-now).seconds 
    
    if ExcFunc.baseFunc.isTradeDay==1 and getHisdata=='0' : #是否交易日
        ExcFunc.MarketOpen()                       
        ontimer(incOpen,incClose)   # incOpen：开盘初始化 incClose：收盘作业
        
    if getHisdata =='1': #获取历史数据
      closeDay=ExcFunc.conf.get(timerType,'closeDay')      #config.ini获取历史数据日期       
      df=ExcFunc.baseFunc.pro.query('trade_cal', start_date=closeDay, end_date=closeDay)
      isTradeDay=int(df.iloc[0,2])
      if isTradeDay==1:
        ExcFunc.MarketClose(closeDay)
      else:
        print(closeDay,'is not trade day!')  

