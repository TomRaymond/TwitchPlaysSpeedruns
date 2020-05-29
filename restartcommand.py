import os
import event
  

class RestartMeta:
    def __init__(self):
        RestartCommand.onRestart = event.EventHandler(event.Event(), self)
        RestartCommand.onRestart += self._restart

    def _restart(self, sender, args):
        projectFolderArg = " -projectFolderPath " + RestartCommand.folderPath
        scriptPathArg = " -mainScriptPath " + RestartCommand.folderPath + "/" + RestartCommand.fileName
        os.system("start cmd /c PowerShell -ExecutionPolicy Unrestricted -File VSCodeRestarter.ps1" + projectFolderArg + scriptPathArg)
        os.kill(os.getpid(), 9)
    
    def restart(self, folderPath, fileName):
        projectFolderArg = " -projectFolderPath " + folderPath
        scriptPathArg = " -mainScriptPath " + folderPath + "/" + fileName
        os.system("start cmd /c PowerShell -ExecutionPolicy Unrestricted -File VSCodeRestarter.ps1" + projectFolderArg + scriptPathArg)
        os.kill(os.getpid(), 9)

class RestartCommand:
    _restart_instance = None
    onRestart = None
    folderPath = ""
    fileName = ""    
    @staticmethod
    def init(folderPath, fileName):
        RestartCommand.folderPath = folderPath
        RestartCommand.fileName = fileName
        _restart_instance = RestartMeta()