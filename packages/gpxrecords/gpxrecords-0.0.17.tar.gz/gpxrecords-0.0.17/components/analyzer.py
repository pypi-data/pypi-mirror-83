#!/usr/bin/python3

import numpy as np
import xml.etree.ElementTree as etree
from datetime import datetime


class WayElement:
    ele = 0
    time = ''
    lon = 0
    lat = 0

    def __init__(self, trkpt_record):
        self.lon = float(trkpt_record.attrib['lon'])
        self.lat = float(trkpt_record.attrib['lat'])
        self.time = trkpt_record.find('{http://www.topografix.com/GPX/1/1}time').text
        self.ele = float(trkpt_record.find('{http://www.topografix.com/GPX/1/1}ele').text)

    def __repr__(self):
        return "Time: {0}, Ele: {1}, Lon: {2}, Lat: {3}".format(self.time, self.ele, self.lon, self.lat)


class DistElement:
    time = 0
    dist = 0
    total_dist = 0
    speed = 0 #in km/h

    def __init__(self, t, d, s):
        self.time = t
        self.dist = d
        self.speed = s

    def __repr__(self):
        return "Time: {0}, Distance: {1}, Speed: {2}".format(self.time, self.dist, self.speed)

class RecordElement:
    total_time = 0
    total_distance = 0
    time = 0
    distance = 0
    timestamp = '',

    def __init__(self, tt, td, t, d, ts):
        self.total_time = tt
        self.total_distance = td
        self.time = t
        self.distance = d
        self.timestamp = ts
        
    def __repr__(self):
        return 'TT: {0}, TD: {1}, T: {2},'\
               ' D: {3}, S: {4}, DM: {5},'\
               ' TS: {6}'\
            .format(
                self.total_time,
                self.total_distance,
                self.time,
                self.distance,
                self.speed,
                self.damaged,
                self.timestamp)

    def intersects(self, other):
        start_time1 = self.total_time
        start_time2 = other.total_time
        end_time1 = start_time1 + self.time
        end_time2 = start_time2 + other.time

        if end_time1 <= start_time2 or end_time2 <= start_time1:
            return False
        
        return True

        
def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res * 1000, 1)


def parse_time(time_record):
    year = int(time_record[:4])
    month = int(time_record[5:7])
    day = int(time_record[8:10])
    hour = int(time_record[11:13])
    minutes = int(time_record[14:16])
    seconds = int(time_record[17:19])
    return datetime(year, month, day, hour, minutes, seconds, 0)


def parse_multi_log(file_name):
    root = etree.parse(file_name).getroot()
    tracks = root.findall('{http://www.topografix.com/GPX/1/1}trk')

    ways = []
    for track in tracks:
        track_points = track.find('{http://www.topografix.com/GPX/1/1}trkseg')
        way = []
        for rec in track_points:
            way += [WayElement(rec)]

        ways += [way]

    return ways


def show_record(dist, rec, fl, zs):
    record = '    {0}m {1}: time = {2}:{3:02}s, avg.speed = {4:.3}km/h,'\
             ' time from start = {5}:{6:02}, dist from start = {7},'\
             ' actual distance = {8}m'\
        .format(
            dist,
            'zs' if zs else '  ',
            int(rec.time / 60),
            int((rec.time * 10) % 600 + .5) / 10,
            dist / rec.time * 3.6,
            int(rec.total_time / 60),
            int(rec.total_time % 60),
            int(rec.total_distance),
            int(rec.distance))

    print(record, file=fl)


def show_abs_record(dist, rec, fl, zs, date):
    record = '    {0}m {1}: time = {2}:{3:02}s, avg.speed = {4:.3}km/h,'\
             ' time from start = {5}:{6:02}, dist from start = {7},'\
             ' actual distance = {8}m, date= {9}'\
        .format(
            dist,
            'zs' if zs else '  ',
            int(rec.time / 60),
            int((rec.time * 10) % 600 + .5) / 10,
            dist / rec.time * 3.6,
            int(rec.total_time / 60),
            int(rec.total_time % 60),
            int(rec.total_distance),
            int(rec.distance),
            date)

    print(record, file=fl)


def seconds_to_string(sec):
    return '{0:02}:{1:02}'.format(
        int(sec/60),
        int((sec * 10) % 600 + .5) / 10
    )


def get_record_data(dist, rec, zs, date=''):
    return (
        '{}{}'.format(dist, 'zs' if zs else ''),
        seconds_to_string(rec.time),
        '{:.3}'.format(dist / rec.time * 3.6),
        seconds_to_string(rec.total_time),
        int(rec.total_distance),
        int(rec.distance),
        date
    )
    

def find_all_distances(route, distance, timestamp):
    distances = []
    damaged_ctr = 0
    prev = route[0]
    first = 0

    for rec in route[1:]:

        first_rec = route[first]
        dist1 = route[first].dist
        dist2 = rec.dist
        while (dist2 - dist1) > distance:
            distances += [
                RecordElement(
                    first_rec.time,
                    dist1,
                    (rec.time - first_rec.time) * distance / (dist2 - dist1),
                    dist2 - dist1,
                    timestamp)]
            first += 1
            first_rec = route[first]              
            if damaged_ctr > 0:
                damaged_ctr -= 1
            dist1 = first_rec.dist
            dist2 = rec.dist

        prev = rec

    return distances


def find_zero_distances(route, distance, threshold, timestamp):
    distances = []
    prev = route[0]

    for i, rec in enumerate(route):
        if prev.speed < threshold <= rec.speed :
            first = prev

            j = i
            sec = route[j]

            while (sec.dist - first.dist) < distance and j < (len(route) - 1):
                j += 1
                sec = route[j]

            if (sec.dist - first.dist) >= distance:
                distances += [
                    RecordElement(
                        first.time,
                        first.dist,
                        (sec.time - first.time) * distance / (sec.dist - first.dist),
                        sec.dist - first.dist,
                        timestamp)]
        prev = rec

    return distances


def find_best_distances(route, distance, threshold, timestamp, count):

    distances = find_all_distances(route, distance, timestamp)
    zero_distances = find_zero_distances(route, distance, threshold, timestamp)

    distances = sorted(distances, key=lambda x : x.time)
    zero_distances = sorted(zero_distances, key=lambda x : x.time)

    max_distances = []
    for rec in distances:
        intersects = False
        for mrec in max_distances:
            intersects = intersects or mrec.intersects(rec)

        if not intersects:
            max_distances += [rec]
            if len(max_distances) >= count:
                break

    return max_distances[:count], zero_distances[:count]

    
def process_log(way):
    prev = way[0]
    route = [DistElement(0, 0, 0)]

    total_dist = 0
    start_time = parse_time(way[0].time)
    prev_time = start_time
    
    for rec in way[1:]:
        dist = haversine_distance(rec.lat, rec.lon, prev.lat, prev.lon)
        total_dist += dist
        rec_time = parse_time(rec.time)
        time = (rec_time - start_time).total_seconds()
        dtime = (rec_time - prev_time).total_seconds()
        
        speed = -1
        
        if dtime > 0:
            speed = dist / dtime * 3.6
            
        route += [DistElement(time, total_dist, speed)]
        prev = rec
        prev_time = rec_time
        
    return way[0].time, route
