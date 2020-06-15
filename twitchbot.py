import twitch, time
import yaml, socket
from datetime import date, datetime
from timer import Countdown
# Twitch API ## https://github.com/PetterKraabol/Twitch-Python 

class TwitchBot:
    def __init__(self, botSettings):
        self._messageSubscribers = []
        self.oldThreads = []
        self.chat = None
        self.helix = twitch.Helix('client-id', use_cache=True)
        self._countdownPeriod = botSettings['reconnectionPeriod']        

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
                       helix=twitch.Helix(client_id=clientID, use_cache=True),
                       timeout = self._countdownPeriod)
        # resubscribe anyone that wanted messages from the channel to the new chat connection               
        for subscriber in self._messageSubscribers:
            self.chat.subscribe(subscriber)
        self.chat.irc.thread_close.subscribe(self._irc_closed)
        print("Connected to chat @" + str(datetime.now()))

    def _irc_closed(self, isClosed) -> None:
        print("Disconnected from chat @" + str(datetime.now()))
        self.connect_chat(self.lastLogin)

    def subscribe(self, subscriber):
        self._messageSubscribers.append(subscriber)