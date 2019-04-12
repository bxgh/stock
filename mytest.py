import requests
import re,random
import tushare as ts
import pandas as pd
from queue import LifoQueue
# import threading
import time as tm
from datetime import datetime as dt
from WindPy import *
import easyquotation
import pymysql

connect=pymysql.connect(host="192.168.151.216",port=3306,user="toshare1",password="toshare1",database="kday_qfq",charset='utf8')  
sql="select concat(LOWER(RIGHT(ts_code,2)), LEFT(ts_code,6)) as code from allKday_closed WHERE trade_date='2019-04-10' "
tscodeDf=pd.read_sql(sql,con=connect)
print(tscodeDf)
# w.start()
quotationQq = easyquotation.use('qq')
quotationSina = easyquotation.use('sina')
# easyquotation.update_stock_codes()
# print(quotationQq.real('sh603956'))
# quotationQq.stocks()

quotation = easyquotation.use("timekline")
data = quotation.real(['603828'], prefix=True)
df=pd.DataFrame.from_dict(data,orient='index')
print(df)

data=quotationQq.market_snapshot(prefix=True) 
df=pd.DataFrame.from_dict(data,orient='index')
df=df.reset_index()
df=df.loc[df['index'].str.contains('sz00|sz30|sh60')]
df=df[(df['volume']>0)]
print(df.columns)

# a1=df[df['code']=='sh603956']

# a1=df.loc[df['code'].str.contains('sh601388')]
# print(a1)


df=df.loc[df['code'].str.contains('sz00|sz30|sh60')]
dftscode=df[(df['volume']>0)]

dftscode=dftscode.reset_index(drop=True)
# dftscode.columns=['code1','code2']
# print(dftscode)
tscodeDf=tscodeDf.reset_index(drop=True)
# dftscode.columns=['code']
# tscodeDf.rename(columns={'code':'0'},inplace=True)
# dftscode.rename(columns={'0':'code'},inplace=True)
# print(dftscode)

df2=[tscodeDf,dftscode]
result=pd.concat(df2)
# df1= dftscode.append(tscodeDf)
# print(result['code'])
df1=result.drop_duplicates(subset=['code'],keep=False)   
df3=df1['code']
stocks=df3.tolist()
data1=quotationQq.stocks(stocks)

df4=pd.DataFrame.from_dict(data1,orient='index')
print(df4)

print(df['code'].size)
dfSH=df.loc[df['code'].str.contains('sz00|sz30|sh60')]
# dfResult=dfSH[(dfSH['volume']>0) ]
# dfSH=df[df['code'].find('sh')>0]
print(dfSH)
# print(dfResult)
print(dfSH['流通市值'].sum())

ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
pro = ts.pro_api() 

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

def stockBasicToH5():
    # ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
    # pro = ts.pro_api() 
    # stockBasic = pro.stock_basic(exchange='',list_status='L',fields='ts_code,symbol,name')  
    AllAStock = w.wset("SectorConstituent","date=20190322;sectorId=a001010100000000")
    if AllAStock.ErrorCode != 0:
        print("Get Data failed! exit!")
        exit()
    stockcode = AllAStock.Data[1]
    stockName = AllAStock.Data[2]
    dfName = pd.DataFrame( stockName ,columns=['stockName'])
    df1 = pd.DataFrame( stockcode ,columns=['upCode'])
    df1['lowCode']=df1['upCode']
    df2=df1['lowCode'].apply(lambda x: tscodeTran(x))
    df3=pd.concat([df1['upCode'],df2,dfName],axis=1)
    filename = 'c:\\ontimeKday\\stockBasic.h5'        
    h5 = pd.HDFStore(filename,'w')
    h5['data'] = df3      
    h5.close()     

def getStockBasicList():
   filename = 'c:\\ontimeKday\\stockBasic.h5'   
   h5 = pd.HDFStore(filename,'r')
   stcodes = h5['data']   
   h5.close()
   stocksList=stcodes['lowCode'].tolist()
#    for i in range(0,len(stocksList),99):
#      codelist=stocksList[i:i+99]
#      stock=w.wsq(codelist,"rt_last")
#      print(stock) 
   return stocksList
     
def getStockBasicQqList():
   filename = 'c:\\ontimeKday\\stockBasic.h5'   
   h5 = pd.HDFStore(filename,'r')
   stcodes = h5['data']   
   h5.close()#    
   stocksList=stcodes['lowCode'].tolist()      
   return stocksList  


def getStockBasicQueue():
   filename = 'c:\\ontimeKday\\stockBasic.h5'   
   h5 = pd.HDFStore(filename,'r')
   stcodes = h5['data']   
   h5.close()
   stocksList=stcodes['ts_code'].tolist()
   for stcodes in stocksList:
     stcodes=tscodeTran(stcodes)  
     stockBasic_queue.put(stcodes, True, 2)             

def getQq():
    data=quotation.stocks(['sh000001', 'sz000001'], prefix=True) 
    df=pd.DataFrame.from_dict(data,orient='index')
    # print(df)
    filename = 'c:\\ontimeKday\\realhq.hd5'        
    h5 = pd.HDFStore(filename,'w', complevel=4, complib='blosc')
    h5['data'] = df      
    h5.close()     

# stockBasicToH5()
tscodesQq=getStockBasicQqList()
# df=quotationQq.get_stock_data(tscodesQq)
print(len(tscodesQq))

while True:    
    data=quotationQq.stocks(tscodesQq, prefix=True) 
    quotationQq.get_stock_data(tscodesQq)
    df=pd.DataFrame.from_dict(data,orient='index')
    result=df[(df['ask1_volume']==0) & (df['volume']>0)]
    print(result)
    tm.sleep(60)





# getStockBasicList()
# stockBasicToH5()

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