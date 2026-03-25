#!/usr/bin/env python3
import os, sys, socket, urllib.request, urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get('PORT', 8080))

NYCPOKE = 'https://nycpokemap.com/query2.php'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://nycpokemap.com/',
    'Origin': 'https://nycpokemap.com',
}

class Handler(SimpleHTTPRequestHandler):

    def log_message(self, fmt, *args):
        first = str(args[0]) if args else ''
        if '/proxy' in first:
            print(f"[proxy] {first[:80]}", flush=True)

    def do_GET(self):
        if self.path.startswith('/proxy'):
            self._handle_proxy()
        else:
            super().do_GET()

    def _handle_proxy(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        mons  = params.get('mons',  [''])[0]
        time_ = params.get('time',  ['0'])[0]
        since = params.get('since', ['0'])[0]

        if not mons:
            self.send_error(400, 'Missing mons')
            return

        target = f"{NYCPOKE}?mons={urllib.parse.quote(mons)}&time={time_}&since={since}"
        try:
            req = urllib.request.Request(target, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_error(e.code, str(e.reason))
        except Exception as e:
            print(f"[proxy] error: {e}", flush=True)
            self.send_error(502, str(e))

# Se placer dans le dossier du script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Creer le serveur et binder immediatement
server = HTTPServer(('0.0.0.0', PORT), Handler)

# Log immediat du port — Render le detecte ici
print(f"Server listening on 0.0.0.0:{PORT}", flush=True)
sys.stdout.flush()

server.serve_forever()
