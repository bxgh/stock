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


def getMa(self,maDate):    #计算均线 ，参数说明：maDate为均线计算日期，即收盘日期   
    edate=datetime.datetime.strptime(maDate, '%Y-%m-%d')
    sdate1 = edate +  datetime.timedelta(-400)
    sdate=dt.strftime(sdate1,'%Y-%m-%d')    
    

    for tscode1 in tscodeDf['ts_code']:      
      # print(tscode1)
      sql1="SELECT * from `kday_"+tscode1+"` ORDER BY trade_date "   #获取股票kday数据
      # print(sql1)
      result1=self.ExecQuery(sql1)
      # print(result1)
      kdayData=pd.DataFrame(result1,columns=['ts_code','trade_date','open','close','high','low','pre_close','change','pct_chg','vol','amount'])   
      kdayData['highHis']=kdayData['high'].max() 
      print(kdayData)
      dfHis= kdayData.tail(1) 
      print(dfHis)
      if tscode1==firstCode :  #'000001.SZ' :
          res1=dfHis
      else:                
          res=res.append(df1)


      sql="SELECT * from `kday_"+tscode1+"` where trade_date >'"+sdate+"'  and trade_date<="+ "'"+maDate+"'"+" ORDER BY trade_date "   #获取股票kday数据
      result=self.ExecQuery(sql)
      df=pd.DataFrame(result,columns=['ts_code','trade_date','open','close','high','low','pre_close','change','pct_chg','vol','amount'])   
      
      try:
         tradeDate=str(df.tail(1).iloc[0,1]) 
        #  tradeDate='2019-03-29' 
      except:
         tradeDate='1970-01-01'  
      # print(tradeDate,tradeDate==str(maDate))         
      if tradeDate==str(maDate):         #剔除停牌股票
        df['ma3']=df['close'].rolling(3).mean()    #计算均线
        df['ma5']=df['close'].rolling(5).mean()
        df['ma10']=df['close'].rolling(10).mean()
        df['ma20']=df['close'].rolling(20).mean()
        df['ma30']=df['close'].rolling(30).mean()
        df['ma60']=df['close'].rolling(60).mean()
        df['ma120']=df['close'].rolling(120).mean()
        df['ma250']=df['close'].rolling(250).mean()      

        df['high3']=df['high'].rolling(3).max() 
        df['high5']=df['high'].rolling(5).max()
        df['high10']=df['high'].rolling(10).max()
        df['high20']=df['high'].rolling(20).max()
        df['high30']=df['high'].rolling(30).max()
        df['high60']=df['high'].rolling(60).max()
        df['highMax']=df['high'].max()
        df1= df.tail(1)    
        if tscode1==firstCode :  #'000001.SZ' :
          res=df1
        else:                
          res=res.append(df1)
    print(res)  
    filename = 'C:\\ontimeKday\\ma\\'+maDate+'.h5'   #保存结果到h5文件
    h5 = pd.HDFStore(filename,'w')
    h5['data'] = res      
    h5.close() 
    
