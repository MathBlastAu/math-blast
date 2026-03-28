#!/usr/bin/env python3
"""No-cache HTTP server for Math Blast preview."""
import http.server, os

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    def log_message(self, format, *args):
        pass  # suppress logs

os.chdir('/Users/leohiem/.openclaw/workspace/projects/math-blast')
print('Server running on http://localhost:3000')
http.server.HTTPServer(('', 3000), NoCacheHandler).serve_forever()
