import win32gui
import win32api 
import lib.win32con as win32con
import win32com.client
import sys

#hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
#hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
#win32gui.SendMessage(hwndChild, win32con.WM_CHAR, 0x4B, 0)

class Window:
    def __init__(self, windowName):
        try:
            self.hwnd = win32gui.FindWindow(None, windowName)
            self.hwndChild = win32gui.GetWindow(self.hwnd, win32con.GW_CHILD)
        except:
            sys.exit('Unable find emulator window: ' + windowName)
        self.shell = win32com.client.Dispatch("WScript.Shell")
        
    def send_key(self, key):
        win32gui.SendMessage(self.hwndChild, win32con.WM_CHAR, key, 0)
    def make_active(self):
        window = win32gui.GetForegroundWindow()
        if(window != self.hwnd):
            self.shell.SendKeys('%')
            win32gui.SetForegroundWindow(self.hwnd)