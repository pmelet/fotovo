from http.server import HTTPServer, BaseHTTPRequestHandler
from points import get_points, get_stats
import json
from flask import Flask
from flask import send_from_directory

app = Flask(__name__)

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return send_from_directory('static', "index.html")

@app.route("/production")
def production():
    points = get_points()
    prod = []
    for p in points:
        prod.append(p.to_dict())
    d = {
        "production": prod,
        "stats"     : get_stats(),
    }  
    return json.dumps(d).encode('utf8')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)