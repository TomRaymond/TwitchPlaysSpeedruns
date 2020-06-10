import yaml, os, sys

ConfigPath = 'Config'
def load_config(filename):
    filepath = ConfigPath + '/' + filename
    if(os.path.isfile(filepath) is False):
        sys.exit('Cannot load config. Unable to find file:\n' + filepath)
        
    settings = None
    with open(filepath) as settingsFile: # load data from given file
        settings = yaml.load(settingsFile, Loader=yaml.FullLoader)

    if(settings is None):
        sys.exit('Unable to load settings file')

    return settings

def load_emulator_inputs(filename):
    filepath = ConfigPath + '/' + filename
    if(os.path.isfile(filepath) is False):
        sys.exit('Cannot load emulator inputs. Unable to find file:\n' + filepath)

    inputData = None
    with open(filepath) as inputFile:
        inputData = yaml.load(inputFile, Loader=yaml.FullLoader)

    if(inputData is None):
        sys.exit('Unable to load emaultor inputs file')
    
    return inputData