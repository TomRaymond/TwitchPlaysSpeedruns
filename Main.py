#Define the imports
import os, subprocess, time # default python libs
import twitchbot, messagehandler, configloader
from restartcommand import RestartCommand
from timer import Timer, Countdown

settings = configloader.load_config('Settings.yaml')
emulator_inputs = configloader.load_emulator_inputs(settings['emulator']['inputsFile'])

handler = messagehandler.MessageHandler(settings, emulator_inputs) # init the message handler

bot = twitchbot.TwitchBot(settings['twitch']['bot']) # init the bot
bot.subscribe(handler.receive_twitch_message) # assign the handler to take messages from the chat bot
bot.connect_chat(settings['twitch']['login']) # Connect the bot to twitch chat using given credentials

Timer.init_timer()
# Setup restart command, allowing callbacks to Main from the subscribed message handler
RestartCommand.init(os.getcwd(), "Main.py")
while True:    
    time.sleep(0.1)
    Timer.update_delta_time()