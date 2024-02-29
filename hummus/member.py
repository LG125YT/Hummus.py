from .role import Role

import fake_useragent
import requests
import json

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])
agent = ua.random

class Avatar:
  def __init__(self,id,avatar,cdn):
    self.id = id
    self.avatar = avatar
    self.url = f"{cdn}avatars/{self.id}/{self.avatar}.png"

class User:
  def __init__(self,instance,data,cdn,token,url,guild_id=None):
    self.instance = instance
    self.guild_id = guild_id
    self.base_url = url
    self.token = token
    self.id = data['id']
    self.username = data['username']
    self.discriminator = data['discriminator']
    self.mention = f"<@{data['id']}>"
    self.avatar = Avatar(self.id,data['avatar'],cdn)
    self.bot = data['bot']

  async def toDict(self):
    return {"id":self.id,"username":self.username,"discriminator":self.discriminator,"mention":self.mention,"avatar":self.avatar.url,"bot":self.bot}

  async def setRoles(self,roles:list):
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def removeRoles(self,roles:list):
    temp = []
    for guild in self.instance.allGuilds:
      if guild.id == self.guild_id:
        for member in guild.members:
          if self.id == member.id:
            temp = member.roles
    idx = 0
    for role in roles:
      if type(roles[0]) == Role:
        if role.id in temp:
          temp.pop(idx)
      else:
        if role in temp:
          temp.pop(idx)
      idx += 1
    roles = temp
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def addRoles(self,roles:list):
    temp = []
    for guild in self.instance.allGuilds:
      if guild.id == self.guild_id:
        for member in guild.members:
          if self.id == member.id:
            temp = member.roles
    if type(roles[0]) == Role:
      for role in roles:
        temp.append(role.id)
      roles = temp
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    print(self.guild_id)
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    print(e.json())
    return e

  async def kick(self):
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent
      }
    e = requests.delete(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}", headers=headers)
    return e

  async def nick(self,nick):
    headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': agent,
        }
    if nick == "None":
        data = json.dumps({'nick': ""})
    else:
        data = json.dumps({'nick': nick})
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

class Member:
  def __init__(self,instance,data,cdn,token,url,guild):
    self.instance = instance
    self.guild_id = guild
    self.id = data['id']
    self.mention = f"<@{data['id']}>"
    self.nick = data['nick']
    self.roles = data['roles']
    self.joined_at = data['joined_at']
    self.deaf = data['deaf']
    self.mute = data['mute']
    self.user = User(instance,data['user'],cdn,token,url,guild)

  async def setRoles(self,roles:list):
    headers = {
      'Authorization': f'Bot {self.instance.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.instance.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def removeRoles(self,roles:list):
    temp = []
    for guild in self.instance.allGuilds:
      if guild.id == self.guild_id:
        for member in guild.members:
          if self.id == member.id:
            temp = member.roles
    idx = 0
    for role in roles:
      if type(roles[0]) == Role:
        if role.id in temp:
          temp.pop(idx)
      else:
        if role in temp:
          temp.pop(idx)
      idx += 1
    roles = temp
    headers = {
      'Authorization': f'Bot {self.instance.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.instance.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def addRoles(self,roles:list):
    temp = []
    for guild in self.instance.allGuilds:
      if guild.id == self.guild_id:
        for member in guild.members:
          if self.id == member.id:
            temp = member.roles
    if type(roles[0]) == Role:
      for role in roles:
        temp.append(role.id)
      roles = temp
    headers = {
      'Authorization': f'Bot {self.instance.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    print(self.user.guild_id)
    e = requests.patch(url=f"{self.instance.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    print(e.json())
    return e

  async def kick(self):
    headers = {
      'Authorization': f'Bot {self.instance.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
      }
    e = requests.delete(url=f"{self.user.base_url}guilds/{self.guild_id}/members/{self.id}", headers=headers)
    return e

  async def nick(self,nick):
    headers = {
        'Authorization': f'Bot {self.user.token}',
        'Content-Type': 'application/json',
      'User-Agent': agent,
        }
    if nick == "None":
        data = json.dumps({'nick': ""})
    else:
        data = json.dumps({'nick': nick})
    e = requests.patch(url=f"{self.user.base_url}/guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

class Presence:
  def __init__(self,instance,data,cdn,token,url,guild):
    self.instance = instance
    self.guild_id = guild
    self.game = data['game']
    self.status = data['status']
    self.user = User(instance,data['user'],cdn,token,url,guild)