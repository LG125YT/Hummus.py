from .member import Author
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
          self.mentions.append(Author(mention,cdn,self.token,self.base_url))
        self.attachments = data['attachments']
        self.embeds = data['embeds']
        self.edited_timestamp = data['edited_timestamp']
        self.pinned = data['pinned']
        self.mention_everyone = data['mention_everyone']
        self.tts = data['tts']
        self.timestamp = data['timestamp']
        self.webhook_id = data['webhook_id']
        self.author = Author(data['author'],cdn,self.token,self.base_url,self.guild_id)
        self.cdn = cdn
      
    async def reply(self, content):
      headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': self.agent
        }
      data = json.dumps({'content': content,
                            'tts': False})
      requests.post(url=f"{self.base_url}/channels/{self.channel}/messages",headers=headers,data=data)
    
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
        print(f)
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
      guild = Guild(e.json(),self.cdn)