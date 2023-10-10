import json
import requests
from websockets.sync.client import connect
import fake_useragent

import os

from .message import Message

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])
agent = ua.random
token = ""
base_url = ""

class Client:
    def __init__(self, prefix,bottoken,status=None,game=None,url=None,websocket=None,cdn=None):
      if url == None:
        url = "https://hummus.sys42.net/api/v6"
      if status == None:
        status = "online"
      if websocket == None:
        websocket = "wss://hummus-gateway.sys42.net/?v=6&encoding=json&compress?=zlib-stream"
      if cdn == None:
        cdn = "https://hummus-cdn.sys42.net/"
      self.prefix = prefix
      self.token = bottoken
      token = bottoken
      self.game = game
      self.base_url = url
      base_url = url
      self.cdn = cdn
      with connect(websocket,user_agent_header=ua.random) as websocket:
        print("restarting...")
        websocket.send(json.dumps({'op': 2,'d': {'token': token,'presence': {'status': status,'game': {"name":game,"type":1}}}}))
        
        while True:
          event = json.loads(websocket.recv())
          if event['t'] == "GUILD_CREATE":
            print(event['d']['name'])
          if event['op'] == 1:
            websocket.send(json.dumps({"op":1}))
          if event['t'] == "MESSAGE_CREATE":
            if event['d']['content'].startswith("!"):
              message = Message(event['d'],token,agent,base_url,cdn)
              func = message.content.replace(self.prefix,"")
              args = func.split(" ")
              thing = getattr(self, args[0])
              if callable(thing) and not "__" in args[0]:
                thing(message)