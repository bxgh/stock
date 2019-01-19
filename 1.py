# -*- coding:utf-8 -*-
# use sched to timing
import time,datetime
import os
import sched
import FbDownQxftp

timerType='fbqx'
ExcFunc=FbDownQxftp.FenBi('20190119') 
openTime= ExcFunc.conf.get(timerType,'marketOpenTime') 
closeTime=ExcFunc.conf.get(timerType,'marketCloseTime')  
tt       =ExcFunc.conf.get(timerType,'closeDay') 
print(tt)

openTimehh=openTime[0:2]
openTimemm=openTime[2:4]
closeTimehh=closeTime[0:2]
closeTimemm=closeTime[2:4]
print(openTimehh,openTimemm)
print(closeTimehh,closeTimemm)

t = time.localtime(time.time()) 
closeDay=time.strftime("%Y%m%d", t) 
closeDay_=time.strftime("%Y-%m-%d", t) 
ExcFunc.conf.set(timerType,'closeDay',closeDay)
ExcFunc.conf.write(open("config.ini", "w"))

# fileList=os.listdir('H:\\fbqxFtp\\csv\\20190117')
# for filename in fileList:    
#     tscode=filename[0:8].lower()
#     ExcFunc.baseFunc.createTable('fbqx_',tscode)
