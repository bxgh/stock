# -*- coding:utf-8 -*-
# use sched to timing
import time,datetime
import os
import sched,threading
import FbDownQxftp
from datetime import datetime as dt
from queue import Queue
import queue

timerType='fbqx'
ExcFunc=FbDownQxftp.FenBi(timerType) 
treadsCounts=ExcFunc.conf.get('fbqx','csvToDbfThrs')

# txtFile='H:/fbqxFtp/csv/20190117/SH600000.csv'
# tscode=txtFile[-12:-4]
# today= txtFile[-21:-13]
# print(txtFile,tscode,today)
# ExcFunc.QxCsvToHd5('H:/fbqxFtp/csv/20190117/SH600000.csv')
filerDir='H:/fbqxFtp/csv/20190117/'
fileList=os.listdir(filerDir)
dealListQueue=queue.Queue()


fileCount=0
for filename in fileList:    
   if fileCount<100:       
    # print(filename)
    dealListQueue.put(filename)
    fileCount+=1

fileTotal=dealListQueue.qsize()
start=dt.now() 

# for filename in dealList:  #17mins
#     txtfile=filerDir+filename
#     print(txtfile)
#     ExcFunc.QxCsvToHd5(txtfile)


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
          for filename in q:
            txt_file=filerDir+filename
            print(txt_file)
            ExcFunc.QxCsvToHd5(txt_file)
            print ("%s processing %s" % (threadName, txt_file))          
          time.sleep(1) 

threadList=[]
csvFileList=[]

threadFileCounts=int(fileTotal/treadsCounts)
# print(threadFileCounts)


for x in range(treadsCounts):
    csvFileList.append([])
    threadList.append('Thread-'+str(x))
    fileCount=0
    while fileCount<threadFileCounts: 
       filename= dealListQueue.get()                   
       csvFileList[x].append(filename)
       fileCount+=1

threads = []
threadID = 0

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, csvFileList[threadID])
    thread.start()
    threads.append(thread)
    threadID += 1

exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")

print(start)
print(dt.now())   