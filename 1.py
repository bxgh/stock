import baseFunction,stockFunction
import time 

now = time.localtime(time.time())      
today=time.strftime("%Y%m%d", now)
mskday = stockFunction.MSSQL(host="192.168.151.213", user="toshare1", pwd="toshare1", db="kday_qfq",myOrms="mysql")  
mskday.kday_close(today)