# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class baseMainWindow
###########################################################################

class baseMainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 917,472 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_toolBar4 = self.CreateToolBar( wx.TB_TEXT, wx.ID_ANY )
		self.dt_today = wx.adv.DatePickerCtrl( self.m_toolBar4, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar4.AddControl( self.dt_today )
		self.dt_start = wx.adv.DatePickerCtrl( self.m_toolBar4, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		self.m_toolBar4.AddControl( self.dt_start )
		self.dt_end = wx.adv.DatePickerCtrl( self.m_toolBar4, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		self.m_toolBar4.AddControl( self.dt_end )
		self.m_toolBar4.AddSeparator()

		self.pk_dir = wx.DirPickerCtrl( self.m_toolBar4, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( 350,24 ), wx.DIRP_DEFAULT_STYLE )
		self.m_toolBar4.AddControl( self.pk_dir )
		self.m_toolBar4.Realize()

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.m_dirPicker9 = wx.DirPickerCtrl( self, wx.ID_ANY, u"G:\\kdayHis", u"选择kdy目录", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		self.m_dirPicker9.SetToolTip( u"选择kdy目录" )

		bSizer11.Add( self.m_dirPicker9, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_fbTxtDir = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self.btn_fbTxtDir, 0, wx.ALL, 5 )

		self.m_button14 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self.m_button14, 0, wx.ALL, 5 )

		self.m_button15 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self.m_button15, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer81, 1, wx.EXPAND, 5 )


		bSizer6.Add( bSizer11, 1, wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_truncKday = wx.Button( self, wx.ID_ANY, u"清空所有Kday", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.btn_truncKday, 0, wx.ALL, 5 )

		self.btn_test = wx.Button( self, wx.ID_ANY, u"测试", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.btn_test, 0, wx.ALL, 5 )

		self.btn_crKdaytb = wx.Button( self, wx.ID_ANY, u"生成kday表", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_crKdaytb.SetToolTip( u"test" )

		bSizer14.Add( self.btn_crKdaytb, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer14, 1, wx.EXPAND|wx.SHAPED, 5 )


		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_getHisDate = wx.Button( self, wx.ID_ANY, u"获取全部kday到hdf5", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.btn_getHisDate, 0, wx.ALL, 5 )

		self.btn_getAllHisKdaysH5 = wx.Button( self, wx.ID_ANY, u"全部历史Hdf5导入SQL", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.btn_getAllHisKdaysH5, 0, wx.ALL, 5 )

		self.btn_calkdayHis = wx.Button( self, wx.ID_ANY, u"获取断传列表", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.btn_calkdayHis, 0, wx.ALL, 5 )

		self.btn_kdayGoOn = wx.Button( self, wx.ID_ANY, u"kday断点续传", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.btn_kdayGoOn, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer8, 1, wx.EXPAND, 5 )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		self.btn_kdayClose = wx.Button( self, wx.ID_ANY, u"日线当日自动收盘", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.btn_kdayClose, 0, wx.ALL, 5 )


		bSizer15.Add( bSizer16, 1, wx.EXPAND, 5 )


		bSizer5.Add( bSizer15, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer5 )
		self.Layout()
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.pk_dir.Bind( wx.EVT_DIRPICKER_CHANGED, self.setKdayDir )
		self.m_dirPicker9.Bind( wx.EVT_DIRPICKER_CHANGED, self.setKdayDir )
		self.btn_fbTxtDir.Bind( wx.EVT_BUTTON, self.getFbTxtDir )
		self.btn_truncKday.Bind( wx.EVT_BUTTON, self.deleteAllKday )
		self.btn_test.Bind( wx.EVT_BUTTON, self.temp )
		self.btn_crKdaytb.Bind( wx.EVT_BUTTON, self.createKdayTable )
		self.btn_getHisDate.Bind( wx.EVT_BUTTON, self.getAllHisKdaysToH5 )
		self.btn_getAllHisKdaysH5.Bind( wx.EVT_BUTTON, self.saveAllHisKdaysH5ToSqlserver )
		self.btn_calkdayHis.Bind( wx.EVT_BUTTON, self.calcKdayHisDays )
		self.btn_kdayGoOn.Bind( wx.EVT_BUTTON, self.kdayHisGoOn )
		self.btn_kdayClose.Bind( wx.EVT_BUTTON, self.kdayClose )
		self.Bind( wx.EVT_TIMER, self.ontimer, id=wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def setKdayDir( self, event ):
		event.Skip()


	def getFbTxtDir( self, event ):
		event.Skip()

	def deleteAllKday( self, event ):
		event.Skip()

	def temp( self, event ):
		event.Skip()

	def createKdayTable( self, event ):
		event.Skip()

	def getAllHisKdaysToH5( self, event ):
		event.Skip()

	def saveAllHisKdaysH5ToSqlserver( self, event ):
		event.Skip()

	def calcKdayHisDays( self, event ):
		event.Skip()

	def kdayHisGoOn( self, event ):
		event.Skip()

	def kdayClose( self, event ):
		event.Skip()

	def ontimer( self, event ):
		event.Skip()


