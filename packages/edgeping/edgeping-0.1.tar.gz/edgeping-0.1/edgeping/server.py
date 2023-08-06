# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import logging
import json
import zlib
import argparse

from http.server import BaseHTTPRequestHandler, HTTPServer
import http.server
import socketserver


PINGS = []


class PingHandling(BaseHTTPRequestHandler):
    def _response(self, body, status=200, content_type="plain/text"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(body)

    def do_DELETE(self):
        if self.path == "/pings":
            PINGS[:] = []
            return self._response(b"OK")
        self._response(b"Not found", 404)

    def do_GET(self):
        logging.info(f"GET {self.path}")
        if self.path == "/status":
            return self._response(b"OK")
        if self.path == "/pings":
            return self._response(json.dumps(PINGS).encode())
        self._response(b"Not found", 404)

    def do_POST(self):
        logging.info(f"POST {self.path}")
        if not self.path.startswith("/submit/"):
            return self._response(b"Not found", 404)
        # /submit/<namespace>/<docType>/<docVersion>/<docId>
        splitted = self.path.split("/")
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)

        if self.headers.get("Content-Encoding") == "gzip":
            data = zlib.decompress(data, zlib.MAX_WBITS | 16)

        ping_data = json.loads(data)
        PINGS.append(ping_data)
        self._response(b"OK")

    do_PUT = do_POST


def _parser():
    parser = argparse.ArgumentParser(description="Mozilla Edge Test Server")
    parser.add_argument(
        "--version",
        action="store_true",
        default=False,
        help="Displays version and exits.",
    )
    parser.add_argument("--host", help="Host to bind", type=str, default="localhost")
    parser.add_argument("-p", "--port", help="Port to bind", type=int, default=7777)
    return parser


def main(args=None):
    if args is None:
        parser = _parser()
        args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    host, port = args.host, args.port
    with socketserver.TCPServer((host, port), PingHandling) as httpd:
        print(f"Running. Set 'toolkit.telemetry.server' value to http://{host}:{port}")
        try:
            httpd.serve_forever()
        finally:
            print("Bye!")


if __name__ == "__main__":
    main()
