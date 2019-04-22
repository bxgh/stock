from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import urllib.request
import os
import stockFunction
from time import sleep
import time
import queue

mskday = stockFunction.MSSQL(host="192.168.151.216", user="toshare1", pwd="toshare1", db="kday_qfq",myOrms="mysql") 
fileList = os.listdir('D:\\h5data\\') 
file_queue = queue.Queue()
for fileName in fileList:
    file_queue.put(fileName, True, 2)  

def load_url():
    # with urllib.request.urlopen(url, timeout=timeout) as conn:
  while True:      
    fileName=file_queue.get()
    mskday.h5FileToH5QfqFile(fileName)
    time.sleep(0.1)
    print(fileName)
  return fileName  


pool = ThreadPoolExecutor(5)
futures = []
for x in range(5):
    futures.append(pool.submit(load_url))
print(wait(futures))
print(file_queue.qsize())