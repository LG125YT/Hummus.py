from .member import User
from .guild import Guild
import requests
import json
import asyncio

class Message:
    def __init__(self,data,token,agent,base_url,cdn,instance):
        self.instance = instance
        self.token = token
        self.agent = agent
        self.base_url = base_url
        self.content = data['content']
        self.channel = data['channel_id']
        self.guild_id = data.get("guild_id")
        self.dm = False
        if self.guild_id == None:
          self.dm = True
        self.id = data['id']
        self.mention_roles = []
        self.mentions = []
        for mention in data['mentions']:
          self.mentions.append(User(mention,cdn,self.token,self.base_url))
        self.attachments = data['attachments']
        self.embeds = data['embeds']
        self.edited_timestamp = data['edited_timestamp']
        self.pinned = data['pinned']
        self.mention_everyone = data['mention_everyone']
        self.tts = data['tts']
        self.timestamp = data['timestamp']
        self.webhook_id = data['webhook_id']
        self.author = User(data['author'],cdn,self.token,self.base_url,self.guild_id)
        self.cdn = cdn

    async def edit(self, content):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
      }
      data = {"content":content}
      r = requests.patch(f"{self.base_url}channels/{self.channel}/messages/{self.id}",headers=headers,data=json.dumps(data))
      return Message(r.json(),self.token,self.agent,self.base_url,self.cdn,self.instance)

    async def send(self, content):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
        }
      data = json.dumps({'content': content,
                            'tts': False})
      e = requests.post(url=f"{self.base_url}/channels/{self.channel}/messages",headers=headers,data=data)
      return Message(e.json(),self.token,self.agent,self.base_url,self.cdn,self.instance)
      
    async def reply(self, content):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
        }
      data = json.dumps({'content': f"> {self.content} (<@{self.author.id}>)\n{content}",
                            'tts': False})
      e = requests.post(url=f"{self.base_url}/channels/{self.channel}/messages",headers=headers,data=data)
      return Message(e.json(),self.token,self.agent,self.base_url,self.cdn,self.instance)
    
    async def getUser(self,id):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
        }
      e = requests.get(url=f"{self.base_url}users/{id}/",headers=headers)
      guildID = None
      if self.guild_id != None:
        for guild in self.instance.allGuilds:
          if self.guild_id == guild.guild.id:
            for member in guild.members:
              if member.id == id:
                guildID = guild.guild.id
      try:
        author = Author(e.json(),self.cdn,self.token,self.base_url,guildID)
        return author
      except Exception as f:
        print(f"could not create author class: {f}")
        if e.json()['code'] == 10001:
          pass

    async def getGuildUser(self,user_id):
      user = await self.getUser(user_id)
      for guild in self.instance.allGuilds:
        if guild.guild.id == user.guild_id:
          for member in guild.members:
            if user_id == member.id:
              return member

    async def getGuild(self,guild):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
        }
      e = requests.get(url=f"{self.base_url}guilds/{guild}",headers=headers)
      #print(e.json())
      #try:
      guild = Guild(e.json(),self.cdn)
      print(guild.id)
        #return channel
      #except Exception:
  
    async def getMessage(self,id):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
      }
      data = {"limit":100} #limit doesnt work but hell who cares
      e = requests.get(url=f"{self.base_url}channels/{self.channel}/messages/",headers=headers,json=data)
      for message in e.json():
        if id == message['id']:
          return Message(message,self.token,self.agent,self.base_url,self.cdn,self.instance)
  
    async def getMessages(self,channel,limit):
      try:
        limit = int(limit)
      except Exception:
        raise Exception("Limit must be an integer.")
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
      
    async def deleteMessage(self,id):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
      }
      e = requests.delete(url=f"{self.base_url}channels/{self.channel}/messages/{id}",headers=headers)
      return e

    async def bulkDelete(self,messages):
      if len(messages) > 100:
        raise Exception("Please provide less than 100 messages!") #1. no spam api!!! 2. i believe this is the limit for bulk delete back then
      ids = []
      for message in messages:
        ids.append(message.id)
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
      }
      for id in ids:
        requests.delete(url=f"{self.base_url}channels/{self.channel}/messages/{id}",headers=headers) #bulk delete endpoint doesnt exist (absolute stupid)