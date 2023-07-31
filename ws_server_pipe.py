# webapp.py

import json
from http.server import BaseHTTPRequestHandler
import socketserver
import asyncio
from websockets.server import serve
import os
from multiprocessing import SimpleQueue



async def echo(websocket):
    await readFromWebServer(websocket)

async def readFromWebServer(websocket):
    global queue
    while True:
        message = queue_ipc.get()
        # server side websocket sends msg to client
        await websocket.send(message)
        message = await websocket.recv()
        queue_rsp.put(message)

async def main():
    print("Started websocket")
    async with serve(echo, "ec2-184-72-133-150.compute-1.amazonaws.com", 8765):
        await asyncio.Future()  # run forever



class WebRequestHandler(BaseHTTPRequestHandler):
    # ...
        
    def do_GET(self):
        global queue_ipc
        send_req = dict()
        tmp = self.requestline.split()
        send_req["type"] = tmp[0]
        send_req["baseurl"] = tmp[1]
        send_req["headers"] = str(self.headers)

        send_req_str = json.dumps(send_req)
        print(send_req_str)
        queue_ipc.put(send_req_str)
        rsp_message = queue_rsp.get()
        message_dict = json.loads(rsp_message)
        print("Message from local server:",str(message_dict))
        self.send_response(message_dict["status_code"])
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(message_dict["body"].encode("utf-8"))
        

    def do_POST(self):
        self.do_GET()

    # ...

if __name__ == "__main__":
    queue_ipc = SimpleQueue()
    queue_rsp = SimpleQueue()
    pid = os.fork()

    if pid > 0:
        with socketserver.TCPServer(("ec2-184-72-133-150.compute-1.amazonaws.com", 8000), WebRequestHandler) as httpd:
            print("serving at port", 8000)
            httpd.serve_forever()
    else:
        asyncio.run(main())