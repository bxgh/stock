from winfenbi import fenbiWin
from winfenbi import fenbiFunction
import wx
import time,os,shutil
from datetime import datetime as dt

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

class FenBimian(fenbiWin.win_fenbi):
  def init_fbmain_window(self):  
    #设置状态栏      
    self.count=100  
    self.status = customStatusBar(self)
    self.statusBar=self.SetStatusBar(self.status) 
    self.fbFunc=fenbiFunction.FenBi()

  def btn_crFbTbls( self, event ):
    self.fbFunc.baseFunc.createTables(self.status,'fenbi_')
    
  def fbqxCsvToDbf( self, event ):   
    fileDir=self.fbFunc.fbqx_ftpdir+'/csv/'+self.fbFunc.today    
    self.fbFunc.putQxFbfileToQueue(fileDir)
    self.fbFunc.threadQxFbToDbf()
   

  def btn_test( self, event ):
    self.fbFunc.testOntime()

    # fileDir=self.fbFunc.fbqx_ftpdir+'/csv/'+self.fbFunc.today    
    # self.fbFunc.putQxFbfileToQueue(fileDir)
    # self.fbFunc.threadQxFbToDbf()  
  
  def btn_validateQxCsvToDbf( self, event ):   
    fileDir=self.fbFunc.fbqx_ftpdir+'/csv/'+self.fbFunc.today    
    self.fbFunc.putQxFbfileToQueue(fileDir)   
    tradeTime =self.fbFunc.today_
    self.fbFunc.validateQxCsvToDbf(tradeTime)

  def btn_truncTables( self, event ):
    stocklist=self.fbFunc.baseFunc.stockBasic_queue
    while not stocklist.empty():
      tscode=stocklist.get()
      stockcode=self.fbFunc.baseFunc.tscodeTran(tscode)
      
      trucSql='if  exists (select * from sysobjects where name='+"'fenbi_"+stockcode+"')"
      trucSql=trucSql+' truncate table' +' fenbi_' + stockcode
      print(trucSql)
      self.fbFunc.baseFunc.ExecSql(trucSql)


  def btn_QQFb( self, event ):
    self.fbFunc.QQFbclose()
  
  def timer_fb( self, event ):#定时器
    t = time.localtime(time.time())  
    StrYMDt = time.strftime("%Y%m%d", t)         
    # StrYMDt='20190104'
    StrIMSt = time.strftime("%H:%M:%S", t)   
    self.nowtime = time.strftime("%H:%M:%S", t) 
    ftpFileName='zbi_'+StrYMDt+'.rar'                      #ftp服务器端当日下载文件名
    localFileName=self.fbFunc.fbqx_ftpdir+'/' +ftpFileName #下载到本地路径和文件名   
    if self.fbFunc.baseFunc.isTradeDay==1  : #是否交易日
       if StrIMSt == '15:00:00':
         self.fbFunc.fbqxDownloading=0 #初始化当日分笔全息数据下载标志，是否正在下载
         self.fbFunc.fbqxDownloaded=0  #初始化当日分笔全息数据下载标志，是否已经下载完毕
         self.fbFunc.extracted=0       #初始化下载后的分笔文件是否已经解压缩
         self.iscsvTodbf=0             #判断csv是否已经入库

       if StrIMSt >= '16:10:00' and StrIMSt < '21:10:00':   #下载分笔全息数据，rar文件          
          if self.fbFunc.fbqxDownloaded==0 :        #全息分笔文件是否下载完毕    
            if self.fbFunc.fbqxDownloading==0 :     #是否正在下载
              self.fbFunc.fbqxDownloading=1
              try:
                ftp = self.fbFunc.baseFunc.ftpconnect("down.licai668.cn", "wwsa518", "ww190103emp")#分笔全息数据Ftp账户 
                self.fbFunc.baseFunc.downloadfile(ftp, ftpFileName,localFileName )
                self.fbFunc.fbqxDownloaded=1 
                ftp.quit() 
              except:
                self.fbFunc.fbqxDownloading=0 
                time.sleep(300)    
          else:                                #下载完毕后解压缩文件到目标文件夹     
            if self.fbFunc.extracted==0:  #没有解压文件
              ftpFileName='zbi_'+StrYMDt+'.rar'
              rarFile=self.fbFunc.fbqx_ftpdir+'/' +ftpFileName
              destDir=self.fbFunc.fbqx_ftpdir+'/csv'
              destFileDir=destDir+'/'+StrYMDt
              self.fbFunc.baseFunc.mkdir(destDir)
              self.fbFunc.baseFunc.mkdir(destFileDir)
              if os.path.exists(rarFile) and not os.listdir(destFileDir):     #判断当日下载文件是否存在，当日解压缩文件夹是否为空       
                try:
                  self.fbFunc.baseFunc.extrRarFile(rarFile,destDir)
                  self.fbFunc.extracted=1
                except:
                  shutil.rmtree(destFileDir)  
            else:   #完成解压文件后，csv文件数据入库
              if  self.iscsvTodbf==0 :
                self.iscsvTodbf=1
                self.fbqxCsvToDbf()

       
    
def main(): 
  pass

if __name__ == '__main__':
  main()