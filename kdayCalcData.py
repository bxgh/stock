import time
from datetime import datetime as dt
import os
import pymysql
import pandas as pd
import numpy as np
import tushare as ts
from io import StringIO
from sqlalchemy import create_engine
import logging
from time import sleep
from queue import LifoQueue
import queue
import threading
import random
import basewin
import timeit

class CALCDATA:
  def __init__(self,host,user,pwd,db):
    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token
    self.pro = ts.pro_api()            #连接tushare  
    self.host=host                     #获取数据库连接字符串
    self.user=user
    self.pwd=pwd
    self.db=db
    self.hisDate_queue = LifoQueue()    #股票历史日期数据，用于分期获取数据
    self.trade_cal_queue = LifoQueue()  #初始化交易日队列
    self.stockBasic_queue = LifoQueue() #初始化股票代码队列
    self.file_queue = queue.Queue()       #kday文件列表队列，用于读取hdf5数据转存到sqlserver
    self.statustotal=0                  #初始化进度条
    self.isTradeDay=1                   #是否交易日
    self.isKdayClosed=0                 #当天是否执行日线收盘作业
    self.allKdayDir='./kday/'
    #股票交易代码list
    self.stockBasic = self.pro.stock_basic(exchange='',fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')      
   


def  GetWriteConnect(self):
    # connectStr1 = "mssql+pymssql://"+self.user + ":" + self.pwd + "@" + self.host+ ":1433/" + self.db+"?charset=utf8"
    connectStr = "mysql+pymysql://"+self.user + ":" + self.pwd + "@" + self.host+ "/"+self.db+"?charset=utf8"  
    # engine=create_engine("mysql+pymysql://toshare1:toshare1@192.168.151.213:3306/kday?charset=utf8",echo=True)                          
    engine=create_engine(connectStr,echo=True)        
    return engine  

def GetConnect(self):
    # self.connect=pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset='utf8')    
    self.connect=pymysql.connect(host=self.host,port=3306,user=self.user,password=self.pwd,database=self.db,charset='utf8')    
    cur=self.connect.cursor()
    return cur

def ExecSql(self,sql):
     cur=self.GetConnect()
     cur.execute(sql)
     self.connect.commit()
     self.connect.close()

def ExecQuery(self,sql):
    cur=self.GetConnect()
    cur.execute(sql)
    resList = cur.fetchall()
    self.connect.close()
    return resList  


