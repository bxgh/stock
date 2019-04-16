import requests
import re,random
import numpy as np
import tushare as ts
import pandas as pd
import time 
from datetime import datetime as dt
import easyquotation
import pymysql
import configparser


class watchStockMarket:
  def __init__(self) :             #初始化
    # easyquotation.update_stock_codes()
    self.quotationQq = easyquotation.use('qq')
    self.quotationSina = easyquotation.use('sina')
    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token
    self.pro = ts.pro_api() 
    #沪深A股股票代码转list供easyquotation调用
    self.tscodeData = self.pro.query('stock_basic', exchange='', list_status='L', fields='symbol')
    self.stockList  = self.tscodeData['symbol'].tolist()                                      
    #连接数据库
    self.connectQfq=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="kday_qfq",charset='utf8')  
    self.connectStat=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="statistics",charset='utf8') 

    #读取config 
    conf = configparser.ConfigParser()
    conf.read('config.ini')              
    # self.openMarket_dir =conf.get('workDir','openMarket_dir') 
    
    #获取昨日涨停个股列表
    #  preUpLimitList=

  def GetConnectStat(self):
    # self.connectQfq=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="kday_qfq",charset='utf8')  
    self.connectStat=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="statistics",charset='utf8')    
    cur=self.connectStat.cursor()
    return cur

  def getOpenMarketData(self):
    while True: 
     try:
      data=self.quotationQq.stocks(self.stockList)
      df=pd.DataFrame.from_dict(data,orient='index')    
      df=df.reset_index()
      df.rename(columns={'index':'tscode'},inplace=True)
      h5 = pd.HDFStore(self.openMarket_dir,'w')
      h5['data'] = df      
      h5.close()      
      break
     except: 
      pass


  def getQqMarketData(self):              #获取新浪盘口数据
   try: 
    data=self.quotationQq.stocks(self.stockList)
    df=pd.DataFrame.from_dict(data,orient='index')    
    df=df.reset_index()
    df.rename(columns={'index':'tscode'},inplace=True)
    # df=df.loc[df['tscode'].str.contains('001|002|000|30|60')]
    df=df[(df['turnover']>0)]
    ups=df[df['涨跌']>0]['code'].count()               #上涨家数
    downs=df[df['涨跌']<0]['code'].count()             #下跌家数   
    draws=df[df['涨跌']==0]['code'].count()            #平盘家数
    upsOpen=df[df['now']-df['open']>0]['code'].count()               #较开盘上涨家数
    downsOpen=df[df['now']-df['open']<0]['code'].count()             #较开盘下跌家数   
    drawsOpen=df[df['now']-df['open']==0]['code'].count()            #较开盘平盘家数
    uplimits=df[df['涨停价']==df['now']]['code'].count() #涨停家数
    downlimits=df[df['跌停价']==df['now']]['code'].count() #涨停家数
    avgzf=df['涨跌(%)'].mean()     
    
    tradeTime=dt.now().strftime('%Y-%m-%d %H:%M:%S')
    curTruc=self.GetConnectStat()      
    exesql=" insert into  watch_market (trade_time,ups,draws,downs,uplimits,downlimits,upsOpen,drawsOpen,downsOpen,avgZf) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    curTruc.execute(exesql,(tradeTime,int(ups),int(draws),int(downs),int(uplimits),int(downlimits),int(upsOpen),int(drawsOpen),int(downsOpen),float(avgzf)))     
    self.connectStat.commit()
    self.connectStat.close() 
   except:
    pass   

  def preUpLimitNow(self)  :
    pass

def main():   
  pass
    # watchMarket=watchStockMarket()  
    # while True:
    # watchMarket.getQqMarketData()
    #   time.sleep(30)


if __name__ == '__main__':
  main()
  

