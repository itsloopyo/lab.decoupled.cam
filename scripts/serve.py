#!/usr/bin/env python3
"""Local dev server for lab.decoupled.cam.

A plain static server with one extra trick: it resolves extensionless
URLs to their `.html` file the way GitHub Pages does, so local dev
matches production. `/privacy` serves `privacy.html`, `/download` serves
`download.html`, `/patreon/callback` serves `patreon/callback.html`, and
`/` serves `index.html`. Opens your default browser on start.

Run via `pixi run dev` (or `python scripts/serve.py`). Stdlib only.
"""

import http.server
import os
import socketserver
import threading
import webbrowser

PORT = 4173
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def translate_path(self, path):
        local = super().translate_path(path)
        # Directory → its index.html.
        if os.path.isdir(local):
            index = os.path.join(local, "index.html")
            if os.path.exists(index):
                return index
        # Extensionless → sibling .html (GitHub Pages clean URLs).
        if not os.path.exists(local) and os.path.exists(local + ".html"):
            return local + ".html"
        return local

    def log_message(self, fmt, *args):
        # Quieter than the default per-request noise.
        print("  " + (fmt % args))


def main():
    os.chdir(ROOT)
    url = f"http://localhost:{PORT}/"
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"lab.decoupled.cam  ->  {url}   (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped.")


if __name__ == "__main__":
    main()
