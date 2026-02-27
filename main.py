from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import os

GS_URL = "https://script.google.com/macros/s/AKfycbw97vCsHukISTL7CiZlIJqPehSkmZIacwTDqkttENzYul556w0B40CTPizaZxhCdM_C/exec"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        req = urllib.request.Request(
            GS_URL,
            data=body,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as _:
                pass
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            print("FORWARD ERROR:", e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"FORWARD ERROR")

    def log_message(self, format, *args):
        print(format % args)

port = int(os.environ.get("PORT", "8080"))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
