# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import tushare as ts
import pymssql
import os
import time
import datetime
from sqlalchemy import *
import threading
#Timer（定时器）是Thread的派生类，
#用于在指定时间后调用一个方法。


# db_engine = pymssql.connect(host='192.168.97.66', port=1433 ,user='sa', password='Sa@9035065', database='today') 

# db_engine=create_engine("mssql+pymssql://sa:Sa@9035065@192.168.97.66:1433/today?charset=utf8",echo=True)
# conn=pymssql.connect(host="*",user="*",password="*",database="*")
# engine=create_engine("mysql+pymysql://toshare1:toshare1@192.168.151.213:3306/kday?charset=utf8",echo=True)  
# ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
# pro = ts.pro_api()
# df = pro.daily(ts_code='000001.SZ', start_date='19911230', end_date='19991231')
# df2 = pro.daily(ts_code='000002.SZ', start_date='19911230', end_date='19991231')
# print(df)

#cal_dates = ts.trade_cal()
#df = pro.daily(trade_date='20180810')
# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# df = pro.get_today_ticks('601388',)
# df = ts.get_tick_data('600000',date='2018-12-07',src='tt')
# df1=df['volume'].sum() #105805
# print(df1)
# df = ts.pro_bar(pro_api=pro, ts_code='601388.SH', adj='qfq', start_date='20181206', end_date='20181206')    
# print(df)
# df.to_sql('kday_601388',engine,if_exists='append',index=false)   
# data.to_sql('today',con=db_engine,if_exists='replace',index=False) 

# txt_file='I:\\fenbiTxt\\20181207\\SH600000.txt'
# txt_file1='I:\\fenbiTxt\\20181207\\SH601388.txt'
# HD5_filename="e:\\test.h5"
# data=pd.read_csv(txt_file,sep='\t', encoding='utf8',names=['trade_time', 'close', 'vol'])
# print(data)
# data1=abs(data['vol']).sum()
# print(data.describe())
# print(data.apply(sum))
# data['trade_time']=data['trade_time'].astype(str).str.zfill(6)
# data['trade_time']='20180105'+data['trade_time']
# data['trade_time']=pd.to_datetime(data['trade_time'])            
# data['close']=data['close']/100
# data.insert(0, 'ts_code', '600000.SH')
# data.insert(4, 'amount', data['close']*data['vol']) 

# h5 = pd.HDFStore(HD5_filename,'w')
# h5['trade_time'] = data      
# h5.close()   
# HD5_filename='e:/20181210.h5'
# rpt=pd.read_hdf(HD5_filename)
# df=rpt[rpt['ts_code'].str.contains('SZ$')]
# amout=df['amount'].sum()

# print(amout)
# pd.set_option('io.hdf.default_format','table')
# data2=pd.read_csv(txt_file1,sep='\t', encoding='utf8',names=['trade_time', 'close', 'vol'])

# store = pd.HDFStore(HD5_filename)
# print(store.keys())
# store.append('ts_code', data)
# store.append('trade_time', data2)
# print(store.get("trade_time"))
# data.to_hdf(HD5_filename,key='trade_time',append=True)
# data.close()

# data=pd.read_csv(txt_file1,sep='\t', encoding='utf8',names=['trade_time', 'close', 'vol'])  
# h5 = pd.HDFStore(HD5_filename,'w',append=True)
# h5['data'] = data      
# h5.close()   
# data=pd.read_hdf(HD5_filename)
# groups = store.select_column('trade_time','vol').unique()

import platform 
os = platform.system()
print(os)

  
