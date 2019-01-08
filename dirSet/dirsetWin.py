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
## Class dirSet
###########################################################################

class dirSet ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"config配置文件目录", pos = wx.DefaultPosition, size = wx.Size( 607,321 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 10 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.lbl_txtfbFileDir = wx.StaticText( self, wx.ID_ANY, u"  Fb_txtFileDir", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
		self.lbl_txtfbFileDir.Wrap( -1 )

		bSizer11.Add( self.lbl_txtfbFileDir, 0, wx.EXPAND|wx.TOP, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"  Fb_txtTodayFileDir", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer11.Add( self.m_staticText7, 0, wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"  Fb_hd5DestDir", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer11.Add( self.m_staticText8, 0, wx.EXPAND|wx.TOP, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"  Fbqx_ftpdir:", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer11.Add( self.m_staticText9, 0, wx.EXPAND|wx.TOP, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"db", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer11.Add( self.m_staticText10, 0, wx.EXPAND|wx.TOP, 5 )

		self.txt_db = wx.StaticText( self, wx.ID_ANY, u"MsorMySql", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_db.Wrap( -1 )

		bSizer11.Add( self.txt_db, 0, wx.ALL, 5 )


		fgSizer1.Add( bSizer11, 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.pk_fbtxtDir = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_SMALL|wx.DIRP_USE_TEXTCTRL )
		self.pk_fbtxtDir.SetMinSize( wx.Size( 100,-1 ) )

		bSizer13.Add( self.pk_fbtxtDir, 0, wx.EXPAND, 5 )

		self.pk_fbtxtTodayDir = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST|wx.DIRP_SMALL )
		bSizer13.Add( self.pk_fbtxtTodayDir, 0, wx.EXPAND, 5 )

		self.pk_fbHd5DestDir = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST|wx.DIRP_SMALL )
		bSizer13.Add( self.pk_fbHd5DestDir, 0, wx.EXPAND, 5 )

		self.pk_fbQxDir = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST|wx.DIRP_SMALL )
		bSizer13.Add( self.pk_fbQxDir, 0, wx.EXPAND, 5 )


		bSizer12.Add( bSizer13, 1, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( bSizer12, 5, wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_confirm = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.btn_confirm, 0, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( bSizer14, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.btn_close = wx.Button( self, wx.ID_ANY, u"关闭", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.btn_close, 0, wx.ALL, 5 )


		fgSizer1.Add( bSizer15, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( fgSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.btn_confirm.Bind( wx.EVT_BUTTON, self.btn_dirSetConfirm )
		self.btn_close.Bind( wx.EVT_BUTTON, self.btn_dirSetWinClose )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def btn_dirSetConfirm( self, event ):
		event.Skip()

	def btn_dirSetWinClose( self, event ):
		event.Skip()


