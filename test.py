from datetime import datetime as dt
import datetime
import time,os
from ftplib import FTP
import queue
import pandas as pd

tscode='SZ300296'
if tscode[0:5]=='SZ300':
    print(tscode[0:6])
else:
    print('no')    
     