import  pymssql

connect=pymssql.connect(host='192.168.151.108',user='wws',password='Wws@28561050',database='chisdb_yyy')  
sql="update zd_charge_item set log_sn=log_sn+1 where code='401833'"
cur=connect.cursor()
cur.execute(sql)     
connect.commit()     
connect.close()

# cur.execute(sql)
# sql="select * from zd_charge_item where code='401833' "
# resList = cur.fetchall()
# print(resList)
# connect.close()
