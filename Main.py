#Define the imports
import os, subprocess, time # default python libs
import twitchbot, messagehandler, configloader
from restartcommand import RestartCommand
from timer import Timer

settings = configloader.load_config('Settings.yaml')
emulator_inputs = configloader.load_emulator_inputs(settings['emulator']['inputsFile'])

bot = twitchbot.TwitchBot() # init the bot
bot.connect_chat(settings['twitch']['login']) # Connect the bot to twitch chat using given credentials

handler = messagehandler.MessageHandler(settings, emulator_inputs) # init the message handler

bot.chat.subscribe(handler.receive_twitch_message) # assign the handler to take messages from the chat bot

Timer.init_timer()
# Setup restart command, allowing callbacks to Main from the subscribed message handler
RestartCommand.init(os.getcwd(), "Main.py")
while True:
    Timer.update_delta_time()