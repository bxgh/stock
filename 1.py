# -*- coding:utf-8 -*-
# use sched to timing
import time,datetime
import os
import sched
import fenbiFunction

t = time.localtime(time.time())  
today = time.strftime("%Y%m%d", t)         
StrIMSt = time.strftime("%H:%M:%S", t)  


fbFunc=fenbiFunction.FenBi()
df=fbFunc.getQQFbOntime('sh601388',0,0)
# fbFunc.testOntime()
print(df)