import requests
import configuration
import points
import sqlite3 as sql
import time


class Point:
    def __init__(self, time, watts, active):
        self.time = time
        self.watts = watts
        self.active = active

    def commit(self):
        con = sql.connect('production.db') 
        cur = con.cursor()
        q = """INSERT OR REPLACE INTO production (Time, Watts, Active) VALUES (?, ?, ?);"""
        cur.execute(q, (self.time, self.watts, self.active))
        con.commit()
        con.close()


    def __str__(self):
        return f"{self.time}: {self.watts} ({self.active})"

def get_points():
        con = sql.connect('production.db') 
        cur = con.cursor()
        q = """SELECT Time, Watts, Active FROM production;"""
        cur.execute(q)
        points = cur.fetchall()
        con.commit()
        con.close()
        return points

print (points.get_points())
