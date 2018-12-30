from winfenbi import fenbiFunction,fenbiWin


class FenBimian(fenbiWin.win_fenbi):
  def init_fbmain_window(self):  
    self.fbFunc=fenbiFunction.FenBi()

  def btn_test( self, event ):
    print('ik！')


def main(): 
  pass

if __name__ == '__main__':
  main()