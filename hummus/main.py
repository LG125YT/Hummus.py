#welcome to stupidity central
import json
import requests
from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect
import fake_useragent
import traceback
import inspect
import asyncio
import base64

from .message import Message
from .role import Role
from .member import User, Member, Presence
from .guild import Guild, Channel, Emoji
from .events import Events
from .allguild import AllGuild
from .fetch import Fetch

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])
agent = ua.random


def splitArgs(function, command, name, instance, mentions,role_mentions):
     func_args = list(inspect.signature(function).parameters.values())[1:]
     custom_kwargs = []

     args = command.replace('“','"').replace('”','"').replace("‘","\"").replace("’","\"").split() #filtering

     if args and args[0] == name:
         args.pop(0)
         if not args:
             return []

     refined = []
     in_quotes = False
     current_arg = ""

     for arg in args:
         if in_quotes:
             current_arg += " " + arg
             if arg.endswith("\""):
                 in_quotes = False
                 refined.append(current_arg.strip("\""))
                 current_arg = ""
             continue

         if arg.startswith("\""):
             in_quotes = True
             current_arg = arg.strip("\"")
         else:
             refined.append(arg)

     role_mention_idx = 0
     mention_idx = 0
     idx = 0
     for arg_name, arg in zip(func_args, refined):
         if idx >= len(refined):
             break

         if arg_name.annotation == str:
             custom_kwargs.append(str(arg))
         elif arg_name.annotation == int:
           try:
             custom_kwargs.append(int(arg))
           except Exception:
             print(f"Ignoring exception: Provided argument '{arg}' is not an integer.")
         elif arg_name.annotation == Role:
           try:
             custom_kwargs.append(role_mentions[role_mention_idx])
             role_mention_idx += 1
           except Exception:
             print(f"\033[91mIgnoring exception: Provided argument '{arg}' is not a role mention.\033[0m")
         elif arg_name.annotation == User:
             try:
                 custom_kwargs.append(mentions[mention_idx])
                 mention_idx += 1
             except Exception:
                 print(f"\033[91mIgnoring exception: Provided argument '{arg}' is not a mention.\033[0m")
         else:
             custom_kwargs.append(arg)

         idx += 1
     return custom_kwargs


class State:
 def __init__(self,instance):
   self.instance = instance

 async def update_avatar(self,file):
   headers = {
     'Authorization': f'Bot {self.instance.token}',
     'Content-Type': 'application/json',
     'User-Agent': agent
   }
   img = base64.b64encode(open(file,'rb').read()).decode('utf-8')
   data = {"avatar":f"data:image/png;base64,{img}"}
   e = requests.patch(f"{self.instance.base_url}users/@me/",json=data,headers=headers)
   return e.json()

 async def update_status(self,status=None,game=None):
   self.instance.connection.send(json.dumps({"op":3,"d":{"status":status,"game":{"name":game,"type":1}}}))

 async def add_friend(self,user):
   headers = {
     'Authorization': f'Bot {self.instance.token}',
     'Content-Type': 'application/json',
     'User-Agent': agent
   }
   e = requests.put(f"{self.instance.base_url}users/@me/relationships/{user}",headers=headers,json={"type":False})

class Client:
   def __init__(self, prefix,token,status=None,game=None,url=None,events:Events=None):
     if url == None:
       url = "https://hummus.sys42.net/api/v6/"
       cdn = "https://hummus-cdn.sys42.net/"
     else:
       if not url[(len(url)-1)] == "/":
         url = url + "/"
     if status == None:
       status = "online"
     if url:
       e = requests.get(url+"/gateway",headers={"User-Agent":agent})
       if e.json().get('url'):
         websocket = e.json()['url']
     if url != None:
       cdn = url.split(".")
       cdn[0] = cdn[0]+"-cdn"
       ok = cdn[0]
       cdn.pop(0)
       for i in cdn:
         ok = ok + "." + i
       cdn = ok.replace("api/v6/","")
     if events == None:
       asyncio.run(self.LISTEN(Events(self),silent=True))
     else:
       self.events = events
     self.websocket = websocket+"?api=v6&encoding=json"
     self.prefix = prefix
     self.token = token
     self.game = game
     self.base_url = url
     self.cdn = cdn
     self.status = status
     self.fetch = Fetch(self.token,self.base_url,self.cdn,self)
     self.state = State(self)

   async def LISTEN(self,instance:Events,silent:bool=False):
     self.events = instance
     if not silent:
       print("\033[92mRegistered Events class to listen.\033[0m")

   async def RUN(self):
     reconnect = False
     session = ""
     seq = ""
     self.allGuilds:list[AllGuild] = []
     while True:
      try:
       with connect(self.websocket,user_agent_header=ua.random) as websocket:
         self.connection = websocket
         print("\033[92mrestarting...\033[0m")
         websocket.send(json.dumps({'op': 2,'d': {'token':self.token,'presence': {'status': self.status,'game': {"name":self.game,"type":1}}}}))
         if reconnect:
           event = json.loads(websocket.recv())
           print(f"\033[92mResuming session with sequence ID {seq}\033[0m")
           if event['t'] == "READY":
             websocket.send(json.dumps({"token":self.token,"session_id":session,"seq":seq,"op":6}))

         while True:
           event = json.loads(websocket.recv())
           seq = event['s']

           if event['t'] == "READY":
             session = event['d']['session_id']
             print("\033[92mready, recieving login guild data\033[0m")
           if event['op'] == 1:
             websocket.send(json.dumps({"op":1}))
           if event['t'] == "TYPING_START":
             member = event['d'].get('member')
             if member:
               member = Member(self,event['d']['member'],self.cdn,self.token,self.base_url,event['d']['guild_id'])
             else:
               member = event['d']['user_id']
             await self.events.on_typing_start(event['d']['channel_id'],member,event['d']['timestamp'])
           if event['t'] == "GUILD_MEMBER_UPDATE":
             guild_idx = 0
             member_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 for member in guild.members:
                   if member.id == event['d']['id']:
                     previous = member
                     new_member = Member(self,event['d'],self.cdn,self.token,self.base_url,event['d']['guild_id'])
                     self.allGuilds[guild_idx].members[member_idx] = new_member
                     await self.events.on_guild_member_update(previous,new_member)
                   member_idx += 1
               guild_idx += 1
           if event['t'] == "GUILD_UPDATE":
             guild_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['id']:
                 updated_guild = Guild(event['d'],self.cdn,self)
                 previous = await guild.toDict()
                 self.allGuilds[guild_idx].guild = updated_guild
                 await self.events.on_guild_update(previous,updated_guild)
               guild_idx += 1
           if event['t'] == "GUILD_EMOJIS_UPDATE":
             guild_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 before = guild.emojis
                 guild.emojis = []
                 for emoji in event['d']['emojis']:
                   self.allGuilds[guild_idx].append(Emoji(emoji,self))
                 await self.events.on_guild_emojis_update(before,guild.emojis)
               guild_idx += 1
           if event['t'] == "GUILD_ROLE_UPDATE":
             guild_idx = 0
             role_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 for role in guild.roles:
                   if role.id == event['d']['role']['id']:
                     previous = role
                     new_role = Role(event['d']['role'])
                     self.allGuilds[guild_idx].roles[role_idx] = new_role
                     await self.events.on_guild_role_update(event['d']['guild_id'],previous,new_role)
                   role_idx += 1
               guild_idx += 1
           if event['t'] == "GUILD_ROLE_CREATE":
             guild_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 new_role = Role(event['d']['role'])
                 self.allGuilds[guild_idx].roles.append(new_role)
                 await self.events.on_guild_role_create(event['d']['guild_id'],new_role)
               guild_idx += 1
           if event['t'] == "GUILD_ROLE_DELETE":
             guild_idx = 0
             role_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 for role in guild.roles:
                   if role.id == event['d']['role_id']:
                     deleted_role = role
                     self.allGuilds[guild_idx].roles.pop(role_idx)
                     await self.events.on_guild_role_delete(event['d']['guild_id'],deleted_role)
                   role_idx += 1
               guild_idx += 1
           if event['t'] == "CHANNEL_CREATE":
             guild_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 new_channel = Channel(event['d'],self)
                 self.allGuilds[guild_idx].channels.append(new_channel)
                 await self.events.on_channel_create(new_channel)
               guild_idx += 1
           if event['t'] == "CHANNEL_UPDATE":
             guild_idx = 0
             channel_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 for channel in guild.channels:
                   if channel.id == event['d']['id']:
                     updated_channel = Channel(event['d'],self)
                     before = guild.channels[channel_idx]
                     self.allGuilds[guild_idx].channels[channel_idx] = updated_channel
                     await self.events.on_channel_update(before,updated_channel)
                   channel_idx += 1
               guild_idx += 1
           if event['t'] == "CHANNEL_DELETE":
             guild_idx = 0
             channel_idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 for channel in guild.channels:
                   if channel.id == event['d']['id']:
                     deleted_channel = guild.channels[channel_idx]
                     self.allGuilds[guild_idx].channels.pop(channel_idx)
                     await self.events.on_channel_delete(deleted_channel)
                   channel_idx += 1
               guild_idx += 1
           if event['t'] == "PRESENCE_UPDATE" and event['d'].get('guild_id'): #how am i going to update a guild presence if theres no guild id?
               guild_idx = 0
               presence_idx = 0
               for guild in self.allGuilds:
                 if guild.id == event['d']['guild_id']:
                   for presence in guild.presences:
                     if presence.user.id == event['d']['user']['id']:
                       new_presence = Presence(self,event['d'],self.cdn,self.token,self.base_url,event['d'].get('guild_id')) #just in case
                       before = guild.presences[presence_idx]
                       self.allGuilds[guild_idx].presences[presence_idx] = new_presence
                       await self.events.on_presence_update(before,new_presence)
                     presence_idx += 1
                 guild_idx += 1
           if event['t'] == "GUILD_CREATE":
             guild = AllGuild(self,event['d'],self.cdn,self.token,self.base_url)
             self.allGuilds.append(guild)
             await self.events.on_guild_create(guild)

           if event['t'] == "GUILD_DELETE":
             idx = 0
             deleted_guild = None
             for guild in self.allGuilds:
               if guild.id == event['d']['id']:
                 deleted_guild = self.allGuilds[idx]
                 self.allGuilds.pop(idx)
               idx += 1
             await self.events.on_guild_delete(deleted_guild)

           if event['t'] == "GUILD_MEMBER_ADD":
             member = Member(self,event['d'],self.cdn,self.token,self.base_url,event['d']['guild_id'])
             idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 self.allGuilds[idx].members.append(member)
               idx += 1
             await self.events.on_guild_member_add(event['d']['guild_id'],member)

           if event['t'] == "GUILD_MEMBER_REMOVE":
             member = User(self,event['d']['user'],self.base_url,self.token,self.cdn)
             idx = 0
             for guild in self.allGuilds:
               if guild.id == event['d']['guild_id']:
                 midx = 0
                 for member in self.allGuilds[idx].members:
                   if member.id == event['d']['user']['id']:
                     self.allGuilds[idx].members.pop(midx)
               idx += 1
             await self.events.on_guild_member_remove(event['d']['guild_id'],member)

           if event['t'] == "MESSAGE_DELETE":
             await self.events.on_message_delete(event['d']['id'],event['d']['channel_id'],event['d']['guild_id'])
             await self.fetch.getMessage(event['d']['channel_id'],event['d']['id'])
           if event['t'] == "MESSAGE_CREATE":
             await self.events.on_message_create(Message(event['d'],self.token,agent,self.base_url,self.cdn,self))
             if event['d']['content'].startswith(self.prefix):
               try:
                 message = Message(event['d'],self.token,agent,self.base_url,self.cdn,self)
                 func = message.content.replace(self.prefix,"")
                 args = func.split(" ")
                 thing = getattr(self, args[0])
                 if callable(thing) and not "__" in args[0] and args[0] != "RUN" and args[0] != "LISTEN":
                   try:
                     command_args = splitArgs(thing,message.content,self.prefix+args[0],self,message.mentions,message.mention_roles)
                     await thing(message,*command_args)
                   except Exception as e:
                     print(f"\033[91mIgnoring exception: {e} \n Traceback: \033[0m")
                     traceback.print_exc()
               except AttributeError as e:
                 if args[0] in str(e):
                   print(f"\033[91mCommand '{args[0]}' not found as a command.\033[0m")
      except Exception as e:
        print(f"\033[91mDisconnected with error {e}, reconnecting...\033[0m")
        traceback.print_exc()
        self.allGuilds = []
        reconnect = True