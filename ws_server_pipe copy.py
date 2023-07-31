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
    #this gets the message back from appliance
    await readFromWebSocket(websocket)


async def readFromWebServer(websocket):
    global queue
    print("inside")
    while True:
        message = queue_ipc.get()
        # server side websocket sends msg to client
        await websocket.send(message)

async def readFromWebSocket(websocket):
    while True:
        message = websocket.recv()
        print("receive from laptop:",message)

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

    def do_POST(self):
        self.do_GET()

    # ...

if __name__ == "__main__":
    queue_ipc = SimpleQueue()
    pid = os.fork()

    if pid > 0:
        with socketserver.TCPServer(("ec2-184-72-133-150.compute-1.amazonaws.com", 8000), WebRequestHandler) as httpd:
            print("serving at port", 8000)
            httpd.serve_forever()
    else:
        asyncio.run(main())