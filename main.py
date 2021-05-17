#!/usr/bin/env python3

from listener import Key_listener
import wx
import os

from irc_bot import *

from bot_panel import bot_panel



class tool_panel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, style=wx.RAISED_BORDER)

		self.parent = parent

		self.build()
		self.set_layout()
		#self.bind_all()

	def build(self):
		self.mainBook = wx.Notebook(self)
		self.bot_panel = bot_panel(self.mainBook, self.parent)

		self.mainBook.AddPage(self.bot_panel, "Bot")

	def set_layout(self):
		mainBox = wx.BoxSizer(wx.HORIZONTAL)
		mainBox.Add(self.mainBook, 4, wx.EXPAND)
		self.SetSizer(mainBox)

	def update(self):
		self.bot_panel.update()

class TwitchMate(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self, parent, wx.ID_ANY, pos=(1,1), size=size, style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX) )

		menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()


		self.listener = Key_listener()

		self.tools = tool_panel(self)

		closeItem = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

		menubar.Append(self.fileMenu, '&File')
		self.SetMenuBar(menubar)


		self.timer = wx.Timer(self)



		self.Bind(wx.EVT_TIMER, self.update, self.timer)
		self.Bind(wx.EVT_MENU, self.OnClose, closeItem)
		self.Bind(wx.EVT_CLOSE, self.OnClose)


		self.timer.Start(20)
		self.build_char()


	def build_char(self):
		pass

	def update(self, evt):
		#self.tracker.update()
		#self.tracker.draw()
		#self.tracker.output()

		#self.canvas.move_head(self.tracker.get_origin())

		#self.canvas.update()
		self.tools.update()

	def OnClose(self, event):
		#self.canvas.OnClose()
		wx.Exit()
		exit()


if __name__ == '__main__':
	app = wx.App()
	view = TwitchMate(parent=None, title='Avatars of Morpheus', size=(600, 850) )
	view.Show()
	app.MainLoop()

