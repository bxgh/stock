import time
from datetime import datetime as dt
import os
import pymysql,pymssql 
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
from ftplib import FTP
import random
import basewin
import timeit


# con = create_engine('mssql+pyodbc://username:password@myhost:port/databasename?driver=SQL+Server+Native+Client+10.0')
# engine=create_engine("mssql+pymssql://sa:1@192.168.151.141:1433/ba_zyyy_new?charset=utf8",echo=True)
#import decimal
class baseFunc:
  def __init__(self,host,port,user,pwd,db,myOrms):
    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token
    self.pro = ts.pro_api()            #连接tushare  
    self.mysqlormssql=myOrms
    self.host=host                     #获取数据库连接字符串
    self.port=int(port)
    self.user=user
    self.pwd=pwd
    self.db=db
    self.engineListAppend=self.GetWriteConnect()
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
    self.isNotTradeDay()                #获取是否交易日
    self.getTrade_cal()                 #初始化交易日期队列、股票代码队列
    self.api = ts.pro_api('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')    
    
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
        logging.info('开始获取%s的数据' % (self.getDatetime('no')))

  def getDatetime(self,type):              #获取当天日期       
      if type=='no':
        taday = dt.now().strftime('%Y%m%d')
      if type=='-' : 
        taday = dt.now().strftime("%Y-%m-%d")
      return taday  
  
  def extrRarFile(self,rarFile,destDir):  #解压缩文件
    folder_name=r"C:\\Program Files\\7-Zip" #7z.exe位置    
    os.chdir(folder_name)    
    cmd = '7z.exe x "{}" -o{} -aos -r'.format(rarFile,destDir)
    os.system(cmd)
  
  def tscodeTran(self,codets):
    tscode=codets[-2:].lower()+codets[0:6]
    return tscode

  def hhmmss(self,timestr):
    hh=timestr[:2]
    mm=timestr[2:4]
    ss=timestr[4:]
    hms=hh+':'+mm+':'+ss    
    return hms

  def getTscodeQueue(self)  : 
     tscodeQueue=queue.Queue()
     stcodes=self.stockBasic
     stocksList=stcodes['ts_code'].tolist()
        #循环将每个交易日塞进队列中
     for stcodes in stocksList:
        tscodeQueue.put(stcodes, True, 2)  
     return tscodeQueue    


  def getTrade_cal(self):             #获取交易日、股票列表队列，用于多线程      
        trade_cal = self.pro.query('trade_cal', exchange='SZSE', start_date=self.getDatetime('no'),
                                   end_date=self.getDatetime('no'), is_open=1)
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
    if self.file_queue.queue.qsize()>0 :
      return
    else:
      # self.file_queue.queue.clear()         
      for file in os.listdir(self.allKdayDir):  
              index1=file[15:23]+'-'+file[5:14]
              stocklist.append([index1,file])
      stocklist.sort()
      for list1 in stocklist:               
          self.file_queue.put(list1[1])

  def isNotTradeDay(self):    
    df=self.pro.query('trade_cal', start_date=self.getDatetime('no'), end_date=self.getDatetime('no'))
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

  def ExecSqlReturn(self,sql):
     cur=self.GetConnect()
     cur.execute(sql)     
     data =cur.fetchall() #获取查询到数据
     return data

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
    if self.mysqlormssql=='mysql':
     exesql = "CALL `create_table`("+ "'"+tableKind+"'" +","+"'"+tableName+"'" +");"         
    if self.mysqlormssql=='mssql':
      if tableKind=='fenbi_':
        exesql = "exec createTableFb "+ "'"+tableKind+"'" +","+"'"+tableName+"'"        
    curCreate=self.GetConnect()               
    curCreate.execute(exesql)
    self.connect.commit()
    self.connect.close()       
    return 

  def createTables(self,statusBar,tableKind) :
    # 批量生成表 
    statusBar.gauge.SetValue(0) #初始化进度条
    df=self.stockBasic
    total1=df['ts_code'].size #获取股票总数，做计算进度条分母
    for index, row in self.stockBasic.iterrows():    
       ts_code=row["ts_code"]
       ts_code=self.tscodeTran(ts_code)
       self.createTable(tableKind,ts_code)  
       progress=int(index*100/total1) #计算进度条      
       statusBar.gauge.SetValue(progress)   
    statusBar.gauge.SetValue(100)                
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
       self.getHisDate(ts_code,list_date)       
    #    hisDates=pd.concat([hisDates,hisDates1],ignore_index=True)  合并dataframe 这里没用 
    # logging.info('共计%s条数据' % (self.hisDate_queue.qsize()))    
    return  
  
  def trucHiskday(self):
    # queue1=self.hisDate_queue   
    # while not queue1.empty():
    #   queue_data1 = queue1.get(True, 2) #从队列中取出数据
    #   stockcode1 = queue_data1[0]      
    #   curTruc=self.GetConnect()   
    #   trucSql ='truncate table' +'[kday_' + stockcode1+']'
    #   curTruc.execute(trucSql)
    #   self.connect.commit()
    #   self.connect.close() 
    #   sleep(random.randint(1, 2))
    curTruc=self.GetConnect()   
    trucSql ='exec [dbo].[deleteAllKday]'
    curTruc.execute(trucSql)
    self.connect.commit()
    self.connect.close()  
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
        try:
          self.getKday(stockcode,sdate,edate)
        except Exception as e:
          sleep(5)
          queue2.put(queue_data)
    # logging.info('线程(%s)结束' % (threading.current_thread().name))
    return  

  def getKdayH5(self,tscode,startDate,endDate):  
    tablename ='kday_'+tscode 
    # df = self.pro.query('daily', ts_code=tscode, start_date=startDate, end_date=endDate)    
    try:
     df = ts.pro_bar(pro_api=self.api, ts_code=tscode, adj='qfq', start_date=startDate, end_date=endDate)    
     filename = self.allKdayDir + tablename + '_' + startDate + '_' + endDate        
     h5 = pd.HDFStore(filename,'w')
     h5['data'] = df      
     h5.close()    
    except :
     h5.close() 
     return 0  
    return 1

  def getAllHisKdaysH5 (self,statusBar):
    '''获指定日期或日期范围的股票数据__股票历史k线数据'''
    # logging.info('线程(%s)启动' % (threading.current_thread().name))    
    queue2=self.hisDate_queue        
    while not queue2.empty():        	
        queue_data = queue2.get(True, 2) #从队列中取出数据
        stockcode = queue_data[0]
        sdate = queue_data[1]
        edate = queue_data[2]
        restqueue=queue2.qsize() 
        geted=self.statustotal-restqueue       
        progress=int(geted*100/self.statustotal) #计算进度条      
        # print(progress)
        statusBar.gauge.SetValue(progress) 
        result =self.getKdayH5(stockcode,sdate,edate)
        if result ==1 :
          sleep(0.1)
        else  :
          queue2.put(queue_data)          
          print('error!')
          return 

        # try:
        #   self.getKdayH5(stockcode,sdate,edate)
        #   sleep(0.1)                                
        # except Exception as e:                    
        #   queue2.put(queue_data)
        #   print(e)
        #   print('error!')
        #   sleep(65)
        #   self.api = ts.pro_api('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')  
    # logging.info('线程(%s)结束' % (threading.current_thread().name))
    return 
  
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

  def kday_close(self,closeday) :  
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
    if (dflen > tradeDay) :
      trucSql = 'delete from allKday_closed where trade_date = '+"'"+closeday+"'"
      curTruc=self.GetConnect()         
      curTruc.execute(trucSql)
      self.connect.commit()
      self.connect.close()  
      i=0
      i1=int(dflen/1000)  
      while i<i1+1 :        
          dfi=df[i*1000:(i+1)*1000]
          try:
            dfi.to_sql(tablename,engineListAppend,if_exists='append',index=False,chunksize=1000)         
            self.isKdayClosed=1
          except:          
            self.isKdayClosed=0
          i=i+1 
    #收盘数据导入个股K线数据表
    readSql = 'select ts_code from allKday_closed where trade_date = '+"'"+closeday+"'" #pd获取收盘日所有日线数据
    tscodeList = pd.read_sql_query(readSql,con = engineListAppend)
    for index,row in tscodeList.iterrows():    
      ts_code=row["ts_code"]
      rrSql = 'select * from `kday_'+ts_code+'` where trade_date = '+"'"+closeday+"'"+' and ts_code='+"'"+ts_code+"'"
      tspd= pd.read_sql_query(rrSql,con = engineListAppend)  #判断是否已经导入日线到个股表
      if len(tspd)==0 :  #如果没有导入，就执行导入。
        wSql='insert into `kday_'+ts_code+"`"+" select * from allKday_closed where trade_date = "+"'"+closeday+"'"+" and ts_code="+"'"+ts_code+"'"
        curTruc=self.GetConnect()         
        curTruc.execute(wSql)
        self.connect.commit()
        self.connect.close()  
        


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

  def ftpconnect(self,host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

  #从ftp下载文件
  def downloadfile(self,ftp, remotepath, localpath):
      bufsize = 1024
      fp = open(localpath, 'wb')
      ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
      ftp.set_debuglevel(0)
      fp.close()

  #从本地上传文件到ftp
  def uploadfile(self,ftp, remotepath, localpath):
      bufsize = 1024
      fp = open(localpath, 'rb')
      ftp.storbinary('STOR ' + remotepath, fp, bufsize)
      ftp.set_debuglevel(0)
      fp.close()

  def test(self,dt):
    # engineListAppend= self.GetWriteConnect()
    # df = self.pro.trade_cal(exchange='', start_date='20180506', end_date='')
    # df.to_sql('trade_cal',engineListAppend,if_exists='append',index=False,chunksize=1000) 
    # df = self.pro.suspend(ts_code='000004.SZ', suspend_date='', resume_date='', fields='')
    # print(df)
    # df =self.stockBasic_queue.get(True,2)
    # dL = self.stockBasic['ts_code'].tolist()     
    # queue1=self.stockBasic_queue
    # queue_1=LifoQueue() 
    # f=open('I:\stocks.txt')    
    # stocks=[line.strip() for line in f.readlines()]
    # for i in range(len(stocks)):
    #      queue_1.put(stocks[i])
    # data1=ts.get_realtime_quotes(dL[0:880])
    # df=self.pro.suspend(ts_code=dL[0:880])    
    print(dt)
    return 
     
def main(): 
  pass

if __name__ == '__main__':
  main()



 

