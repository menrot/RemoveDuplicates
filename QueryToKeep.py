from Tkinter import *

class Result:
    def __init__(self, a):
        self.selected = a


def QueryToKeep(ListOfFolders):

    selectedResult = Result(-1)

    def submitted(event=None):

        selectedResult.selected = selected.get()
        window.destroy()
        return selectedResult


    def quitted():
        lbl.configure(text="Quitted")
        selectedResult.selected = -1
        window.destroy()



    window = Tk()

    window.bind('<Return>', submitted)

    window.title("Folder to keep")
    window.geometry('700x200')

    lbl = Label(window, text="Select folder to keep")
    lbl.grid(column=0, row=0)

    btn = Button(window, text="Submit", command=submitted)
    btn.grid(column=0, row=4)

    btn = Button(window, text="Quit", command=quitted)
    btn.grid(column=1, row=4)

    selected = IntVar()

    rad1 = Radiobutton(window, text=ListOfFolders[0], value=1, variable=selected)
    rad1.grid(column=0, row=1, sticky=W)

    if len(ListOfFolders) >= 2:
        rad2 = Radiobutton(window, text=ListOfFolders[1], value=2, variable=selected)
        rad2.grid(column=0, row=2, sticky=W)

    if len(ListOfFolders) == 3:
        rad3 = Radiobutton(window, text=ListOfFolders[2], value=3, variable=selected)
        rad3.grid(column=0, row=3, sticky=W)



    window.mainloop()

    return (selectedResult.selected)







