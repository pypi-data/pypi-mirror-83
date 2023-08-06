#! /usr/bin/env python
# -*- coding:utf-8 -*-
# install ws4py
# pip install ws4py
# easy_install ws4py
from ws4py.client.threadedclient import WebSocketClient
import json

class MyWebsocket(WebSocketClient):
    def opened(self):
        msg = json.dumps({"model": 1, "Token": "d7b501d2-fe5d-4a26-a799-1e67e037bfb5"})
        self.send(msg)

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        msg= json.dumps(m)
        print("recv:"+msg)



def start():
    try:
        ws = MyWebsocket('ws://192.168.3.216:8181/', protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()


def onMessage(that, resolve, type, data):

