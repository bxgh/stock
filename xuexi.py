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


url="https://pc.xuexi.cn/points/login.html?ref=https://www.xuexi.cn/"  #学习强国
# url="https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html"
driver = webdriver.Firefox()
driver.maximize_window()
driver.get(url)
time.sleep(5)
driver.execute_script('window.scrollTo(0,10000)')     
time.sleep(30)                                                             #扫码登录
read_times=0                                                               #初始化阅读次数
today=datetime.date.today() 
oneday=datetime.timedelta(days=2) 
yesterday=today-oneday  
today=yesterday.strftime('%Y-%m-%d')  
today = dt.now().strftime('%Y-%m-%d')                                      #初始化阅读日期
sdate = dt.now().strftime("%Y-%m-%d-%H:%M:%S")
home_handle = driver.current_window_handle                                 #登录后主页handle
news=driver.find_element_by_xpath('//div[@id="Cds1ok08g8ns00"]')           #重要新闻链接地址
study=driver.find_element_by_xpath('//div[@id="C4b17trj9ay600"]')          #学习时评链接地址
zonghenew=driver.find_element_by_xpath('//div[@id="Cnr0zbz511qo0"]')       #综合新闻链接地址

while True:
  if read_times>7:                                 #阅读次数大于10，结束阅读
    break
  driver.switch_to_window(home_handle) 
  news.click()                                       #打开重要新闻窗口
  all_handles = driver.window_handles                #获取所有窗口句柄     
  for handle in all_handles:
   if handle != home_handle:
      news_handle=handle                             #重要新闻窗口句柄

  driver.switch_to_window(news_handle)               #切换到重要新闻窗口
  time.sleep(2)      
  getItem=driver.find_elements_by_class_name("word-item")  #获取新闻列表  
  for divId in getItem[0:18]:
    driver.switch_to_window(news_handle)
    itemDate=divId.text
    # print(itemDate,today)
    if itemDate==today:
        divId.click()                                     #进入新闻页面
        all_handles = driver.window_handles               #获取所有窗口句柄     
        for handle in all_handles:
          if handle != home_handle and handle!=news_handle:        
            driver.switch_to_window(handle)
            # page_handle=handle 
            for x in range(1,20):
              js='window.scrollTo(0,'+str(300*x)+')'      #滚动阅读
              randamTime=random.randint(600,800)
              sleepTime=randamTime/100
              time.sleep(sleepTime)              
              driver.execute_script(js)              
        driver.close()                                    #关闭新闻页面
        read_times=read_times+1                           #阅读次数加1 
        print(read_times)
        if read_times>7:                                 #阅读次数大于10，结束阅读
          break
    # time.sleep(2)    
  driver.switch_to_window(news_handle)
  driver.close()
  
  driver.switch_to_window(home_handle)
  study.click()                                       #打开重要新闻窗口
  all_handles = driver.window_handles                #获取所有窗口句柄     
  for handle in all_handles:
   if handle != home_handle:
      study_handle=handle                             #重要新闻窗口句柄

#########################################
  randamTime=random.randint(6000,8000)
  sleepTime=randamTime/100
  time.sleep(sleepTime)   

  driver.switch_to_window(study_handle)               #切换到<学习时评>窗口
  time.sleep(2)      
  getItem=driver.find_elements_by_class_name("text-wrap")  #获取列表  text-wrap  word-item
  for divId in getItem[0:18]:
    driver.switch_to_window(study_handle)
    itemDate=divId.text
    print(itemDate,today)
    if itemDate==today:
        divId.click()                                     #进入新闻页面
        all_handles = driver.window_handles               #获取所有窗口句柄     
        for handle in all_handles:
          if handle != home_handle and handle!=study_handle:        
            driver.switch_to_window(handle)
            # page_handle=handle 
            for x in range(1,20):
              js='window.scrollTo(0,'+str(300*x)+')'      #滚动阅读
              randamTime=random.randint(600,800)
              sleepTime=randamTime/100
              time.sleep(sleepTime)                 
              driver.execute_script(js)              
        driver.close()                                    #关闭新闻页面
        read_times=read_times+1                           #阅读次数加1 
        print(read_times)
        if read_times>7:                                 #阅读次数大于10，结束阅读
          break
    # time.sleep(2)    
  driver.switch_to_window(study_handle)
  driver.close()


  

driver.quit()

edate = dt.now().strftime("%Y-%m-%d-%H:%M:%S")                                
print(sdate,edate)