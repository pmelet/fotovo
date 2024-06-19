import requests
import configuration
import points
import sqlite3 as sql
import time


class Point:
    def __init__(self, time, readtime, watts, active):
        self.time = time
        self.readtime = readtime
        self.watts = watts
        self.active = active

    def commit(self):
        con = sql.connect('production.db') 
        cur = con.cursor()
        q = """INSERT OR REPLACE INTO production (Time, Readtime, Watts, Active) VALUES (?, ?, ?, ?);"""
        cur.execute(q, (self.time, self.readtime, self.watts, self.active))
        con.commit()
        con.close()


    def __str__(self):
        return f"{self.time}: {self.watts} ({self.active})"

def get_points():
        con = sql.connect('production.db') 
        cur = con.cursor()
        q = """SELECT Time, Readtime, Watts, Active FROM production;"""
        cur.execute(q)
        points = cur.fetchall()
        con.commit()
        con.close()
        return points


def setup_database():
    try:
        con = sql.connect('production.db') 
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
    print (points.get_points())
