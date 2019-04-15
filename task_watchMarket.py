import  watchMarket
import time
from datetime import datetime as dt



watchMarket=watchMarket.watchStockMarket()  
T=True
while T:
    now = dt.now().strftime('%H%M%S')
    if now>'113100':
      T=False  
    else:
      watchMarket.getQqMarketData()
    time.sleep(30)    
print('end!')