import Tkinter as tk
from Tkinter import *

class Color:
    def __init__(self, r):
        self.r = r

def requestColor():

    # this will be modified later by the save command
    result = Color(0)

    colorGUI = tk.Tk()
    colorGUI.title('Select Color')

    rLabel = Label(colorGUI, text='R: ', anchor=tk.E)
    gLabel = Label(colorGUI, text='G: ', anchor=tk.E)
    bLabel = Label(colorGUI, text='B: ', anchor=tk.E)

    rEntry = Entry(colorGUI)
    gEntry = Entry(colorGUI)
    bEntry = Entry(colorGUI)

    def saveCommand():
        # set the new values
        result.r = int(rEntry.get())
        colorGUI.destroy()

    def quitCommand():
        # keep the default values
        colorGUI.destroy()

    saveButton = Button(colorGUI, text='SAVE', command=saveCommand)
    quitButton = Button(colorGUI, text='CANCEL', command=quitCommand)

    rEntry.insert(0, 0)

    rLabel.grid(row=0, column=0, sticky=tk.E)
    rEntry.grid(row=0, column=1)
    gLabel.grid(row=1, column=0, sticky=tk.E)
    gEntry.grid(row=1, column=1)
    bLabel.grid(row=2, column=0, sticky=tk.E)
    bEntry.grid(row=2, column=1)
    quitButton.grid(row=3, column=0, sticky=tk.E+tk.W)
    saveButton.grid(row=3, column=1, sticky=tk.E+tk.W)

    colorGUI.mainloop()

    return result

color = requestColor()


print('Color(%s)' % color.r)