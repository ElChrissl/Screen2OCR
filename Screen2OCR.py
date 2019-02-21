import tkinter as tk
import subprocess
from PIL import Image, ImageTk
from PIL import ImageGrab
import pytesseract
import pyperclip
import win32clipboard
from io import BytesIO
from time import sleep

# ---------------------------------------------------------------------------------------------------Mainwindow

# Initialisiere Mainwindow
screen2ocr = tk.Tk()
screen2ocr.title("Screen2OCR")
screen2ocr.geometry("400x200")
screen2ocr.iconbitmap(".\logo.ico")
screen2ocr.resizable(0, 0)

# ---------------------------------------------------------------------------------------------------Screenshot

# Screenshot-Funktion
def screenshot ():
    shot = tk.Tk()
    shot.title("  ")
    shot.iconbitmap()
    shot.attributes('-fullscreen', True)
    shot.attributes("-alpha", 0.3)
    shot.configure(background="black")
    shot.after(1, lambda: shot.focus_force())

    def cancelshot(event):
        shot.destroy()
    shot.bind("q", cancelshot)
    shot.bind("Q", cancelshot)
    shot["cursor"] = "crosshair"


    def clickstart(event):
        global x1, y1
        global w
        x1 = event.x
        y1 = event.y

    def mousemove(event):
        global x3, y3
        global canvas_width, canvas_height
        global w
        x3 = event.x
        y3 = event.y
        canvas_width = (x3 - x1)
        canvas_height = (y3 - y1)
        u1 = shot.winfo_screenwidth() + 10
        v1 = shot.winfo_screenheight() + 10
        w = tk.Canvas(master=shot, width=u1, height=v1, background="black")
        w.place(x="-5", y="-5")
        w = tk.Canvas(master=shot, width=canvas_width, height=canvas_height, background="white")
        w.place(x=x1, y=y1)




    def clickend(event):
        global x1, y1
        global x2, y2
        global x3, y3
        x2 = event.x
        y2 = event.y
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('.\images\capture.png')
        x1, y1 = None, None
        x2, y2 = None, None
        x3, y3 = None, None
        shot.destroy()


    shot.bind("<Button-1>", clickstart)
    shot.bind("<Motion>", mousemove)
    shot.bind("<ButtonRelease-1>", clickend)
    shot.mainloop()

# ---------------------------------------------------------------------------------------------------OCR



# OCR-Funktion
def ocr():
    global german, english
    pytesseract.pytesseract.tesseract_cmd = r".\Tesseract-OCR\tesseract.exe"
    imgpath = Image.open(".\images\capture.png")
    if german == 1:
        text = pytesseract.image_to_string(imgpath, lang="deu")
    elif english == 1:
        text = pytesseract.image_to_string(imgpath, lang="eng")
    elif german == 1 and english == 1:
        text = pytesseract.image_to_string(imgpath, lang="deu+eng")
    else:
        text = pytesseract.image_to_string(imgpath, lang="deu")
    pyperclip.copy(text)

# ---------------------------------------------------------------------------------------------------Image2Clipboard

def image2clipboard():
    def send_to_clipboard(clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()
    filepath = '.\images\capture.png'
    image = Image.open(filepath)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)

# ---------------------------------------------------------------------------------------------------Dropdownmenü-Def


# Funktionen des Dropdown Menüs
def restart():
    subprocess.Popen('Screen2OCR.exe')
    screen2ocr.after(1000, screen2ocr.destroy)
def ende1():
    screen2ocr.destroy()
def ende2(event):
    screen2ocr.destroy()



# Shortcuts
screen2ocr.bind("<Escape>", ende2)


# DropdownMenü About - Erweiterte Informationen
def createaboutwindow():
    aboutwindow = tk.Toplevel(screen2ocr)
    aboutwindow.geometry("400x180")
    aboutwindow.title("About")
    aboutwindow.iconbitmap(".\logo.ico")
    textinabout = tk.Label(aboutwindow, text=("Erstellt von Christoph Grammenidis\nVersion 1.81   "
                                              "13/12/2018\n\nIt's free, no problem!"))
    textinabout.place(y=5, x=180)
    aboutlogo = ImageTk.PhotoImage(Image.open("./logo.jpg"))
    logo_image = tk.Label(master=aboutwindow, image=aboutlogo)
    logo_image.image = aboutlogo
    logo_image.place(y=5, x=5)

# ---------------------------------------------------------------------------------------------------Dropdown-Layout

# Menübar / DropdownMenü
menubar = tk.Menu(master=screen2ocr)
filemenu = tk.Menu(master=screen2ocr, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
languagemenu = tk.Menu(master=screen2ocr, tearoff=0)
filemenu.add_cascade(label="Language for OCR", menu=languagemenu)
german = 1
english = 0
languagemenu.add_checkbutton(label="German", variable=german, onvalue=1)
languagemenu.add_checkbutton(label="English", variable=english, onvalue=1)
filemenu.add_command(label="Restart", command=restart)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=ende1)
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=createaboutwindow)
menubar.add_cascade(label="Help", menu=helpmenu)
screen2ocr.config(menu=menubar)

# ---------------------------------------------------------------------------------------------------Buttons

# Buttons
shotbutton = tk.Button(master=screen2ocr, text="Take a screenshot", command=screenshot, bg="white")
shotbutton.place(x=20, y=20, height=50, width=150)
shotlabel = tk.Label(master=screen2ocr, text="Press Q to cancel...")
shotlabel.place(x=20, y=80, width=150, height=50)
shot2clipboardbutton = tk.Button(master=screen2ocr, text="Copy image to clipboard", command=image2clipboard, bg="white")
shot2clipboardbutton.place(x=230, y=80, width=150, height=50)

ocrbutton = tk.Button(master=screen2ocr, text="OCR your screenshot", command=ocr, bg="white")
ocrbutton.place(x=230, y=20, height=50, width=150)

# ---------------------------------------------------------------------------------------------------

# Window soll dauerhaft aktiv sein
screen2ocr.mainloop()