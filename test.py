import urllib.request
import re
import datetime
import pandas as pd
import numpy
from queue import LifoQueue
import queue
import threading
import baseFunction


 
def getHtml(url):
    while True:
        try:
            html = urllib.request.urlopen(url, timeout=5).read()
            break
        except:
            print("超时重试")
    html = html.decode('gbk')
    return html
 
 
def getTable(html):
    s = r'(?<=<table class="datatbl" id="datatbl">)([\s\S]*?)(?=</table>)'
    pat = re.compile(s)
    code = pat.findall(html)
    return code
 
 
def getTitle(tableString):
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
 
 
def getBody(tableString):
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
def getSinaFb(date,stockList): #爬取新浪单个分笔数据
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
        tscode=codets[-2:].lower()+codets[0:6]
        while True:
            Url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + tscode + '&date=' + date + '&page=' + str(page)
            print(Url)
            html = getHtml(Url)
            table = getTable(html)
            if len(table) != 0:
                tbody = getBody(table[0])
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

symbol = 'sz000001'
dateObj = datetime.datetime(2018, 12, 28)
date = dateObj.strftime("%Y-%m-%d")
page = 1   
Url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + symbol + '&date=' + date + '&page=' + str(page)
print(Url)
html = getHtml(Url)
table = getTable(html)
tbody = getBody(table[0])
data=pd.DataFrame(tbody,columns=['trade_time','price','updown','vol','amount','bs'])  
data['trade_time']=date+' '+data['trade_time']
data.insert(0, 'ts_code', symbol) 

data=data.sort_values(by="trade_time")
print(data)

# baseFunc = baseFunction.baseFunc(host="127.0.0.1\MSSERVER2008", user="sa", pwd="123", db="fenbi",myOrms="mssql") 
# stockList=baseFunc.stockBasic_queue
# getSinaFb('2018-12-28',stockList)

# class get_Fb(threading.Thread):    
#     def __init__(self,name,queue,date_begin):
#         threading.Thread.__init__(self)
#         self.name = name
#         self.queue = queue
#         self.begin = date_begin
#     def run(self):
#         process_data(self.begin,self.queue)
#         print("Exiting " + self.name)

# threads = []
# for i in range(7):
#     thread = get_qfq('thread'+ str(i), stock_code_queue,old_date)
#     thread.start()
#     threads.append(thread)
# for thread in threads:
#     thread.join()
 

  
