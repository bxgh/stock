# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class onTimerSet
###########################################################################

class onTimerSet ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"config配置onTimer", pos = wx.DefaultPosition, size = wx.Size( 484,367 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u" 分笔全息", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer11.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u" 分笔腾讯", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer11.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u" 日线收盘", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer11.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"全息FTP下载", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer11.Add( self.m_staticText9, 0, wx.ALL, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"db", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer11.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.txt_db = wx.StaticText( self, wx.ID_ANY, u"MsorMySql", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_db.Wrap( -1 )

		bSizer11.Add( self.txt_db, 0, wx.ALL, 5 )


		fgSizer1.Add( bSizer11, 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.txt_fbqx_onTimer = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.txt_fbqx_onTimer, 0, wx.ALL|wx.EXPAND, 5 )

		self.txt_fbQq_onTimer = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.txt_fbQq_onTimer, 0, wx.ALL|wx.EXPAND, 5 )

		self.txt_kday_onTimer = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.txt_kday_onTimer, 0, wx.ALL|wx.EXPAND, 5 )

		self.txt_QxFtpDownload = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.txt_QxFtpDownload, 0, wx.ALL|wx.EXPAND, 5 )

		self.txt_db = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.txt_db, 0, wx.ALL|wx.EXPAND, 5 )

		cbo_MsorMysqlChoices = [ u"mssql", u"mysql" ]
		self.cbo_MsorMysql = wx.ComboBox( self, wx.ID_ANY, u"mysql", wx.DefaultPosition, wx.DefaultSize, cbo_MsorMysqlChoices, 0 )
		bSizer13.Add( self.cbo_MsorMysql, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer12.Add( bSizer13, 1, wx.EXPAND, 5 )


		fgSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )


		fgSizer1.Add( bSizer14, 1, wx.EXPAND, 5 )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )


		fgSizer1.Add( bSizer15, 1, wx.EXPAND, 5 )

		bSizer151 = wx.BoxSizer( wx.VERTICAL )


		fgSizer1.Add( bSizer151, 1, wx.EXPAND, 5 )

		bSizer152 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_close = wx.Button( self, wx.ID_ANY, u"关闭", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer152.Add( self.btn_close, 0, wx.ALL, 5 )

		self.btn_onTimerconfirm = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer152.Add( self.btn_onTimerconfirm, 0, wx.ALL, 5 )


		fgSizer1.Add( bSizer152, 1, wx.EXPAND, 5 )


		self.SetSizer( fgSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.btn_close.Bind( wx.EVT_BUTTON, self.btn_Close )
		self.btn_onTimerconfirm.Bind( wx.EVT_BUTTON, self.btn_onTimersetConfirm )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def btn_Close( self, event ):
		event.Skip()

	def btn_onTimersetConfirm( self, event ):
		event.Skip()


