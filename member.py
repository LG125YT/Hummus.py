import requests
import json

class Avatar:
  def __init__(self,id,avatar,cdn):
    self.id = id
    self.avatar = avatar
    self.url = f"{cdn}avatars/{self.id}/{self.avatar}.png"

class User:
  def __init__(self,data,cdn,token,url,guild_id=None):
    self.guild_id = guild_id
    self.base_url = url
    self.token = token
    self.id = data['id']
    self.username = data['username']
    self.discriminator = data['discriminator']
    self.avatar = Avatar(self.id,data['avatar'],cdn)
    self.bot = data['bot']

  async def kick(self):
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': self.agent
      }
    e = requests.delete(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}", headers=headers)
    return e

  async def nick(self,nick):
    headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json'
        }
    if nick == "None":
        data = json.dumps({'nick': ""})
    else:
        data = json.dumps({'nick': nick})
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

class Member:
  def __init__(self,data,cdn,token,url,guild):
    self.guild = guild
    self.id = data['id']
    self.nick = data['nick']
    self.roles = data['roles']
    self.joined_at = data['joined_at']
    self.deaf = data['deaf']
    self.mute = data['mute']
    self.user = User(data['user'],cdn,token,url,guild)
    
  async def kick(self):
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json'
      }
    e = requests.delete(url=f"{self.user.base_url}guilds/{self.guild}/members/{self.id}", headers=headers)
    return e

  async def nick(self,nick):
    headers = {
        'Authorization': f'Bot {self.user.token}',
        'Content-Type': 'application/json'
        }
    if nick == "None":
        data = json.dumps({'nick': ""})
    else:
        data = json.dumps({'nick': nick})
    e = requests.patch(url=f"{self.user.base_url}/guilds/{self.guild}/members/{self.id}",headers=headers,data=data)
    return e

class Presence:
  def __init__(self,data,cdn,token,url,guild):
    self.guild = guild
    self.game = data['game']
    self.status = data['status']
    self.user = User(data['user'],cdn,token,url,guild)