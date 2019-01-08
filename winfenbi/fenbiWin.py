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
## Class win_fenbi
###########################################################################

class win_fenbi ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"分笔数据", pos = wx.DefaultPosition, size = wx.Size( 500,315 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"基本数据维护", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		self.m_staticText1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText1.SetForegroundColour( wx.Colour( 0, 0, 255 ) )

		bSizer6.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_crFbTbls = wx.Button( self, wx.ID_ANY, u"批量生成分笔表", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_crFbTbls, 0, wx.ALL, 5 )

		self.m_button10 = wx.Button( self, wx.ID_ANY, u"增量生成分笔表", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button10, 0, wx.ALL, 5 )

		self.m_button11 = wx.Button( self, wx.ID_ANY, u"删 除 当 日数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button11, 0, wx.ALL, 5 )

		self.m_button12 = wx.Button( self, wx.ID_ANY, u"test", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button12, 0, wx.ALL, 5 )


		gbSizer2.Add( bSizer6, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"数据下载", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText11.SetForegroundColour( wx.Colour( 0, 0, 255 ) )

		bSizer7.Add( self.m_staticText11, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_button5 = wx.Button( self, wx.ID_ANY, u"腾讯分笔", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button5, 0, wx.ALL, 5 )

		self.m_button6 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button6, 0, wx.ALL, 5 )

		self.m_button7 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button7, 0, wx.ALL, 5 )

		self.m_button8 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button8, 0, wx.ALL, 5 )


		gbSizer2.Add( bSizer7, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"数据分析", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		self.m_staticText12.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText12.SetForegroundColour( wx.Colour( 0, 0, 255 ) )

		bSizer3.Add( self.m_staticText12, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_button91 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button91, 0, wx.ALL, 5 )

		self.m_button101 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button101, 0, wx.ALL, 5 )

		self.m_button111 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button111, 0, wx.ALL, 5 )

		self.m_button121 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button121, 0, wx.ALL, 5 )


		gbSizer2.Add( bSizer3, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		self.SetSizer( gbSizer2 )
		self.Layout()
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, wx.ID_ANY )
		self.m_timer1.Start( 1000 )


		self.Centre( wx.BOTH )

		# Connect Events
		self.m_crFbTbls.Bind( wx.EVT_BUTTON, self.btn_crFbTbls )
		self.m_button11.Bind( wx.EVT_BUTTON, self.btn_truncTables )
		self.m_button12.Bind( wx.EVT_BUTTON, self.btn_test )
		self.m_button5.Bind( wx.EVT_BUTTON, self.btn_QQFb )
		self.Bind( wx.EVT_TIMER, self.timer_fb, id=wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def btn_crFbTbls( self, event ):
		event.Skip()

	def btn_truncTables( self, event ):
		event.Skip()

	def btn_test( self, event ):
		event.Skip()

	def btn_QQFb( self, event ):
		event.Skip()

	def timer_fb( self, event ):
		event.Skip()


