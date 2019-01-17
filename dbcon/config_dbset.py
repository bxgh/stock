from dbcon import datasetWin
import configparser
import base64
import pymssql,pymysql

#config文件配置数据库连接
class databaseSetWindow(datasetWin.databaseSet): 
  def init_dbSet_window(self):          
     #获取config配置文件     
     self.conf = configparser.ConfigParser()
     self.conf.read('config.ini') 
     host=self.conf.get('database','host_fenbi') 
     host=base64.decodestring(bytes(host, 'utf-8'))     #解密     
     self.txt_host.SetValue(host)

     port=self.conf.get('database','port_fenbi') 
     port=base64.decodestring(bytes(port, 'utf-8'))     #解密     
     self.txt_port.SetValue(port)

     user=self.conf.get('database','user_fenbi') 
     user=base64.decodestring(bytes(user, 'utf-8'))     #解密     
     self.txt_user.SetValue(user)

     pwd=self.conf.get('database','pwd_fenbi') 
     pwd=base64.decodestring(bytes(pwd, 'utf-8'))     #解密     
     self.txt_pwd.SetValue(pwd)

     db=self.conf.get('database','db_fenbi') 
     db=base64.decodestring(bytes(db, 'utf-8'))     #解密     
     self.txt_db.SetValue(db)

     mysqlormssql=self.conf.get('database','msormy_fenbi') 
     mysqlormssql=base64.decodestring(bytes(mysqlormssql, 'utf-8'))     #解密     
     self.cbo_MsorMysql.SetValue(mysqlormssql)
    #  host=self.conf.get()        

  def dbsetConfirm( self, event ):    
     host=self.txt_host.GetValue() 
     host_decode= base64.b64encode(bytes(host, 'utf-8')) #加密存入
     host_fenbi=str(host_decode,'utf-8')     
     self.conf.set("database", "host_fenbi", host_fenbi)

     port=self.txt_port.GetValue() 
     port_decode= base64.b64encode(bytes(port, 'utf-8')) #加密存入
     port_fenbi=str(port_decode,'utf-8')     
     self.conf.set("database", "port_fenbi", port_fenbi)
     
     user=self.txt_user.GetValue() 
     user_decode= base64.b64encode(bytes(user, 'utf-8')) #加密存入
     user_fenbi=str(user_decode,'utf-8')     
     self.conf.set("database", "user_fenbi", user_fenbi)

     pwd=self.txt_pwd.GetValue() 
     pwd_decode= base64.b64encode(bytes(pwd, 'utf-8')) #加密存入
     pwd_fenbi=str(pwd_decode,'utf-8')     
     self.conf.set("database", "pwd_fenbi", pwd_fenbi)

     db=self.txt_db.GetValue() 
     db_decode= base64.b64encode(bytes(db, 'utf-8')) #加密存入
     db_fenbi=str(db_decode,'utf-8')     
     self.conf.set("database", "db_fenbi", db_fenbi)

     mysqlormssql=self.cbo_MsorMysql.GetValue() 
     sql_decode= base64.b64encode(bytes(mysqlormssql, 'utf-8')) #加密存入
     msormy_fenbi= str(sql_decode,'utf-8')     
     self.conf.set("database", "msormy_fenbi", msormy_fenbi)

     self.conf.write(open("config.ini", "w"))   
     self.Destroy()

  def btnTestLink( self, event ):
    host=self.txt_host.GetValue()
    port=int(self.txt_port.GetValue())
    user=self.txt_user.GetValue()    
    pwd=self.txt_pwd.GetValue()
    db=self.txt_db.GetValue()
    mysqlormssql=self.cbo_MsorMysql.GetValue()
    
    if mysqlormssql=='mssql':
     try:
       self.connect=pymssql.connect(host=host,user=user,password=pwd,database=db,charset='utf8')        
      #  tkinter.messagebox.showinfo('提示','数据库连接成功。')
     except Exception as e:
       pass
      #  tkinter.messagebox.showwarning('提示','数据库连接失败。')
        
    if mysqlormssql=='mysql':     
     try:
       connect=pymysql.connect(host=host,port=port,user=user,password=pwd,database=db,charset='utf8')       
      #  tkinter.messagebox.showinfo('提示','数据库连接成功。')
     except Exception as e:
      pass 
      #  tkinter.messagebox.showwarning('提示','数据库连接失败。')     
        

  def dbsetWinClose( self, event ):
    #  self.Hide() 
      self.Destroy()