from Tkinter import *

class Result:
    def __init__(self, a):
        self.a = a


def QueryToKeep(ListOfFolders):

    selectedResult = Result(-1)

    def submitted(event=None):

        selectedResult.a = selected.get()

        window.destroy()
        return selectedResult


    def quitted():
        lbl.configure(text="Quitted")
        selectedResult.a = -1
        window.destroy()



    window = Tk()

    window.bind('<Return>', submitted)

    window.title("Folder to keep")
    window.geometry('500x200')

    lbl = Label(window, text="Select folder to keep")
    lbl.grid(column=0, row=0)

    btn = Button(window, text="Submit", command=submitted)
    btn.grid(column=1, row=4)

    btn = Button(window, text="Quit", command=quitted)
    btn.grid(column=2, row=4)

    selected = IntVar()

    rad1 = Radiobutton(window, text=ListOfFolders[0], value=1, variable=selected)

    if len(ListOfFolders)>=2:
        rad2 = Radiobutton(window, text=ListOfFolders[1], value=2, variable=selected)

    if len(ListOfFolders)==3:
        rad3 = Radiobutton(window, text=ListOfFolders[2], value=3, variable=selected)

    rad1.grid(column=0, row=1)

    rad2.grid(column=0, row=2)

    rad3.grid(column=0, row=3)

    window.mainloop()

    return (selectedResult)







