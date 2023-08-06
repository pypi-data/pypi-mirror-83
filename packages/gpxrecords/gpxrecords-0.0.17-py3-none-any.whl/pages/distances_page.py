#!/usr/bin/python3

from tkinter import *
from tkinter import ttk

from components.settings import export_settings
from pages.calculate_page import CalculatePage

#
# Distances selection
#


class DistancesPage:
    def __init__(self, root, settings, ways):
        self.root = root
        self.settings = settings
        self.ways = ways

        main_frame = ttk.Frame(root)
        self.main_frame = main_frame

        dist_frame = ttk.Labelframe(main_frame, text='Distances')

        # NOTE!
        # For variable usage class exemplar has to be stored
        # In this case it is captured in Button callback
        # If no capture - class has to be stored by ordinary way
        self.distances = [100, 300, 500, 1000, 1500, 3000, 5000, 10000, 15000, 20000, 40000, 42195]
        self.dist_selections = [BooleanVar(root) for rec in self.distances]

        for i, (v, rec) in enumerate(zip(self.dist_selections, self.distances)):
            v.set(rec in self.settings.distances)
            Checkbutton(
                dist_frame,
                text='{} m'.format(rec),
                variable=v
            ).grid(row=(i%4), column=(i//4))

        dist_frame.grid(row=0, column=0)

        attempts_frame = ttk.Labelframe(main_frame, text="Attempt count")
        self.attempts = StringVar()
        self.attempts.set(str(settings.attempts))
        attempt_box = ttk.Combobox(
            attempts_frame,
            values=[x+1 for x in range(10)],
            state='readonly',
            textvariable=self.attempts
        )

        attempt_box.pack()
        attempts_frame.grid(row=1, column=0, pady=30)

        button = Button(
            main_frame,
            text='Next',
            command=lambda : self.next()
        )

        button.grid(row=2, column=0)
        main_frame.grid(row=0, column=0, sticky='nsew')

    def next(self):
        self.settings.distances = []
        for i, (v, rec) in enumerate(zip(self.dist_selections, self.distances)):
            if v.get():
                self.settings.distances.append(rec)

        self.settings.attempts = int(self.attempts.get())
        export_settings(self.settings)
        self.main_frame.destroy()
        CalculatePage(self.root, self.settings, self.ways)