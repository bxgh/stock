# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class baseMainWindow
###########################################################################

class baseMainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Alwaysup", pos = wx.DefaultPosition, size = wx.Size( 901,494 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_condb = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"数据库连接", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_condb )

		self.m_dir = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"文件目录", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_dir )

		self.m_menubar1.Append( self.m_menu1, u"数据配置" )

		self.SetMenuBar( self.m_menubar1 )

		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, wx.ID_ANY )
		self.m_timer1.Start( 1000 )

		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"config配置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		self.m_staticText1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText1.SetForegroundColour( wx.Colour( 0, 0, 255 ) )

		bSizer2.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_button1 = wx.Button( self, wx.ID_ANY, u"分析数据库连接", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )

		self.m_button2 = wx.Button( self, wx.ID_ANY, u"分笔数据库连接", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button2, 0, wx.ALL, 5 )

		self.m_button11 = wx.Button( self, wx.ID_ANY, u"日线数据库连接", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button11, 0, wx.ALL, 5 )

		self.m_button12 = wx.Button( self, wx.ID_ANY, u"文件目录", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button12, 0, wx.ALL, 5 )


		gbSizer1.Add( bSizer2, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"数据维护", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText2.SetForegroundColour( wx.Colour( 0, 0, 255 ) )

		bSizer3.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_button3 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button3, 0, wx.ALL, 5 )

		self.m_button4 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button4, 0, wx.ALL, 5 )


		gbSizer1.Add( bSizer3, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"数据处理", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		self.m_staticText3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText3.SetForegroundColour( wx.Colour( 0, 0, 255 ) )

		bSizer4.Add( self.m_staticText3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_Fb = wx.Button( self, wx.ID_ANY, u"分笔数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_Fb, 0, wx.ALL, 5 )


		gbSizer1.Add( bSizer4, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"数据分析", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		self.m_staticText4.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText4.SetForegroundColour( wx.Colour( 0, 0, 255 ) )

		bSizer6.Add( self.m_staticText4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_button6 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button6, 0, wx.ALL, 5 )


		gbSizer1.Add( bSizer6, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.m_richText2 = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,350 ), 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer7.Add( self.m_richText2, 1, wx.EXPAND |wx.ALL, 5 )


		gbSizer1.Add( bSizer7, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		self.SetSizer( gbSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.connectDb, id = self.m_condb.GetId() )
		self.Bind( wx.EVT_MENU, self.SetFileDir, id = self.m_dir.GetId() )
		self.Bind( wx.EVT_TIMER, self.ontimer, id=wx.ID_ANY )
		self.m_button1.Bind( wx.EVT_BUTTON, self.menu_connectDb )
		self.m_button2.Bind( wx.EVT_BUTTON, self.menu_connectFbDb )
		self.m_button11.Bind( wx.EVT_BUTTON, self.menu_connectKDb )
		self.m_button12.Bind( wx.EVT_BUTTON, self.menu_SetFileDir )
		self.m_Fb.Bind( wx.EVT_BUTTON, self.menu_FbUse )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def connectDb( self, event ):
		event.Skip()

	def SetFileDir( self, event ):
		event.Skip()

	def ontimer( self, event ):
		event.Skip()

	def menu_connectDb( self, event ):
		event.Skip()

	def menu_connectFbDb( self, event ):
		event.Skip()

	def menu_connectKDb( self, event ):
		event.Skip()

	def menu_SetFileDir( self, event ):
		event.Skip()

	def menu_FbUse( self, event ):
		event.Skip()


