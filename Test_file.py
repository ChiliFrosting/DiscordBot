from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from dotenv import load_dotenv

load_dotenv()


host= "localhost"
port= 3000
url= os.getenv("token_generation_endpoint")
class http_server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/hmtl")
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>Hello World!</h1></body></html>", "utf-8"))
        self.wfile.write(bytes(f"<html><body><h1>{url}</h1></body></html>", "utf-8"))
        

server= HTTPServer((host, port), http_server)
server.serve_forever()
server.server_close()