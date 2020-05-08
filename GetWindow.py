import ctypes
import win32gui
#EnumWindows = ctypes.windll.user32.EnumWindows
#EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
#GetWindowText = ctypes.windll.user32.GetWindowTextW
#GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
#IsWindowVisible = ctypes.windll.user32.IsWindowVisible

#titles = []
#def foreach_window(hwnd, lParam):
#    if IsWindowVisible(hwnd):
#        length = GetWindowTextLength(hwnd)
#        buff = ctypes.create_unicode_buffer(length + 1)
#        GetWindowText(hwnd, buff, length + 1)
#        titles.append((hwnd, buff.value))
#    return True
Hwnd = win32gui.FindWindow(None, "Task Manager")
windowText = win32gui.GetWindowText(Hwnd)
print(windowText)