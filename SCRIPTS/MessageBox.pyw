from tkinter import Tk, messagebox
from sys import argv

root = Tk()
root.withdraw()

messagebox.showerror(argv[1], argv[2])