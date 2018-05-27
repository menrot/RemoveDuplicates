from Tkinter import *
import tkMessageBox
import re


def submitted(event=None):
    test_str = txt.get()
    matchResponse = re.match(regex, test_str, re.IGNORECASE)

    if matchResponse == None:
        Result = 'Fail'
        tkMessageBox.showerror(test_str, "Verification " + Result)
    elif len(test_str) == matchResponse.endpos:
        Result = 'Success'
        tkMessageBox.showinfo(test_str, "Verification " + Result)
    else:
        Result = 'Fail'
        tkMessageBox.showerror(test_str, "Verification " + Result)


def quitted():
    lbl.configure(text="Quitted")
    exit()


def QueryToKeep():
    regex = ur"^([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63})|(\+972 ?[0-9]{9}) | (\+380 ?[0-9]{9}) |((\([0-9]{3}\) *|[0-9]{3} *-? *)[0-9]{3} *-? *[0-9]{4})"

    window = Tk()

    window.bind('<Return>', submitted)

    window.title("Email / Phone")
    window.geometry('500x200')

    lbl = Label(window, text="type Email/Phone:")
    lbl.grid(column=0, row=0)

    txt = Entry(window, width=45)
    txt.grid(column=1, row=1)

    btn = Button(window, text="Submit", command=submitted)
    btn.grid(column=1, row=2)

    btn = Button(window, text="Quit", command=quitted)
    btn.grid(column=2, row=2)

    window.mainloop()
    return





