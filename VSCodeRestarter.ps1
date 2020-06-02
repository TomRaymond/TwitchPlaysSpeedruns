param ($projectFolderPath, $mainScriptPath)
Get-Process | Where-Object { $_.MainWindowTitle -like '*Visual Studio Code' } | Stop-Process # Get old VS Code window and close it
cmd.exe /c "code $projectFolderPath -g $mainScriptPath" # Start new VS Code window and open it on the main.py
Start-Sleep 5 # let new window startup

# Find the new window and send it F5 to start debugging / run the program
$wshell = New-Object -ComObject wscript.shell;
$wshell.AppActivate('Main.py - TwitchPlaysSpeedruns - Visual Studio Code')
Start-Sleep 1 # let windows tab to the new screen
$wshell.SendKeys("{F5}") # start debugging command
Start-Sleep 1
$wshell.SendKeys("{ENTER}") # select debug as python (which is defualt option)