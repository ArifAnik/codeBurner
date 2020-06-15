#!/usr/bin/env python3
import subprocess
from tkinter import *
from tkinter import filedialog
from pathlib import Path


def openfile():
    e.delete(0, END)
    global fileName
    global pathName

    if choice.get() == 1:
        fileName = filedialog.askopenfilename(initialdir='/home/anik/Desktop/pyCharm', title="select file", filetypes=(('file', '*.c'), ('all files', '*.*')))
    else:
        fileName = filedialog.askopenfilename(initialdir='/home/anik/Desktop/pyCharm', title="select file", filetypes=(('file', '*.hex'), ('all files', '*.*')))

    e.insert(0, fileName)

    pathName = str(Path(fileName).parent)


def upload():
    if choice.get() == 1:
        makeBinary = "avr-gcc -Wall -g -Os -mmcu=atmega8 -o " + pathName + "/main.bin " + fileName
        output = subprocess.run(makeBinary.split(), capture_output=True, text=True)
        if output.returncode == 0:
            myLabel = Label(myFrame, text="Successfully compiled to Binary file")
            myLabel.pack()
        else:
            myLabel = Label(myFrame, text=output.stderr)
            myLabel.pack()

        makeHex = "avr-objcopy -j .text -j .data -O ihex " + pathName + "/main.bin " + pathName + "/main.hex"
        output = subprocess.run(makeHex.split(), capture_output=True, text=True)
        if output.returncode == 0:
            myLabel = Label(myFrame, text="Successfully converted to Hex file")
            myLabel.pack()
        else:
            myLabel = Label(myFrame, text=output.stderr)
            myLabel.pack()

        uploadHex = "avrdude -p m8 -c usbasp -U flash:w:" + pathName + "/main.hex:i -F -P usb"
        output = subprocess.run(uploadHex.split(), capture_output=True, text=True)
        if output.returncode == 0:
            myLabel = Label(myFrame, text="Successfully uploaded!!")
            myLabel.pack()
        else:
            myLabel = Label(myFrame, text=output.stderr)

    else:
        uploadHex = "avrdude -p m8 -c usbasp -U flash:w:" + pathName + "/main.hex:i -F -P usb"
        output = subprocess.run(uploadHex.split(), capture_output=True, text=True)
        if output.returncode == 0:
            myLabel = Label(myFrame, text="Successfully uploaded!!")
            myLabel.pack()
        else:
            myLabel = Label(myFrame, text=output.stderr)


root = Tk()
root.title("Lets BURN it!!!")
root.geometry('600x600')

e = Entry(root)
e.place(relwidth=0.6, relheight=0.05, rely=0.01, relx=0.2)

pathLabel = Label(root, text='Path:')
pathLabel.place(relwidth=0.1, relheight=0.06, rely=0.01, relx=0.1)

myFrame = Frame(root, bg='#ffffff', highlightbackground="grey", highlightcolor="grey", highlightthickness=2)
myFrame.place(relwidth=0.8, relheight=0.65, relx=0.1, rely=0.1)


burnText = """ 
  Burn
    &
                  Pray!                
"""
burnButton = Button(root, text=burnText, bg='#A2B5CD', command=upload, highlightbackground="grey", highlightcolor="grey", highlightthickness=4)
burnButton.place(relwidth=0.13, relheight=0.13, rely=0.85, relx=0.8)

openButton = Button(root, text="Open File", bg='#A2B5CD', command=openfile)
openButton.place(relwidth=0.15, relheight=0.05, rely=0.01, relx=0.8)


choice = IntVar()
choice.set("1")
choiceLabel = Label(root, text="Choose:", )
choiceLabel.place(relwidth=0.1, relheight=0.06, rely=0.75, relx=0.1)
compileUpload = Radiobutton(root, text="Compile & Upload (*.c file)", variable=choice, value=1)
justUpload = Radiobutton(root, text="Just upload(*.hex file)", variable=choice, value=2)
compileUpload.place(relx=0.2, rely=0.76)
justUpload.place(relx=0.55, rely=0.76)


root.mainloop()