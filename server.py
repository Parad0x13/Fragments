import re
import cgi
import json
import time
import argparse
import threading
from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from fragments.gameloop import GameLoop

# [TODO] See if server.HTTP_OK and stuff like that can be used instead
HTTP_OK          = 200
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN   = 403
HTTP_NOT_FOUND   = 404

class LocalData(object):
    records = {}

    def load():
        fh = open("save.dat", "r")
        LocalData.records = json.load(fh)

    def save():
        print("Sever is saving state, expect lag")
        fh = open("save.dat", "w")
        fh.write(json.dumps(LocalData.records))

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search("/addrecord/*", self.path):
            ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
            if ctype == "application/json":
                length = int(self.headers.get("content-length"))
                rfile_str = self.rfile.read(length).decode("utf-8")
                # [TODO/BUG] Ensure we do sanity checking here
                data = json.loads(rfile_str)

                record_id = self.path.split("/")[-1]
                # [TODO/BUG] This does not account for items already existing in records
                LocalData.records[record_id] = data
                print(f"User has added record {record_id}: {data}")

                self.send_response(HTTP_OK)
                self.end_headers()
            else:
                self.send_response(HTTP_BAD_REQUEST, "Bad Request: must give data")
        else:
            self.send_response(HTTP_FORBIDDEN)

        self.end_headers()    # [TODO] Find out why this has to be here specifically

    def do_GET(self):
        if re.search("/userdata", self.path):
            record_id = self.path.split("/")[-1]
            if record_id in LocalData.records:
                self.send_response(HTTP_OK)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                data = json.dumps(LocalData.records[record_id])
                print(f"User has requested data {record_id}: {data}")
                self.wfile.write(data.encode("utf-8"))
            else:
                self.send_response(HTTP_NOT_FOUND, "Not Found: record does not exist")
        elif re.search("/shutdown", self.path):
            # Must shutdown in another thread or we'll hang
            def kill_me_please(): self.server.shutdown()
            threading.Thread(target = kill_me_please).start()

            self.send_response(HTTP_OK)
        else:
            self.send_response(HTTP_FORBIDDEN)

        self.end_headers()    # [TODO] Find out why this has to be here specifically

def main():
    parser = argparse.ArgumentParser(description = "HTTP Server")
    parser.add_argument("port", type = int, help = "Listening port for HTTP Server")
    parser.add_argument("ip", help = "HTTP Server IP")
    args = parser.parse_args()

    server = HTTPServer((args.ip, args.port), HTTPRequestHandler)
    print("HTTP Server Running...")
    server.serve_forever()

SERVER_ACTIVE = True
def mainLoop():
    gameLoop = GameLoop()

    # Thread should die elegantly once this function returns without calling itself again
    #while SERVER_ACTIVE:
        gameLoop.tick()

if __name__ == "__main__":
    LocalData.load()

    threading.Thread(target = mainLoop).start()

    print("Main Loop Activated...")
    main()

    SERVER_ACTIVE = False
    LocalData.save()
    print("Server has shutdown elegantly")
