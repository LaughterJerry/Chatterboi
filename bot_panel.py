#!/usr/bin/env python3

from collections import OrderedDict

import wx
import os
import random

import json

from datetime import *

from irc_bot import *


class bot_panel(wx.Panel):
	def __init__(self, parent, grandparent):
		wx.Panel.__init__(self, parent)

		self.parent = parent
		self.grandparent = grandparent

		self.login_deets = {
			"HOST":"", 
			"PORT":0,
			"PASS":"", 
			"NICK":"",
			"CHAN":""
			}

		self.irc = None

		self.commands = {}

		self.start_time = datetime.now()

		self.build()
		self.create_menus()
		#self.set_layout()
		self.bind_all()

	def bind_all(self):
		self.con_but.Bind(wx.EVT_BUTTON, self.connect)
		self.text_entry.Bind(wx.EVT_TEXT_ENTER, self.send_msg)
		self.command_but.Bind(wx.EVT_BUTTON, self.add_cmd)
		self.response_but.Bind(wx.EVT_BUTTON, self.add_resp)

		self.grandparent.Bind(wx.EVT_MENU, self.save_login, self.save_profile)
		self.grandparent.Bind(wx.EVT_MENU, self.load_login, self.load_profile)

		self.grandparent.Bind(wx.EVT_MENU, self.save_bot, self.bot_save)
		self.grandparent.Bind(wx.EVT_MENU, self.load_bot, self.bot_load)

	def create_menus(self):
		self.save_profile = self.grandparent.fileMenu.Append(wx.ID_ANY, "&Save Login info", "Save Login")
		self.load_profile = self.grandparent.fileMenu.Append(wx.ID_ANY, "&Load Login info", "Load Login")
		self.bot_save = self.grandparent.fileMenu.Append(wx.ID_ANY, "&Save Bot", "Save Bot")
		self.bot_load = self.grandparent.fileMenu.Append(wx.ID_ANY, "&Load Bot", "Load Bot")

	def writeData(self, pathname, data):
		try:
			with open(pathname, 'w') as file:
				file.write(json.dumps(data))
		except IOError:
			wx.LogError("Cannot save current data in file %s" % pathname)

	def save_bot(self, event):
		with wx.FileDialog(self, "Save Bot Script", wildcard="BOT files (*.bot)|*.bot",
			style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.writeData(pathname, self.commands)

	def load_bot(self, event):
		with wx.FileDialog(self, "Load Bot Script", wildcard="BOT files (*.bot)|*.bot",
			style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.commands = json.loads(open(pathname, 'r').read())

			self.commandList.Set(list(self.commands.keys()))
			self.commandList.SetSelection(0)


	def save_login(self, event):
		with wx.FileDialog(self, "Save Login Info", wildcard="JSON files (*.json)|*.json",
			style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			self.login_deets["HOST"] = self.HOST_ctrl.GetLineText(0)
			self.login_deets["PORT"] = int(self.PORT_ctrl.GetLineText(0))
			self.login_deets["PASS"] = self.PASS_ctrl.GetLineText(0)
			self.login_deets["NICK"] = self.NICK_ctrl.GetLineText(0)
			self.login_deets["CHAN"] = self.CHAN_ctrl.GetLineText(0)

			pathname = fileDialog.GetPath()
			str_deets = self.login_deets
			self.writeData(pathname, str_deets)

	def load_login(self, event):
		with wx.FileDialog(self, "Load Login Info", wildcard="JSON files (*.json)|*.json",
			style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.login_deets = json.loads(open(pathname, 'r').read())

			self.HOST_ctrl.Clear()
			self.PORT_ctrl.Clear()
			self.PASS_ctrl.Clear()
			self.NICK_ctrl.Clear()
			self.CHAN_ctrl.Clear()	

			self.HOST_ctrl.AppendText(self.login_deets["HOST"])
			self.PORT_ctrl.AppendText(str(self.login_deets["PORT"]))
			self.PASS_ctrl.AppendText(self.login_deets["PASS"])
			self.NICK_ctrl.AppendText(self.login_deets["NICK"])
			self.CHAN_ctrl.AppendText(self.login_deets["CHAN"])

	def get_response(self, stim):
		return random.choice(self.commands[stim]["resp"])

	def build(self):
		self.chat_log = wx.TextCtrl(self, pos=(160,0), size=(400,300), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP)
		self.text_entry = wx.TextCtrl(self, pos=(160, 305), size=(400, 20), style=wx.TE_PROCESS_ENTER)

		self.HOST_text = wx.StaticText(self, label="Host:", pos=(10,10))
		self.HOST_ctrl = wx.TextCtrl(self, pos=(10, 30))

		self.PORT_text = wx.StaticText(self, label="Port:", pos=(10,60))
		self.PORT_ctrl = wx.TextCtrl(self, pos=(10, 80))

		self.PASS_text = wx.StaticText(self, label="Password/oauth:", pos=(10,110))
		self.PASS_ctrl = wx.TextCtrl(self, pos=(10, 130), style=wx.TE_PASSWORD)

		self.NICK_text = wx.StaticText(self, label="Nickname/profile:", pos=(10,160))
		self.NICK_ctrl = wx.TextCtrl(self, pos=(10, 180))

		self.CHAN_text = wx.StaticText(self, label="Channel:", pos=(10,210))
		self.CHAN_ctrl = wx.TextCtrl(self, pos=(10, 240))

		self.con_but = wx.Button(self, label="Connect Bot", pos = (10, 270))

		self.chat_text = wx.StaticText(self, label="Type to chat: ", pos=(85,308))

		self.command_text = wx.StaticText(self, label="Enter new Command:", pos=(10,350))
		self.command_ctrl = wx.TextCtrl(self, size=(250, 20), pos = (10, 370))
		self.command_but = wx.Button(self, label="Set Command", pos = (10, 400))
		self.commandList = wx.ListBox(self, wx.ID_ANY, size=(250,300), pos=(10, 430))

		self.response_text = wx.StaticText(self, label="Enter new Response:", pos=(300,350))
		self.response_ctrl = wx.TextCtrl(self, size=(250, 20), pos = (300, 370))
		self.response_but = wx.Button(self, label="Set Response", pos = (300, 400))
		self.responseList = wx.ListBox(self, wx.ID_ANY, size=(250,300), pos=(300, 430))

	def add_resp(self, event):
		resp = self.response_ctrl.GetLineText(0)
		self.response_ctrl.Clear()

		if resp != "":
			stim = self.commandList.GetString(self.commandList.GetSelection())

			self.commands[stim]["resp"].append(resp)

	def add_cmd(self, event):
		stim = self.command_ctrl.GetLineText(0)
		self.command_ctrl.Clear()
		if stim != "":
			self.commands[stim] = {"resp":[],"counter":0}

			self.commandList.Set(list(self.commands.keys()))
			self.commandList.SetSelection(0)

	def send_msg(self, event):
		text = self.text_entry.GetLineText(0)
		self.irc.send(self.login_deets["CHAN"], text)
		self.log(self.login_deets["NICK"] + " : " + text)
		self.text_entry.Clear()

	def connect(self, event):
		self.start_irc()

	def start_irc(self):
		self.irc = IRC(self)

		self.login_deets["HOST"] = self.HOST_ctrl.GetLineText(0)
		self.login_deets["PORT"] = int(self.PORT_ctrl.GetLineText(0))
		self.login_deets["PASS"] = self.PASS_ctrl.GetLineText(0)
		self.login_deets["NICK"] = self.NICK_ctrl.GetLineText(0)
		self.login_deets["CHAN"] = self.CHAN_ctrl.GetLineText(0)

		self.irc.connect(self.login_deets["HOST"], self.login_deets["PORT"], self.login_deets["CHAN"], self.login_deets["NICK"], self.login_deets["PASS"])

	def log(self, msg):
		self.chat_log.AppendText(msg + "\n")

	def update(self):
		if len(self.commands.keys()) > 0:
			self.responseList.Set(self.commands[self.commandList.GetString(self.commandList.GetSelection())]["resp"] )
		if self.irc != None:
			text = self.irc.get_response()
			if text != None:
				if "PRIVMSG" in text and self.login_deets["CHAN"] in text:
					name = text.split("!", 1)[0][1:]
					msg = text.split("PRIVMSG " + self.login_deets["CHAN"] + " :", 1)[1]

					self.log(name + "  :  " + msg)

					if msg.startswith("!roll"):
						parts = msg.split("!roll ")[1]
						quant, die = parts.split("d")
						quant = int(quant)
						die = int(die)

						if quant < 101:
							dice = []

							for d in range(quant):
								dice.append(random.randrange(die)+1)

							total = sum(dice)

							self.irc.send(self.login_deets["CHAN"], "@%s You rolled %d (%s)" % (name, total, str(dice) ) )
							self.log(self.login_deets["NICK"] + " bot :  " + "@%s You rolled %d (%s)" % (name, total, str(dice) ))

					elif msg.startswith("!uptime"):
						resp = "%s hours, %s minutes" % (datetime.now().hour - self.start_time.hour, datetime.now().minute - self.start_time.minute)
						self.irc.send(self.login_deets["CHAN"], resp )
						self.log(self.login_deets["NICK"] + " bot :  " + resp )
					else:
						for stim in self.commands.keys():
							if stim in msg:
								resp = self.get_response(stim)
								if "{incr}" in resp:
									self.commands[stim]["counter"] += 1
								resp = resp.format(name=name, incr=self.commands[stim]["counter"])
								self.irc.send(self.login_deets["CHAN"], resp )
								self.log(self.login_deets["NICK"] + " bot :  " + resp )

				else:
					self.log(text)
					if  ":End of /NAMES list" in text:
						self.log("CONNECTED TO CHAT! GLHF!\n")
