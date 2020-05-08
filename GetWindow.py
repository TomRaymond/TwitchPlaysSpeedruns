import win32gui
import win32api 
import lib.win32con as win32con

hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
win32gui.SendMessage(hwndChild, win32con.WM_CHAR, 0x4B, 0)