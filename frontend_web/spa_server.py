from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class SPARequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        requested_path = self.path.split("?", 1)[0].split("#", 1)[0]
        filesystem_path = Path(self.translate_path(requested_path))

        if requested_path == "/" or filesystem_path.exists():
            self.path = requested_path
        else:
            self.path = "/index.html"

        return super().do_GET()


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 3000), SPARequestHandler)
    server.serve_forever()
