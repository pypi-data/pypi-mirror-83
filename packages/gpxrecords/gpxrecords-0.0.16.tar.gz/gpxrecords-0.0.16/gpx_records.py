#!/usr/bin/python3


from tkinter.filedialog import *
from tkinter import ttk

from components.settings import import_settings

from pages.dir_page import DirPage


def convert_gui():
    settings = import_settings()

    root = Tk()
    root.title('GPX files analysis')
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)

    DirPage(root, settings)
    root.mainloop()

#
# Start
#

if __name__ == '__main__':
    convert_gui()
