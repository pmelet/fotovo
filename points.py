import sqlite3 as sql
from os.path import join, dirname
from datetime import date, datetime, timedelta, time as dtime
import time
import pytz

_DATABASE = join(dirname(__file__), 'production.db')

_ENVOY = "Envoy"
_ENPHASE = "Enphase"

class Point:
    def __init__(self, time, readtime, watts, lifetime, active, source=_ENVOY):
        self.time = time
        self.lifetime = lifetime
        self.readtime = readtime
        self.watts = watts
        self.active = active
        self.source = source

    def commit(self):
        con = sql.connect(_DATABASE) 
        cur = con.cursor()
        q = """INSERT OR REPLACE INTO production (Time, Readtime, Watts, Lifetime, Active, Source) VALUES (?, ?, ?, ?, ?, ?);"""
        cur.execute(q, (self.time, self.readtime, self.watts, self.lifetime, self.active, self.source))
        con.commit()
        con.close()

    @staticmethod
    def bulkCommit(array, source=_ENPHASE):
        con = sql.connect(_DATABASE) 
        cur = con.cursor()
        q = """INSERT OR REPLACE INTO production (Time, Readtime, Watts, Lifetime, Active, Source) VALUES (?, ?, ?, ?, ?, ?);"""
        cur.executemany(q, [(
            self.time, 
            self.readtime, 
            self.watts, 
            self.lifetime, 
            self.active, 
            self.source or source
        ) for self in array])
        con.commit()
        con.close()        

    def to_dict(self):
        return {
            "time": self.time,
            "readtime" : self.readtime,
            "watts" : self.watts,
            "lifetime": self.lifetime,
            "active": self.active,
            "source": self.source,
        }

    def __str__(self):
        return f"{self.time}: {self.watts} ({self.active})"

def get_points():
    timezone = pytz.timezone("Europe/Paris")
    con = sql.connect(_DATABASE) 
    cur = con.cursor()
    f = datetime.combine(date.today(), dtime()).timestamp()
    #print (df)
    #f = datetime.strptime(df, "%Y-%m-%d %H:%M:%S %Z").timestamp()
    q = f"""SELECT 
                Time,
                Readtime, 
                Watts, 
                Lifetime,
                Active,
                Source
            FROM production WHERE Active > 0 AND Time >= {f};"""
    cur.execute(q)
    points = cur.fetchall()
    con.commit()
    con.close()
    ret = []
    for p in points:
        Time, Readtime, Watts, Lifetime, Active, Source = p
        ret.append(Point(
            time=Time, #dt.replace(tzinfo=pytz.utc).timestamp(), 
            readtime=Readtime, 
            watts=Watts, 
            lifetime=Lifetime, 
            active=Active,
            source=Source,
        ))
    return ret


def get_hist_points(delta=timedelta(days=1)):
    con = sql.connect(_DATABASE) 
    cur = con.cursor()
    fordate = date.today()-delta
    f = datetime.strptime(fordate.strftime("%Y-%m-%d 00:00:00"), "%Y-%m-%d %H:%M:%S").timestamp()
    q = f"""SELECT 
                strftime("{date.today().strftime("%Y-%m-%d")} %H:%M:%S", datetime(Time, 'unixepoch')), 
                Time,
                Readtime, 
                Watts, 
                Lifetime,
                Active,
                Source
            FROM production WHERE Active > 0 AND Time BETWEEN {f} AND {f+(delta+timedelta(days=1)).total_seconds()};"""
    cur.execute(q)
    points = cur.fetchall()
    con.commit()
    con.close()
    ret = []
    for p in points:
        TimeStr, _, Readtime, Watts, Lifetime, Active, Source = p
        dt = datetime.strptime(TimeStr, "%Y-%m-%d %H:%M:%S")
        ret.append(Point(
            time=dt.replace(tzinfo=pytz.utc).timestamp(), 
            readtime=Readtime, 
            watts=Watts, 
            lifetime=Lifetime, 
            active=Active,
            source=Source,
        ))
    return ret

def get_stats(days=14):
    #timezone = pytz.timezone("Europe/Paris")
    con = sql.connect(_DATABASE) 
    cur = con.cursor()
    f = int(datetime.strftime(date.today(), "%j"))
    # only take the last 14 days
    # TODO: replace with the known value for the same day of year +/- 14days
    q = f"""SELECT
            strftime("{date.today().strftime("%Y-%m-%d")} %H:00", datetime(Time, 'unixepoch')), 
            avg(Watts), 
            min(Watts), 
            max(Watts) 
        FROM production 
        WHERE
            strftime("%j", datetime(Time, 'unixepoch')) BETWEEN "{f-days}" AND "{f+days}"
        GROUP by 1;"""
    print (q)
    cur.execute(q)
    points = cur.fetchall()
    con.commit()
    con.close()
    ret = []
    for p in points:
        slot, avg, min, max = p
        #dt = timezone.localize(datetime.strptime(slot, "%Y-%m-%d %H:%M"))
        dt = datetime.strptime(slot, "%Y-%m-%d %H:%M") + timedelta(minutes=30)
        ret.append({
            "time": dt.replace(tzinfo=pytz.utc).timestamp(),
            "min":  min,
            "avg":  avg,
            "max":  max,
        })
    return ret

def setup_database():
    try:
        con = sql.connect(_DATABASE) 
        cur = con.cursor()     
        cur.execute(f"""CREATE TABLE IF NOT EXISTS production(
                    Time INTEGER PRIMARY KEY, 
                    Readtime INT, Watts REAL, 
                    CalcWatts REAL, 
                    Lifetime REAL, 
                    Active INT,
                    Source TEXT)""") 
        con.commit() 
    except Exception as e: 
        if con: 
            con.rollback() 
        print("Unexpected error %s:" % e.args[0]) 
    finally: 
        if con: 
            con.close()  

if __name__ == "__main__":
    print ("\n".join(map(str,get_stats())))
