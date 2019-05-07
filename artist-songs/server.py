import http.server
import socketserver
import http.client
import json
import urllib.parse as urlparse
import sys


IP = "localhost"
PORT = 8000

try:
    TOKEN = sys.argv[1]
except:
    TOKEN =  "aX7cunegAzBjVT7x8aWBFpT4olnRdvGnAbywa3rnAh-QSNs2osUELjZpzX6ILj34"

def get_singer(singer, TOKEN):

    headers = {"Authorization": "Bearer " + TOKEN}
    conn = http.client.HTTPSConnection("api.genius.com")
    conn.request("GET", "https://api.genius.com/search?q=" + singer + "&page=1&per_page=20", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()
    repos = json.loads(repos_raw)
    content = """<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <html>
    <head>
    <body style='background-color: #FFF892'>
    <CENTER><IMG SRC="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/URJC_logo.svg/1200px-URJC_logo.svg.png" ALIGN="BOTTOM" width="150" height="50"/> </CENTER>
    <HR>
    <title>RESULTADOS</title>
    </head>
    <body>
    <CENTER><FONT FACE="arial"><H1>RESULTADOS DE LA BÚSQUEDA:</H1></FONT> """

    for song in repos['response']['hits']:
        content += "<li>" + str(song['result']['full_title']) + "<p><img src=" + song['result'][
            'song_art_image_thumbnail_url'] + '></li> <HR> '

    return content

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        action = False
        path = self.path
        default_headers= True

        if path == "/":
            filename = "index.html"
            action = True

        elif "?" in path:
            parsed = urlparse.urlparse(path)
            if "searchSongs" in path:
                singer = (urlparse.parse_qs(parsed.query)["artist"][0]).replace(" ","+")
                content = get_singer(singer, TOKEN)
            else:
                default_headers = False
                self.send_response(404)
                self.send_header("HTTP/1.0", "404 Not Found")
                content = str(self.send_error(404))
        else:
            default_headers = False
            self.send_response(404)
            self.send_header("HTTP/1.0", "404 Not Found")
            content = str(self.send_error(404))

        if default_headers:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')

        self.end_headers()

        if action:
            with open(filename, "r") as f:
                content = f.read()
        else:
            pass
        self.wfile.write(bytes(content, "utf8"))
        return

Handler = testHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("Serving at port", PORT)
print("Localhost:" , IP)
print("Token:", TOKEN)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()

