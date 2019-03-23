import time
from datetime import datetime as dt
import urllib.request
import requests
import re
import os, base64,shutil
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
import baseFunction
import configparser

class FenBi:
  def __init__(self,timerType):   
    #  self.txtFenbiFileDir=conf.get("workDir", "txtFenbiFileDir")
    #  print(self.txtFenbiFileDir)
     #获取config配置文件     
     self.conf = configparser.ConfigParser()
     self.conf.read('config.ini') 
     #数据库连接
     host=self.conf.get('database','host_fenbi')
     host=base64.decodestring(bytes(host, 'utf-8')) 
     host= str(host, encoding = "utf-8")
     port=self.conf.get('database','port_fenbi')
     port=base64.decodestring(bytes(port, 'utf-8')) 
     port= str(port, encoding = "utf-8")
     user=self.conf.get('database','user_fenbi')
     user=base64.decodestring(bytes(user, 'utf-8'))     #解密     
     user= str(user, encoding = "utf-8")  
     pwd=self.conf.get('database','pwd_fenbi')
     pwd=base64.decodestring(bytes(pwd, 'utf-8'))
     pwd= str(pwd, encoding = "utf-8")
     db=self.conf.get('database','db_fenbi')
     db=base64.decodestring(bytes(db, 'utf-8'))
     db= str(db, encoding = "utf-8")
     mysqlormssql=self.conf.get('database','msormy_fenbi')
     mysqlormssql=base64.decodestring(bytes(mysqlormssql, 'utf-8'))
     mysqlormssql= str(mysqlormssql, encoding = "utf-8")
     #文件目录
     self.fbtxt_todaydir=self.conf.get('workDir','fb_txtFileTodayDir')
     self.hd5DestDir=self.conf.get('workDir','fb_hd5DestDir')  
     self.fbqx_ftpdir=self.conf.get('workDir','fbqx_ftpdir') 
     #代码范围
     self.fbqx_dmscope=self.conf.get('dmScope','fbqx')
     self.fbqx_onTimer=self.conf.get('onTimer','fbqx')
     self.onTimer_isFbqxFtpDown=self.conf.get('onTimer','isfbqxftpdown')


     self.baseFunc = baseFunction.baseFunc(host=host,port=port, user=user, pwd=pwd, db=db,myOrms=mysqlormssql)   
     
     self.fenbiQueue=self.baseFunc.stockBasic_queue
     self.fbQxFileQueue=LifoQueue()
     self.fbOntimeQueue=queue.Queue()
     self.pblist=[]
     self.trdlist=[]     
     t = time.localtime(time.time()) 
     self.today=time.strftime("%Y%m%d", t)  
     self.today_=time.strftime("%Y-%m-%d", t)  
     self.nowtime = time.strftime("%H:%M:%S", t) 
     self.fbqxDownloaded=0 #全息分笔数据下载标志，是否已经下载完毕
     self.fbqxDownloading=0 #全息分笔数据下载标志，是否正在下载
     self.extracted=0       #分笔文件是否已经解压缩标志
     self.iscsvTodbf=0      #判断csv是否已经入库
     self.timerType=timerType
  
  def MarketOpen(self):   #初始化数据，每日执行。FbDownQxftp.py
    self.fbqxDownloading=0 #初始化当日分笔全息数据下载标志，是否正在下载
    self.fbqxDownloaded=0  #初始化当日分笔全息数据下载标志，是否已经下载完毕
    self.extracted=0       #初始化下载后的分笔文件是否已经解压缩
    self.iscsvTodbf=0             #判断csv是否已经入库
    
    t = time.localtime(time.time()) 
    closeDay=time.strftime("%Y%m%d", t) 
    closeDay_=time.strftime("%Y-%m-%d", t)     
    self.conf.set(self.timerType,'closeDay',closeDay)  #初始化收盘日期存入config.ini 格式：20190118
    self.conf.set(self.timerType,'closeDay_',closeDay_)#初始化收盘日期存入config.ini 格式：2019-01-18
    self.conf.write(open("config.ini", "w"))

  def MarketClose(self,closeDay): #大富翁全息分笔数据ftp下载    FbDownQxftp.py     
   while True:
    start=dt.now()    
    exitFlag = 0
    treadsCounts=40
    threadList=[]
    csvFileList=[]    
    treadsCounts=int(self.conf.get('fbqx','csvToDbfThrs'))

    class myThread (threading.Thread):
      def __init__(self, threadID, name, q):
          threading.Thread.__init__(self)
          self.threadID = threadID
          self.name = name
          self.q = q
      def run(self):
          print ("开启线程：" + self.name)
          process_data(self.name, self.q)          
          print ("退出线程：" + self.name)
  
    def process_data(threadName, q):  #供线程使用的过程
        while not exitFlag:
            for filename in q:
                txt_file=filerDir+filename               
                self.QxCsvToHd5(txt_file)
                print ("%s processing %s" % (threadName, txt_file))          
            time.sleep(1) 

    filerDir=self.fbqx_ftpdir+'/csv/' +closeDay+'/'           #下载到本地路径和文件名        
    fileList=os.listdir(filerDir)
    dealListQueue=queue.Queue()
    for filename in fileList:      
      dealListQueue.put(filename)
    fileTotal=dealListQueue.qsize()
    
    threadFileCounts=int(fileTotal/treadsCounts)

    for x in range(treadsCounts):
        csvFileList.append([])
        threadList.append('Thread-'+str(x))
        fileCount=0
        while fileCount<threadFileCounts: 
            filename= dealListQueue.get()                   
            csvFileList[x].append(filename)
            fileCount+=1
    while not dealListQueue.empty():
        filename= dealListQueue.get()
        csvFileList[0].append(filename)

    threads = []
    threadID = 0

    # 创建新线程
    for tName in threadList:
        thread = myThread(threadID, tName, csvFileList[threadID])
        thread.start()
        threads.append(thread)
        print(threadID,len(csvFileList[threadID]))
        threadID += 1
    
    # print(len(threadList))
    exitFlag = 1

    # 等待所有线程完成    
    for t in threads:
        t.join()
        
    print ("退出主线程")

    print(start)
    print(dt.now())   
                       

  def extrRar(self):
      self.baseFunc.allKdayDir='I:\\BaiduNetdiskDownload\\fenbi2018\\'
      self.baseFunc.getFileQueue()
      
      destDir="I:\\fenbiTxt\\"              #解压目标文件夹
      folder_name=r"C:\\Program Files\\7-Zip" #7z.exe位置    
      os.chdir(folder_name)
      while not self.baseFunc.file_queue.empty():
          rar_file=self.baseFunc.file_queue.get()
          if rar_file[-3:]=='rar':             
             rar_file=self.baseFunc.allKdayDir+rar_file
             cmd = '7z.exe x "{}" -o{} -aos -r'.format(rar_file,destDir)
            #   print(cmd)
            #  os.system(cmd)
          if rar_file[-3:]=='.7z':             
             rar_file=self.baseFunc.allKdayDir+rar_file                       
             cmd = '7z.exe x "{}" -o{} -aos -r'.format(rar_file,destDir)            
             print(cmd)
            #  os.system(cmd)   
      else:
          print(rar_file)
  
  def putQxFbfileToQueue(self,fileDir):    #全息分笔数据文件生成文件名队列
    for fileName in os.listdir(fileDir):       
      if fileName[0:5]==self.fbqx_dmscope:
       self.fbQxFileQueue.put(fileDir+'/'+fileName) 
        

  def QxCsvToHd5(self,txt_file):     #大富翁全息分笔数据入库                   
          tscode=txt_file[-12:-4]       #SH603001   
          tscode=tscode.lower()    
          today= txt_file[-21:-13]      
          if os.access(txt_file, os.R_OK):            
            data=pd.read_csv(txt_file)            
            data['Time']=pd.to_datetime(today+data['Time'].astype(str).str.zfill(6), format='%Y%m%d%H%M%S')
            data.insert(0, 'ts_code', tscode)
            del data['Mtime']             
            try:
             engineListAppend=self.baseFunc.engineListAppend
             data.to_sql(tscode,engineListAppend,if_exists='append',index=False,chunksize=1000)
             os.remove(txt_file)
            except:
             pass


  def threadQxFbToHd51(self): #多线程生成当日分笔数据汇总文件     
    pblist=[]     
      
    while not self.fbQxFileQueue.empty():          
        txt_file=self.fbQxFileQueue.get() #SH603001.txt             
        tscode=txt_file[-12:-4]       #SH603001   
        print(txt_file)
        print(tscode)
        if os.access(txt_file, os.R_OK):            
          data=pd.read_csv(txt_file)                          
          # data.insert(0, 'ts_code', tscode)  

          # # data['trade_time']=data['trade_time'].astype(str).str.zfill(6)
          # # data['trade_time']=fenbi_time+data['trade_time']
          data['Time']=self.today+data['Time'].astype(str).str.zfill(6)            
          # data['close']=data['close']/100            
          data.insert(0, 'ts_code', tscode)
          # data.insert(4, 'amount', abs(data['close']*data['vol']))            
          # data.insert(5, 'BS', abs(data['vol'])/data['vol'])             
          # data['vol']=abs(data['vol'])        
          # print(data)
          pblist.append(data)   #dataframe数据存入list  

    # for x in range(20): #建立线程        
    #   x += 1                             
    #   # t = threading.Thread(target=show, args=(x,))
    #   t1 = threading.Thread(target=QxCsvToHd5, args=(x,),name='getFenbiday %d 号进程' % (x)) #生成分笔日数据
    #   t1.start()
    #   t1.join()      
    
    print('allAppend is ok!')               

    result = pd.concat(pblist)   
    del result['Mtime']   
    
    # todayHdFileName=self.hd5DestDir
    h5 = pd.HDFStore('e:/20181210.h5','w', complevel=4, complib='blosc')
    h5['ts_code'] = result
    h5.close()
    print(result)       

  def threadQxFbToDbf(self): #大富翁全息分笔数据收盘下载数据（全部下载完成需要6个小时）
    start=dt.now()    
    exitFlag = 0
    treadsCounts=10
    # pblist=[]
    class myThread (threading.Thread):
      def __init__(self, threadID, name, q):
          threading.Thread.__init__(self)
          self.threadID = threadID
          self.name = name
          self.q = q
      def run(self):
          print ("开启线程：" + self.name)
          process_data(self.name, self.q)
          print ("退出线程：" + self.name)
  
    def process_data(threadName, q):
      while not exitFlag:
          # queueLock.acquire()
          if not workQueue.empty():
              txt_file = q.get()
              self.QxCsvToHd5(txt_file)
              # queueLock.release()
              print ("%s processing %s" % (threadName, txt_file))          
          time.sleep(1) 

    threadList=[]
    csvFileList=[]
    for x in range(treadsCounts):
      threadList.append('Thread-'+str(x))
      
    # threadList = ["Thread-1", "Thread-2", "Thread-3","Thread-4","Thread-5","Thread-6","Thread-7","Thread-8","Thread-9","Thread-10","Thread-11","Thread-12"]
    # nameList = ["One", "Two", "Three", "Four", "Five"]
    # queueLock = threading.Lock()
    workQueue=self.fbQxFileQueue
    threads = []
    threadID = 1

    # 创建新线程
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    # queueLock.acquire()
    # workQueue=self.baseFunc.stockBasic_queue        
    # queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    print ("退出主线程")

    print(start)
    print(dt.now())

  def validateQxCsvToDbf(self,tradeTime) :#检验csv文件数据是否已经完全入库
     #根据csv文件
     while not self.fbQxFileQueue.empty():
      txt_file=self.fbQxFileQueue.get() 
      tscode=txt_file[-12:-4]       #SH603001   
      tscode=tscode.lower() 
      # tradeTime=self.today_  #2019-01-07
      findSql='select count(*) from fenbi_'+tscode +" where convert(char(10),Time,121)='"+tradeTime+"'"
      # print(findSql)
      if os.access(txt_file, os.R_OK):            
          data=pd.read_csv(txt_file)            
          csvCounts=data['Time'].count()
          findResult=self.baseFunc.ExecSqlReturn(findSql)
          # print(findResult)
          dbfCounts=findResult[0][0]
          # print(csvCounts,' ',dbfCounts)
          if csvCounts==dbfCounts:
            os.remove(txt_file)
            pass
          else:
            delSql='delete from fenbi_'+tscode +" where convert(char(10),Time,121)='"+tradeTime+"'" 
            self.baseFunc.ExecSql(delSql)

     

  def putTxtFileToQueue(self,scope): #生成分笔数据文件队列，供多线程使用
    if scope=='today' :                      #生成当日数据文件队列     
      list = os.listdir(self.fbtxt_todaydir) #fbtxt_todaydir:当日分笔数据目录，只能保存当日分笔数据 
      if  len(list)!=1:                      #保证该目录下只有当天的分笔文件
        return 0
      else:
        todaydir= os.path.join(todaydir,list[0])   
      stocklist=[]      
      if not self.fenbiQueue.empty():
       return
      else:               
         for file in os.listdir(todaydir):  
               index1=file[15:23]+'-'+file[5:14]
               stocklist.append([index1,file])
         stocklist.sort()
         for list1 in stocklist:               
            self.fenbiQueue.put(todaydir+'/'+list1[1]) #存入队列：eg I:\fenbiTxtToday\20181210SZ000999.txt
    return 1    
     
    
  def threadTxtToHd5day(self): #多线程生成当日分笔数据汇总文件
    isok=self.putTxtFileToQueue('today')  
    pblist=[] 
    
    def txtToHd5Today1(args):                
      i=0
      while not self.fenbiQueue.empty():    
      # while i<10:
          txt_file=self.fenbiQueue.get() #SH603001.txt             
          tscode=txt_file[-10:-4]+'.'+txt_file[-12:-10]       #603001.SH   
          print(tscode)
          if os.access(txt_file, os.R_OK):            
            data=pd.read_csv(txt_file,sep='\t', encoding='utf8',names=['trade_time', 'close', 'vol'])                          
            data.insert(0, 'ts_code', tscode)  

            # data['trade_time']=data['trade_time'].astype(str).str.zfill(6)
            # data['trade_time']=fenbi_time+data['trade_time']
            data['trade_time']=self.today+data['trade_time'].astype(str).str.zfill(6)            
            data['close']=data['close']/100            
            # data.insert(0, 'ts_code', tscode)
            data.insert(4, 'amount', abs(data['close']*data['vol']))            
            data.insert(5, 'BS', abs(data['vol'])/data['vol'])             
            data['vol']=abs(data['vol'])        
            # print(data)
            pblist.append(data)   #dataframe数据存入list                     
      # result = pd.concat(self.trdlist[x])
      # h5 = pd.HDFStore('e:/20181210_'+'%d' %x+'.h5','w', complevel=4, complib='blosc')
      # h5['ts_code'] = result
      # h5.close()
    #   print(result)
      # t = time.localtime(time.time())       
      # StrIMSt = time.strftime("%H:%M:%S", t)  
      # print(StrIMSt)

    if isok==1 :
      for x in range(20): #建立线程        
        # x += 1                             
        # t = threading.Thread(target=show, args=(x,))
        t1 = threading.Thread(target=txtToHd5Today1, args=(x,),name='getFenbiday %d 号进程' % (x)) #生成分笔日数据
        t1.start()
        t1.join() 
      
      
      print('allAppend is ok!')
                
 
      result = pd.concat(pblist)
      # tempdf=result.pop('trade_time')    
      # tempdf=pd.to_datetime(today+tempdf.astype(str).str.zfill(6))  
      # result['trade_time1']= tempdf              
      # # result.insert(1, 'date', today) 
      # result['close']=result['close']/100     
      # result.insert(4, 'amount', abs(result['close']*result['vol']))            
      # result.insert(5, 'BS', abs(result['vol'])/result['vol'])             
      # result['vol']=abs(result['vol'])   
      
      todayHdFileName=self.hd5DestDir
      h5 = pd.HDFStore('e:/20181210.h5','w', complevel=4, complib='blosc')
      h5['ts_code'] = result
      h5.close()
      print(result)  
     
  def calcDpFenbi(self):
    h5 = pd.HDFStore('e:/20181210.h5','r')
    df = h5['ts_code']
    dfSZ=df[df['ts_code'].str.contains('SZ$')]
    dfSH=df[df['ts_code'].str.contains('SH$')]
    trans_num=len(df) # '总成交笔数',
    # ave__num= # '均笔成交量',
    # ave_amout # '均笔成交金额',
    # buy_num #'买入笔数',
    # buy_amount#'买入金额（万元）',
    # buy_ave_num#'买入每笔成交量',
    # buy_ave_amount#'买入均笔金额',
    # sell_num # '卖出笔数',
    # sell_amount#'卖出金额（万元）',
    # sell_ave_num #'卖出每笔成交量',
    # sell_ave_amount #'卖出均笔金额',
    # buy_sell_num #'买入卖出比（成交量）',
    # buy_sell_amount #'买入卖出比（成交金额）',
    
    trans_num=len(df)
    # print(volnum_sh)
         

  def txtToHd5Today(self,x):
     t = time.localtime(time.time())       
     StrIMSt = time.strftime("%H:%M:%S", t)  
     print(StrIMSt)
     isok=self.putTxtFileToQueue('today')

     i=0
   #   while not self.fenbiQueue.empty():    
     while i<50:
          txt_file=self.fenbiQueue.get() #SH603001.txt             
          tscode=txt_file[-10:-4]+'.'+txt_file[-12:-10]       #603001.SH   
          fenbi_time=txt_file[-21:-13]
          if os.access(txt_file, os.R_OK):
            print(tscode) 
            data=pd.read_csv(txt_file,sep='\t', encoding='utf8',names=['trade_time', 'close', 'vol'])   
            data['trade_time']=data['trade_time'].astype(str).str.zfill(6)
            data['trade_time']=fenbi_time+data['trade_time']
            data['trade_time']=pd.to_datetime(data['trade_time'])            
            data['close']=data['close']/100            
            data.insert(0, 'ts_code', tscode)
            data.insert(4, 'amount', abs(data['close']*data['vol']))            
            data.insert(5, 'BS', abs(data['vol'])/data['vol'])             
            data['vol']=abs(data['vol'])   
            print(x)
            self.trdlist[x].append(data)   #dataframe数据存入list 
          i=i+1
          print(i)
     result = pd.concat(self.trdlist[x])
     h5 = pd.HDFStore('e:/'+fenbi_time+'.h5','w', complevel=4, complib='blosc')
     h5['ts_code'] = result
     h5.close()
   #   print(result)
     t = time.localtime(time.time())       
     StrIMSt = time.strftime("%H:%M:%S", t)  
     print(StrIMSt)
   #   09:55:27
   #         

  def txtToHd5 (self):
    rootdir = self.txtFenbiFileDir    
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        fenbi_time=list[i]
        self.baseFunc.allKdayDir=path+"\\"
        self.baseFunc.getFileQueue() 
        while not self.baseFunc.file_queue.empty():    
          txtFile=self.baseFunc.file_queue.get() #SH603001.txt 
          tscode=txtFile[2:8]+'.'+txtFile[0:2]       #603001.SH
          txt_file=path+"\\"+txtFile             #I:\fenbiTxt\20180102\SH603001.txt
         #  if os.path.isfile(txt_file):
          if os.access(txt_file, os.R_OK):
            print(txt_file) 
            data=pd.read_csv(txt_file,sep='\t', encoding='utf8',names=['trade_time', 'close', 'vol'])   
            data['trade_time']=data['trade_time'].astype(str).str.zfill(6)
            data['trade_time']=fenbi_time+data['trade_time']
            data['trade_time']=pd.to_datetime(data['trade_time'])            
            data['close']=data['close']/100
            data.insert(0, 'ts_code', tscode)
            data.insert(4, 'amount', abs(data['close']*data['vol']))
            if data['close']>0:
              data.insert(5, 'BS', 'B') 
            else:  
              data.insert(5, 'BS', 'S') 
          self.pblist.append(data)
           
            
         
        
        
            # HD5_filename = self.hd5DestDir +tscode   
            # if os.path.isfile(txt_file):      
            #    h5 = pd.HDFStore(HD5_filename,'w')
            #    h5['data'] = data      
            #    h5.close()             
   #  if os.access("/file/path/foo.txt", os.W_OK):
  
  def getHtml(self,url):
      while True:
          try:
              html = urllib.request.urlopen(url, timeout=5).read()
              break
          except:
              print("超时重试")
      html = html.decode('gbk')
      return html
    
  def getTable(self,html):
      s = r'(?<=<table class="datatbl" id="datatbl">)([\s\S]*?)(?=</table>)'
      pat = re.compile(s)
      code = pat.findall(html)
      return code
    
  def getTitle(self,tableString):
      s = r'(?<=<thead)>.*?([\s\S]*?)(?=</thead>)'
      pat = re.compile(s)
      code = pat.findall(tableString)
      s2 = r'(?<=<tr).*?>([\s\S]*?)(?=</tr>)'
      pat2 = re.compile(s2)
      code2 = pat2.findall(code[0])
      s3 = r'(?<=<t[h,d]).*?>([\s\S]*?)(?=</t[h,d]>)'
      pat3 = re.compile(s3)
      code3 = pat3.findall(code2[0])
      return code3
    
  def getBody(self,tableString):
      s = r'(?<=<tbody)>.*?([\s\S]*?)(?=</tbody>)'
      pat = re.compile(s)
      code = pat.findall(tableString)
      s2 = r'(?<=<tr).*?>([\s\S]*?)(?=</tr>)'
      pat2 = re.compile(s2)
      code2 = pat2.findall(code[0])
      s3 = r'(?<=<t[h,d]).*?>(?!<)([\s\S]*?)(?=</)[^>]*>'
      pat3 = re.compile(s3)
      code3 = []
      for tr in code2:
          code3.append(pat3.findall(tr))
      return code3
    
  # 股票代码
  def getSinaFb(self,date,stockList): #爬取新浪单个分笔数据
      # symbol = 'sz000001'
      # # 日期
      # dateObj = datetime.datetime(2018, 12, 28)
      # date = dateObj.strftime("%Y-%m-%d")
      
      # 页码，因为不止1页，从第一页开始爬取 
    pblist=[] 
    while not stockList.empty():
          page = 1   
          # Url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + symbol + '&date=' + date + '&page=' + str(page)
          # print(Url)
          # html = getHtml(Url)
          # table = getTable(html)
          # tbody = getBody(table[0])
          # data=pd.DataFrame(tbody,columns=['trade_time','price','updown','vol','amount','bs'])  
          # data['trade_time']=date+' '+data['trade_time']
          # data.insert(0, 'ts_code', symbol) 
          # print(data)

          codets=stockList.get()
          tscode=self.baseFunc.tscodeTran(codets)  #转换股票代码000001.SZ为sz000001
          while True:
              Url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + tscode + '&date=' + date + '&page=' + str(page)
              print(Url)
              html = self.getHtml(Url)
              table = self.getTable(html)
              if len(table) != 0:
                  tbody = self.getBody(table[0])
                  if len(tbody) == 0:
                      print("结束")
                      break
                  else:
                      data=pd.DataFrame(tbody,columns=['time','price','updown','vol','amount','bs'])  
                      data=pd.DataFrame(tbody,columns=['trade_time','price','updown','vol','amount','bs'])  
                      data['trade_time']=date+' '+data['trade_time']
                      data.insert(0, 'ts_code', tscode)
                      pblist.append(data)                     
                      print(pblist)
              else:
                  print("当日无数据")
                  break
              page += 1
            
    result = pd.concat(pblist)
    print(result)
  
    
  def QQFbclose(self): #腾讯分笔数据收盘下载数据（全部下载完成需要6个小时）
    start=dt.now()
    print(start)
    exitFlag = 0
    class myThread (threading.Thread):
      def __init__(self, threadID, name, q):
          threading.Thread.__init__(self)
          self.threadID = threadID
          self.name = name
          self.q = q
      def run(self):
          print ("开启线程：" + self.name)
          process_data(self.name, self.q)
          print ("退出线程：" + self.name)
  
    def process_data(threadName, q):
      while not exitFlag:
          # queueLock.acquire()
          if not workQueue.empty():
              tscode = q.get()
              tscode =self.baseFunc.tscodeTran(tscode)
              self.getQQFbOneAllPgToDbf(tscode)
              # queueLock.release()
              print ("%s processing %s" % (threadName, tscode))

          else:
              queueLock.release()
          time.sleep(1) 

    threadList = ["Thread-1", "Thread-2", "Thread-3","Thread-4","Thread-5","Thread-6"]
    nameList = ["One", "Two", "Three", "Four", "Five"]
    queueLock = threading.Lock()
    workQueue=self.fenbiQueue
    threads = []
    threadID = 1

    # 创建新线程
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    # queueLock.acquire()
    # workQueue=self.baseFunc.stockBasic_queue        
    # queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    print ("退出主线程")
    print(start)
    print(dt.now())

  def test1(self):     
     self.getQQFbOneAllPgToDbf('sh600000')
     stockBasic_queue=self.baseFunc.stockBasic_queue #股票代码队列000001.SZ

       
    # tscode = 'sz000001'
    # # dateObj = datetime.datetime(2018, 12, 28)
    # # date =self.baseFunc.getDatetime('-')
    # # date = date.strftime("%Y-%m-%d")
    # date='2018-12-28'
    # page = 1   
    # pblist=pd.DataFrame(columns=['trade_time','price','updown','vol','amount','bs'])
    # while page<10:
    #           Url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + tscode + '&date=' + date + '&page=' + str(page)
    #           print(Url)
    #           html = self.getHtml(Url)
    #           table = self.getTable(html)
    #           if len(table) != 0:
    #               tbody = self.getBody(table[0])
    #               if len(tbody) == 0:
    #                   print("结束")
    #                   break
    #               else:
    #                   data=pd.DataFrame(tbody)
    #                   print(data)
    #                   pblist.append(data,ignore_index=True)                     
    #                   print(pblist)
                      
    #           else:
    #               print("当日无数据")
    #               break
    #           page += 1   
    # pblist['trade_time']=date+' '+pblist['trade_time']     
    # print(pblist)  
    

  def getQQFbContent(self,url):  #获取腾讯股票实时分笔接口数据
      while True:
          try:
              content = requests.get(url).text
              break
          except:
              print("超时重试")      
      return content

  def dealQQFbContent(self,content): #处理腾讯股票实时分笔接口数据，转换为dataframe格式
    s = r'\".*"'
    pat = re.compile(s)
    code = pat.findall(content)
    code=code[0].replace('"','') 
    code=code+'|'
    s=r'.*?\S\|'
    pat = re.compile(s)
    code1 = pat.findall(code)
    s=r'(.*?)\/'
    pat2 = re.compile(s)
    code3=[]
    for fb in code1:
      fb=re.sub(r'\|','/',fb)  
      code3.append(pat2.findall(fb))
      df=pd.DataFrame(code3,columns=('id','trade_time','price','updown','vol','amount','bs'))
    return df

  def getQQFbOneAllPgToDbf(self,tscode):#获取腾讯单只股票实时所有分笔数据（收盘处理）
    page=0    
    fblist=[]
    while True:
      rd=random.randint(0,10000)    
      url = 'http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c='+tscode+'&p='+str(page)+'&'+str(rd)      
      content = self.getQQFbContent(url)  #获取腾讯股票实时分笔接口数据，单页数据每页70条   
      if len(content) != 0:
        df=self.dealQQFbContent(content) #处理腾讯股票实时分笔接口数据，转换为dataframe格式
        fblist.append(df)
      else:
        print(page)
        break  
      page+=1
    try :
      result = pd.concat(fblist,ignore_index=True)   #合并所有页 
      result.insert(1, 'ts_code', tscode)    
      result['trade_time']=self.baseFunc.getDatetime('-')+' '+result['trade_time']   
      #导入股票列表到数据库      
      engineListAppend=self.baseFunc.engineListAppend
      result.to_sql('fenbi_'+tscode,engineListAppend,if_exists='append',index=False,chunksize=1000)  
    except:
      pass  
    # print(result)
    # df = pd.read_csv('I:/fbHd5Dest/zbi_20190102/20190102/SZ000002.csv')

  def test(self):
    # workQueue=queue.Queue()
    # tempQueue=self.baseFunc.getTscodeQueue()
    # while not tempQueue.empty():
    #    tscode=tempQueue.get()      
    #    workQueue.put([tscode,0],2)       
    # print(workQueue.get())    
    # print(tempQueue.qsize())    
    # print(self.baseFunc.getTscodeQueue().qsize())
    print('ok')

  def testOntime(self):    
    stcodes=self.baseFunc.stockBasic    
    stocksList=stcodes['ts_code'].tolist()
    stocksList=['600000.SH','600601.SH','601388.SH','601857.SH']    
    for stcodes in stocksList: 
        stcodes=self.baseFunc.tscodeTran(stcodes)       
        self.fbOntimeQueue.put([stcodes,0], True, 2) 
    print(self.fbOntimeQueue.qsize())          
    while not self.fbOntimeQueue.empty() and self.nowtime <'15:30' :
      content=self.fbOntimeQueue.get()
      tscode=content[0]      
      page=content[1]
      print(tscode,' ',page)
      page=self.getQQFbOntime(tscode,page)
      # print(tscode,' ',page)
      # workQueue.put([tscode,page], True, 2)  
      print('3 ',self.fbOntimeQueue.qsize())     
    print('ok')  
    
  def getQQFbOntime(self,tscode,page):#获取腾讯单只股票实时所有分笔数据（收盘处理）            
    fblist=[]
    while True:
      rd=random.randint(0,10000)    
      url = 'http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c='+tscode+'&p='+str(page)+'&'+str(rd)      
      content = self.getQQFbContent(url)  #获取腾讯股票实时分笔接口数据，单页数据每页70条   
      if len(content) != 0:
        df=self.dealQQFbContent(content) #处理腾讯股票实时分笔接口数据，转换为dataframe格式
        fblist.append(df)
      else:
        print(tscode,'  ',page)          
        break               
      page+=1
    try :
      result = pd.concat(fblist,ignore_index=True)   #合并所有页 
      result.insert(1, 'ts_code', tscode)    
      result['trade_time']=self.baseFunc.getDatetime('-')+' '+result['trade_time']   
      # print('result')
      #导入股票列表到数据库      
      engineListAppend=self.baseFunc.engineListAppend
      result.to_sql('fenbi_'+tscode,engineListAppend,if_exists='append',index=False,chunksize=1000)  
    except:
      pass
    print('1 ',self.fbOntimeQueue.qsize()) 
    self.fbOntimeQueue.put([tscode,page-1], True, 2)   
    print('2 ',self.fbOntimeQueue.qsize()) 
    return page    

  def threadQQonTime(self): #腾讯分笔数据实时下载数据
    start=dt.now()    
    exitFlag = 0
    # pblist=[]
    class myThread (threading.Thread):
      def __init__(self, threadID, name, q):
          threading.Thread.__init__(self)
          self.threadID = threadID
          self.name = name
          self.q = q
      def run(self):
          print ("开启线程：" + self.name)
          process_data(self.name, self.q)
          print ("退出线程：" + self.name)
  
    def process_data(threadName, q):
      while not exitFlag:
          # queueLock.acquire()
          if not workQueue.empty():
              txt_file = q.get()
              self.QxCsvToHd5(txt_file)
              # queueLock.release()
              print ("%s processing %s" % (threadName, txt_file))          
          time.sleep(1) 
    threadList=[]
    for x in range(20):
      threadList.append('Thread-'+str(x))
    # threadList = ["Thread-1", "Thread-2", "Thread-3","Thread-4","Thread-5","Thread-6","Thread-7","Thread-8","Thread-9","Thread-10","Thread-11","Thread-12"]
    # nameList = ["One", "Two", "Three", "Four", "Five"]
    # queueLock = threading.Lock()
    workQueue=self.fbQxFileQueue
    threads = []
    threadID = 1

    # 创建新线程
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    # queueLock.acquire()
    # workQueue=self.baseFunc.stockBasic_queue        
    # queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    print ("退出主线程")

    print(start)
    print(dt.now())


def main(): 
  pass

if __name__ == '__main__':
  main()