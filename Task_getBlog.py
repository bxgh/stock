#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from datetime import datetime as dt
import datetime
import random
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import codecs  
import configparser

while True:
  try:
    engine=create_engine("mysql+pymysql://toshare1:toshare1@192.168.151.216:3306/kday?charset=utf8",echo=True)   
    connect=pymysql.connect(host='192.168.151.216',port=3306,user='toshare1',password='toshare1',database='kday',charset='utf8')    
    cur=connect.cursor()
    today=datetime.date.today() 
    sqlday = today.strftime('%Y-%m-%d')
    readSql='select ID,address from blog'       
    blogDf = pd.read_sql_query(readSql,con = engine)          #获取已导入博客地址列表

    conf = configparser.ConfigParser()
    conf.read('config.ini')   
    blogHtmlDir = conf.get('workDir','blog_dir') 

    url="http://blog.eastmoney.com/lyq113/"                        #博客地址
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)
    time.sleep(5)
    driver.execute_script('window.scrollTo(0,10000)')     
    blogHome='http://blog.eastmoney.com/lyq113/blog_'                #博客地址前缀

    data = []
    for line in open("index.html","r"):                         #读取html编码
      data.append(line)

    news=driver.find_elements_by_class_name('articleList')           #博客文章地址列表
    nameList=[]
    for article in news :
        title=article.get_attribute('id')[8:]
        nameList.append(title)

    dfnews=pd.DataFrame(nameList,columns=['ID'])
    dfnews['address']=dfnews.apply(lambda x :blogHome+x['ID']+".html",axis=1)
    blogDf=pd.merge(dfnews,blogDf,on=['address'])
    df=pd.concat([blogDf,dfnews]) 
    df=df.drop_duplicates(subset='address',keep=False)            #最新博客文章地址列表    

    for index,row in df.iterrows():  
      blogurl=row['address']                                     #address
      driver.get(blogurl)
      driver.execute_script('window.scrollTo(0,10000)') 
      blogbody=driver.find_element_by_class_name('articleBody')   #获取博客内容
      blogOuthtml=blogbody.get_attribute('outerHTML')                  #content
      blogOuthtml=blogOuthtml.replace('16px','48px')
      blogTitle=driver.find_element_by_class_name('articleTitle').text #title  
      blogTime=driver.find_element_by_class_name('time').text          #datetime 
      blogTitle=blogTitle.replace(blogTime,'')                  #处理结果
      if len(blogTime)>19:
        blogTime=blogTime[1:]
        blogTime=blogTime[0:-1]        
      blogID=row['ID']
      blogFileName=str(blogID)+'.html'   
      exesql=" insert into  blog (ID,title,content,blogtime,address) value (%s,%s,%s,%s,%s)"  #保存博客到数据库   
      try :
        cur.execute(exesql,(blogID,blogTitle,blogOuthtml,blogTime,blogurl))  
        connect.commit()         
        blogFileName=blogHtmlDir+blogFileName  
        with codecs.open(blogFileName,"w","utf-8") as f:                                        #博客内容生成html文件           
          for i in data:                                                                
              f.writelines(i) 
          f.writelines(blogOuthtml)
          f.writelines('</body>')
          f.writelines('</html>')
      except:
        pass    
      time.sleep(15)
    connect.close()    
    driver.quit()    
    time.sleep(60*60)  #一小时
  except:
    time.sleep(60*10)  #10分钟 