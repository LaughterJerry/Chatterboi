import socket
import sys
import time

class IRC:
 
	irc = socket.socket()
  
	def __init__(self, parent=None):
		# Define the socket
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.parent = parent
 
		self.send_list = []

	def send(self, channel, msg):
		# Transfer data
		self.irc.sendall(bytes("PRIVMSG " + channel + " :" + msg + "\r\n", "UTF-8"))
 
	def connect(self, server, port, channel, botnick, botpass):
		# Connect to the server
		try:
			if self.parent != None:
				self.parent.log("Connecting to: " + server)
			else:
				print("Connecting to: " + server)
			self.irc.connect((server, port))

			# Perform user authentication

			self.irc.send(bytes("PASS " + botpass + " " + "\r\n", "UTF-8"))
			self.irc.send(bytes("NICK " + botnick + "\r\n", "UTF-8"))
			time.sleep(5)

			# join the channel
			self.irc.send(bytes("JOIN " + channel + "\r\n", "UTF-8"))
			self.parent.log("CONNECTED!")
		except:
			self.parent.log(str(sys.exc_info()[0]) + "\n" + "Please try connecting again")

 
	def get_response(self):
		self.irc.setblocking(0)
		# Get the response
		try:
			resp = self.irc.recv(2040).decode("UTF-8")
			if resp.find('PING') != -1:					  
				self.irc.send(bytes('PONG ' + resp.split()[1] + '\r\n', "UTF-8")) 
		except:
			resp = None
 
 
		return resp