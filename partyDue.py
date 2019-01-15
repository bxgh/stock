# -*- coding: utf-8 -*-
import pandas as pd
import xlrd,os
import pymssql
from sqlalchemy import create_engine

connectStr = "mssql+pymssql://"+'wws' + ":" + 'Wws@28561050'+ "@" + '192.168.156.35'+ "/"+'yanfa'+"?charset=utf8" 
engine=create_engine(connectStr,echo=True)

dfDir='D:\\微云同步助手\\410054\\研发\\党费\\'
pblist=[]
for fileName in os.listdir(dfDir):
    if fileName[-4:]=='xlsx':
        branch=fileName[0:-7]
        fileName=dfDir+fileName
        df=pd.read_excel(fileName,header=None)
        df = df.drop([0,1,2,3])    #删除表头(前4行)    
        del df[0]   #删除其他列，保留姓名列
        del df[2]
        del df[3]        
        df.insert(0, 'branch', branch) #插入支部名称
        pblist.append(df)
result = pd.concat(pblist,sort=False,ignore_index=True) 
del result[4]     #删除其他列，保留姓名列
del result[5]
del result[6]
result.dropna(axis=0, how='any', inplace=True)  #去掉空值
result.columns=['branch','name']

print(result)        
result.to_sql('party_branch_employee',engine,if_exists='append',index=False,chunksize=1000)  
# txt_zb='d:\\df\\zb1.csv'     
# data_zb=pd.read_csv(txt_zb,header=None)   
# print(data_zb)