from dmScopeSet import dmScopeSetWin
import configparser

#config文件配置代码范围(600,601,602,603,000,002,300)
class dmScopeSetWindow(dmScopeSetWin.dmScopeSet): 
  def init_dmScopeSet_window(self):       
     #获取config配置文件 
     self.conf = configparser.ConfigParser()
     self.conf.read('config.ini') 
     #读取config：workDir配置，在对应控件上显示    
     dmscope_fbqx =self.conf.get('dmScope','fbqx')     
     self.txt_fbqx_dmscope.SetValue(dmscope_fbqx)
    

  def btn_dmScopesetConfirm( self, event ):
     dmscope_fbqx=self.txt_fbqx_dmscope.GetValue()    

     self.conf.set('dmScope','fbqx',dmscope_fbqx)     

     self.conf.write(open("config.ini", "w"))   
     self.Destroy()

  def btn_Close( self, event ):
	  self.Destroy()
   