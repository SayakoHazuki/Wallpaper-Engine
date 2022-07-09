import pyautogui
import tkinter
import win32gui
import win32con
import ctypes
from ctypes import c_bool, c_int, windll
from ctypes.wintypes import HWND, UINT
from PIL import ImageTk, Image

W = 1920
H = 1080

tk = tkinter.Tk(className="Wallpaper")
tk.geometry(f"{W}x{H}")

canvasX = int(W*1.15)
canvasY = int(H*1.15)
canvasXOffset = 0-W*0.075
canvasYOffset = 0-H*0.075
canvas = tkinter.Canvas(tk, width=canvasX, height=canvasY, bd=-2)
canvas.place(x=canvasXOffset, y=canvasYOffset)

imagePath = "./background.jpg"
originalImage = Image.open(imagePath)
imageX = int(1988*1.15)
imageY = int(1080*1.15)
image = originalImage.resize((imageX, imageY), Image.ANTIALIAS)

img = ImageTk.PhotoImage(image)
canvas.create_image(canvasX/2, canvasY/2, image=img, anchor=tkinter.CENTER)


def updateCanvasPos():
    global canvasXOffset, canvasYOffset
    originalX = canvasXOffset
    originalY = canvasYOffset
    cursorPos = pyautogui.position()
    canvasXOffset = int(0 - (cursorPos.x * 0.15))
    canvasYOffset = int(0 - (cursorPos.y * 0.15))
    canvasXOffset = min(-2, canvasXOffset)
    canvasXOffset = max(W*-0.15 + 2, canvasXOffset)
    canvasYOffset = min(-2, canvasYOffset)
    canvasYOffset = max(H*-0.15 + 2, canvasYOffset)
    canvasXOffset = 0.85 * originalX + 0.15 * canvasXOffset
    canvasYOffset = 0.85 * originalY + 0.15 * canvasYOffset
    canvas.place(x=canvasXOffset, y=canvasYOffset)
    tk.after(1, updateCanvasPos)


hwnd = tk.winfo_id()
tk.update()

tk.after(20, updateCanvasPos)
tk.overrideredirect(True)

def getHwnd():
    progman = win32gui.FindWindow("Progman", "Program Manager")
    a = win32gui.SendMessageTimeout(progman, 0x052C, 0, 0, win32con.SMTO_NORMAL, 0x03E8)
    print("a:", a)
    hwnd_workW = None
    while 1:
        hwnd_workW = win32gui.FindWindowEx(None, hwnd_workW, "WorkerW", None)
        if not hwnd_workW:
            continue
        hView = win32gui.FindWindowEx(hwnd_workW, None, "SHELLDLL_DefView", None)
        if not hView:
            continue
        h = win32gui.FindWindowEx(None, hwnd_workW, "WorkerW", None)
        while h:
            win32gui.SendMessage(h, 0x0010, 0, 0)
            h = win32gui.FindWindowEx(None, hwnd_workW, "WorkerW", None)
        break 
    return h

WorkerW_hwnd = getHwnd()
print(hwnd, WorkerW_hwnd)
win32gui.SetParent(hwnd, WorkerW_hwnd)

tk.mainloop()

