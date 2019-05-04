import configparser
import datetime
import logging
import os
import queue
import random
import threading
import time
import timeit
from datetime import datetime as dt
from decimal import Decimal
from io import StringIO
from queue import LifoQueue
from time import sleep
import numpy as np
import pandas as pd
import pymysql
import tushare as ts
from sqlalchemy import create_engine
import pymssql
import jieba

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 对句子去除停用词
def movestopwords(sentence):
    stopwords = stopwordslist('jiebastopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence:
        if word not in stopwords:
            if word != '\t'and'\n':
                outstr += word
                # outstr += " "
    return outstr

def getKeywords(content,title):  #提取conent关键词做title
  if len(title) <2:              #title源数据为空才提取
    if len(content)>50:
        content_seg = jieba.cut(content)    # jieba分词
        listcontent = ''
        for i in content_seg:
            listcontent += i
            listcontent += " "   
        listcontent = movestopwords(listcontent)    # 去除停用词        
        listcontent = listcontent.replace("   ", " ").replace("  ", " ")
        wordResult=listcontent[0:20]        #取前20字符做title
    else:
        wordResult=content[0:50]    
  else:
     wordResult=title       
  return wordResult

ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token
pro = ts.pro_api() 
engine=create_engine("mysql+pymysql://toshare1:toshare1@192.168.151.216:3306/kday?charset=utf8",echo=True)   

while True:
    today=datetime.date.today() 
    sqlday = today.strftime('%Y-%m-%d')
    oneday=datetime.timedelta(days=1) 
    tomorrow=today+oneday
    startday = today.strftime('%Y%m%d')              #起始日期：今天
    endday = tomorrow.strftime('%Y%m%d')             #结束日期：明天
   


    try:
        dfchannels = pro.news(src='sina', start_date=startday, end_date=endday)
        dfchannels['channels']='sina'
        dfchannels1 = pro.news(src='10jqka', start_date=startday, end_date=endday)
        dfchannels1['channels']='10jqka'
        dfchannels2 = pro.news(src='eastmoney', start_date=startday, end_date=endday)
        dfchannels2['channels']='eastmoney'
        dfchannels3 = pro.news(src='yuncaijing', start_date=startday, end_date=endday)
        dfchannels3['channels']='yuncaijing'
        dfchannels4 = pro.news(src='wallstreetcn', start_date=startday, end_date=endday)
        dfchannels4['channels']='wallstreetcn'    
        dfRes=pd.concat([dfchannels,dfchannels1,dfchannels2,dfchannels3,dfchannels4])

        readSql='select * from news where datetime >"'+sqlday +'"'       
        newsDf = pd.read_sql_query(readSql,con = engine)
        df=pd.concat([newsDf,dfRes])   
        df=df.drop_duplicates(subset=['content'],keep=False)
        df= df.sort_values('datetime')
        # print(df)
        df['title']=df.apply(lambda x : getKeywords(x['content'],x['title']),axis=1)
        # print(df)
        df=df.drop_duplicates(subset=['title'],keep='first')
        # print(df) 
        if df.size>0:
          df.to_sql('news',engine,if_exists='append',index=False,chunksize=1000) 
    except:
        time.sleep(300)   
    time.sleep(300)