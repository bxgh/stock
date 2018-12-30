from winfenbi import fenbiWin
from winfenbi import fenbiFunction
import wx

class customStatusBar(wx.StatusBar):#设置底部状态栏、进度条
    def __init__(self, parent):        
        wx.StatusBar.__init__(self,parent,-1)
        self.SetStatusText('   进度：',0)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-2,-1])
        self.count=0
        self.gauge=wx.Gauge(self,1001,100,pos=(75,4),size=(265,20))
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        self.gauge.SetValue(0)   

class FenBimian(fenbiWin.win_fenbi):
  def init_fbmain_window(self):  
    #设置状态栏      
    self.count=100  
    self.status = customStatusBar(self)
    self.statusBar=self.SetStatusBar(self.status) 
    self.fbFunc=fenbiFunction.FenBi()

  def btn_crFbTbls( self, event ):
    self.fbFunc.baseFunc.createTables(self.status,'fenbi_')
    
  def btn_test( self, event ):
    self.fbFunc.test()


def main(): 
  pass

if __name__ == '__main__':
  main()