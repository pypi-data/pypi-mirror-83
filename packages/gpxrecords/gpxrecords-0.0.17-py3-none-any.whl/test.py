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


def import_settings(file_name):
    with open(file_name, 'r') as file:
        return jsonpickle.decode(json.load(file))

settings1 = import_settings('settings.json')
settings2 = import_settings(settings_file.name)
settings3 = import_settings('/home/n/.gpx_records/settings.json')
