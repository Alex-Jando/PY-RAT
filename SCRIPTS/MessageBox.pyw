from tkinter import Tk, messagebox
from sys import argv

root = Tk()
root.withdraw()

TITLE = ''
MSG = ''

try:
    messagebox.showerror(argv[1], argv[2])
except:
    messagebox.showerror(TITLE, MSG)
