import twitch
import yaml
# Twitch API ## https://github.com/PetterKraabol/Twitch-Python 

class TwitchBot:

    def __init__(self):
        self.chat = None
        self.helix = twitch.Helix('client-id', use_cache=True)

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

    def reconnect_chat(self):
        self.connect_chat(self.lastLogin)
        print("No input for 5 minutes. Reconnecting to chat")

    # event handle for triggering reset
    def reconnect_trigger(self, sender, args):
        self.reconnect_chat()