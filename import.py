import sys
import csv
from datetime import datetime
import pytz
import points

def import_file(path):
    with open(path) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        ps = []
        for row in spamreader:
            datestr, wh = row
            try:
                watts = float(wh)*4 # assuming 15 minutes
                time = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S %z")
                #timestamp = time.replace(tzinfo=pytz.utc).timestamp()
                timestamp = time.timestamp()
                print (datestr, time, timestamp)
            except Exception as e:
                print ("skip", row, e)
                continue
            ps.append(points.Point(time=timestamp, readtime=-1, watts=watts, lifetime=-1, active=-1))
    
    points.Point.bulkCommit(ps)

if __name__ == "__main__":
    for path in sys.argv[1:]:
        import_file(path)