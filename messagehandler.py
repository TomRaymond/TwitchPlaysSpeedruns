
import twitch
import yaml
import keyholder
import keypresser
import GetWindow

class MessageHandler:
    def __init__(self, emulatorWindowTitle):
        self.adminCommands = []
        self.publicCommands = []
        self.adminList = []
        self.emulatorWindow = GetWindow.Window(emulatorWindowTitle)

    # loads a specified input file to the message handler
    def load_inputs(self, configFile):
        with open(configFile) as inputFile:
            inputData = yaml.load(inputFile, Loader=yaml.FullLoader)
            self.adminCommands = inputData['AdminInputs']
            self.publicCommands = inputData['PublicInputs']
        
    # loads a list of admins to the message handler. Overrides currently active list
    def load_admins(self, adminFile):
        with open(adminFile) as adminFile:
            adminData = yaml.load(adminFile, Loader=yaml.FullLoader)
            self.adminList = adminData['usernames']

    # commands that can run by anyone
    def public_commands(self, msg, user, channelChat):
        self._run_command(self.publicCommands, msg)

    # commands that can only be run by admins
    def admin_commands(self, msg, user, channelChat):
        if(user not in self.adminList):
            return # if the are not a mod, do nothing else
        if msg == "modcheck": channelChat.send('you are a mod')
        self._run_command(self.adminCommands, msg)

    def _run_command(self, commandList, message):
        for command in commandList:
            for alias in command['aliases']:
                if alias == message: # check if this is a direct match to the key
                    self.emulatorWindow.make_active() # ensure window is active before seding key
                    # pass the key for the match key alias to the heyholder
                    keyholder.holdForSeconds(command['key'], command['time'])
                    return # do nothing else

    def multi_command(self, msg, user, channelChat):
        split_message = msg.split()
        #if they called for a multi command
        if(split_message[0] == "!m" or split_message[0] == "!multi"):
            i = 0
            for commandLetter in split_message[1]: 
                if(i == 10): break # run the first 10 individual letters as a command through the standard command functions
                self.public_commands(commandLetter, user, channelChat)
                self.admin_commands(commandLetter, user, channelChat)
                i += 1
            return True
        else:
            return False

    # can be subscribed to the twitch bot to receive messages when sent in twitch chat
    def receive_twitch_message(self, message: twitch.chat.Message) -> None:
        msg = message.text.lower()
        user = message.sender.lower()

        if(self.multi_command(msg, user, message.chat)): return #if this message was handled by multi command, do nothing else

        self.public_commands(msg, user, message.chat)
        self.admin_commands(msg, user, message.chat)