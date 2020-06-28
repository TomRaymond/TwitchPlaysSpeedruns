import twitch
import yaml, socket
from timer import Countdown
# Twitch API ## https://github.com/PetterKraabol/Twitch-Python 

class TwitchBot:

    def __init__(self, botSettings):
        self.chat = None
        self.helix = twitch.Helix('client-id', use_cache=True)
        self._countdownPeriod = botSettings['reconnectionPeriod']
        self.reconnectionCountdown = Countdown(botSettings['reconnectionPeriod'],False, True)
        self.reconnectionCountdown.subscribe(self.reconnect_trigger)

    def connect_chat(self, authData):    
        self.lastLogin = authData            
        channelName = authData['channel']
        username = str(authData['username'])
        key = authData['key']            
        clientID = authData['clientID']
        # connect to twitch chat
        self.chat = twitch.Chat(channel=channelName,
                       nickname=username,
                       oauth=key,
                       helix=twitch.Helix(client_id=clientID, use_cache=True))
        self.chat.subscribe(self.receive_twitch_message)
        print("Connected to chat")

    def reconnect_chat(self):       
        self.chat.irc.active = False
        self.chat.dispose()
        self.connect_chat(self.lastLogin)
        print("No input for "+ str(self._countdownPeriod )+" seconds. Refreshing Connection to Twitch.")

    def receive_twitch_message(self, message: twitch.chat.Message) -> None:
        self.reconnectionCountdown.reset() # if a message is received, reset the connection

    # event handle for triggering reset
    def reconnect_trigger(self, sender, args):
        self.reconnect_chat()