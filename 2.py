# -*- coding:utf-8 -*-
# use sched to timing
import time,datetime
import os
import sched
import baseFunction,stockFunction,FbQx_csvToDbf,FbQQ_onTimeGet
 
 
# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)
 
 

 
 
# 每60秒查看下网络连接情况
if __name__ == '__main__':
   
  timerType='fbqx'
  ExcFunc=FbQx_csvToDbf.FenBi(timerType) 
  ExcFunc.MarketClose('20190121')

  
  # ExcFunc=FbQQ_onTimeGet.FenBi(timerType) 
  # ExcFunc.MarketClose('20190118')