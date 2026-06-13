#!/usr/bin/env python3
"""
Tiny static server for Replit (and local preview).
--------------------------------------------------
The Replit "Run" button starts this. It serves:
    /            -> the landing page (landing/index.html)
    /intake      -> the practice intake form (intake/intake-form.html)
    /sample      -> the rendered sample Blueprint (samples/westbrook-family-medicine.html)
plus every file in the repo by its normal path (e.g. /samples/westbrook-family-medicine.pdf).

This is only the public-facing front door. To GENERATE a Blueprint, use the Shell:
    cd pipeline && python3 generate.py inputs_westbrook.json

No framework, standard library only.
"""

import http.server
import socketserver
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8000"))

ROUTES = {
    "/": "landing/index.html",
    "/intake": "intake/intake-form.html",
    "/sample": "samples/westbrook-family-medicine.html",
}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        if path in ROUTES:
            self.path = "/" + ROUTES[path]
        return super().do_GET()

    def log_message(self, fmt, *args):
        pass  # quiet


def main():
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving on http://0.0.0.0:{PORT}")
        print("  /        landing page")
        print("  /intake  intake form")
        print("  /sample  sample Blueprint (HTML)")
        print("Generate a Blueprint from the Shell: cd pipeline && python3 generate.py inputs_westbrook.json")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
