from tkinter import *
from tkinter import ttk
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="I have written down the key", command=root.destroy).grid(column=0, row=1)
root.mainloop()

main = Tk()
frm = ttk.Frame(main, padding=25)
frm.grid()
ttk.Label(frm, text="Hello and welcome to Omega Financial Services").grid(column=0, row=0)
ttk.Label(frm, text="A company by RETIS Software Inc").grid(column=0, row=1)
ttk.Label(frm, text="\n").grid(column=0, row=2)
ttk.Label(frm, text="Loading...").grid(column=0, row=3)
main.mainloop()

