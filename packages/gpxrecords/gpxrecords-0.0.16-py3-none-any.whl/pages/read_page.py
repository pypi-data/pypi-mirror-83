#!/usr/bin/python3

from tkinter import *
from tkinter import ttk

import glob
import threading

from components.analyzer import parse_multi_log
from pages.tracks_page import TracksPage

#
# Second page - read files
#


class ReadPage:
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings

        main_frame = ttk.Frame(root)
        self.main_frame = main_frame

        Grid.rowconfigure(main_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 0, weight=1)

        text = Text(main_frame)
        self.text = text

        text.grid(column=0, row=0, sticky='nsew')
        main_frame.grid(column=0, row=0, sticky='nsew')

        files = []

        for dirname in settings.dirs:
            files += glob.glob(dirname + '/*.gpx')

        if not files:
            text.insert(INSERT, 'Files not found')
            return

        self.files = files
        self.ways = []
        self.new_text = ""
        self.lock = threading.Lock()

        self.read_thread = threading.Thread(target=self.read_files)
        self.read_thread.start()

        self.next_tick()

    def read_files(self):
        ways = []
        with self.lock:
            files = self.files.copy()

        for file in files:
            with self.lock:
                self.new_text += 'Processing: {}\n'.format(file)
            new_ways = parse_multi_log(file)
            new_ways = [(file, x) for x in new_ways]
            with self.lock:
                self.ways += new_ways

        with self.lock:
            self.ways = sorted(self.ways, key=lambda x : x[1][0].time)

    def next_tick(self):
        with self.lock:
            self.text.insert(INSERT, self.new_text)
            self.new_text = ''

        if self.read_thread.is_alive():
            self.root.after(200, self.next_tick)
        else:
            self.text.insert(INSERT, 'Finished')
            self.main_frame.destroy()
            TracksPage(self.root, self.settings, self.ways)
