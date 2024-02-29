from .permissions import Permissions
from .member import Avatar, User
from .role import Role

import requests
import fake_useragent
import json

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])

headers = {"Authorization":"","Content-Type":"application/json","User-Agent":ua.random}

class Guild:
  def __init__(self,data,cdn,instance):
    self.instance = instance
    self.id = data['id']
    self.name = data['name']
    self.icon = Avatar(self.id,data['icon'],cdn)
    self.owner_id = data['owner_id']
    self.features = data['features']
    self.region = data['region']
    self.roles = []
    for role in data['roles']:
      self.roles.append(role)
    self.cdn = cdn
    self.emojis = []
    for emoji in data['emojis']:
      self.emojis.append(emoji)
    self.voice_states = []
    for voice_state in data['voice_states']:
      self.voice_states.append(voice_state)
    self.afk_timeout = data['afk_timeout']

class PermOverwrites:
  def __init__(self,data):
    if type(data) == dict:
      self.id = data['id']
      self.type = data['type']
      self.allow = Permissions(data['allow'])
      self.deny = Permissions(data['deny'])
    if type(data) == Role:
      self.id = data.id
      self.type = "role"
      self.allow = Permissions(data.permissions)
      self.deny = Permissions(0)

  def toDict(self):
    self.allow.update()
    self.deny.update()
    return {"id":self.id,"type":self.type,"allow":self.allow.value,"deny":self.deny.value}

class Channel:
  def __init__(self,data,instance):
    self.headers = headers
    self.headers['Authorization'] = f"Bot {instance.token}"
    self.instance = instance
    if data['type'] == 0:
      self.topic = data['topic']
      self.last_message_id = data['last_message_id']
      self.nsfw = bool(data.get('nsfw'))
    if data['type'] == 2:
      self.bitrate = data['bitrate']
      self.user_limit = data.get('user_limit')
    self.type = data['type']
    self.id = data['id']
    self.guild_id = data['guild_id']
    self.name = data['name']
    self.permission_overwrites = []
    for overwrite in data['permission_overwrites']:
      self.permission_overwrites.append(PermOverwrites(overwrite))
    self.position = data['position']

  async def toDict(self):
    if self.type == 0:
      return {"name":self.name,"permission_overwrites":self.permission_overwrites,"position":self.position,"topic":self.topic,"nsfw":self.nsfw,"last_message_id":self.last_message_id,"type":self.type,"id":self.id,"guild_id":self.guild_id}
    elif self.type == 2:
      return {"bitrate":self.bitrate,"name":self.name,"permission_overwrites":self.permission_overwrites,"position":self.position,"user_limit":self.user_limit,"type":self.type,"id":self.id,"guild_id":self.guild_id}

  async def changeName(self,name):
    headers['Authorization'] = f"Bot {self.instance.token}"
    data = json.dumps({'name': name})
    e = requests.patch(url=f"{self.instance.base_url}/channels/{self.id}",headers=headers,data=data)
    if e.json().get('code') == 403:
      raise Exception("Bot does not have 'Manage Channels' permissions")
    return Channel(e.json(),self.instance)

  async def changePerms(self,role:Role,overwrite:PermOverwrites):
    if type(role) != Role:
      raise Exception("Please provide a Role object.")
    if type(overwrite) != PermOverwrites:
      raise Exception("Please provide a Permissions Overwrite (PermOverwrites) object.")
    role.permissions.update()
    overwrite.allow.update()
    overwrite.deny.update()
    data = {"id":role.id,"type":overwrite.type,"allow":overwrite.allow.value,"deny":overwrite.deny.value}
    headers['Authorization'] = f"Bot {self.instance.token}"
    e = requests.put(url=f"{self.instance.base_url}channels/{self.id}/permissions/{role.id}",headers=headers,json=data)
    if e.status_code == 204:
      return
    if e.json().get('code') == 403:
      raise Exception("Bot does not have 'Manage Channels' permissions")

class Emoji:
  def __init__(self,data,instance):
    self.id = data['id']
    self.name = data['name']
    self.guild_id = data['guild_id']
    self.roles = []
    for role in data['roles']:
      self.roles.append(role)
    self.user = User(instance,data['user'],instance.cdn,instance.token,instance.base_url,self.guild_id)
    self.require_colons = data['require_colons']
    self.managed = data['managed']
    self.allNamesString = data['allNamesString']

  async def toDict(self):
    return {"id":self.id,"name":self.name,"roles":self.roles,"user":self.user.toDict(),"require_colons":self.require_colons,"managed":self.managed,"allNamesString":self.allNamesString}