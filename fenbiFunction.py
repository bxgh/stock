import time
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
import basewin
import timeit
import baseFunction
import configparser
import main_win

class FenBi:
  def __init__(self):     
    #  conf=main_win.conf  #获取config配置文件   
    #  self.txtFenbiFileDir=conf.get("workDir", "txtFenbiFileDir")
    #  print(self.txtFenbiFileDir)
     self.baseFunc = baseFunction.baseFunc(host="127.0.0.1\MSSERVER2008", user="sa", pwd="123", db="fenbi",myOrms="mssql")   
     self.hd5DestDir="H:\\fenbiHd5\\"    
     self.fenbiQueue=LifoQueue()
     self.pblist=[]
     self.trdlist=[]

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
  
  def putTxtFileToQueue(self,scope): #生成分笔数据文件队列，供多线程使用
    if scope=='today' :                      #生成当日数据文件队列
      # rootdir = self.txtFenbiFileDir         #txt分笔文件根目录
      todaydir = 'I:/fenbiTxtToday'         #当日分笔数据目录，只能保存当日分笔数据 
      # todaydir=self.txtFenbiFileDir
      list = os.listdir(todaydir) 
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
    t = time.localtime(time.time())    
    today=time.strftime("%Y%m%d", t) 
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
            data['trade_time']=today+data['trade_time'].astype(str).str.zfill(6)            
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
    print(volnum_sh)
         

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
  

def main(): 
  pass

if __name__ == '__main__':
  main()