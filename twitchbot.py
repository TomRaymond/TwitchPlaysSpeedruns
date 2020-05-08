import twitch
import yaml
# Twitch API ## https://github.com/PetterKraabol/Twitch-Python 

class TwitchBot:

    def __init__(self):
        self.chat = None
        self.helix = twitch.Helix('client-id', use_cache=True)

    def connect_chat(self, authFile):                
        with open(authFile) as authFile: # load data from given file
            authData = yaml.load(authFile, Loader=yaml.FullLoader)
            channelName = authData['channel']
            username = str(authData['username'])
            key = authData['key']            
            clientID = authData['clientID']
        # connect to twitch chat
        self.chat = twitch.Chat(channel=channelName,
                       nickname=username,
                       oauth=key,
                       helix=twitch.Helix(client_id=clientID, use_cache=True))        