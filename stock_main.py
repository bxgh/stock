import time
from datetime import datetime as dt
import pymssql
import pandas as pd
import numpy as np
import tushare as ts
from io import StringIO
from sqlalchemy import create_engine
import logging
from time import sleep
from queue import LifoQueue
import threading
import random


# con = create_engine('mssql+pyodbc://username:password@myhost:port/databasename?driver=SQL+Server+Native+Client+10.0')
# engine=create_engine("mssql+pymssql://sa:1@192.168.151.141:1433/ba_zyyy_new?charset=utf8",echo=True)
#import decimal
class MSSQL:
  def __init__(self,host,user,pwd,db):
    self.host=host
    self.user=user
    self.pwd=pwd
    self.db=db
    self.hisDate_queue = LifoQueue() #股票历史日期数据，用于分期获取数据
    self.trade_cal_queue = LifoQueue() 
    self.stockBasic_queue = LifoQueue()
    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
    self.pro = ts.pro_api()
    self.stockBasic = self.pro.stock_basic(exchange='',fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    self.getTrade_cal() #初始化交易日期队列、股票代码队列

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

  def getDatetime(self): #获取当天日期
        '''获取当天日期的函数 '''
        taday = dt.now().strftime('%Y%m%d')
        return taday  

  def getTrade_cal(self):  #获取交易日、股票列表队列，用于多线程      
        trade_cal = self.pro.query('trade_cal', exchange='SZSE', start_date=self.getDatetime(),
                                   end_date=self.getDatetime(), is_open=1)
        #将日期列转换为list，便于使用队列
        trade_cals = trade_cal['cal_date'].tolist()
        for trade_cal in trade_cals:
            self.trade_cal_queue.put(trade_cal, True, 2)   
        #股票代码存入队列
        stcodes=self.stockBasic
        stocksList=stcodes['ts_code'].tolist()
        #循环将每个交易日塞进队列中
        for stcodes in stocksList:
            self.stockBasic_queue.put(stcodes, True, 2)   

  def  GetWriteConnect(self):
    # connectStr1 = "mssql+pymssql://"+self.user + ":" + self.pwd + "@" + self.host+ ":1433/" + self.db+"?charset=utf8"
    connectStr = "mssql+pymssql://"+self.user + ":" + self.pwd + "@" + self.host+ "/"+self.db+"?charset=utf8"                            
    engine=create_engine(connectStr,echo=True)    
    # cur=self.engine.cursor()
    return engine  
  def GetConnect(self):
    if not self.db:
      raise(NameError,'没有目标数据库')
    self.connect=pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset='utf8')    
    cur=self.connect.cursor()
    if not cur:
      raise(NameError,'数据库访问失败')
    else:
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
    return  

  def createTable(self,tableKind,tableName):
    # 生成表
    exesql ="exec createTable " +"'"+tableKind+"'" +","+"'"+tableName+"'"     
    curCreate=self.GetConnect()               
    curCreate.execute(exesql)
    self.connect.commit()
    self.connect.close()       
    return 

  def createTables(self,tableKind) :
    # 批量生成表
    # df = self.pro.stock_basic(exchange='',fields='ts_code')  
    for index, row in self.stockBasic.iterrows():    
       ts_code=row["ts_code"]
       self.createTable(tableKind,ts_code)                
    return

  def getHisDate(self,tsCode,listDate):  
    # 根据股票发行日期按3年一组分组，tushare获取历史数据最好以3年为时间段
    a = time.strptime(listDate,'%Y%m%d');
    sYear = a.tm_year  
    today = str(pd.Timestamp(dt.now())-pd.Timedelta(days = 1))[:10]  
    eYear = today[:4]    
    today = today[:4]+today[5:7]+today[8:10]
    listInt = int((int(eYear)-int(sYear))/3)+1
    dateList = [[0 for i in range(0)] for i in range(listInt)]
    i=0
    while (i < listInt ):
        if i == 0 :
          startDate = listDate
        else : 
          startDate = str(int(sYear)+i*3)+'0101'
        if i== listInt-1:
          endDate  = today
        else : 
          endDate  = str(int(sYear)-1+(i+1)*3)+'1231'
        dateList[i].append(tsCode)
        dateList[i].append(startDate)  
        dateList[i].append(endDate) 
        self.hisDate_queue.put(dateList[i], True, 1)   #将分好的日期存入队列   
        i = i + 1    
    # hisDate = pd.DataFrame(dateList, columns=['tsCode','startDate', 'endDate']) 为dataframe设置标题
    return    
  def getHisDates(self,stockList): 
    #讲所有股票的历史日期列表按3年分组存入队列，供获取历史数据使用       
    for index, row in stockList.iterrows():    
       ts_code=row["ts_code"]
       list_date=row["list_date"]       
       self.getHisDate(ts_code,list_date)       
    #    hisDates=pd.concat([hisDates,hisDates1],ignore_index=True)  合并dataframe 这里没用 
    # logging.info('共计%s条数据' % (self.hisDate_queue.qsize()))    
    return  
  
  def trucHiskday(self):
    queue1=self.hisDate_queue   
    while not queue1.empty():
      queue_data1 = queue1.get(True, 2) #从队列中取出数据
      stockcode1 = queue_data1[0]      
      curTruc=self.GetConnect()   
      trucSql ='truncate table' +'[kday_' + stockcode1+']'
      curTruc.execute(trucSql)
      self.connect.commit()
      self.connect.close() 
      sleep(random.randint(1, 2))
    return   

  def getKday(self,tscode,startDate,endDate):  
    df = self.pro.query('daily', ts_code=tscode, start_date=startDate, end_date=endDate)
    engineListAppend= self.GetWriteConnect()
    tablename ='kday_'+tscode    
    df.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000) 
    # logging.info('--> %s 的数据共计:%s 条 <--' %(tscode, len(df)))   
    return

  def getHisKdays (self):
    '''获指定日期或日期范围的股票数据__股票历史k线数据'''
    # logging.info('线程(%s)启动' % (threading.current_thread().name))    
    queue2=self.hisDate_queue
    while not queue2.empty():        	
        queue_data = queue2.get(True, 2) #从队列中取出数据
        stockcode = queue_data[0]
        sdate = queue_data[1]
        edate = queue_data[2]
        self.getKday(stockcode,sdate,edate) 
        # sleep(random.randint(1, 2))
    # logging.info('线程(%s)结束' % (threading.current_thread().name))
    return 
  
  def getSuspend(self,tscode,suspendDate):
    #参数说明：tscode:股票代码;suspendDate:查询起始日期
    if suspendDate=='': ##全部历史停牌信息
        df = self.pro.suspend(ts_code=tscode, suspend_date='', resume_date='', fields='')
        df.drop_duplicates('suspend_date',keep='last',inplace=True)  #日期去重
        engineListAppend= self.GetWriteConnect()
        tablename ='ts_suspend'    
        df.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000) 
    else :  ##指定日期后停牌信息
        df = self.pro.suspend(ts_code=tscode, suspend_date=suspendDate, resume_date='', fields='')
        df.drop_duplicates('suspend_date',keep='last',inplace=True)  #日期去重
        engineListAppend= self.GetWriteConnect()
        tablename ='ts_suspend'    
        df.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000)     
    return

  def getSuspends(self,stockQueue,suspendDate):
    #参数说明：stockQueue:查询股票队列;suspendDate:查询起始日期
    # queue1=self.stockBasic_queue 
    fo = open("I:\stocks_e.txt", "r+")    #错误数据存入文件 
    if suspendDate=='': ##全部历史停牌信息    
      while not stockQueue.empty():  
        try:
            queue_data = stockQueue.get(True, 2)   #从股票队列中取出股票代码
            stockcode = queue_data                 
            self.getSuspend(stockcode,'') 
        except Exception as e:         
            #  queue2.put(stockcode) # 将没有爬取成功的数据放回队列里面去，以便下次重试。
            fo.seek(0, 2)
            line = fo.write(stockcode)
            time.sleep(10)
            continue  
    else:
       while not stockQueue.empty():  
        try:
            queue_data = stockQueue.get(True, 2)   #从股票队列中取出股票代码
            stockcode = queue_data                   
            self.getSuspend(stockcode,suspendDate) 
        except Exception as e:         
            #  queue2.put(stockcode) # 将没有爬取成功的数据放回队列里面去，以便下次重试。
            fo.seek(0, 2)
            line = fo.write(stockcode)
            time.sleep(10)
            continue             
    return    

  def temp(self):
    engineListAppend= self.GetWriteConnect()
    # df = self.pro.trade_cal(exchange='', start_date='20180506', end_date='')
    # df.to_sql('trade_cal',engineListAppend,if_exists='append',index=False,chunksize=1000) 
    # df = self.pro.suspend(ts_code='000004.SZ', suspend_date='', resume_date='', fields='')
    # print(df)
    # df =self.stockBasic_queue.get(True,2)
    # dL = self.stockBasic['ts_code'].tolist()     
    # queue1=self.stockBasic_queue
    queue_1=LifoQueue() 
    f=open('I:\stocks.txt')    
    stocks=[line.strip() for line in f.readlines()]
    for i in range(len(stocks)):
         queue_1.put(stocks[i])
    # data1=ts.get_realtime_quotes(dL[0:880])
    # df=self.pro.suspend(ts_code=dL[0:880])    
    return queue_1
     
def main():
  ms = MSSQL(host="127.0.0.1\MSSERVER2008", user="sa", pwd="123", db="stock")  
  ms.getSuspends(ms.temp(),'')


#   ms.getSuspends()
 
  
#   ms.log()
  #resList = ms.ExecQuery("select * from zd_unit_code")  
#   ms.StockList()
#   print(resList)
#   ms.getKday("000008.SZ","20180101","20181120")
#   ms.setStockList()
#   ms.createTables('kday_')

#   stoc_basic=ms.stockBasic
#   ms.getHisDates(stoc_basic) 

#   for x in range(5):
#       x += 1
#       t1 = threading.Thread(target=ms.getSuspends, name='getHisKdays %d 号进程' % (x))
#       t1.start()
#       t1.join()

#   ms.temp('')

#   print(df)
if __name__ == '__main__':
  main()
#   input("执行完成:")


 

