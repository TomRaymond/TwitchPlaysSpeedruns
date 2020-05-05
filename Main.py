#Define the imports
import twitch
import keypresser
import keyholder
import time
import yaml
t = twitch.Twitch()

ConfigPath = 'Config'
DefaultConfigPath = 'DefaultConfigPath'
 


## Load in our configurations
adminData = None
authData = None
inputData = None
with open(ConfigPath+'/Admin.yaml') as adminFile:
    adminData = yaml.load(adminFile, Loader=yaml.FullLoader)
with open(ConfigPath+'/Auth.yaml') as authFile:
    authData = yaml.load(authFile, Loader=yaml.FullLoader)
with open(ConfigPath+'/InputKeys.yaml') as inputFile:
    inputData = yaml.load(inputFile, Loader=yaml.FullLoader)

username = authData['username']
key = authData['key']
adminList = adminData['usernames']
adminCommands = inputData['AdminInputs']
publicCommands = inputData['PublicInputs']

# connect to twitch
t.twitch_connect(username, key)

def public_commands(msg, username):
    print(username + ": " + msg.encode('utf-8'))
    for command in publicCommands:
        for alias in command['aliases']:
            if alias == msg: # check if this is a direct match to the key
                keyholder.holdForSeconds(command['key'], command['time'])
                return # do nothing else 

def admin_commands(msg, username):    
    print(username + ": " + msg.encode('utf-8'))
    if msg == "modcheck": print("You are a mod")
    for command in adminCommands:
        for alias in command['aliases']:
            if alias == msg: # check if this is a direct match to the key
                # pass the key for the match key alias to the heyholder
                keyholder.holdForSeconds(command['key'], command['time'])
                return # do nothing else

#The main loop
while True:
    # 1/5th of a second between messages checks
    time.sleep(0.2)
    #Check for new mesasages
    new_messages = t.twitch_recieve_messages()
 
    if new_messages:
        for message in new_messages:
            #Wuhu we got a message. Let's extract some details from it
            msg = message['message'].lower()
            username = message['username'].lower()            
            public_commands(msg, username)
            if(username in adminList):               
               admin_commands(msg, username)