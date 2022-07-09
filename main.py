import pyautogui
import tkinter
import win32gui
import win32con
import win32api
from PIL import ImageTk, Image

# Config
wallpaperPath = "./background.jpg"

# Tkinter init
tk = tkinter.Tk(className="Wallpaper")

monitorInfo = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
monitorArea = monitorInfo.get("Monitor")
W = monitorArea[2]
H = monitorArea[3]

tk.geometry(f"{W}x{H}")
tk.overrideredirect(True)
hwnd = tk.winfo_id()

# Canvas
canvasX = int(W*1.15)
canvasY = int(H*1.15)
canvasXOffset = 0-W*0.075
canvasYOffset = 0-H*0.075

canvas = tkinter.Canvas(tk, width=canvasX, height=canvasY, bd=-2)
canvas.place(x=canvasXOffset, y=canvasYOffset)

# Canvas > Wallpaper Image
originalImage = Image.open(wallpaperPath)
imageW, imageH = originalImage.size

imageToScrnW = W / imageW
imageToScrnH = H / imageH
print(imageToScrnW, imageToScrnH)
imageToScrnRatio = max(imageToScrnW, imageToScrnH)
imageTargetW = int(imageW * imageToScrnRatio * 1.15)
imageTargetH = int(imageH * imageToScrnRatio * 1.15)
print(imageW*imageToScrnRatio, imageH*imageToScrnRatio)

image = originalImage.resize((imageTargetW, imageTargetH), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
canvas.create_image(canvasX/2, canvasY/2, image=img, anchor=tkinter.CENTER)

# Updating Canvas Displaying Area According To Mouse Pos


def updateCanvasPos():
    global canvasXOffset, canvasYOffset
    cursorPos = pyautogui.position()

    originalX = canvasXOffset
    originalY = canvasYOffset

    canvasXOffset = int(0 - (cursorPos.x * 0.15))
    canvasXOffset = min(-2, canvasXOffset)
    canvasXOffset = max(W*-0.15 + 2, canvasXOffset)
    canvasXOffset = 0.85 * originalX + 0.15 * canvasXOffset

    canvasYOffset = int(0 - (cursorPos.y * 0.15))
    canvasYOffset = min(-2, canvasYOffset)
    canvasYOffset = max(H*-0.15 + 2, canvasYOffset)
    canvasYOffset = 0.85 * originalY + 0.15 * canvasYOffset

    canvas.place(x=canvasXOffset, y=canvasYOffset)
    tk.after(1, updateCanvasPos)


def getHwnd():
    progman = win32gui.FindWindow("Progman", "Program Manager")
    a = win32gui.SendMessageTimeout(
        progman, 0x052C, 0, 0, win32con.SMTO_NORMAL, 0x03E8)
    print("a:", a)
    hwnd_workW = None
    while 1:
        hwnd_workW = win32gui.FindWindowEx(None, hwnd_workW, "WorkerW", None)
        if not hwnd_workW:
            continue
        hView = win32gui.FindWindowEx(
            hwnd_workW, None, "SHELLDLL_DefView", None)
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

tk.after(20, updateCanvasPos)
tk.mainloop()
