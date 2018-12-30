from dirSet import dirsetWin
import configparser

#config文件配置文件目录
class dirSetWindow(dirsetWin.dirSet): #lx:目录类型
  def init_dirSet_window(self):       
     #获取config配置文件 
     self.conf = configparser.ConfigParser()
     self.conf.read('config.ini') 
     #读取config：workDir配置，在对应控件上显示    
     fb_txtfbfiledir =self.conf.get('workDir','fb_txtfiledir')
     fb_txtFileTodayDir =self.conf.get('workDir','fb_txtFileTodayDir')
     fb_hd5DestDir =self.conf.get('workDir','fb_hd5DestDir')
     self.pk_fbtxtDir.SetPath(fb_txtfbfiledir) 
     self.pk_fbtxtTodayDir.SetPath(fb_txtFileTodayDir) 
     self.pk_fbHd5DestDir.SetPath(fb_hd5DestDir) 

  def btn_dirSetConfirm( self, event ):
     fb_txtfbfiledir=self.pk_fbtxtDir.GetPath()
     fb_txtFileTodayDir=self.pk_fbtxtTodayDir.GetPath()
     fb_hd5DestDir=self.pk_fbHd5DestDir.GetPath()

     self.conf.set('workDir','fb_txtfiledir',fb_txtfbfiledir)
     self.conf.set('workDir','fb_txtFileTodayDir',fb_txtFileTodayDir)
     self.conf.set('workDir','fb_hd5DestDir',fb_hd5DestDir)

     self.conf.write(open("config.ini", "w"))   
     self.Destroy()

  def btn_dirSetWinClose( self, event ):
	  self.Destroy()
   