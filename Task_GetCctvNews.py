import configparser
import datetime
import logging
import os
import queue
import random
import threading
import time
import timeit
from datetime import datetime as dt
from decimal import Decimal
from io import StringIO
from queue import LifoQueue
from time import sleep
import numpy as np
import pandas as pd
import pymysql
import tushare as ts
from sqlalchemy import create_engine
import pymssql

#获取昨天新闻联播内容，每天早上6:00执行
ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token
pro = ts.pro_api() 
engine=create_engine("mysql+pymysql://toshare1:toshare1@192.168.151.216:3306/kday?charset=utf8",echo=True)   

while True:
    today=datetime.date.today() 
    sqlday = today.strftime('%Y-%m-%d')
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday
    startday = today.strftime('%Y%m%d')              #今天
    endday = yesterday.strftime('%Y%m%d')             #昨天


    try:
        dfRes =  pro.cctv_news(date=endday)
        dfRes['channels']='cctv'               
        dfRes['datetime']=endday
        del dfRes['date']
        readSql='select * from news where channels="cctv" and datetime >"'+endday +'"'       
        newsDf = pd.read_sql_query(readSql,con = engine)
        df=pd.concat([newsDf,dfRes])   
        # print(df)
        df=df.drop_duplicates(subset=['title'],keep=False)
        df= df.sort_values('datetime')      
        # print(df) 
        if df.size>0:
          df.to_sql('news',engine,if_exists='append',index=False,chunksize=1000) 
        break  
    except:
        time.sleep(300)   
   