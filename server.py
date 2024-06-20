from http.server import HTTPServer, BaseHTTPRequestHandler
from points import get_points
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
    d = {"production": prod}  
    return json.dumps(d).encode('utf8')

class PointsRequestHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        points = get_points()
        prod = []
        for p in points:
            prod.append(p.to_dict())
        d = {"production": prod}  
        json_as_str = json.dumps(d).encode('utf8')
        print (json_as_str)
        self.wfile.write(bytes(json_as_str))

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, PointsRequestHandler)
    httpd.serve_forever()

#if __name__ == "__main__":
#    run()


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)