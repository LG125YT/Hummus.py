from .author import Author
from .guild import Guild
import requests
import json
import asyncio

class Message:
    def __init__(self,data,token,agent,base_url,cdn):
        self.token = token
        self.agent = agent
        self.base_url = base_url
        self.content = data['content']
        self.channel = data['channel_id']
        self.guild = data.get("guild_id")
        self.dm = False
        if self.guild == None:
          self.dm = True
        self.id = data['id']
        self.mentions = []
        for mention in data['mentions']:
          self.mentions.append(Author(mention,cdn))
        self.attachments = data['attachments']
        self.embeds = data['embeds']
        self.edited_timestamp = data['edited_timestamp']
        self.pinned = data['pinned']
        self.mention_everyone = data['mention_everyone']
        self.tts = data['tts']
        self.timestamp = data['timestamp']
        self.webhook_id = data['webhook_id']
        self.author = Author(data['author'],cdn)
        self.cdn = cdn
      
    def reply(self, content):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
        }
      data = json.dumps({'content': content,
                            'tts': False})
      requests.post(url=f"{self.base_url}/channels/{self.channel}/messages",headers=headers,data=data)
    
    def getUser(self,id):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
        }
      e = requests.get(url=f"{self.base_url}users/{id}/",headers=headers)
      try:
        author = Author(e.json(),self.cdn)
        return author
      except Exception:
        if e.json()['code'] == 10001:
          pass

    def getGuild(self,guild):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
        }
      e = requests.get(url=f"{self.base_url}guilds/{guild}",headers=headers)
      guild = Guild(e.json(),self.cdn)