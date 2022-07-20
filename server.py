# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer # python2
from http.server import BaseHTTPRequestHandler, HTTPServer # python3
import time
class HandleRequests(BaseHTTPRequestHandler):

    def _set_headers(self):
        time.sleep(5)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_POST(self):
        '''Reads post request body'''
        self._set_headers()
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)

    def do_PUT(self):
        self.do_POST()

host = ''
port = 8000
HTTPServer((host, port), HandleRequests).serve_forever()