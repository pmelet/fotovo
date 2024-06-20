from http.server import HTTPServer, BaseHTTPRequestHandler


class PointsRequestHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        print ("GET")

def run():
    server_address = ('', 80)
    httpd = HTTPServer(server_address, PointsRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    run()