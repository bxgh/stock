# -*- coding:utf-8 -*-
# use sched to timing
import time,datetime
import os
import sched
from winfenbi import fenbiFunction

t = time.localtime(time.time())  
today = time.strftime("%Y%m%d", t)         
StrIMSt = time.strftime("%H:%M:%S", t)  


fbFunc=fenbiFunction.FenBi()
ftp = fbFunc.baseFunc.ftpconnect("down.licai668.cn", "wwsa518", "ww190103emp")#分笔全息数据Ftp账户 
fbFunc.nowtime = StrIMSt
ftpFileName='zbi_'+today+'.rar'                      #大富翁全息分笔数据ftp服务器端当日下载文件名
localFileName=fbFunc.fbqx_ftpdir+'/' +ftpFileName    #本地路径和文件名   
fbFunc.baseFunc.downloadfile(ftp, ftpFileName,localFileName)  #下载全息分笔数据
