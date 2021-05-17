# Chatterboi
 Twitch Chatbot and irc interface

Twitch chat offers an IRC connection option, this makes creating a chatbot relatively easy
twitces IRC uses an atypical format for posting so this chatbot can only work on twitch for the moment

required libraries:
	wxpython

usage:

python main.py

generate oauthkey: https://twitchapps.com/tmi/
enter login details in the left side panel, 
	irc.chat.twitch.tv
	6667
	[oauthtoken]
	username
	#username

room names have the same name as the user who created them with a # in front

bot commands are set by entering a command on the left and a response on the right
commands can be strict 1:1 such as automatically issuing a ban if a certain word is detected or randomly chosen from a list
simply keep adding responses to the response category
use {var} to keep track of how many times a response has been issued

user can also type directly into chat itself bypassing the bot if desired

GL;HF!