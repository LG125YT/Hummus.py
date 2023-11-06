import requests
import fake_useragent
import json
from .message import Message

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])

class Fetch:
  def __init__(self,token,url,cdn,instance):
    self.token = token
    self.base_url = url
    self.cdn = cdn
    self.instance = instance
    self.agent = ua.random
  
  async def getMessage(self,channel,id):
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': self.agent
    }
    data = {"limit":100}
    e = requests.get(url=f"{self.base_url}channels/{channel}/messages/",headers=headers,json=data)
    for message in e.json():
      if id == message['id']:
        return Message(message,self.token,self.agent,self.base_url,self.cdn,self.instance)

  async def getMessages(self,channel,limit):
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': self.agent
    }
    data = {"limit":limit}
    e = requests.get(url=f"{self.base_url}channels/{channel}/messages/",headers=headers,json=data)
    messages = []
    i = 0
    for message in e.json():
      if i < limit:
        messages.append(Message(message,self.token,self.agent,self.base_url,self.cdn,self.instance))
      i += 1
    return messages