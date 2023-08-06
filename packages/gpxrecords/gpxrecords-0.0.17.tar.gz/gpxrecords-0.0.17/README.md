### About program

Easy way to process a bunch of .gpx logs to get best times on selected distances.

### Installation

Python3 is required. Download latest version for your OS from https://www.python.org/downloads/ and install it.

After that, open console (for Windows users, it can be found in Accessories folder of the Start Menu) or terminal (for Linux users).

Execute following commands:

    pip3 install setuptools
	pip3 install gpxrecords

### Usage

Open console (or terminal) and execute:

    gpx-records

Several windows will be appeared in the following order:
- folders selections: specify directories where your .gpx logs are stored;
- logs selection: select logs you want to analyze;
- distances selection: specify distances and number of attempts for each distance;

After processing, table will be shown with following columns:
- Distance. Two types of distance is shown here: distances with best times in the current log (simple number, i.e. 100), and distances with zero start speed (100zs, for example).
- Time;
- Average speed;
- Time from start: location of the distance in the log;
- Distance from start: location of the distance in the log;
- Actual distance. Due to large GPS sampling time actually logged distance fits required size in very rare cases, so recalculating method is used for required distance time calculation. See more in Accuracy chapter of this manual.

In the end of the table absolute records for processed logs is given.

All records and settings are stored in .gpx_records directory of your home directory or user folder for Windows.

### Accuracy

GPS is not very accurate method for distance measurement, so some best practices are recommended:
- Use special GPS trackers. Smartphone log quality is often very poor;
- Use high sampling rate: 1 sample in second, for example is good enough for accurate results;
- Do not hide GPS tracker deep inside your bag.

If you use smartphone applications, such as Strava and Runtastic, be very careful, when use this program for short distances analysis. These applications can turn on autopause feature for log compression purposes (even if user didn't selected it), so first several seconds of the log can be missed. Be critical to given results and don't be too proud if you occasionaly "beat" world record on your moring jogging.

Quality of the log can be indirectly estimated by "Actual distance" field of the table. Difference between actual and required distances don't have to be too large since large difference usually is the sign of GPS failure and leads to large inaccuracy in time calculaton.

Time is recalculated by following formula:

    time = actual_distance_time * distance / actual_distance

