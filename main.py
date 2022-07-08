import pyautogui
import tkinter
from PIL import ImageTk, Image

W = 1920
H = 1080

tk = tkinter.Tk()
tk.geometry(f"{W}x{H}")
tk.attributes('-fullscreen', True)

canvasX = int(W*1.15)
canvasY = int(H*1.15)
canvas = tkinter.Canvas(tk, width=canvasX, height=canvasY, bd=-2)
canvas.place(x=0-W*0.115, y=0-H*0.075)

imagePath = "./background.jpg"
originalImage = Image.open(imagePath)
imageX = int(1988*1.15)
imageY = int(1080*1.15)
image = originalImage.resize((imageX, imageY), Image.ANTIALIAS)

img = ImageTk.PhotoImage(image)
canvas.create_image(canvasX/2, canvasY/2, image=img, anchor=tkinter.CENTER)


def updateCanvasPos():
    global canvas
    cursorPos = pyautogui.position()
    canvasXOffset = int(0 - (cursorPos.x * 0.15))
    canvasYOffset = int(0 - (cursorPos.y * 0.15))
    canvasXOffset = min(-2, canvasXOffset)
    canvasXOffset = max(W*-0.15 + 2, canvasXOffset)
    canvasYOffset = min(-2, canvasYOffset)
    canvasYOffset = max(H*-0.15 + 2, canvasYOffset)
    print(canvasXOffset,canvasYOffset)
    canvas.place(x=canvasXOffset, y=canvasYOffset)
    tk.after(1, updateCanvasPos)


tk.after(20, updateCanvasPos)
tk.mainloop()
