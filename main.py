import json
import requests
from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect
import fake_useragent
import time
import inspect

from .message import Message
from .events import Events

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])
agent = ua.random
token = ""
base_url = ""

def splitArgs(function,command,name):
  func_args = inspect.signature(function).parameters
  
  kwargs = {param: default.default for param, default in func_args.items() if default.default is not inspect.Parameter.empty}
  
  print(kwargs)
  
  custom_kwargs = {}
  args = command.replace('“','"').replace('”','"').split(" ") #filtering
  if args[0] == name:
    args.pop(0)
    if len(args) == 0:
      args.append("")
  idx = 0
  refined = []
  conc = ""
  for arg in args:
    if conc != "":
      conc = conc + " " + arg.replace("\"","")
      if arg[-1] == "\"":
        refined.append(conc)
        conc = ""
    else:
      if arg.startswith("\""):
        conc = arg.replace("\"","")
      else:
        refined.append(arg)
        
  for arg in kwargs:
    custom_kwargs[arg] = refined[idx]
    idx += 1
    
  return custom_kwargs

class Client:
    def __init__(self, prefix,bottoken,status=None,game=None,url=None,websocket=None,cdn=None,events:Events=None):
      if url == None:
        url = "https://hummus.sys42.net/api/v6/"
      if status == None:
        status = "online"
      if websocket == None:
        websocket = "wss://hummus-gateway.sys42.net/?v=6&encoding=json&compress?=zlib-stream"
      if cdn == None:
        cdn = "https://hummus-cdn.sys42.net/"
      if events == None:
        events = Events()
      self.websocket = websocket
      self.prefix = prefix
      self.token = bottoken
      token = bottoken
      self.game = game
      self.base_url = url
      base_url = url
      self.cdn = cdn
      self.events = events
      self.status = status
      
    async def run(self):
      reconnect = False
      session = ""
      seq = ""
      while True:
          with connect(self.websocket,user_agent_header=ua.random) as websocket:
            print("restarting...")
            websocket.send(json.dumps({'op': 2,'d': {'token':self.token,'presence': {'status': self.status,'game': {"name":self.game,"type":1}}}}))
            if reconnect:
              event = json.loads(websocket.recv())
              if event['t'] == "READY":
                websocket.send(json.dumps({"token":self.token,"session_id":session,"seq":seq,"op":6}))
            
            while True:
              event = json.loads(websocket.recv())
              seq = event['s']
              if event['t'] == "READY":
                session = event['d']['session_id']
                print("ready!")
              if event['t'] == "GUILD_CREATE":
                print(event['d']['name'])
              if event['op'] == 1:
                websocket.send(json.dumps({"op":1}))
              if event['t'] == "MESSAGE_CREATE":
                await self.events.on_message_create(Message(event['d'],self.token,agent,self.base_url,self.cdn))
                if event['d']['content'].startswith("!"):
                  try:
                    message = Message(event['d'],self.token,agent,self.base_url,self.cdn)
                    func = message.content.replace(self.prefix,"")
                    args = func.split(" ")
                    thing = getattr(self, args[0])
                    if callable(thing) and not "__" in args[0]:
                      kwargs = splitArgs(thing,message.content.replace(self.prefix+args[0]+" ",""),self.prefix+args[0])
                      await thing(message,**kwargs)
                  except AttributeError:
                    print(f"Command '{args[0]}' not found as a command.")