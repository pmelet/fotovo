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
                time = datetime.strptime(datestr[:19], "%Y-%m-%d %H:%M:%S")
                time = time.replace(tzinfo=pytz.utc).timestamp()
            except:
                print ("skip", row)
                continue
            ps.append(points.Point(time=time, readtime=-1, watts=watts, active=-1))
    
    points.Point.bulkCommit(ps)

if __name__ == "__main__":
    for path in sys.argv[1:]:
        import_file(path)