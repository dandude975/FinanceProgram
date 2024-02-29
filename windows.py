import tkinter as tk
from tkinter import *
from tkinter import ttk
import time

window = Tk()
window.title("Omega Financial Services")
frm = ttk.Frame(window, padding=25)
frm.grid()
introA = tk.Label(frm, text="Hello and welcome to Omega Financial Services").grid(column=0, row=0)
intorB = tk.Label(frm, text="A company by RETIS Software Inc").grid(column=0, row=1)
space = tk.Label(frm, text="\n").grid(column=0, row=2)
continue_ = tk.Label(frm, text="Press any key to continue").grid(column=0, row=3)

# Create an event handler
def handle_keypress(event):
    continue_.destroy()
    introA = tk.Label(frm, text="Hello and welcome to Omega Financial Services").grid(column=0, row=0)
    intorB = tk.Label(frm, text="A company by RETIS Software Inc").grid(column=0, row=1)
    space = tk.Label(frm, text="\n").grid(column=0, row=2)
    loading = tk.Label(frm, text="Loading...").grid(column=0, row=3)
    time.sleep(5)

window.bind("<Key>", handle_keypress)
window.bind("<Return>", handle_keypress)

window.mainloop()