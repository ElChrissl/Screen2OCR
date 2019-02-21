import tkinter as tk
import subprocess
from PIL import Image, ImageTk
from PIL import ImageGrab
import pytesseract
import pyperclip
import numpy as np
import cv2

# ---------------------------------------------------------------------------------------------------Mainwindow

# Initialisiere Mainwindow
screen2ocr = tk.Tk()
screen2ocr.title("Screen2OCR")
screen2ocr.geometry("400x200")
screen2ocr.iconbitmap(".\logo.ico")
screen2ocr.resizable(0, 0)

# ---------------------------------------------------------------------------------------------------Screenshot

#Screenshot-Funktion
def screenshot ():
    shot = tk.Tk()
    shot.title("  ")
    shot.iconbitmap()
    shot.attributes('-fullscreen', True)
    shot.attributes("-alpha", 0.3)
    shot.after(1, lambda: shot.focus_force())
    def cancelshot(event):
        shot.destroy()
    shot.bind("q", cancelshot)
    shot.bind("Q", cancelshot)
    shot["cursor"] = "crosshair"

    def clickstart(event):
        global x1, y1
        x1 = event.x
        y1 = event.y
        shot.bind("<Motion>", mousemove)

    def mousemove(event):
        global x3, y3
        x3 = event.x
        y3 = event.y
        while cv2.setMouseCallback(shot, onMouse=True):
            cv2.rectangle(x1,y1,x3,y3)

    def clickend(event):
        global x2, y2
        x2 = event.x
        y2 = event.y
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('.\images\capture.png')
        shot.destroy()


    shot.bind("<Button-1>", clickstart)
    shot.bind("<ButtonRelease-1>", clickend)
    shot.mainloop()

# ---------------------------------------------------------------------------------------------------OCR

#OCR-Funktion
def ocr ():
    pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe'
    imgpath = Image.open('.\images\capture.png')
    text= pytesseract.image_to_string(imgpath, lang="deu+eng")
    pyperclip.copy (text)

# ---------------------------------------------------------------------------------------------------Dropdownmenü-Def

# Funktionen des Dropdown Menüs
def restart():
    subprocess.Popen('Screen2OCR.exe')
    screen2ocr.after(1000, screen2ocr.destroy)

def ende(event):
    screen2ocr.destroy()


# "Escape" beendet das Programm
screen2ocr.bind("<Escape>", ende)


# DropdownMenü About - Erweiterte Informationen
def createaboutwindow():
    aboutwindow = tk.Toplevel(screen2ocr)
    aboutwindow.geometry("400x180")
    aboutwindow.title("About")
    aboutwindow.iconbitmap(".\logo.ico")
    textinabout = tk.Label(aboutwindow,
                           text="Erstellt von Christoph Grammenidis\nVersion 1.01   13/12/2018\n\nIt's free, no problem!")
    textinabout.place(y=5, x=180)
    aboutlogo = ImageTk.PhotoImage(Image.open("./logo.jpg"))
    logo_image = tk.Label(master=aboutwindow, image=aboutlogo)
    logo_image.image = aboutlogo
    logo_image.place(y=5, x=5)

# ---------------------------------------------------------------------------------------------------Dropdown-Layout

# Menübar / DropdownMenü
menubar = tk.Menu(screen2ocr)
filemenu = tk.Menu(master=screen2ocr, tearoff=0)
filemenu.add_command(label="Settings")
filemenu.add_command(label="Restart", command=restart)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=ende)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=createaboutwindow)
menubar.add_cascade(label="Help", menu=helpmenu)
screen2ocr.config(menu=menubar)

# ---------------------------------------------------------------------------------------------------Buttons

# Buttons
shotbutton = tk.Button (master=screen2ocr, text= "Take a screenshot!",command= screenshot, bg="white")
shotbutton.place(x= 20,y= 20, height=50, width= 150)
shotlabel = tk.Label(master= screen2ocr, text= "Press Q to cancel...")
shotlabel.place(x= 20, y=80, width= 150, height= 50)

ocrbutton = tk.Button (master=screen2ocr, text= "OCR your screenshot!",command= ocr, bg="white")
ocrbutton.place(x= 230,y= 20, height=50, width= 150)

# ---------------------------------------------------------------------------------------------------

# Window soll dauerhaft aktiv sein
screen2ocr.mainloop()