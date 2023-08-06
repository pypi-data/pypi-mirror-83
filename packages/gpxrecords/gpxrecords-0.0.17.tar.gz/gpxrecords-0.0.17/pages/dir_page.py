#!/usr/bin/python3

from tkinter import ttk
from tkinter.filedialog import *

from components.settings import export_settings
from pages.read_page import ReadPage

#
# First page, dir selection
#


class DirPage:
    def __init__(self, root, settings):

        self.settings = settings
        self.root = root

        main_frame = ttk.Frame(root)
        self.main_frame = main_frame

        Grid.rowconfigure(main_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 0, weight=1)

        dirlist = Listbox(main_frame)
        self.dirlist = dirlist

        for i, track_dir in enumerate(settings.dirs):
            dirlist.insert(i, track_dir)

        dirlist.grid(row=0, column=0, sticky='news')

        button_frame = ttk.Frame(main_frame)
        Grid.rowconfigure(button_frame, 0, weight=1)
        Grid.columnconfigure(button_frame, 0, weight=1)
        Grid.columnconfigure(button_frame, 1, weight=1)
        Grid.columnconfigure(button_frame, 2, weight=1)

        add_button = Button(
            button_frame,
            text="Add",
            command=lambda : self.add_dir()
        )
        add_button.grid(column=0, row=0)

        rm_button = Button(
            button_frame,
            text="Remove",
            command=lambda : self.rm_dir()
        )
        rm_button.grid(column=1, row=0)

        next_button = Button(
            button_frame,
            text="Next",
            command=lambda : self.next()
        )
        next_button.grid(column=2, row=0)
        button_frame.grid(column=0, row=1)

        main_frame.grid(column=0, row=0, sticky='nsew')

    def add_dir(self):
        new_dir = askdirectory(mustexist=True)
        if new_dir:
            self.dirlist.insert(0, new_dir)
            self.settings.dirs.append(new_dir)

    def rm_dir(self):
        for rec in self.dirlist.curselection():
            item = self.dirlist.get(rec)
            self.dirlist.delete(rec)
            self.settings.dirs.remove(item)

    def next(self):
        export_settings(self.settings)
        self.main_frame.destroy()
        ReadPage(self.root, self.settings)
