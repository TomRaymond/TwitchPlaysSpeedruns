#Define the imports
import twitchbot
import messagehandler
from restartcommand import RestartCommand
import os
import subprocess
import time
from Timer import Timer

ConfigPath = 'Config'
DefaultConfigPath = 'DefaultConfigPath'

bot = twitchbot.TwitchBot() # init the bot
bot.connect_chat(ConfigPath+'/Auth.yaml') # Connect the bot to twitch chat using given credentials

handler = messagehandler.MessageHandler("Untitled - Notepad") # init the message handler
handler.load_inputs(ConfigPath+'/InputKeys.yaml') # load the message parsing file
handler.load_admins(ConfigPath+'/Admin.yaml') # load the admin file

bot.chat.subscribe(handler.receive_twitch_message) # assign the handler to take messages from the chat bot

Timer.init_timer()
# Setup restart command, allowing callbacks to Main from the subscribed message handler
RestartCommand.init(os.getcwd(), "Main.py")
while True:
    Timer.update_delta_time()