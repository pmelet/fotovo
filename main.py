import requests
import configuration
import points
import sqlite3 as sql
import time

def table_exists(table_name):
    conn = sql.connect('production.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    print (result)
    conn.close()
    return result is not None

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
    return points.Point(
        time     = int(time.time()),
        readtime = p['readingTime'],
        active   = p['activeCount'],
        watts    = p['wNow'],
    )

if __name__ == "__main__":
    points.setup_database()
    session = get_session_cookie()
    while True:
        p = get_production_info(session)
        print (p)
        p.commit()
        print (points.get_points())
        if p.watts > 0.0:
            time.sleep(30) # 30 seconds if we're producing
        else:
            time.sleep(900) # 15 minutes if we're not producing