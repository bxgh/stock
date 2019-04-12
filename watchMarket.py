import requests
import re,random
import numpy as np
import tushare as ts
import pandas as pd
from queue import LifoQueue
# import threading
import time 
from datetime import datetime as dt
# from WindPy import *
import easyquotation
import pymysql


class watchStockMarket:
  def __init__(self) :             #初始化
    # easyquotation.update_stock_codes()
    self.quotationQq = easyquotation.use('qq')
    self.quotationSina = easyquotation.use('sina')
    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token
    self.pro = ts.pro_api() 
    self.tscodeData = self.pro.query('stock_basic', exchange='', list_status='L', fields='symbol')
    self.stockList  = self.tscodeData['symbol'].tolist()                                      #沪深A股股票代码转list供easyquotation调用
    self.connectQfq=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="kday_qfq",charset='utf8')  
    self.connectStat=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="statistics",charset='utf8') 

  def GetConnectStat(self):
    # self.connectQfq=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="kday_qfq",charset='utf8')  
    self.connectStat=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="statistics",charset='utf8')    
    cur=self.connectStat.cursor()
    return cur


  def getQqMarketData(self):              #获取新浪盘口数据
    data=self.quotationQq.stocks(self.stockList)
    df=pd.DataFrame.from_dict(data,orient='index')    
    df=df.reset_index()
    df.rename(columns={'index':'tscode'},inplace=True)
    # df=df.loc[df['tscode'].str.contains('001|002|000|30|60')]
    df=df[(df['turnover']>0)]
    ups=df[df['涨跌']>0]['code'].count()               #上涨家数
    downs=df[df['涨跌']<0]['code'].count()             #下跌家数   
    draws=df[df['涨跌']==0]['code'].count()            #平盘家数
    uplimits=df[df['涨停价']==df['now']]['code'].count() #涨停家数
    downlimits=df[df['跌停价']==df['now']]['code'].count() #涨停家数
    
    tradeTime=dt.now().strftime('%Y-%m-%d %H:%M:%S')
    curTruc=self.GetConnectStat()      
    exesql=" insert into  watch_market (trade_time,ups,draws,downs,uplimits,downlimits) value (%s,%s,%s,%s,%s,%s)"
    curTruc.execute(exesql,(tradeTime,int(ups),int(draws),int(downs),int(uplimits),int(downlimits)))      
    self.connectStat.commit()
    self.connectStat.close()  



def main(): 
    # 
    # sql="select concat(LOWER(RIGHT(ts_code,2)), LEFT(ts_code,6)) as code from allKday_closed WHERE trade_date='2019-04-10' "
    # tscodeDf=pd.read_sql(sql,con=connect)

    # w.start() 
    # print(quotationQq.real('sh603956'))
    # quotationQq.stocks()
    
    watchMarket=watchStockMarket()  
    while True:
      watchMarket.getQqMarketData()
      time.sleep(30)


if __name__ == '__main__':
  main()

  quotationSina = easyquotation.use('sina')



  data=quotationSina.market_snapshot(prefix=True) 
  df=pd.DataFrame.from_dict(data,orient='index')
  df=df.reset_index()
  df.rename(columns={'index':'tscode'},inplace=True)
  df=df.loc[df['tscode'].str.contains('sz00|sz30|sh60')]
  df=df[(df['turnover']>0)]
  print(df)

