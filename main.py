import requests
import configuration
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

def table_exists(table_name):
    conn = sql.connect('production.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    print (result)
    conn.close()
    return result is not None

def setup_database():
    try:
        con = sql.connect('production.db') 
        cur = con.cursor()     
        cur.execute(f"CREATE TABLE IF NOT EXISTS production(Time INTEGER PRIMARY KEY, Watts REAL, Active INT)") 
        con.commit() 
    except Exception as e: 
        if con: 
            con.rollback() 
        print("Unexpected error %s:" % e.args[0]) 
    finally: 
        if con: 
            con.close()  


def get_session_cookie():
    url = "https://192.168.1.63/auth/check_jwt"
    headers = {"Authorization": "Bearer " + configuration._TOKEN}
    r = requests.get(url=url, headers=headers, verify=False)
    return r.headers['Set-Cookie']

def get_basic_info(session):
    url = "https://192.168.1.63/home.json"
    headers = {"Cookie": session}
    r = requests.get(url=url, headers=headers, verify=False)
    j = r.json()
    return j['network']

def get_production_info(session):
    url = "https://192.168.1.63/production.json"
    headers = {"Cookie": session}
    r = requests.get(url=url, headers=headers, verify=False)
    j = r.json()
    p = j['production'][0]
    return Point(
        time   = p['readingTime'],
        active = p['activeCount'],
        watts  = p['wNow'],
    )

setup_database()
session = get_session_cookie()
while True:
    p = get_production_info(session)
    print (p)
    p.commit()
    print (get_points())
    time.sleep(30)