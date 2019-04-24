import time,datetime
from decimal import Decimal
from datetime import datetime as dt
import os
import pymysql
import pymssql
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
import timeit
import configparser


# con = create_engine('mssql+pyodbc://username:password@myhost:port/databasename?driver=SQL+Server+Native+Client+10.0')
# engine=create_engine("mssql+pymssql://sa:1@192.168.151.141:1433/ba_zyyy_new?charset=utf8",echo=True)
#import decimal
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
    self.createTables('','kday_')
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

  def createTable(self,tableKind,tableName):
    # 生成表,使用sqlserver存储过程实现（createTable）
    # exesql ="exec createTable " +"'"+tableKind+"'" +","+"'"+tableName+"'"    
    exesql = "CALL `create_table`("+ "'"+tableKind+"'" +","+"'"+tableName+"'" +");"         
    curCreate=self.GetConnect()               
    curCreate.execute(exesql)
    self.connect.commit()
    self.connect.close()       
    return 

  def createTables(self,statusBar,tableKind) :
    # 批量生成表 
    # statusBar.gauge.SetValue(0) #初始化进度条
    df=self.stockBasic
    total1=df['ts_code'].size #获取股票总数，做计算进度条分母
    for index, row in self.stockBasic.iterrows():    
       ts_code=row["ts_code"]
       self.createTable(tableKind,ts_code)  
      #  progress=int(index*100/total1) #计算进度条      
    #    statusBar.gauge.SetValue(progress)   
    # statusBar.gauge.SetValue(100)                
    return

  def renCol(self,tableKind,tableName):
    # 修改表字段名
    # exesql ="exec renameCol " +"'"+tableKind+"'" +","+"'"+tableName+"'"  
    exesql="CALL `updatecolumn` ("+"'"+tableName+"'"+")"
    try:
      curCreate=self.GetConnect()
      curCreate.execute(exesql)
      self.connect.commit()
      self.connect.close()
    except Exception as e: 
      print(e)                
    return 

  def renameCols(self,statusBar,tableKind) :
    # 批量修改表字段名 
    statusBar.gauge.SetValue(0) #初始化进度条
    df=self.stockBasic
    total1=df['ts_code'].size #获取股票总数，做计算进度条分母    
    for index, row in self.stockBasic.iterrows():    
       ts_code=row["ts_code"]
       self.renCol(tableKind,ts_code) 
       progress=int(index*100/total1) #计算进度条      
       statusBar.gauge.SetValue(progress)   
    statusBar.gauge.SetValue(100)                       
    return 
  
  def getHisDate(self,tsCode,listDate):  
    # 根据股票发行日期按3年一组分组，tushare获取历史数据最好以3年为时间段
    a = time.strptime(listDate,'%Y%m%d');
    datezone=15  #tushare pro 一次只能获取4000条数据，折合kday数据15年
    sYear = a.tm_year  
    today = str(pd.Timestamp(dt.now())-pd.Timedelta(days = 1))[:10]  
    eYear = today[:4]    
    today = today[:4]+today[5:7]+today[8:10]
    listInt = int((int(eYear)-int(sYear))/datezone)+1
    dateList = [[0 for i in range(0)] for i in range(listInt)]
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
        dateList[i].append(tsCode)
        dateList[i].append(startDate)  
        dateList[i].append(endDate) 
        
        self.hisDate_queue.put(dateList[i], True, 1)   #将分好的日期存入队列   
        i = i + 1    
    # hisDate = pd.DataFrame(dateList, columns=['tsCode','startDate', 'endDate']) 为dataframe设置标题

    return  

  def getHisDates(self,stockList): 
    #讲所有股票的历史日期列表按3年分组存入队列，供获取历史数据使用       
    self.hisDate_queue.queue.clear()
    for index, row in stockList.iterrows():    
       ts_code=row["ts_code"]
       list_date=row["list_date"]   
      #  if ts_code[0:3]=='001':
       self.getHisDate(ts_code,list_date)      #list_date：股票上市日期 
    #    hisDates=pd.concat([hisDates,hisDates1],ignore_index=True)  合并dataframe 这里没用 
    # logging.info('共计%s条数据' % (self.hisDate_queue.qsize()))    
    return  
  
  def getWholeKday(self) :  #获取所有股票K线历史数据，初始化数据
    self.trucHiskday()   
    # result=df[(df['ask1_volume']==0) & (df['volume']>0)]
    self.getHisDates(self.stockBasic)
    self.getHisKdays()


  def trucHiskday(self):     #mysql删除所有K线历史数据
    for index,row in self.stockBasic.iterrows():
     stockcode=row['ts_code']
     sql='DELETE from `kday_'+stockcode+'`'
     try :
      self.ExecSql(sql)      
     except:
       pass 
        

  def getKday(self,tscode,startDate,endDate):  
    # df = self.pro.query('daily', ts_code=tscode, start_date=startDate, end_date=endDate)
    df = ts.pro_bar(pro_api=self.pro, ts_code=tscode, adj='qfq', start_date=startDate, end_date=endDate)  
    engineListAppend= self.GetWriteConnect()
    tablename ='kday_'+tscode   
    if df.size>0 :
     df.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000) 
    # logging.info('--> %s 的数据共计:%s 条 <--' %(tscode, len(df)))   
    return
 
  def getHisKdays (self):
    '''获指定日期或日期范围的股票数据__股票历史k线数据'''
    # logging.info('线程(%s)启动' % (threading.current_thread().name))    
    queue2=self.hisDate_queue    
    stockGotList=[]
    while not queue2.empty():                	
        queue_data = queue2.get(True, 2) #从队列中取出数据
        stockcode = queue_data[0]
        print(stockcode)
        sdate = queue_data[1]
        edate = queue_data[2]  
        if edate>sdate:    
         while True:
          try:
            self.getKday(stockcode,sdate,edate)              
            break
          except Exception as e:          
            if e=='index out of bounds':
              print(stockcode)
              break
            else:  
              time.sleep(121)
    return  
 
  #获取单只个股历史k线数据保存为h5文件（除权数据）。入参：tscode 股票代码(600000.SH)
  def getKdayH5(self,tscode):      
    listDate=self.stockBasic[self.stockBasic['ts_code']==tscode]['list_date'].iloc[0]    
    # print(ts_listdate)
    a = time.strptime(listDate,'%Y%m%d')
    datezone=15  #tushare pro 一次只能获取4000条数据，折合kday数据15年
    sYear = a.tm_year  
    today = str(pd.Timestamp(dt.now())-pd.Timedelta(days = 1))[:10] #截止日期到昨日 
    eYear = today[:4]    
    today = today[:4]+today[5:7]+today[8:10]
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
    print(tablename)
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
   while True:                  #获取tushare当日收盘行情
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
        # print(loctscode)
        try:
          tstemp=filelistDf.loc[filelistDf['fileName'].str.contains(loctscode)]
          h5fileName=tstemp.iloc[0,0]      
          h5 = pd.HDFStore(self.kdayH5Qfq_dir+h5fileName,'r')
          h5His = h5['data']
          # h5His.drop['adj_factor']
          # h5His.drop(['adj_factor'],axis=1,inplace=True)
          resH5=pd.concat([h5His,dfRes])
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
  
  #收盘根据除权因子变化找到分红股票，重新导入前复权行情数据
  def kdayCloseH5qfq(self):    
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday
    cqtoday = today.strftime('%Y%m%d')
    cqyesterday = yesterday.strftime('%Y%m%d')
    cqtoday='20190423'
    cqyesterday='20190418'
    df1 = self.pro.adj_factor(ts_code='', trade_date=cqyesterday)   #当天除权因子
    df2 = self.pro.adj_factor(ts_code='', trade_date=cqtoday)   #昨天除权因子
    df=pd.concat([df1,df2])
    df=df.drop_duplicates(subset=['ts_code','adj_factor'],keep=False)  #去重，未除权的数据去掉
    df=df[df['adj_factor']>1.000]                                   #去除新股
    df=df[df['trade_date']==cqtoday]                                #留下最新日期除权数据
    dfFenHong=df.sort_values('ts_code')
    # print(dfFenHong)
    for  index,row in dfFenHong.iterrows():
       ts_code=row["ts_code"]
      #  print(ts_code)
       filename=self.getKdayH5(ts_code)
       print(filename)
       self.h5FileToH5QfqFile(filename)


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


  def saveH5ToSqlserver(self,FileName,engineListAppend) :    
    stockFileName=self.allKdayDir + FileName
    tablename = FileName[0:14]
    h5 = pd.HDFStore(stockFileName,'r')
    df = h5['data']
    # engineListAppend= self.GetWriteConnect()     
    dflen=len(df)  
    i=0
    if dflen<1001:
      try:
       df.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000) 
      except:
       h5.close()  
       return 0 
    else:
      i1=int(dflen/1000)  
      while i<i1+1 :
        print(i)
        dfi=df[i*1000:(i+1)*1000] 
        print(dfi)
        try:
         dfi.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000)         
        except:
         h5.close()  
         return 0
        i=i+1
    h5.close()      
    return 1    
    
  def calcKdayHisDays (self)  :
    self.getFileQueue()    
    engineListAppend= self.GetWriteConnect() 
    i=0
    dateList=[]
    while not self.file_queue.empty() :      
      filename=self.file_queue.get()      
      ts_code=filename[5:14]
      sDate=filename[15:23]
      eDate=filename[24:]
      h5 = pd.HDFStore(self.allKdayDir+filename,'r')
      df1 = h5['data']
      tradedays=df1.iloc[:,0].size
      h5.close()    

      startDate = sDate[0:4]+'-'+sDate[4:6]+'-'+sDate[6:8]
      endDate = eDate[0:4]+'-'+eDate[4:6]+'-'+eDate[6:8]
      # tableName='['+filename[0:14]+']' #mssql
      tableName='`'+filename[0:14]+'`' #mysql
      readSql = 'select count(*) from ' +tableName+' where trade_date between '+"'"+startDate+"'"+' and '+"'"+endDate +"'"
      data = pd.read_sql_query(readSql,con = engineListAppend)
      tradeDay=data.iloc[0,0]
      
      if tradedays==tradeDay:
        i=i+1
        print(i)
      else :  
        filename1=filename[0:14]+'_'+sDate+'_'+eDate
        dateList.append([filename1])
    
    dfresult= pd.DataFrame(dateList, columns=['filename'])    
    print(dfresult)
    h5 = pd.HDFStore('.\\kdayRest','w')
    h5['data'] = dfresult      
    h5.close()      
  
  def KdayHisGoOn(self) :
    h5 = pd.HDFStore('.\kdayrest','r')
    df1 = h5['data']
    engineListAppend= self.GetWriteConnect()
    for index, row in df1.iterrows():
      filename=row["filename"]
      SqlResult=self.saveH5ToSqlserver(filename,engineListAppend)           
      if SqlResult==0:
        print(filename)
    h5.close()

  def kday_closed(self):
    wSql="INSERT into analysisUnit(ts_code,trade_date,`open`,`close`,high,low,pre_close,`change`,pct_chg,vol,amount)"
    wSql=wSql+" select * from allKday_closed "    
    curTruc=self.GetConnect()         
    curTruc.execute(wSql)
    self.connect.commit()
    self.connect.close()  
    wSql=" delete from allKday_closed "    
    curTruc=self.GetConnect()         
    curTruc.execute(wSql)
    self.connect.commit()
    self.connect.close()  

  def kday_close(self,closeday) :  
   T=True
   maday=closeday[0:4]+'-'+closeday[4:6]+'-'+closeday[6:8]   
   while  T:
    df=self.pro.daily(trade_date=closeday)    
    engineListAppend= self.GetWriteConnect()
    tablename ='allKday_closed'   
    dflen=len(df)  
    #接收tushare收盘数据
    readSql = 'select count(*) from allKday_closed where trade_date = '+"'"+closeday+"'"
    data = pd.read_sql_query(readSql,con = engineListAppend)       
    try :
      tradeDay=data.iloc[0,0]
    except:  
      tradeDay=0  
    print('1',dflen,tradeDay)   
    if (dflen > tradeDay) :
      trucSql = 'delete from allKday_closed where trade_date = '+"'"+closeday+"'"
      curTruc=self.GetConnect()         
      curTruc.execute(trucSql)
      self.connect.commit()
      self.connect.close()  
      try:
        # 导入总表allKday_closed
        df.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000)         
        #收盘数据导入个股K线数据表
        readSql = 'select ts_code from allKday_closed where trade_date = '+"'"+closeday+"'" #pd获取收盘日所有日线数据
        tscodeList = pd.read_sql_query(readSql,con = engineListAppend)        
        for index,row in tscodeList.iterrows():    
          ts_code=row["ts_code"]
          # print(ts_code)
          self.createTable('kday_',ts_code)
          rrSql = 'select * from `kday_'+ts_code+'` where trade_date = '+"'"+closeday+"'"+' and ts_code='+"'"+ts_code+"'"
          tspd= pd.read_sql_query(rrSql,con = engineListAppend)  #判断是否已经导入日线到个股表
          if len(tspd)==0 :  #如果没有导入，就执行导入。
            wSql="INSERT into `kday_"+ts_code+"`"+"(ts_code,trade_date,`open`,`close`,high,low,pre_close,`change`,pct_chg,vol,amount)"
            wSql=wSql+" select * from allKday_closed where trade_date = "+"'"+closeday+"'"+" and ts_code="+"'"+ts_code+"'"
            # print(wSql)
            curTruc=self.GetConnect()         
            curTruc.execute(wSql)
            self.connect.commit()
            self.connect.close()    
      except:
        pass                          
    else:
      try:           
        self.getMa(maday) 
        self.calcMa(maday)  
        T=False 
      except:
        pass   
  

  def kday_getAllHis(self,closeday):
    df=self.pro.daily(trade_date=closeday)
    engineListAppend= self.GetWriteConnect()
    tablename ='analysisUnit'   
    dflen=len(df)  
    #接收tushare收盘数据
    readSql = 'select count(*) from analysisUnit where trade_date = '+"'"+closeday+"'"
    data = pd.read_sql_query(readSql,con = engineListAppend)    
    try :
      tradeDay=data.iloc[0,0]
    except:  
      tradeDay=0     
    if (dflen > tradeDay) :
      trucSql = 'delete from analysisUnit where trade_date = '+"'"+closeday+"'"
      curTruc=self.GetConnect()         
      curTruc.execute(trucSql)
      self.connect.commit()
      self.connect.close()  
      try:
        # 导入总表allKday_closed
        df.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000)         
      except:
        pass  

  def saveAllH5ToSqlserver(self,statusBar,engineListAppend) :  
    queue2=self.file_queue    
    while not queue2.empty():        	
        queue_data = queue2.get() #从队列中取出数据
        FileName = queue_data        
        restqueue=queue2.qsize() 
        geted=self.statustotal-restqueue       
        progress=int(geted*100/self.statustotal) #计算进度条      
        # print(progress)
        statusBar.gauge.SetValue(progress) 
        SqlResult=self.saveH5ToSqlserver(FileName,engineListAppend)           
        if SqlResult==0:
          print('error!')
          print(queue2.qsize)
          queue2.put(queue_data)
          print(queue2.qsize)
          sleep(60)
          
    # logging.info('线程(%s)结束' % (threading.current_thread().name))

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

  def mkdir(self,path):   
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\") 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path) 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)          
        return True
    else:
        pass
        return False

  def test(self):
    pass

  def analysisHis(self,closeday):
    engineListAppend= self.GetWriteConnect()
    readSql = 'select ts_code,close from analysisUnit where trade_date = '+"'"+closeday+"'" #pd获取收盘日所有日线数据
    tscodeList = pd.read_sql_query(readSql,con = engineListAppend)  
    file_handle = open('highHis.txt', 'w')
    for index,row in tscodeList.iterrows():    
      ts_code=row["ts_code"]
      close=row["close"]
      hisSql="SELECT min(low) as lowHis,max(high) as highHis  from `kday_"+ts_code+"`" +"where trade_date<='"+closeday+"'"
      hisResult = pd.read_sql_query(hisSql,con = engineListAppend)  
      if len(hisResult)>0:
       lowHis=hisResult.loc[0,'lowHis']
       highHis=hisResult.loc[0,'highHis']
       hisSql="SELECT trade_date  from `kday_"+ts_code+"`" +"where low="+str(lowHis)
       dateResult = pd.read_sql_query(hisSql,con = engineListAppend) 
       lowHisDate=dateResult.loc[0,'trade_date']
       hisSql="SELECT trade_date  from `kday_"+ts_code+"`" +"where high="+str(highHis)
       dateResult = pd.read_sql_query(hisSql,con = engineListAppend)
       highHisDate=dateResult.loc[0,'trade_date'] 
      #  exesql="update analysisUnit set highHis="+str(highHis)+",highHis_date='"+str(highHisDate)+"',lowHis="+str(lowHis)+",lowHis_date='"+str(lowHisDate)+"', priceScaleHis="+str(close-lowHis)+"/"+str(highHis-lowHis)+"*100 where ts_code='"+ts_code+"' and trade_date='"+closeday+"'"
      #  print(exesql)
      #  curTruc=self.GetConnect()         
      #  curTruc.execute(exesql)
      #  self.connect.commit()
      #  self.connect.close()  
      #  print(lowHis,highHis,lowHisDate,highHisDate)    
      #  file_handle.write("index"+","+"Kernel"+“,"+"Context"+","+"Stream"+'\n') # 写列名
       dm=ts_code[7:9]+ts_code[0:6]
       priceScaleHis=round((close-lowHis)/(highHis-lowHis)*100,2) 
      #  serise = dm+","+str(highHis)+","+str(highHisDate)+","+ str(lowHis)+","+ str(lowHisDate)+","+str(priceScaleHis)  # 每个元素都是字符串，使用逗号分割拼接成一个字符串
      #  print(dm)
       serise=dm+"\t"+str(highHis)
       print(serise)
       file_handle.write(serise+'\n') # 末尾使用换行分割每一行。
    file_handle.close()

  def limitCounts(self,closeday):
    engineListAppend= self.GetWriteConnect()
    readSql="select count(*) as upCounts from allKday_closed where  ts_code like "+"'"+'%%.SH'+"'"+" and pct_chg>9.98 and trade_date="+"'"+closeday+"'"
    tscodeList = pd.read_sql_query(readSql,con = engineListAppend)     
    upLimitSH=tscodeList.loc[0,'upCounts']
    readSql="select count(*) as upCounts from allKday_closed where  ts_code like "+"'"+'%%.SZ'+"'"+" and pct_chg>9.98 and trade_date="+"'"+closeday+"'"
    tscodeList = pd.read_sql_query(readSql,con = engineListAppend)     
    upLimitSZ=tscodeList.loc[0,'upCounts']
    readSql="select count(*) as upCounts from allKday_closed where  ts_code like "+"'"+'%%.SZ'+"'"+" and pct_chg<-9.98 and trade_date="+"'"+closeday+"'"
    tscodeList = pd.read_sql_query(readSql,con = engineListAppend)     
    downLimitSZ=tscodeList.loc[0,'upCounts']
    readSql="select count(*) as upCounts from allKday_closed where  ts_code like "+"'"+'%%.SH'+"'"+" and pct_chg<-9.98 and trade_date="+"'"+closeday+"'"
    tscodeList = pd.read_sql_query(readSql,con = engineListAppend)     
    downLimitSH=tscodeList.loc[0,'upCounts']
    statistic=[]
    statistic.append(upLimitSH)
    statistic.append(upLimitSZ)
    statistic.append(downLimitSH)    
    statistic.append(downLimitSZ)
    # print(upLimitSH,upLimitSZ,downLimitSH,downLimitSZ)
    return statistic

  def limitSave(self,limitContent):
    upLimitSH=int(limitContent[0])
    upLimitSZ=int(limitContent[1])
    downLimitSH=int(limitContent[2])
    downLimitSZ=int(limitContent[3])
    print(upLimitSH,upLimitSZ,downLimitSH,downLimitSZ)
    # for index,row in tscodeList.iterrows(): 
    curTruc=self.GetConnect()      
    exesql=" insert into  zflimit (ts_code,trade_date,uplimit_counts,downlimit_counts) value (%s,%s,%s,%s)"
    curTruc.execute(exesql,('000001.SH','20190313',upLimitSH,downLimitSH))  
    exesql=" insert into  zflimit (ts_code,trade_date,uplimit_counts,downlimit_counts) value (%s,%s,%s,%s)"
    curTruc.execute(exesql,('399001.SZ','20190313',upLimitSZ,downLimitSZ))  
    self.connect.commit()
    self.connect.close()  

  

  def getMa(self,maDate):    #计算均线 ，参数说明：maDate为均线计算日期，即收盘日期   
    edate=datetime.datetime.strptime(maDate, '%Y-%m-%d')
    sdate1 = edate +  datetime.timedelta(-400)
    sdate=dt.strftime(sdate1,'%Y-%m-%d')    
    sql="select ts_code from allKday_closed WHERE trade_date='"+maDate+"'"    
    connect=pymysql.connect(host=self.host,port=3306,user=self.user,password=self.pwd,database=self.db,charset='utf8')      
    # connect=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="kday_qfq",charset='utf8')      
    tscodeDf=pd.read_sql(sql,con=connect)
    firstCode=tscodeDf.head(1).iloc[0,0]
    print(firstCode)
    connect.close()

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
    

  def calcMa(self,calDate):
    maDir='c:\\ontimeKday\\ma\\'
    filename = maDir+calDate+".h5"       
    h5 = pd.HDFStore(filename,'r')
    ma =h5['data'] 

    ma['ma3up']=ma.apply(lambda r: (float(r['close'])-r['ma3'])*100/r['ma3'], axis=1)
    ma['ma5up']=ma.apply(lambda r: (float(r['close'])-r['ma5'])*100/r['ma5'], axis=1)  
    ma['ma10up']=ma.apply(lambda r: (float(r['close'])-r['ma10'])*100/r['ma10'], axis=1)  
    ma['ma20up']=ma.apply(lambda r: (float(r['close'])-r['ma20'])*100/r['ma20'], axis=1) 
    ma['ma30up']=ma.apply(lambda r: (float(r['close'])-r['ma30'])*100/r['ma30'], axis=1) 
    ma['ma60up']=ma.apply(lambda r: (float(r['close'])-r['ma60'])*100/r['ma60'], axis=1) 
    ma['ma120up']=ma.apply(lambda r: (float(r['close'])-r['ma120'])*100/r['ma120'], axis=1)     
    try :
      ma['ma250up']=ma.apply(lambda r: (float(r['close'])-r['ma250'])*100/r['ma250'], axis=1) 
    except:
      ma['ma250up']=ma.apply(lambda r: (float(r['close'])-r['ma240'])*100/r['ma240'], axis=1)   
    
    ts_code='000000.SZ'
    opens=ma[ma['close']>0]['close'].count()
    uplimits  =ma[(ma['close']-ma['high']==0) & (ma['pct_chg']>9.9)]['close'].count()
    downlimits=ma[(ma['close']-ma['low']==0) & (ma['pct_chg']<-9.9)]['close'].count()
    ma3up=ma[ma['ma3up']>0]['ma3up'].count()
    ma5up=ma[ma['ma5up']>0]['ma5up'].count()
    ma10up=ma[ma['ma10up']>0]['ma10up'].count()
    ma20up=ma[ma['ma20up']>0]['ma20up'].count()
    ma30up=ma[ma['ma30up']>0]['ma30up'].count()
    ma60up=ma[ma['ma60up']>0]['ma60up'].count()
    ma120up=ma[ma['ma120up']>0]['ma120up'].count()
    ma240up=ma[ma['ma250up']>0]['ma250up'].count()
    
    sql="INSERT INTO zflimit (ts_code,trade_date,uplimits,downlimits,opens,ma3ups,ma5ups,ma10ups,ma20ups,ma30ups,ma60ups,ma120ups,ma250ups ) values ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    connect=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="statistics",charset='utf8')  
    cur=connect.cursor()     
    cur.execute(sql,(ts_code,calDate,int(uplimits),int(downlimits),int(opens),int(ma3up),int(ma5up),int(ma10up),int(ma20up),int(ma30up),int(ma60up),int(ma120up),int(ma240up),)) 
    connect.commit()
    connect.close()    
    

    # print(ma[(ma['close']-ma['high']==0) & (ma['pct_chg']>9.91)])
    # print(ma3up,ma5up,ma10up,ma20up,ma30up,ma60up,ma120up,ma240up)

    h5.close()

  def addKday(self): #行情数据清除   
    for index,row in self.stockBasic.iterrows():      
     dm=row['ts_code']
     sql='DELETE from `kday_'+dm+'` where trade_date>"2018-10-31"'
     self.ExecSql(sql)
     while True:
      try:
        self.getKday(dm,'20181101','20190322')
        break
      except:
        time.sleep(301) 
      
    #  print(dm+' is ok !')
    

  

def main():  
  # maDir='c:\\ontimeKday\\ma\\'
  # filename = maDir+'2018-01-02'+".h5"       
  # h5 = pd.HDFStore(filename,'r')
  # ma =h5['data'] 
  # print(ma)
  # h5.close()



  mskday = MSSQL(host="192.168.151.216", user="toshare1", pwd="toshare1", db="kday_qfq",myOrms="mysql") 
  mskday.kdayCloseH5qfq()
  mskday.kdayCloseH5qfq()
  mskday.kdayCloseH5('20190423')
  mskday.getAllHisKdaysH5()

  mskday.getMa('2019-04-16')
  mskday.kday_close('20190412') 
  # mskday.calcMa('2019-04-11')
  # mskday.getWholeKday()
  trade_cal = mskday.pro.query('trade_cal', exchange='SZSE', start_date='2018010',end_date='20190404', is_open=1)
        #将日期列转换为list，便于使用队列
  trade_cals = trade_cal['cal_date'].tolist()
  for trade_cal in trade_cals:
    trade_cal=trade_cal[0:4]+'-'+trade_cal[4:6]+'-'+trade_cal[6:8]
    print(trade_cal)
    # mskday.getMa(trade_cal)
    mskday.calcMa(trade_cal)


  # mskday.test()
  # mskday.clearKday()

  # filename = 'c:\\ontimeKday\\ma\\20190403.h5'   
  # h5 = pd.HDFStore(filename,'r')
  # ma =h5['data'] 
  # ma['ma3_a']=ma.apply(lambda r: (float(r['close'])-r['ma3'])*100/r['ma3'], axis=1)
  # ma['ma5_a']=ma.apply(lambda r: (float(r['close'])-r['ma5'])*100/r['ma5'], axis=1)  
  # print(ma[ma['ma3_a']<0]['ma3_a'].count())
  # h5.close()

  # df=result[result['tradeDate']> dt.strptime('2017-01-01','%Y-%m-%d').date()]
  # date = dt.strptime('2017-01-01','%Y-%m-%d')
    #  df[(df['ask1_volume']==0) & (df['volume']>0)]
  # print(df)
  # statistics = MSSQL(host="192.168.151.216", user="toshare1", pwd="toshare1", db="statistics",myOrms="mysql")  
  # mskday.analysisHis('20190304')  
  # mskday.kday_close('20190304')
  # statistic=mskday.limitCounts('20190313')
  # statistics.limitSave(statistic)
  # print(statistic)
  #补充总表行情
  # trade_cal = mskday.pro.query('trade_cal', exchange='SZSE', start_date='20190101',end_date='20190304', is_open=1)
  #       #将日期列转换为list，便于使用队列
  # trade_cals = trade_cal['cal_date'].tolist()
  # for trade_cal in trade_cals:
  #   mskday.kday_getAllHis(trade_cal)

if __name__ == '__main__':
  mskday = MSSQL(host="192.168.151.216", user="toshare1", pwd="toshare1", db="kday_qfq",myOrms="mysql") 
  mskday.kdayCloseH5qfq()



 

