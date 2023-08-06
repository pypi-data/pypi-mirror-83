#!/usr/bin/python3

from tkinter import *
from tkinter import ttk

import threading

from components.analyzer import process_log, find_best_distances
from pages.records_page import RecordsPage

#
# Records calculation page
#


class CalculatePage:
    def __init__(self, root, settings, ways):
        self.root = root
        self.settings = settings
        self.ways = ways

        main_frame = ttk.Frame(root)
        self.main_frame = main_frame

        Grid.rowconfigure(main_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 0, weight=1)

        text = Text(main_frame)
        self.text = text

        text.grid(column=0, row=0, sticky='nsew')
        main_frame.grid(column=0, row=0, sticky='nsew')

        self.new_text = ""
        self.lock = threading.Lock()

        self.read_thread = threading.Thread(target=self.calc_records)
        self.read_thread.start()

        self.next_tick()

    def calc_records(self):

        with self.lock:
            ways = self.ways.copy()
            settings = self.settings.copy()

        all_records = {}
        tracks = []
        distances = settings.distances
        count = settings.attempts
        threshold = 1 #km/h

        for file, way in ways:
            desc = way[0].time
            with self.lock:
                self.new_text += 'Processing: {}\n'.format(desc)
            date, track = process_log(way)
            tracks.append((date, track))

            records = [find_best_distances(track, x, threshold, date, count) for x in distances]
            all_records[date] = records

        with self.lock:
            self.tracks = tracks
            self.records = all_records

    def next_tick(self):
        with self.lock:
            self.text.insert(INSERT, self.new_text)
            self.new_text = ''

        if self.read_thread.is_alive():
            self.root.after(200, self.next_tick)
        else:
            self.text.insert(INSERT, 'Finished')
            self.main_frame.destroy()
            RecordsPage(self.root, self.settings, self.tracks, self.records)

