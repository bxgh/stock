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


class MSSQL:
  def __init__(self,host,user,pwd,db,myOrms):
    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token
    # self.api = ts.pro_api('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')  
    self.pro = ts.pro_api()            #连接tushare  
    self.mysqlormssql=myOrms
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
    # self.stockBasic = self.pro.stock_basic(exchange='',fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    self.stockBasic = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    self.isNotTradeDay()                #获取是否交易日
    self.getTrade_cal()                 #初始化交易日期队列、股票代码队列    
    self.conf = configparser.ConfigParser()
    self.conf.read('config.ini')       
     #读取config：workDir配置，在对应控件上显示    
    self.kdayH5_dir = self.conf.get('workDir','kdayH5_dir') 
    self.kdayH5Qfq_dir = self.conf.get('workDir','kdayH5Qfq_dir') 

  def MarketOpen(self)  :   #开盘初始化
    self.stockBasic = self.pro.stock_basic(exchange='',fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    self.isNotTradeDay()                #获取是否交易日
    self.getTrade_cal()                 #初始化交易日期队列、股票代码队列
    # if self.isTradeDay==1:    
    self.stockBasic() 

  def log(self):
        ''' 日志功能函数'''
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            r'G:\python_code\hqms\log.log', encoding='utf-8')
        # handlerStream = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # logger.addHandler(handlerStream)
        logging.info('开始获取%s的数据' % (self.getDatetime()))

  def stockBasicH5(self):   
    filename = '.\\stockBasic.hd5'        
    h5 = pd.HDFStore(filename,'w')
    h5['data'] = self.stockBasic      
    h5.close()  

  def getDatetime(self):              #获取当天日期       
        taday = dt.now().strftime('%Y%m%d')
        return taday  

  def getTrade_cal(self):             #获取交易日、股票列表队列，用于多线程      
        trade_cal = self.pro.query('trade_cal', exchange='SZSE', start_date='20190101',
                                   end_date=self.getDatetime(), is_open=1)
        #将日期列转换为list，便于使用队列    
        # print(trade_cal)            
        trade_cals = trade_cal['cal_date'].tolist()                   
        self.cqtoday=str(trade_cal.tail(1).iloc[0,1])      #除权用日期
        self.cqyesterday=str(trade_cal.tail(2).iloc[0,1])  #除权用日期
        # print(self.cqtoday,self.cqyesterday)
        for trade_cal in trade_cals:
            self.trade_cal_queue.put(trade_cal, True, 2)   

        #股票代码存入队列
        stcodes=self.stockBasic
        stocksList=stcodes['ts_code'].tolist()
        #循环将每个交易日塞进队列中
        for stcodes in stocksList:
            self.stockBasic_queue.put(stcodes, True, 2)   
        
  def getFileQueue(self):
    stocklist=[]
    filelist=[] 
    self.file_queue.queue.clear()         
    for file in os.listdir(self.allKdayDir):  
            index1=file[15:23]+'-'+file[5:14]
            stocklist.append([index1,file])
    stocklist.sort()
    for list1 in stocklist:               
        self.file_queue.put(list1[1])

  def isNotTradeDay(self):    
    df=self.pro.query('trade_cal', start_date=self.getDatetime(), end_date=self.getDatetime())
    self.isTradeDay=int(df.iloc[0,2])

  def  GetWriteConnect(self):
    # connectStr1 = "mssql+pymssql://"+self.user + ":" + self.pwd + "@" + self.host+ ":1433/" + self.db+"?charset=utf8"
    if self.mysqlormssql=='mysql':
     connectStr = "mysql+pymysql://"+self.user + ":" + self.pwd + "@" + self.host+ "/"+self.db+"?charset=utf8"  
    if self.mysqlormssql=='mssql':
     connectStr = "mssql+pymssql://"+self.user + ":" + self.pwd + "@" + self.host+ "/"+self.db+"?charset=utf8" 
    # connectStr = "mysql+pymysql://"+self.user + ":" + self.pwd + "@" + self.host+ "/"+self.db+"?charset=utf8"  
    # engine=create_engine("mysql+pymysql://toshare1:toshare1@192.168.151.213:3306/kday?charset=utf8",echo=True)                          
    engine=create_engine(connectStr,echo=True)    
    # cur=self.engine.cursor()
    return engine  

  def GetConnect(self):
    if self.mysqlormssql=='mssql':
     self.connect=pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset='utf8')    
    if self.mysqlormssql=='mysql':
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
    return list(resList)  

  def setStockList(self):    
    #每日更新最新股票列表
    #清空股票列表
    curTruc=self.GetConnect()    
    curTruc.execute("truncate table  stock_basic")
    self.connect.commit()
    self.connect.close()  
    #获取最新股票列表
    engineListAppend= self.GetWriteConnect()
    #导入股票列表到数据库
    self.stockBasic.to_sql('stock_basic',engineListAppend,if_exists='append',index=False,chunksize=1000)    
    
    curTruc=self.GetConnect()    
    curTruc.execute("truncate table  trade_cal")
    self.connect.commit()
    self.connect.close() 
    df = self.pro.trade_cal(exchange='', start_date='19910101', end_date='')
    df.to_sql('trade_cal',engineListAppend,if_exists='append',index=False,chunksize=1000)      
    return  
 
  #获取单只个股历史k线数据保存为h5文件（除权数据）。入参：tscode 股票代码(600000.SH)
  def getKdayH5(self,tscode):      
    listDate=self.stockBasic[self.stockBasic['ts_code']==tscode]['list_date'].iloc[0]    
    # print(ts_listdate)
    a = time.strptime(listDate,'%Y%m%d')
    datezone=15  #tushare pro 一次只能获取4000条数据，折合kday数据15年
    sYear = a.tm_year  
    # today = str(pd.Timestamp(dt.now())-pd.Timedelta(days = 1))[:10] #截止日期到昨日 
    today = dt.now().strftime('%Y%m%d')    
    eYear = today[:4]    
    # today = today[:4]+today[5:7]+today[8:10]
    listInt = int((int(eYear)-int(sYear))/datezone)+1
    dataList = []    
    i=0
    while (i < listInt ):
        if i == 0 :
          startDate = listDate
        else : 
          startDate = str(int(sYear)+i*datezone)+'0101'
        if i== listInt-1:
          endDate  = today
        else : 
          endDate  = str(int(sYear)-1+(i+1)*datezone)+'1231'
        
        T=True
        while T:
          try:      
            df1 = ts.pro_bar(pro_api=self.pro, ts_code=tscode, start_date=startDate, end_date=endDate) 
            df2 = self.pro.adj_factor(ts_code=tscode, start_date=startDate, end_date=endDate)
            df=pd.merge(df1,df2)               
            dataList.append(df)  
            T=False     
          except Exception as e:  
            if e=='index out of bounds':
                print('error in'+tscode)
                T=False
            else:  
                time.sleep(121)         
        i = i + 1        
    resultDf=pd.concat(dataList)    
    resultDf=resultDf.sort_values('trade_date', ascending=True)      
    tablename ='kday_'+tscode[7:9]+tscode[0:6]     
    # print(tablename)
    if resultDf.size>0:
      filename = self.kdayH5_dir + tablename + '_' + listDate + '_' + today  
      filenameRes= tablename + '_' + listDate + '_' + today     
      h5 = pd.HDFStore(filename,'w')
      h5['data'] = resultDf      
      h5.close() 
    return filenameRes      

  #获取所有个股历史k线数据保存为h5文件（除权数据），需要45分钟左右
  def getAllHisKdaysH5 (self):
    '''获指所有股票数据__股票历史k线数据，截止到昨日'''
    for index, row in self.stockBasic.iterrows():
       ts_code=row["ts_code"]
       filename=self.getKdayH5(ts_code)

  #收盘补充h5qfq数据,入参：closeday:收盘日期(20190418)
  def kdayCloseH5(self,closeday): 
   engineListAppend= self.GetWriteConnect() 
   while True:                  #获取tushare当日收盘行情,保存数据到mysql数据库
     try :
       df=self.pro.daily(trade_date=closeday)
       if df.size>0 :
         df.to_sql('daily_data',engineListAppend,if_exists='append',index=False,chunksize=1000)  #收盘数据保存到mysql数据库
        #  print(df['ts_code'].size)
       break
     except:
       time.sleep(300)  

   while True:               
    if df.size>0: 
      h5fileList=os.listdir(self.kdayH5Qfq_dir)
      filelistDf=pd.DataFrame(h5fileList,columns=['fileName'])
      for index, row in df.iterrows():
        ts_code=row["ts_code"]                   #600618.SH
        loctscode=ts_code[7:9]+ts_code[0:6]      #SH600618
        dfRes=df[df['ts_code']==ts_code]       
        # print(loctscode)
        try:
          tstemp=filelistDf.loc[filelistDf['fileName'].str.contains(loctscode)]
          h5fileName=tstemp.iloc[0,0]      
          h5 = pd.HDFStore(self.kdayH5Qfq_dir+h5fileName,'r')
          h5His = h5['data']
          # h5His.drop['adj_factor']
          # h5His.drop(['adj_factor'],axis=1,inplace=True)
          resH5=pd.concat([h5His,dfRes])
          resH5.drop_duplicates(subset=['trade_date'],keep='first',inplace=True) 
          # print(resH5)
          h5.close()
          h5 = pd.HDFStore(self.kdayH5Qfq_dir+h5fileName,'w') 
          h5['data'] = resH5
          h5.close() 
          print(loctscode) 
        except: #新股
          h5fileName='kday_'+loctscode
          h5 = pd.HDFStore(self.kdayH5Qfq_dir+h5fileName,'w') 
          h5['data'] = dfRes
          h5.close() 
      break    
  

  #收盘根据除权因子变化找到分红股票，重新导入前复权行情数据,不需要传日期参数，默认为当天为最新日期
  def kdayCloseH5qfq(self):    
    # today=datetime.date.today() 
    # oneday=datetime.timedelta(days=1) 
    # yesterday=today-oneday
    # cqtoday = today.strftime('%Y%m%d')              #今天
    # cqyesterday = yesterday.strftime('%Y%m%d')      #跟昨天复权因子相比
    # cqtoday='20190424'
    # cqyesterday='20190418'
    chuquan_queue=LifoQueue()
    while True:
      try :
        df1 = self.pro.adj_factor(ts_code='', trade_date=self.cqyesterday)   #当天除权因子
        df2 = self.pro.adj_factor(ts_code='', trade_date=self.cqtoday)   #昨天除权因子  
        df=pd.concat([df1,df2])
        df=df.drop_duplicates(subset=['ts_code','adj_factor'],keep=False)  #去重，未除权的数据去掉
        df=df[df['adj_factor']>1.000]                                   #去除新股
        df=df[df['trade_date']==self.cqtoday]                                #留下最新日期除权数据
        dfFenHong=df.sort_values('ts_code')     
        stocksList=dfFenHong['ts_code'].tolist()
        #除权股票代码塞进队列中
        for stcodes in stocksList:
            chuquan_queue.put(stcodes, True, 2)   

        # for  index,row in dfFenHong.iterrows():
        while not chuquan_queue.empty():
            # ts_code=row["ts_code"]
            ts_code=chuquan_queue.get(True,2)
            # print(ts_code)
            filename=self.getKdayH5(ts_code)                             #重新获取最新历史数据，截止日期today
            #  print(filename)
            self.h5FileToH5QfqFile(filename)                             #将历史数据转为前复权数据，保存到h5qfq
            filename=self.kdayH5Qfq_dir+filename[0:13]
            self.H5QfqDataToSqlData(filename,0)                          #将最新前复权数据存入mysql数据库，filename:'D:\h5qfqdata\kday_SH600396',0:收盘作业
        break    
      except:
        if len(ts_code)>0 :
          chuquan_queue.put(ts_code, True, 2)  
        time.sleep(121) 
        
  #h5原始行情数据转前复行情h5文件
  def h5FileToH5QfqFile(self,h5fileName):       
    h5 = pd.HDFStore(self.kdayH5_dir+h5fileName,'r')
    df = h5['data']    
    df= df.sort_values('trade_date')
    df=df.drop_duplicates(['trade_date'])
    maxFactor=df.tail(1).iloc[0,11]
    df['open']=df.apply(lambda x : round(x['open']*x['adj_factor']/maxFactor,2),axis=1)
    df['high']=df.apply(lambda x : round(x['high']*x['adj_factor']/maxFactor,2),axis=1)
    df['low']=df.apply(lambda x :  round(x['low']*x['adj_factor']/maxFactor,2),axis=1)
    df['close']=df.apply(lambda x :round(x['close']*x['adj_factor']/maxFactor,2),axis=1)
    df['pre_close']=df.apply(lambda x :round(x['pre_close']*x['adj_factor']/maxFactor,2),axis=1)
    df['vol']=df.apply(lambda x : round(x['vol']*maxFactor/x['adj_factor'],2),axis=1)
    df.drop(['adj_factor'],axis=1,inplace=True)
    h5.close()
    h5QfqfileName=self.kdayH5Qfq_dir+h5fileName[0:13]
    h5 = pd.HDFStore(h5QfqfileName,'w')
    h5['data'] = df
    h5.close()

  #h5行情文件转h5前复权文件初始化，一次性转换所有文件
  def h5dataToh5QfqInit(self) :
     for h5file in os.listdir(self.kdayH5_dir): 
       print(h5file)
       self.h5FileToH5QfqFile(h5file)
   

  #h5前复权K线数据转mysql数据库初始化，清空后一次性转换所有数据，kdayH5Qfq_dir为H5前复权文件存放目录
  def H5QfqDataToSqlDataInit(self) :    
    isinit=1
    for h5qfqfile in os.listdir(self.kdayH5Qfq_dir): 
       h5qfqFileName=self.kdayH5Qfq_dir+h5qfqfile
       print(h5qfqFileName)
       self.H5QfqDataToSqlData(h5qfqFileName,isinit)
  
  #h5前复权K线数据转mysql数据，单文件转换，FileName为H5前复权文件:'D:\h5qfqdata\kday_SH600396',isinit:初始化1，收盘任务0
  def  H5QfqDataToSqlData(self,FileName,isinit) :    
    if isinit==0 : #如果执行收盘任务，要先删除原来该股票k线数据      
       ts_code=FileName[-6:]+'.'+FileName[-8:-6]
       sql="delete from daily_data where ts_code='"+ts_code+"'"
       curTruc=self.GetConnect()         
       curTruc.execute(sql)
       self.connect.commit()
       self.connect.close() 
    
    h5 = pd.HDFStore(FileName,'r')   #读取H5qfq数据
    df = h5['data']
    engineListAppend= self.GetWriteConnect()     
    df.to_sql('daily_data',engineListAppend,if_exists='append',index=False,chunksize=1000)  #存入mysql数据库 
    h5.close()  

  def kdayCloseH5Only(self,closeday):    
   while True:                  
     try :
       df=self.pro.daily(trade_date=closeday)       
       break
     except:
       time.sleep(120)  

   while True:               
    if df.size>0: 
      h5fileList=os.listdir(self.kdayH5Qfq_dir)
      filelistDf=pd.DataFrame(h5fileList,columns=['fileName'])
      for index, row in df.iterrows():
        ts_code=row["ts_code"]                   #600618.SH
        loctscode=ts_code[7:9]+ts_code[0:6]      #SH600618
        dfRes=df[df['ts_code']==ts_code]    
        try:
          tstemp=filelistDf.loc[filelistDf['fileName'].str.contains(loctscode)]
          h5fileName=tstemp.iloc[0,0]      
          h5 = pd.HDFStore(self.kdayH5Qfq_dir+h5fileName,'r')
          h5His = h5['data']          
          resH5=pd.concat([h5His,dfRes])          
          resH5.drop_duplicates(subset=['trade_date'],keep='first',inplace=True) 
          h5.close()
          h5 = pd.HDFStore(self.kdayH5Qfq_dir+h5fileName,'w') 
          h5['data'] = resH5
          h5.close() 
          print(loctscode) 
        except: #新股
          h5fileName='kday_'+loctscode
          h5 = pd.HDFStore(self.kdayH5Qfq_dir+h5fileName,'w') 
          h5['data'] = dfRes
          h5.close() 
      break    
  
  #收盘根据除权因子变化找到分红股票，重新导入前复权行情数据,不需要传日期参数，默认为当天为最新日期,数据不入库，供本地使用
  def kdayCloseH5qfqOnly(self):    
    # today=datetime.date.today() 
    # oneday=datetime.timedelta(days=1) 
    # yesterday=today-oneday
    # cqtoday = today.strftime('%Y%m%d')              #今天
    # cqyesterday = yesterday.strftime('%Y%m%d')      #跟昨天复权因子相比
    # cqtoday='20190424'
    # cqyesterday='20190426'
    # print(self.cqtoday)
    while True:
      try :
        # self.cqyesterday='20190430'
        df1 = self.pro.adj_factor(ts_code='', trade_date=self.cqyesterday)   #当天除权因子
        df2 = self.pro.adj_factor(ts_code='', trade_date=self.cqtoday)   #昨天除权因子  
        df=pd.concat([df1,df2])
        df=df.drop_duplicates(subset=['ts_code','adj_factor'],keep=False)  #去重，未除权的数据去掉
        df=df[df['adj_factor']>1.000]                                   #去除新股
        df=df[df['trade_date']==self.cqtoday]                                #留下最新日期除权数据
        dfFenHong=df.sort_values('ts_code')        
        for  index,row in dfFenHong.iterrows():
            ts_code=row["ts_code"]
            print(ts_code)
            filename=self.getKdayH5(ts_code)                             #重新获取最新历史数据，截止日期today
            #  print(filename)
            self.h5FileToH5QfqFile(filename)                             #将历史数据转为前复权数据，保存到h5qfq           
        break    
      except:
        time.sleep(121) 
     

def main():  
  mskday = MSSQL(host="192.168.151.216", user="toshare1", pwd="toshare1", db="kday",myOrms="mysql")  
  if mskday.isTradeDay==1 :
    closeDay=mskday.getDatetime()    
    mskday.kdayCloseH5(closeDay)
    mskday.kdayCloseH5qfq()
 
if __name__ == '__main__':
  main()
  # mskday = MSSQL(host="192.168.151.216", user="toshare1", pwd="toshare1", db="kday",myOrms="mysql") 
  
  # mskday.kdayCloseH5Only('20190508') 
  # mskday.kdayCloseH5qfqOnly()     

  # mskday.kdayCloseH5('20190507')
  # mskday.kdayCloseH5qfq()
  