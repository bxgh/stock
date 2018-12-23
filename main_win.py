#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import basewin,datasetwin,dirsetWin
import baseFunction
import stockFunction
import kdayCalcData
import fenbiFunction
import numpy as np
import time
from datetime import datetime,date
import datetime
import pandas as pd
import threading
import rarfile
import os 
import configparser

class customStatusBar(wx.StatusBar):#设置底部状态栏、进度条
    def __init__(self, parent):        
        wx.StatusBar.__init__(self,parent,-1)
        self.SetStatusText('   进度：',0)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-2,-1])
        self.count=0
        self.gauge=wx.Gauge(self,1001,100,pos=(75,4),size=(265,20))
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        self.gauge.SetValue(0)   
             

class MianWindow(basewin.baseMainWindow):
    def init_main_window(self):        
    #   global conf  #声明config文件全局变量
      #设置状态栏      
      self.count=100       
      self.status = customStatusBar(self)
      self.statusBar=self.SetStatusBar(self.status)  
      #配置数据库连接      
    #   host_fenbi=conf.get('database','host_fenbi')
    #   print(host_fenbi)
      self.localFenbi = fenbiFunction.FenBi() 
         
      self.mskday = stockFunction.MSSQL(host="192.168.151.213", user="toshare1", pwd="toshare1", db="kday_qfq",myOrms="mysql")   
    #   self.kdayCal = kdayCalcData.CALCDATA(host="192.168.151.213", user="toshare1", pwd="toshare1", db="kday_qfq",myOrms="mysql") 
      self.mskday.allKdayDir=self.m_dirPicker9.GetPath()+"\\"
     
     
      self.m_timer1.Start(1000)             

    def getSetDate(self,event):
      dt=self.dt_start.GetValue()      
      dtstr=dt.Format("%Y%m%d")

    def getFbTxtDir( self, event ):
    #   getDir=self.m_dirPicker9.GetPath() 
    #   self.localFenbi.txtFenbiFileDir=
      txtFenbiFileDir=self.m_dirPicker9.GetPath()
    #   cf = configparser.ConfigParser()
    #   cf.read('config.ini')
      conf.set("workDir", "txtFenbiFileDir", txtFenbiFileDir)
      conf.write(open("config.ini", "w"))      


    def calcKdayHisDays(self,event) :
       self.mskday.calcKdayHisDays()

    def kdayHisGoOn( self, event ):
        self.mskday.KdayHisGoOn()

    def temp(self, event):
      

        #  self.localFenbi.txtToHd5Today()
        #  self.localFenbi.threadTxtToHd5day()
        #    self.localFenbi.calcDpFenbi()          
        # dataset_win.Show()   
        dirset_win.Show()
        #   txtFile=self.localFenbi.allKdayDir+'\\'+'SH600000.txt'
        #   print(txtFile)
        
        #   engineListAppend= self.localFenbi.GetWriteConnect()         
        #   data.to_sql('fenbi_SH600000',engineListAppend,if_exists='append',index=False,chunksize=1000)
        #    self.mskday.getFileQueue() #得到所有股票存储H5文件列表
        #    self.mskday.statustotal=self.mskday.file_queue.qsize() #设置进度条总数   
        #    for x in range(10): #建立线程
        #      x += 1
        #      t1 = threading.Thread(target=self.mskday.saveAllH5ToSqlserver(self.status), name='getHisKdays %d 号进程' % (x)) #获取tushare数据
        #      t1.start()
        #      t1.join()     
        #   print(self.mskday.allKdayDir) 
        #    self.mskday.getHisDates(self.mskday.stockBasic)
        #   print(self.mskday.hisDate_queue.get())statustotal
        #   self.hisDate_queue.clear() 
        #   self.mskday.getHisDates(self.mskday.stockBasic)
        # self.mskday.getKdayH5('002862.SZ','20000101','20181129')
        # h5 = pd.HDFStore(self.mskday.allKdayDir+'kday_002862.SZ_20170411_20181201','r')
        # df = h5['data']
        # engineListAppend= self.mskday.GetWriteConnect()  
        # SqlResult=self.mskday.saveH5ToSqlserver('kday_002862.SZ_20170411_20181201',engineListAppend)   
        # df.to_sql('kday_002862.SZ',engineListAppend,if_exists='append',index=False,chunksize=1000)
        # h5.close()
        
        # engineListAppend= self.mskday.GetWriteConnect()   
        # self.mskday.saveH5ToSqlserver('kday_000004.SZ_19910114_20051231',engineListAppend)
        # self.mskday.renameCols(self.status,'kday_')
        # print(self.mskday.file_queue.get())       
        

    def createKdayTable(self, event ):
       self.mskday.createTables(self.status,'kday_')    #每天定时获取最新股市股票代码列表，如果有新股，生成kday表
       #    self.mskday.createTable('kday_','000002.SZ') 

    def getAllHisKdaysToH5( self, event ):
       if self.mskday.hisDate_queue.qsize()==0:          
          self.mskday.getHisDates(self.mskday.stockBasic) #得到所有股票历史日期
       self.mskday.statustotal=self.mskday.hisDate_queue.qsize() #设置进度条总数
       self.mskday.getAllHisKdaysH5(self.status)     
    
    def saveAllHisKdaysH5ToSqlserver( self, event ):
       self.mskday.getFileQueue() #得到所有股票存储H5文件列表
       self.mskday.statustotal=self.mskday.file_queue.qsize() #设置进度条总数 
       engineListAppend= self.mskday.GetWriteConnect() 
       self.mskday.saveAllH5ToSqlserver(self.status,engineListAppend)  
    #    for x in range(10): #建立线程
    #      x += 1
    #      t1 = threading.Thread(target=self.mskday.saveAllH5ToSqlserver(self.status,engineListAppend), name='getHisKdays %d 号进程' % (x)) #获取tushare数据
    #      t1.start()
    #      t1.join() 

    def renameCol_click(self, event):
      self.mskday.renameCols(self.status,'kday_') 

    def kdayClose(self,event):
      dt=self.dt_today.GetValue()      
      closeday=dt.Format("%Y%m%d")
      self.mskday.kday_close(closeday) 
    
    def creatKday_click(self, event):
      self.mskday.createTables(self.status,'kday_')       

    def deleteAllKday( self, event ):
    #   self.mskday.trucHiskday()  
      print(self.localFenbi.fenbiQueue.qsize())


    def ontimer( self, event ):
        t = time.localtime(time.time())  
        StrYMDt = time.strftime("%Y-%m-%d", t)         
        StrIMSt = time.strftime("%H:%M:%S", t) 
        today=time.strftime("%Y%m%d", t) 
        self.threadtime=StrIMSt
        self.SetStatusText(StrYMDt+' '+StrIMSt,1)#显示时间   
        
        if StrIMSt == '08:00:00':             #市场初始化
            self.mskday.getTrade_cal()
            self.mskday.isNotTradeDay()            
            self.mskday.setStockList()
            self.mskday.isKdayClosed=0 

        if StrIMSt == '14:54:00':          
            print('hk')
        
        if self.mskday.isTradeDay==1:   
            if StrIMSt == '16:00:00': 
                if  self.mskday.isKdayClosed==0  :
                    self.mskday.kday_close(today)  

            if StrIMSt == '17:00:00': 
                if  self.mskday.isKdayClosed==0  :
                    self.mskday.kday_close(today)     

            if StrIMSt == '18:00:00': 
                if  self.mskday.isKdayClosed==0  :
                    self.mskday.kday_close(today) 

            if StrIMSt == '19:00:00': 
                if  self.mskday.isKdayClosed==0  :
                    self.mskday.kday_close(today) 

            if StrIMSt == '20:00:00': 
                if  self.mskday.isKdayClosed==0  :
                    self.mskday.kday_close(today)    
                
            if StrIMSt == '21:00:00': 
                if  self.mskday.isKdayClosed==0  :
                    self.mskday.kday_close(today)            
        

class databaseSetWindow(datasetwin.databaseSet): 
  def init_dbSet_window(self): 
     #获取config配置文件     
     self.conf = configparser.ConfigParser()
     self.conf.read('config.ini') 
    #  host=self.conf.get()        

  def dbsetConfirm( self, event ):
     host=self.txt_host.GetValue()  
     self.conf.set("database", "txtFenbiFileDir", host)
     self.conf.write(open("config.ini", "w"))   
     self.Hide()

  def dbsetWinClose( self, event ):
    self.Hide() 

class dirSetWindow(dirsetWin.dirSet): 
  def init_dirSet_window(self):       
     #获取config配置文件 
     self.conf = configparser.ConfigParser()
     self.conf.read('config.ini') 
     #读取config：workDir配置，在对应控件上显示
     txtfenbifiledir =self.conf.get('workDir','txtfenbifiledir')
     self.pk_fbtxtDir.SetPath(txtfenbifiledir)

  def dirsetConfirm( self, event ):
     txtfenbifiledir=self.pk_fbtxtDir.GetPath()
     self.conf.set('workDir','txtfenbifiledir',txtfenbifiledir)
     self.conf.write(open("config.ini", "w"))   
     self.Hide()

  def dirsetWinClose( self, event ):
	  self.Hide()
   

if __name__ == '__main__':
    app = wx.App()
    #主窗口
    main_win = MianWindow(None)
    main_win.init_main_window()
    main_win.Show()
    
    #dbset设置config窗口，默认不显示
    dataset_win=databaseSetWindow(None)
    dataset_win.init_dbSet_window()

    # dirsert设置config窗口，默认不显示
    dirset_win=dirSetWindow(None)
    dirset_win.init_dirSet_window()

    app.MainLoop()