#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import io

from components.analyzer import get_record_data
from components.settings import get_records_file_name

#
# Records displaying page
#


class Table:
    def __init__(self, columns):
        self.columns = columns
        split_line = ''

        for col in columns:
            split_line += '+'
            split_line += '-' * (len(col) + 2)

        split_line += '+'
        self.split_line = split_line

    def show_title(self, fl, title):
        l = len(self.split_line) - 2
        print('+{}+'.format('-' * l), file=fl)
        l1 = l - len(title)
        l2 = l1 // 2
        print('|{}|'.format(' ' * l), file=fl)
        print('|{}{}{}|'.format(' ' * l2, title, ' ' * (l1 - l2)), file=fl)
        print('|{}|'.format(' ' * l), file=fl)

    def show_header(self, fl):
        print(self.split_line, file=fl)
        for col in self.columns:
            print('| {} '.format(col), file=fl, end='')

        print('|', file=fl)
        print(self.split_line, file=fl)

    def show_line(self, fl, values):
        l = 0
        for val, col in zip(values, self.columns):
            val = str(val)
            print('| {} '.format(val), file=fl, end='')
            if len(col) > len(val):
                print(' ' * (len(col) - len(val)), file=fl, end='')
        print('|', file=fl)

    def end_line(self, fl):
        print(self.split_line, file=fl)


class RecordsPage:
    def __init__(self, root, settings, tracks, records):
        self.root = root
        self.settings = settings
        self.tracks = tracks
        self.records = records

        main_frame = ttk.Frame(root)

        text = Text(main_frame)
        self.text = text

        text.grid(row=0, column=0, sticky='nsew')

        scroller = Scrollbar(main_frame, command=self.text.yview)
        scroller.grid(row=0, column=1, sticky='nsew')
        self.text['yscrollcommand'] = scroller.set

        Grid.rowconfigure(main_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 0, weight=1)

        main_frame.grid(sticky='nsew')
        self.show_records()


    def show_records(self):
        record_text = ''
        dates = [*self.records.keys()]
        dates = sorted(dates);

        distances = self.settings.distances
        distances = sorted(distances)

        all_records = self.records
        count = self.settings.attempts

        max_records = {x: [] for x in distances}
        zs_records = {x: [] for x in distances}

        record_text = ''

        record_table = Table(
            ('Distance, m', '  Time, s  ', 'Avg. speed, km/h',
             'Time from start', 'Dist from start', 'Act.distance')
        )

        abs_record_table = Table(
            ('Distance, m', '  Time, s  ', 'Avg. speed, km/h',
             'Time from start', 'Dist from start', 'Act.distance',
             '          Date          ')
        )

        with io.StringIO() as fl:
            for date in dates:
                record_table.show_title(
                    fl,
                    'Time and date: {}'.format(date)
                )
                record_table.show_header(fl)
                for (dist, rec) in zip(distances, all_records[date]):
                    records = rec[0]
                    max_records[dist] += records
                    for time in records:
                        record_table.show_line(fl, get_record_data(dist, time, False, time.timestamp))

                    records = rec[1]
                    zs_records[dist] += records
                    for time in records:
                        record_table.show_line(fl, get_record_data(dist, time, True, time.timestamp))

                    if rec[0] or rec[1]:
                        record_table.end_line(fl)

                print('', file=fl)

            abs_record_table.show_title(
                fl,
                'Absolute records'
            )
            abs_record_table.show_header(fl)
            for dist in distances:
                records = sorted(max_records[dist], key=lambda x: x.time)
                for time in records[:count]:
                    abs_record_table.show_line(fl, get_record_data(dist, time, False, time.timestamp))

                records1 = sorted(zs_records[dist], key=lambda x: x.time)
                for time in records1[:count]:
                    abs_record_table.show_line(fl, get_record_data(dist, time, True, time.timestamp))

                if records or records1:
                    abs_record_table.end_line(fl)

            record_text = fl.getvalue()

        self.text.insert(END, record_text)
        # self.text.config(state=DISABLED)

        with open(get_records_file_name(), 'w') as fl:
            fl.write(record_text)

    def show_tracks(self):

        tracks = self.tracks

        for date, _ in tracks:
            self.track_listbox.insert(END, date)

