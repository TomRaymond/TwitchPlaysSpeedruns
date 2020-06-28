
import twitch
import yaml
import GetWindow
import re
import inputcontroller
from datetime import date, datetime
from restartcommand import RestartCommand

class MessageHandler:
    def __init__(self, settings, emulatorInputs):
        self.adminCommands = emulatorInputs['AdminInputs']
        self.publicCommands = emulatorInputs['PublicInputs']
        self.adminList = settings['twitch']['admins']
        self.botName = settings['twitch']['login']['username']
        self.emulatorWindow = GetWindow.Window(settings['emulator']['windowName'])

    # loads a specified input file to the message handler
    def load_inputs(self, inputsData):
        self.adminCommands = inputsData['AdminInputs']
        self.publicCommands = inputsData['PublicInputs']

    # commands that can run by anyone
    def public_commands(self, msg, user, channelChat):
        self._run_command(self.publicCommands, msg)

    # commands that can only be run by admins
    def admin_commands(self, msg, user, channelChat):
        if(user not in self.adminList): return # if the are not a mod, do nothing else
        self._run_command(self.adminCommands, msg)

    def _run_command(self, commandList, message): 
        keyboardInput = self.parse_input(commandList, message)
        if(keyboardInput.keys == []): return # If input was invalid (had no matching keys) then return 

        self.emulatorWindow.make_active() # ensure window is active before sending key
        inputcontroller.KeyboardInput.hold_for_seconds(keyboardInput.keys, keyboardInput.hold_time)

    # looks up the given command, returns blank key input if none found
    def resolve_single_input(self, commandList, givenCommand):
        for command in commandList:
            for alias in command['aliases']:
                if alias == givenCommand: # check if this is a direct match to the key
                    keyInput = inputcontroller.KeyInput(command['key'], command['time'])
                    return keyInput # do nothing else
        return inputcontroller.KeyInput([], 0)

    def parse_input(self, commandList, givenInput): # [m+k]:1  k:2 j        
        givenTime = None        
        commandStatement = givenInput
        if(':' in givenInput): # Check for custom defined key press time
                splitMessage = givenInput.split(':')
                commandStatement = splitMessage[0]
                givenTime = self.convert_time_input(splitMessage[1])

        commandStatement = commandStatement.translate({ord(c):None for c in ' \n\t\r'}) # strip whitespace
        multiKeypress = re.findall(r'(?<=\[)[\w\d\+]+(?=\])', givenInput) # match any letters, numbers or '+' that fall between a '[' and a ']'
        
        keyInput = None
        if(len(multiKeypress) == 1): # if there is a single '[' to ']' match
            keyInput = self.resolve_multikey_input(commandList, multiKeypress[0])
        else:
            keyInput = self.resolve_single_input(commandList, commandStatement)
        
        if(givenTime != None):
            keyInput.hold_time = givenTime
        return keyInput

    def resolve_multikey_input(self, commandList, multiInput):
        splitMultiInput = multiInput.split('+')
        resolvedKeys = []
        for singleInput in splitMultiInput:
            resolvedKeys.append(self.resolve_single_input(commandList, singleInput))

        multiKeyInput = inputcontroller.KeyInput([], 0)
        for resolvedKey in resolvedKeys: # add all resolved keys into a single keyboard keyhold command. 
            multiKeyInput.keys.extend(resolvedKey.keys)
            if(multiKeyInput.hold_time < resolvedKey.hold_time): # the combined multi keypress will hold for the longest defined time
                multiKeyInput.hold_time = resolvedKey.hold_time

        return multiKeyInput

    def parse_hold_time(self, givenInput):
            if(':' in givenInput):
                splitMessage = givenInput.split(':')
                return self.convert_time_input(splitMessage[1])
            else:
                return None        

    def convert_time_input(self, time):        
        try:
            convertedTime = float(time)
            if(convertedTime < 0.2):
                convertedTime = 0.2
            if(convertedTime > 3):
                convertedTime = 3
            return convertedTime
        except ValueError:
            return None

    def multi_command(self, msg, user, channelChat):
        if(self.validate_multi_command(msg) == False): return False # not a multi command, do nothing else

        message_arguments = msg.split(" ", 1)[1] # split on first space "!m j\n,k ,l " -> "j\n,k ,l "
        message_arguments = message_arguments.translate({ord(c):None for c in ' \n\t\r'}) # remove all whitespace including tabs and endline statements "j,k ,l " -> "j,k,l"
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

        if(split_message[0] == "!m" or split_message[0] == "!multi"): 
            return True # command name must be either !m or !multi
        else: 
            return False

    def restart_script(self, msg, user):
        if(user not in self.adminList):
            return False # if the are not a mod, do nothing else
        if(msg != "!restartscript"): return False

        RestartCommand.onRestart.call() # call for a restart, don't bother returning as the scripts closing down

    def action_log(self, msg, user, channel):
        # valid log calls are: "!log" to have the log repeated for the user / "!log update {msg}" to change the log 
        if(msg == "!oracle"): # if this is a call for the log, provide it and return
            self.repeat_action_log(channel)
            return True

        if(user not in self.adminList):
            return False # if the are not a mod, do nothing else
        # beginning of string must start with "!log update " (^!log\supdate\s) followed by any number of characters (.+)
        tokens = re.findall(r'^!oracle\supdate\s.+', msg)
        if(len(tokens) == 0): return False        
        #"!log update my new log message" -> ["!log"] ["update"] ["my new log message"]       
        split_message = tokens[0].split(" ", 2)
        self.save_action_log(user, split_message[2], channel)
        return True

    def repeat_action_log(self, channel):
        with open("LogFile.txt", 'r') as logFile:
            data = logFile.read()
            channel.send(data)

    def save_action_log(self, user, logMessage, channel):
        with open("LogFile.txt", 'w') as logFile:
            logFile.write("The oracle bestows knowledge from the great hero " + str(user) + " and tells you: " + str(logMessage))
            channel.send("The Oracle appreciates your wisdom")

    def mod_check(self, msg, user, channel):
        if (msg == "!modcheck"):
            if(user in self.adminList):
                channel.send(str(user) + ' you are a mod')
            else:
                channel.send(str(user) + ' you are not a mod')

            return True # this was a modcheck command so return true
        return False
    
    def bot_commands(self, msg, user, channel):       
        # each function returns false unless the 'msg' matches it's command word
        if(self.mod_check(msg, user, channel)): return # !modcheck
        if(self.multi_command(msg, user, channel)): return # !m / !multi
        if(self.restart_script(msg, user)): return # !restartscript
        if(self.action_log(msg, user, channel)): return # !oracle

    # can be subscribed to the twitch bot to receive messages when sent in twitch chat
    def receive_twitch_message(self, message: twitch.chat.Message) -> None:
        msg = message.text.lower()
        user = message.sender.lower()
        print(user + " sent: " + msg + " @ " + str(datetime.now()))
        if(self.botName.lower() == user): return # Ignore any messages from self
        #if(self.multi_command(msg, user, message.chat)): return #if this message was handled by multi command, do nothing else
        # if this is a bot command (any message with a '!' at the start)
        if(msg[0] == "!"):
            self.bot_commands(msg, user,  message.chat) # handle it as a bot command and do nothing else
            return
        else: # see if this is a regular single command
            self.public_commands(msg, user, message.chat)
            self.admin_commands(msg, user, message.chat)