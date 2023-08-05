#!/usr/bin/python3

import json
import jsonpickle

from pathlib import Path

data_dir = Path.home() / '.gpx_records'
settings_file = data_dir / 'settings.json'
records_file = data_dir / 'records.txt'


class Settings(object):
    def __init__(self):
        self.dirs = []
        self.tracks = []
        self.distances =[]
        self.attempts = 5

    def copy(self):
        new_settings = Settings()
        new_settings.dirs = self.dirs.copy()
        new_settings.tracks = self.tracks.copy()
        new_settings.distances = self.distances.copy()
        new_settings.attempts = self.attempts

        return new_settings


def import_settings():
    if settings_file.exists() and settings_file.is_file():
        with open(str(settings_file), 'r') as file:
            return jsonpickle.decode(json.load(file))

    data_dir.mkdir(mode=0o777, parents=False, exist_ok=True)
    return Settings()


def export_settings(data):
    with open(str(settings_file), 'w') as file:
        return json.dump(jsonpickle.encode(data), file)


def get_records_file_name():
    return str(records_file)

