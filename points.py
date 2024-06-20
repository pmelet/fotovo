import sqlite3 as sql
from os.path import join, dirname
from datetime import date, datetime
import time
import pytz

_DATABASE = join(dirname(__file__), 'production.db')

class Point:
    def __init__(self, time, readtime, watts, active):
        self.time = time
        self.readtime = readtime
        self.watts = watts
        self.active = active

    def commit(self):
        con = sql.connect(_DATABASE) 
        cur = con.cursor()
        q = """INSERT OR REPLACE INTO production (Time, Readtime, Watts, Active) VALUES (?, ?, ?, ?);"""
        cur.execute(q, (self.time, self.readtime, self.watts, self.active))
        con.commit()
        con.close()

    def to_dict(self):
        return {
            "time": self.time,
            "readtime" : self.readtime,
            "watts" : self.watts,
            "active": self.active,
        }

    def __str__(self):
        return f"{self.time}: {self.watts} ({self.active})"

def get_points():
    con = sql.connect(_DATABASE) 
    cur = con.cursor()
    q = """SELECT Time, Readtime, Watts, Active FROM production;"""
    cur.execute(q)
    points = cur.fetchall()
    con.commit()
    con.close()
    ret = []
    for p in points:
        ret.append(Point(*p))
    return ret

def get_stats():
    #timezone = pytz.timezone("Europe/Paris")
    con = sql.connect(_DATABASE) 
    cur = con.cursor()
    q = f"""select 
        strftime("{date.today().strftime("%Y-%m-%d")} %H:00", datetime(Time, 'unixepoch')), 
        avg(Watts), 
        min(Watts), 
        max(Watts) 
    from production 
    group by 1;"""
    cur.execute(q)
    points = cur.fetchall()
    con.commit()
    con.close()
    ret = []
    for p in points:
        slot, avg, min, max = p
        #dt = timezone.localize(datetime.strptime(slot, "%Y-%m-%d %H:%M"))
        dt = datetime.strptime(slot, "%Y-%m-%d %H:%M")
        epoch = time.mktime(dt.timetuple())
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
        cur.execute(f"CREATE TABLE IF NOT EXISTS production(Time INTEGER PRIMARY KEY, Readtime INT, Watts REAL, Active INT)") 
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
