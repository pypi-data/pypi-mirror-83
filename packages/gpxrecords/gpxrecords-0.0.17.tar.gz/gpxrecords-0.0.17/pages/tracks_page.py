#!/usr/bin/python3

from tkinter import *
from tkinter import ttk

from components.analyzer import parse_time
from components.settings import export_settings

from pages.distances_page import DistancesPage

#
# Tracks selection
#


class TracksPage:
    def __init__(self, root, settings, ways):
        self.root = root
        self.settings = settings

        main_frame = ttk.Frame(root)
        self.main_frame = main_frame

        Grid.rowconfigure(main_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 2, weight=1)

        left_frame = Frame(main_frame)
        right_frame = Frame(main_frame)
        Grid.rowconfigure(left_frame, 0, weight=1)
        Grid.columnconfigure(left_frame, 0, weight=1)
        Grid.rowconfigure(right_frame, 0, weight=1)
        Grid.columnconfigure(right_frame, 0, weight=1)

        self.left_box = Listbox(left_frame, selectmode=EXTENDED)
        self.right_box = Listbox(right_frame, selectmode=EXTENDED)

        left_scroller = Scrollbar(left_frame, command=self.left_box.yview)
        self.left_box['yscrollcommand'] = left_scroller.set
        right_scroller = Scrollbar(right_frame, command=self.right_box.yview)
        self.right_box['yscrollcommand'] = right_scroller.set

        self.ways = {}
        self.way_list = []

        for way in ways:
            description = self.make_track_description(way)
            self.ways[description[1]] = (description[0], way)
            self.way_list.append(description)

        self.add_list_items()

        self.left_box.grid(column=0, row=0, sticky='nsew')
        left_scroller.grid(column=1, row=0, sticky='nsew')

        self.right_box.grid(column=0, row=0, sticky='nsew')
        right_scroller.grid(column=1, row=0, sticky='nsew')

        left_frame.grid(column=0, row=0, sticky='nsew')
        right_frame.grid(column=2, row=0, sticky='nsew')

        middle_frame = ttk.Frame(main_frame)

        right_button = Button(
            middle_frame,
            text=">>>",
            command=lambda : self.add_right()
        )
        right_button.pack()

        left_button = Button(
            middle_frame,
            text="<<<",
            command=lambda : self.add_left()
        )
        left_button.pack()

        done_button = Button(
            middle_frame,
            text="Next",
            command=lambda : self.next()
        )
        done_button.pack(pady=30)

        middle_frame.grid(column=1, row=0)
        main_frame.grid(column=0, row=0, sticky='nsew')

    def make_track_description(self, way):
        start_element = way[1][0]
        end_element = way[1][-1]
        start_time = parse_time(start_element.time)
        end_time = parse_time(end_element.time)

        return start_element.time, "{}, {} points, {} seconds".format(
            start_element.time,
            len(way[1]),
            (end_time - start_time).total_seconds()
        )

    def add_list_items(self):
        for desc in self.way_list:
            if desc[0] in self.settings.tracks:
                self.right_box.insert(END, desc[1])
            else:
                self.left_box.insert(END, desc[1])

    def add_right(self):
        for rec in self.left_box.curselection():
            self.settings.tracks.append(
                self.ways[self.left_box.get(rec)][0]
            )

        self.left_box.delete(0, END)
        self.right_box.delete(0, END)
        self.add_list_items()

    def add_left(self):
        for rec in self.right_box.curselection():
            self.settings.tracks.remove(
                self.ways[self.right_box.get(rec)][0]
            )

        self.left_box.delete(0, END)
        self.right_box.delete(0, END)
        self.add_list_items()

    def next(self):
        export_settings(self.settings)
        ways = []
        for rec in self.right_box.get(0, END):
            ways.append(
                self.ways[rec][1]
            )
        self.main_frame.destroy()
        DistancesPage(self.root, self.settings, ways)
