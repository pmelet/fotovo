from http.server import HTTPServer, BaseHTTPRequestHandler
from points import get_points, get_stats, get_hist_points
import json
from flask import Flask
from flask import send_from_directory
from datetime import date, timedelta

app = Flask(__name__)

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return send_from_directory('static', "index.html")

@app.route("/production")
def production():
    prod = []
    yesterday = []
    for p in get_points():
        prod.append(p.to_dict())
    
    for p in get_hist_points(delta=timedelta(days=14)):
        yesterday.append(p.to_dict())
    d = {
        "production": prod,
        "yesterday" : yesterday,
        "stats"     : get_stats(days=14),
    }  
    return json.dumps(d).encode('utf8')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)