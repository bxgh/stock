# -*- coding: utf-8 -*-
import pandas as pd
# import xlrd
import os
import pymssql
import queue
from sqlalchemy import create_engine
import tushare as ts
import django
import easyquotation

quotationQq = easyquotation.use('qq')
result=quotationQq.stocks('600519')
data=result['600519']
data=quotationQq.real('600519')
print(data)

tscode='603039' 
tsdm='sh'+tscode+'.js'
quotation = easyquotation.use("timekline")
df = quotation.real([tscode], prefix=True) 
data =df[tsdm]
data['yestclose']=65.4
print(data)

# for h5file in os.listdir('D:\\h5data\\'): 
#     h5file1='D:\\h5data\\'+h5file    
#     h5 = pd.HDFStore(h5file1,'r')     
#     df = h5['data']
#     df=df.set_index('trade_date') 
#     print(df)
# #     h5.close()

ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
pro = ts.pro_api()
# df = pro.cctv_news(date='20190506')
# pro = ts.pro_api()
# df = pro.news(src='sina', start_date='20190401', end_date='20190430')
# print(df)
df1=ts.pro_bar(api=pro, ts_code='603919.SH',freq='m',start_date='20190517', end_date='20190517')  
# df=pro.daily(trade_date='20190506')
print(df1)
# df1 = pro.adj_factor(ts_code='', trade_date='20190419')
# df2 = pro.adj_factor(ts_code='', trade_date='20190423')
# df=pd.concat([df1,df2])
# df=df.drop_duplicates(subset=['ts_code','adj_factor'],keep=False)
# df=df[df['adj_factor']>1.000]
# df=df[df['trade_date']=='20190423']
# df=df.sort_values('ts_code')
# print(df)


h5 = pd.HDFStore('testdf0430','r')
df = h5['data']
# df= df.sort_values('trade_date')

df['maxZf'] = df.apply(lambda x :round((x['highest']-x['lowest'])/x['lowest']*100,2),axis=1)
df['lostZf'] = df.apply(lambda x :round((x['highest']-x['lowest1'])/x['highest']*100,2),axis=1)
df['tscode'] = df.apply(lambda x :x['ts_code'][0:6],axis=1)
df=df.sort_values('lostZf')
# print(df)
# df=df[(df['highestDate']>df['lowestDate']) ]
# df=df[df['ts_code']=='300176.SZ']
df=df[(df['lowerDateDiff1']<5) & (df['lostZf']>35) &(df['lowest1']!=-1)]
# df=df[(df['lowest1']==-1) & (df['pct_chg']<0) &(df['lowerDateDiff']<10)]
res=df['ts_code'].tolist()
# df['tscode'].to_excel("tscode0430.xlsx")
print(df[['ts_code','highest','lowest','lowest1','low','close','maxZf','lostZf','highDateDiff','lowerDateDiff','lowerDateDiff1','pct_chg']])
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
df['priceMax']=df['high'].max()   
df['priceMin']=df['low'].min()
df['amountMax']=df['amount'].max()  
df['amountMin']=df['amount'].min()  

print(df)

df=df.drop_duplicates(['trade_date'])
maxFactor=df.tail(1).iloc[0,11]
df['open']=df.apply(lambda x : round(x['open']*x['adj_factor']/maxFactor,2),axis=1)
df['high']=df.apply(lambda x : round(x['high']*x['adj_factor']/maxFactor,2),axis=1)
df['low']=df.apply(lambda x :  round(x['low']*x['adj_factor']/maxFactor,2),axis=1)
df['close']=df.apply(lambda x :round(x['close']*x['adj_factor']/maxFactor,2),axis=1)
df['pre_close']=df.apply(lambda x :round(x['pre_close']*x['adj_factor']/maxFactor,2),axis=1)
df['vol']=df.apply(lambda x : round(x['vol']*maxFactor/x['adj_factor'],2),axis=1)


f=df[df['trade_date']>'20110908']
print(f)
print(maxFactor)

ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
pro = ts.pro_api()
df1 = pro.adj_factor(ts_code='', trade_date='20190419')
df2 = pro.adj_factor(ts_code='', trade_date='20190423')

# df=pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# startDate='19930505'
# endDate='20190417'
# tscode='001872.SZ'
# tscode1='SZ001872'
df1=ts.pro_bar(pro_api=pro, ts_code='002006.SZ',adj='qfq',start_date='20110909', end_date='20190419')  
print(df1)
# df2=ts.pro_bar(pro_api=pro, ts_code=tscode, start_date='20030101', end_date=endDate)  
# df=pd.concat([df1,df2])
# df=df.sort_values('trade_date', ascending=False)   
# filename = 'D:\\h5data\\' + 'kday_' +tscode1 + '_' + startDate + '_' + endDate        
# h5 = pd.HDFStore(filename,'w')
# h5['data'] = df      
# h5.close()
# print(df)

# fileList=os.listdir('D:\\h5data\\')
# fileList.sort()
# filelistDf=pd.DataFrame(fileList,columns=['fileName'])
# df=filelistDf.loc[filelistDf['fileName'].str.contains('SH600000')]
# print(df.loc[0,'fileName'])
# print(df['fileName'])
# filelistDf['symbol']=filelistDf.fileName.apply(lambda x: x[7:13] )
# filelistDf['listdate']=filelistDf.fileName.apply(lambda x: x[14:22] )

# print(df,filelistDf)
# comdf=pd.merge(df,filelistDf,on='symbol')

# df1=comdf[comdf['list_date']!=comdf['listdate']]
# print(df1)
# comdf[comdf['list_date']<>'20199')]


# h5 = pd.HDFStore('D:\\h5data\\kday_SZ000001_19910403_20190418','r')
# df1 = h5['data']
# print(df1)

tscode1=''
file1=''
for h5file in os.listdir('D:\\h5data\\'):  
    tscode2=h5file[5:13]
    if tscode1==tscode2:     
     tscode1=tscode2
     endDate=h5file[23:33]
     h5file1='D:\\h5data\\'+file1
     h5file2='D:\\h5data\\'+h5file
     h5 = pd.HDFStore(h5file1,'r')
     hh5= pd.HDFStore(h5file2,'r')
     df1 = h5['data']
     df2=hh5['data']
     df=pd.concat([df1,df2])
     df=df.sort_values(by = 'trade_date', ascending=False)   
     filename = 'D:\\h5data1\\' + 'kday_' +tscode1 + '_' + startDate + '_' + endDate        
     hhh5 = pd.HDFStore(filename,'w')
     hhh5['data'] = df      
     h5.close()    
     hh5.close()
     hhh5.close()
     os.remove(h5file1)
     os.remove(h5file2)
     file1=h5file
     print(h5file,filename)
    else:
     tscode1=tscode2 
     file1=h5file
     startDate=h5file[14:22]



h5 = pd.HDFStore('D:\\h5data1\\kday_SH600000_19991110_20190417','r')
hh5= pd.HDFStore('D:\\h5data\\kday_SZ000001_20060101_20190417','r')
df1 = h5['data']
df2=hh5['data']
df=pd.concat([df1,df2])
df=df.sort_values(by = 'trade_date', ascending=False)
print(df)

fbQQCodeQueue = queue.Queue()

# 设置tushare.token
ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
pro = ts.pro_api()
pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# print(df1,df2)
try:
 df1 = ts.pro_bar(pro_api=pro, ts_code='600000.SH', start_date='19991110', end_date='20190417') 
 df2 = pro.adj_factor(ts_code='600000.SH', start_date='19991110', end_date='20190417')
 df=pd.merge(df1,df2) 
 print(df)
except Exception as e:
 print(e)
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