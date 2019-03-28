import requests
import re,random
import tushare as ts
import pandas as pd
from queue import LifoQueue
import threading
import time
from datetime import datetime as dt
from WindPy import *
# import easyquotation



ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token
pro = ts.pro_api()    
# df=ts.pro_bar(pro_api=pro, ts_code='002107.SZ', adj='qfq',start_date='20181228', end_date='20190322', ma=[3,5,20,60])
df=ts.pro_bar(pro_api=pro,  ts_code='002017.SZ', adj='qfq',start_date='20181228', end_date='20190325') 
df3=df.head(5)['close'].mean()
df.apply(lambda x:x.max()-x.min())
# ma3=df3['close'].mean()
print(df3)
# df = pro.index_dailybasic(trade_date='20190322')
# df = pro.index_basic(market='SZSE')
# df = ts.pro_bar(pro_api=pro, trade_date='20190322',adj='qfq', ma=[3,5, 20, 50])
# df = pro.daily(trade_date='20190322')
# df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(df3)

# w.start()
stockBasic_queue = LifoQueue()
quotation = easyquotation.use('qq')

def tscodeTran(codets):  #000001.SZ to sz000001
    tscode=codets[-2:].lower()+codets[0:6]
    return tscode

###############################################################################

def getQQFbContent(url):  #获取腾讯股票实时分笔接口数据
    while True:
          try:
              content = requests.get(url).text
              break
          except:
              print("超时重试")      
    return content

def dealQQLimitContent(content,tscode): #处理腾讯股票实时行情接口数据，转换为dataframe格式
    s = r'\".*"'
    pat = re.compile(s)  
    code = pat.findall(content)  
    code=code[0].replace('"','') 
    code=code+'~' 
    code=code.replace('~~','~') 
    s=r'(.*?)\~'
    pat2 = re.compile(s)
    df=[]
    code2=pat2.findall(code)
    df.append(code2)   
    return df

def stockBasicH5():
    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
    pro = ts.pro_api() 
    stockBasic = pro.stock_basic(exchange='',list_status='L',fields='ts_code,symbol,name')  
    filename = 'c:\\ontimeKday\\stockBasic.hd5'        
    h5 = pd.HDFStore(filename,'w')
    h5['data'] = stockBasic      
    h5.close()     

def getStockBasicList():
   filename = 'c:\\ontimeKday\\stockBasic.hd5'   
   h5 = pd.HDFStore(filename,'r')
   stcodes = h5['data']   
   h5.close()
   stocksList=stcodes['ts_code'].tolist()
#    for i in range(0,len(stocksList),99):
#      codelist=stocksList[i:i+99]
#      stock=w.wsq(codelist,"rt_last")
#      print(stock) 
   return stocksList
     
def getStockBasicQqList():
   filename = 'c:\\ontimeKday\\stockBasic.hd5'   
   h5 = pd.HDFStore(filename,'r')
   stcodes = h5['data']   
   h5.close()
   aList=stcodes['ts_code'].tolist()
   stocksList=[]
   for stcodes in aList:
     stcodes=tscodeTran(stcodes)  
     stocksList.append(stcodes)   
   return stocksList  


def getStockBasicQueue():
   filename = 'c:\\ontimeKday\\stockBasic.hd5'   
   h5 = pd.HDFStore(filename,'r')
   stcodes = h5['data']   
   h5.close()
   stocksList=stcodes['ts_code'].tolist()
   for stcodes in stocksList:
     stcodes=tscodeTran(stcodes)  
     stockBasic_queue.put(stcodes, True, 2)             

def threadQQonTime(): #腾讯分笔数据实时下载数据
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
              tscode = q.get()      
              rd=random.randint(0,10000)    
              url = 'http://qt.gtimg.cn/q=s_'+tscode+'&'+str(rd)      
              content = getQQFbContent(url)  #获取腾讯股票实时分笔接口数据，单页数据每页70条   
              if len(content) != 0:
                dealQQLimitContent(content,tscode) #处理腾讯股票实时分笔接口数据，转换为dataframe格式        
              print ("%s processing %s" % (threadName, tscode))          
        #   time.sleep(1) 


    threadList=[]
    for x in range(20):                      #设置线程数量
      threadList.append('Thread-'+str(x))
    # threadList = ["Thread-1", "Thread-2", "Thread-3","Thread-4","Thread-5","Thread-6","Thread-7","Thread-8","Thread-9","Thread-10","Thread-11","Thread-12"]
    # nameList = ["One", "Two", "Three", "Four", "Five"]
    # queueLock = threading.Lock()
    workQueue=stockBasic_queue
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

def getQq():
    data=quotation.stocks(['sh000001', 'sz000001'], prefix=True) 
    df=pd.DataFrame.from_dict(data,orient='index')
    # print(df)
    filename = 'c:\\ontimeKday\\realhq.hd5'        
    h5 = pd.HDFStore(filename,'w', complevel=4, complib='blosc')
    h5['data'] = df      
    h5.close()     




tscodes=getStockBasicQqList()
data=quotation.stocks(tscodes, prefix=True) 
df=pd.DataFrame.from_dict(data,orient='index')
print(df['time'])

# getStockBasicList()
# stockBasicH5()

# getStockBasicQueue()

# hdfcontent=[]
# while not stockBasic_queue.empty():
#     tscode = stockBasic_queue.get()      
#     rd=random.randint(0,10000)    
#     url = 'http://qt.gtimg.cn/q=s_'+tscode+'&'+str(rd)      
#     content = getQQFbContent(url)  #获取腾讯股票实时分笔接口数据，单页数据每页70条   
#     print(content)
#     if len(content) != 0:
#       df=dealQQLimitContent(content,tscode) #处理腾讯股票实时分笔接口数据，转换为dataframe格式   
#       hdfcontent.append(df)
# # threadQQonTime()
# print(hdfcontent)

# try :
#         df=pd.DataFrame(code3,columns=('id','trade_time','price','updown','vol','amount','bs','dd','ddd'))    
#         filename = 'c:\\ontimeKday\\'+tscode+'.hd5'        
#         h5 = pd.HDFStore(filename,'w',complevel=4, complib='blosc')
#         h5['data'] = df      
#         h5.close()    
# except:
#     pass    

# rd=random.randint(0,10000)    
# tscode='sz000858'
# url = 'http://qt.gtimg.cn/q=s_'+tscode+'&'+str(rd)      
# content = getQQFbContent(url)  #获取腾讯股票实时分笔接口数据，单页数据每页70条   
# if len(content) != 0:
#  df=dealQQLimitContent(content) #处理腾讯股票实时分笔接口数据，转换为dataframe格式
# print(df)

# h5 = pd.HDFStore('c:\\ontimeKday\\sz000858.hd5','r')
# stcodes = h5['data']   
# h5.close()
# stocksList=stcodes['trade_time'].tolist()
# for trade_time in stocksList:
#     print(trade_time)