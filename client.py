#!/usr/bin/env python

import asyncio
import ssl
from websockets.sync.client import connect
import json
import requests

appliance_url = "https://rbac-qa3.cisco.com/iam/scim"

async def hello():
    with connect("ws://ec2-184-72-133-150.compute-1.amazonaws.com:8765") as websocket:
        while True:
            message = websocket.recv()
            print(f"Received: {message}")
            message_dict = json.loads(message)
            url_to_send = appliance_url + message_dict["baseurl"]
            headers = message_dict["headers"]
            header_dict = dict()
            for header in headers.split("\n"):
                if header == "":
                    continue
                spl = header.split(":")
                if spl[0] == "Authorization":
                    
                    header_dict[spl[0]] = str(spl[1]).strip()
                    break
                
            if (message_dict["type"]== "GET"):
                print("Sending request to ",url_to_send )
                print(header_dict)
                rsp = requests.get(url_to_send,headers=header_dict,verify=False)
                print("Response from appliance: ")
                print(rsp.text)
                rsp_dict = dict()
                rsp_dict["status_code"] = rsp.status_code
                rsp_dict["body"] = rsp.text
                websocket.send(json.dumps(rsp_dict))

loop = asyncio.new_event_loop()
loop.create_task(hello())
loop.run_forever()
