# -*- coding: utf-8 -*-
import pandas as pd
import xlrd
import os
import pymssql
import queue
from sqlalchemy import create_engine
import tushare as ts


fbQQCodeQueue = queue.Queue()

# 设置tushare.token
ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
pro = ts.pro_api()
stockBasic = pro.stock_basic(
    exchange='', fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
stocksList = stockBasic['ts_code'].tolist()
for stcodes in stocksList:
    tscode = stcodes[-2:].lower()+stcodes[0:6]
    fbQQCodeQueue.put(tscode, True, 2)


filecounts = fbQQCodeQueue.qsize()  # 分笔文件总数
threadcounts = 9  # 线程数
threadFileCounts = int(filecounts/threadcounts)+1
print(filecounts,threadFileCounts)


threadList = []
fbqxFileLists = []
fbqxFileList = []

for x in range(threadcounts):
    fbqxFileLists.append([])

for x in range(threadcounts):    
    fbqxFileList = []
    i = 0
    if x<threadcounts-1:
     while i < threadFileCounts:                       
        tscode = fbQQCodeQueue.get()
        fbqxFileList.append([tscode, 0])
        fbqxFileLists[x].append(fbqxFileList)
        i += 1 
    else:
       while not fbQQCodeQueue.empty()     :
        tscode = fbQQCodeQueue.get()
        fbqxFileList.append([tscode, 0])
        fbqxFileLists[x].append(fbqxFileList)      
          
    
for x in range(threadcounts):
  print(fbqxFileLists[x][0])