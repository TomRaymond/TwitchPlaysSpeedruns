
import twitch
import yaml
import keyholder
import GetWindow
from restartcommand import RestartCommand

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
                    print("    pressed " + command['key'])
                    keyholder.holdForSeconds(command['key'], command['time'])
                    return # do nothing else

    def multi_command(self, msg, user, channelChat):
        if(self.validate_multi_command(msg) == False): return False # not a multi command, do nothing else

        message_arguments = msg.split(" ", 1)[1] # split on first space "!m j\n,k ,l " -> "j\n,k ,l "
        message_arguments.translate({ord(c):None for c in ' \n\t\r'}) # remove all whitespace including tabs and endline statements "j,k ,l " -> "j,k,l"
        message_argument_list = message_arguments.split(',') # split the arguments into an iterable list "j,k,l" -> ["j","k","l"]
        i = 0
        for command in message_argument_list: 
            if(i == 10): break # run the first 10 individual letters as a command through the standard command functions
            self.public_commands(command, user, channelChat)
            self.admin_commands(command, user, channelChat)
            i += 1
        return True
    
    def validate_multi_command(self, msg):
        # Validate given command. "!m j,k,l"  ![command_name] [command_arguments]
        if(" " not in msg): return False # Must have a space 
        split_message = msg.split(" ", 1) # split on first space [!m] [j,k,l]
        if("," not in split_message[1]): return False # Must have at least 1 comma in the arguements section
        if(split_message[0] != "!m" or split_message[0] != "!multi"): return False # command name must be either !m or !multi

        return True # if none of the above return False, this is valid

    def restart_script(self, msg, user):
        if(user not in self.adminList):
            return False # if the are not a mod, do nothing else
        if(msg != "!restartscript"): return False

        RestartCommand.onRestart.call() # call for a restart, don't bother returning as the scripts closing down

    def bot_commands(self, msg, user, channel):        
        if(self.multi_command(msg, user, channel)): return # if handled by multi command, do nothing else
        if(self.restart_script(msg, user)): return # if handled by restart_script, do nothing else

    # can be subscribed to the twitch bot to receive messages when sent in twitch chat
    def receive_twitch_message(self, message: twitch.chat.Message) -> None:
        msg = message.text.lower()
        user = message.sender.lower()

        #if(self.multi_command(msg, user, message.chat)): return #if this message was handled by multi command, do nothing else
        # if this is a bot command (any message with a '!' at the start)
        if(msg[0] == "!"): 
            self.bot_commands(msg, user,  message.chat) # handle it as a bot command and do nothing else
            return
        else: # see if this is a regular single command
            self.public_commands(msg, user, message.chat)
            self.admin_commands(msg, user, message.chat)
