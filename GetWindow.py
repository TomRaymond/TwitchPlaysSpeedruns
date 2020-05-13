import win32gui
import win32api 
import lib.win32con as win32con

#hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
#hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
#win32gui.SendMessage(hwndChild, win32con.WM_CHAR, 0x4B, 0)

class Window:
    def __init__(self, windowName):
        self.hwnd = win32gui.FindWindow(None, windowName)
        self.hwndChild = win32gui.GetWindow(self.hwnd, win32con.GW_CHILD)
    def SendKey(self, key):
        win32gui.SendMessage(self.hwndChild, win32con.WM_CHAR, key, 0)