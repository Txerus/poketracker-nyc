#!/usr/bin/env python3
"""
NYC PokeTracker - Serveur local avec proxy integre
Lance avec: python server.py
Puis ouvre: http://localhost:8080
"""
import sys, os, json, urllib.request, urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
NYCPOKE_BASE = 'https://nycpokemap.com/query2.php'

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Silences les logs des fichiers statiques, garde les erreurs proxy
        first = str(args[0]) if args else ''
        if '/proxy' in first:
            print(f"[proxy] {args[0]} -> {args[1]}")

    def do_GET(self):
        # ── Proxy endpoint: /proxy?mons=...&time=...&since=...
        if self.path.startswith('/proxy'):
            self.handle_proxy()
        else:
            # Fichiers statiques (HTML, etc.)
            super().do_GET()

    def handle_proxy(self):
        # Parse query string
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        mons   = params.get('mons',  [''])[0]
        time_  = params.get('time',  ['0'])[0]
        since  = params.get('since', ['0'])[0]

        if not mons:
            self.send_error(400, 'Missing mons param')
            return

        target = f"{NYCPOKE_BASE}?mons={urllib.parse.quote(mons)}&time={time_}&since={since}"

        try:
            req = urllib.request.Request(
                target,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; PokeTracker/1.0)',
                    'Accept': 'application/json',
                    'Referer': 'https://nycpokemap.com/',
                    'Origin': 'https://nycpokemap.com',
                }
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(data)

        except urllib.error.HTTPError as e:
            print(f"[proxy] HTTPError {e.code}: {target[:80]}")
            self.send_error(e.code, f'Upstream error: {e.reason}')
        except Exception as e:
            print(f"[proxy] Error: {e}")
            self.send_error(502, f'Proxy error: {e}')

if __name__ == '__main__':
    # Serve from the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '.')
    # If run from Downloads, serve from current directory
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])

    print(f"\n{'='*50}")
    print(f"  NYC PokeTracker - Serveur local")
    print(f"{'='*50}")
    print(f"  URL: http://localhost:{PORT}/nyc-poketracker-pwa.html")
    print(f"  Proxy: http://localhost:{PORT}/proxy?mons=...")
    print(f"  Dossier: {os.getcwd()}")
    print(f"{'='*50}\n")

    server = HTTPServer(('localhost', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServeur arrete.")
