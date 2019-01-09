from ontimerSet import onTimerSetWin
import configparser

#config文件配置定时器
class onTimerSetWindow(onTimerSetWin.onTimerSet): 
  def init_onTimerSet_window(self):       
     #获取config配置文件 
     self.conf = configparser.ConfigParser()
     self.conf.read('config.ini') 
     #读取config：workDir配置，在对应控件上显示    
     onTimer_fbqx =self.conf.get('onTimer','fbqx') 
     onTimer_fbQq =self.conf.get('onTimer','fbQq') 
     onTimer_kday =self.conf.get('onTimer','kday')     
     self.txt_fbqx_onTimer.SetValue(onTimer_fbqx)
     self.txt_fbQq_onTimer.SetValue(onTimer_fbQq)
     self.txt_kday_onTimer.SetValue(onTimer_kday)
    

  def btn_onTimersetConfirm( self, event ):
     onTimer_fbqx=self.txt_fbqx_onTimer.GetValue() 
     onTimer_fbQq=self.txt_fbQq_onTimer.GetValue()   
     onTimer_kday=self.txt_kday_onTimer.GetValue()

     self.conf.set('onTimer','fbqx',onTimer_fbqx)   
     self.conf.set('onTimer','fbQq',onTimer_fbQq)       
     self.conf.set('onTimer','kday',onTimer_kday)    

     self.conf.write(open("config.ini", "w"))   
     self.Destroy()

  def btn_Close( self, event ):
	  self.Destroy()
   