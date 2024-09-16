#welcome to stupidity central
import websockets
from websockets.sync.client import connect
import _thread as thread
import fake_useragent
import traceback
import requests
import inspect
import asyncio
import json
import time

from .utils import Commands, CustomStatus, ClientSettings
from .utils import Context,CustomizableExceptions
from .user import User, Member, Presence
from .guild import PartialGuild, Guild
from .guild import Channel, Emoji
from .message import Message
from .ready import Ready
from .role import Role
from .http import HTTP

from datetime import datetime
from typing import *

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])
agent = ua.random


async def splitArgs(function,message,instance):
	func_args = list(inspect.signature(function).parameters.values())[1:]
	custom_kwargs = []

	args = message.content.replace('“','"').replace('”','"').replace("‘","\"").replace("’","\"").split() #filtering

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

		if arg.startswith("\"") and not arg.endswith("\"") and instance.settings.split_by_quotations:
			in_quotes = True
			current_arg = arg.strip("\"")
		else:
			refined.append(arg)

	role_mention_idx = 0
	mention_idx = 0
	idx = 0
	mentioned = dict()
	for arg_name, arg in zip(func_args, refined):
		if idx >= len(refined):
			break

		if arg_name.annotation == str:
			custom_kwargs.append(str(arg))
		elif arg_name.annotation == int:
			try:
				custom_kwargs.append(int(arg))
			except Exception:
				await instance.custom_exceptions.onInvalidInteger(arg,message)
		elif arg_name.annotation == bool:
			if arg.lower() == "true":
				custom_kwargs.append(True)
			elif arg.lower() == "false":
				custom_kwargs.append(False)
			else:
				await instance.custom_exceptions.onInvalidBoolean(arg,message)
		elif arg_name.annotation == Role:
			clean = arg.replace("<@&","").replace(">","")
			try:
			    if not (arg.startswith("<@&") and arg.endswith(">")) and not (clean in [str(r.id) for r in message.mention_roles] or mentioned.get(clean)):
			        raise Exception
			    if mentioned.get(clean):
			        custom_kwargs.append(mentioned[clean])
			    else:
			        custom_kwargs.append(message.mention_roles[role_mention_idx])
			        mentioned[clean] = message.mention_roles[role_mention_idx]
			        role_mention_idx += 1
			except Exception as e:
			    await instance.custom_exceptions.onInvalidRole(arg,message)
		elif arg_name.annotation == User:
			clean = arg.replace("<@","").replace(">","").replace("!","")
			if not arg.startswith("<@") and not arg.endswith(">") and not (clean in [str(m.id) for m in message.mentions] or mentioned.get(clean)):
				return await instance.custom_exceptions.onInvalidMention(arg,message)
			if mentioned.get(clean):
				custom_kwargs.append(mentioned[clean])
			else:
				m = message.mentions[mention_idx]
				custom_kwargs.append(m)
				mentioned[clean] = m
				mention_idx += 1
		elif arg_name.annotation == Member:
			clean = arg.replace("<@","").replace(">","").replace("!","")
			try:
				if not arg.startswith("<@") and not arg.endswith(">") and not (clean in [str(m.id) for m in message.mentions] or mentioned.get(clean)):
					raise Exception #User.getGuildMember() can also raise an exception that should be caught, so we do not return here
				if mentioned.get(clean):
					custom_kwargs.append(mentioned[clean])
				else:
					m = await message.mentions[mention_idx].getGuildMember()
					custom_kwargs.append(m)
					mentioned[clean] = m
					mention_idx += 1
			except Exception:
				await instance.custom_exceptions.onInvalidMention(arg,message)
		elif arg_name.annotation == Channel:
			found = False
			for channel in message.guild.channels:
				if f"<#{channel.id}>" == arg:
					found = True
					custom_kwargs.append(channel)
					break
			if not found:
				return await instance.custom_exceptions.onInvalidChannel(arg,message)
		else:
			custom_kwargs.append(arg)

		idx += 1
	return custom_kwargs


default_exceptions = CustomizableExceptions()
default_settings = ClientSettings()
default_status = CustomStatus(type=0)

class Client:
	def __init__(self,token,commands:Union[Commands,None]=None,url="https://hummus.sys42.net/api/v6/",cdn=None,custom_status:CustomStatus=default_status,exception_handler:CustomizableExceptions=default_exceptions,settings:ClientSettings=default_settings):
		self.websocket = ""
		self.ping = None
		self.state:Ready = None #type:ignore
		self.custom_exceptions:CustomizableExceptions = exception_handler
		self.commands:Union[Commands,None] = commands
		self.settings:ClientSettings = settings
		if isinstance(commands,Commands):
			self.prefix = commands.prefix
			self.commands.instance = self #type:ignore
		elif commands is None:
			self.prefix = None
		else:
		    raise TypeError("Commands must be of type Commands.")
		self.s = requests.session()
		self.s.headers = {"Authorization":token,"Content-Type":"application/json","User-Agent":agent}
		self.http:HTTP = HTTP(self)
		if not url.endswith("/"):
			url = url + "/"
		e = requests.get(url+"gateway",headers={"User-Agent":agent})
		if e.json().get('url'):
			self.websocket = e.json()['url']+"?api=v6&encoding=json"
			if not self.websocket.startswith("wss://"):
				self.websocket = "wss://" + self.websocket
		else:
			raise Exception("Please tell the website owner to add '/gateway' as an API endpoint.")
		if cdn:
			self.cdn = cdn
		else:
			cdn = url.split(".")
			cdn[0] = cdn[0]+"-cdn"
			cdn = ".".join(cdn)
			self.cdn = cdn.replace("api/","").replace("v6/","")
		if not self.cdn.endswith("/"):
			self.cdn = cdn + "/"
		self.status = custom_status._toJson()
		self.token = token
		self.base_url = url

	def __log(self,message): #this will likely have file logging functionality at some point
		if self.settings.logging:
			print(message)

	async def run(self):
		reconnect = False
		last_event = None
		session = ""
		seq = None
		self.guilds:list[Guild] = []
		while True:
			try:
				with connect(self.websocket,additional_headers=self.s.headers,user_agent_header=ua.random,max_size=None) as websocket:
					self.connection = websocket
					self.__log("\033[32mrestarting...\033[0m")
					if reconnect:
						self.__log(f"\033[32mResuming session with sequence ID {seq}\033[0m")
						websocket.send(json.dumps({"d":{"token":self.token,"session_id":session,"seq":seq},"op":6}))
					else:
						websocket.send(json.dumps({'op': 2,'d': {'token':self.token,'presence': self.status}}))

					while True:
						event = json.loads(websocket.recv())
						if reconnect:
						    print(event)
						if event.get('s'):
						    seq = event['s']
						if not event.get('t'):
						    event['t'] = None

						if event['t']:
						    last_event = event

						if event['t'] == "READY":
							session = event['d']['session_id']
							self.__log("\033[32mready, recieving login guild data\033[0m")
							self.state = Ready(event['d'],self)
							self.user = self.state.user
							self.__start_time = datetime.now()
							websocket.send(json.dumps({"op":1}))
							if not self.state.guilds_are_unavailable:
								self.guilds = self.state.guilds
							thread.start_new_thread(asyncio.run,(self.on_ready(self.state),))

						if event['op'] == 1:
							self.__start_time = datetime.now()
							websocket.send(json.dumps({"op":1}))

						if event['op'] == 11:
							passed = datetime.now() - self.__start_time
							self.ping = f"{passed.total_seconds()*1000} ms"

						if event['t'] == "CHANNEL_PINS_UPDATE":
							thread.start_new_thread(asyncio.run,(self.channel_pins_update(event['d']['channel_id'],event['d'].get('last_pin_timestamp')),))

						if event['t'] == "GUILD_BAN_ADD":
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									thread.start_new_thread(asyncio.run,(self.on_guild_ban_add(guild,User(event['d']['user'],self,event['d']['guild_id'])),))
									break

						if event['t'] == "GUILD_BAN_REMOVE":
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									thread.start_new_thread(asyncio.run,(self.on_guild_ban_remove(guild,User(event['d']['user'],self,event['d']['guild_id'])),))
									break

						if event['t'] == "TYPING_START":
							member = event['d'].get('member')
							channel = event['d']['channel_id']
							if member:
								is_guild = True
								member = Member(member,event['d']['guild_id'],self)
								for guild in self.guilds:
									if guild.id == event['d']['guild_id']:
										for c in guild.channels:
											if c.id == event['d']['channel_id']:
												channel = c
												break
										break
							else:
								is_guild = False
								member = event['d']['user_id']
								for dm in self.state.private_channels:
									if dm.id == event['d']['channel_id']:
										channel = dm
										for user in dm.recipients:
											if user.id == member:
												member = user
												break
										break
							thread.start_new_thread(asyncio.run,(self.on_typing_start(is_guild,channel,member,event['d']['timestamp']),))

						if event['t'] == "GUILD_MEMBER_UPDATE":
							guild_idx = 0
							member_idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									for member in guild.members:
										if member.id == event['d']['id']:
											new_member = Member(event['d'],event['d']['guild_id'],self)
											self.guilds[guild_idx].members[member_idx] = new_member
											thread.start_new_thread(asyncio.run,(self.on_guild_member_update(member,new_member),))
											break
										member_idx += 1
									break
								guild_idx += 1

						if event['t'] == "GUILD_UPDATE":
							guild_idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['id']:
									updated_guild = PartialGuild(event['d'],self)
									self.guilds[guild_idx]._update_data(updated_guild)
									thread.start_new_thread(asyncio.run,(self.on_guild_update(guild,updated_guild),))
									break
								guild_idx += 1

						if event['t'] == "GUILD_EMOJIS_UPDATE":
							guild_idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									before = guild.emojis
									after = [Emoji(emoji,self) for emoji in event['d']['emojis']]
									self.guilds[guild_idx].emojis = after
									thread.start_new_thread(asyncio.run,(self.on_guild_emojis_update(guild,before,after),))
									break
								guild_idx += 1

						if event['t'] == "GUILD_ROLE_UPDATE":
							guild_idx = 0
							role_idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									for role in guild.roles:
										if role.id == event['d']['role']['id']:
											new_role = Role(event['d']['role'],event['d']['guild_id'],self)
											self.guilds[guild_idx].roles[role_idx] = new_role
											thread.start_new_thread(asyncio.run,(self.on_guild_role_update(guild,role,new_role),))
											break
										role_idx += 1
									break
								guild_idx += 1

						if event['t'] == "GUILD_ROLE_CREATE":
							guild_idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									new_role = Role(event['d']['role'],event['d']['guild_id'],self)
									self.guilds[guild_idx].roles.append(new_role)
									thread.start_new_thread(asyncio.run,(self.on_guild_role_create(guild,new_role),))
									break
								guild_idx += 1

						if event['t'] == "GUILD_ROLE_DELETE":
							guild_idx = 0
							role_idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									for role in guild.roles:
										if role.id == event['d']['role_id']:
											deleted_role = role
											self.guilds[guild_idx].roles.pop(role_idx)
											thread.start_new_thread(asyncio.run,(self.on_guild_role_delete(guild,deleted_role),))
											break
										role_idx += 1
									break
								guild_idx += 1

						if event['t'] == "CHANNEL_CREATE":
							for dm in self.state.private_channels:
								if dm.id == event['d']['id']:
									channel = Channel(event['d'],self)
									self.state.private_channels.append(channel)
									thread.start_new_thread(asyncio.run,(self.on_channel_create(None,channel),))
							guild_idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									channel = Channel(event['d'],self)
									self.guilds[guild_idx].channels.append(channel)
									thread.start_new_thread(asyncio.run,(self.on_channel_create(guild,channel),))
									break
								guild_idx += 1

						if event['t'] == "CHANNEL_UPDATE":
							guild_idx = 0
							channel_idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									for channel in guild.channels:
										if channel.id == event['d']['id']:
											updated_channel = Channel(event['d'],self)
											self.guilds[guild_idx].channels[channel_idx] = updated_channel
											thread.start_new_thread(asyncio.run,(self.on_channel_update(guild,channel,updated_channel),))
											break
										channel_idx += 1
									break
								guild_idx += 1

						if event['t'] == "CHANNEL_DELETE":
							channel_idx = 0
							if not event['d'].get('guild_id'):
								for channel in self.state.private_channels:
									if channel.id == event['d']['id']:
										self.state.private_channels.pop(channel_idx)
										thread.start_new_thread(asyncio.run,(self.on_channel_delete(None,channel),))
										break
									channel_idx += 1
							guild_idx = 0
							for guild in self.guilds:
								if guild.id == event['d'].get('guild_id'):
									for channel in guild.channels:
										if channel.id == event['d']['id']:
											self.guilds[guild_idx].channels.pop(channel_idx)
											thread.start_new_thread(asyncio.run,(self.on_channel_delete(guild,channel),))
											break
										channel_idx += 1
									break
								guild_idx += 1

						if event['t'] == "PRESENCE_UPDATE":
							if event['d'].get('guild_id'):
								guild_idx = 0
								presence_idx = 0
								for guild in self.guilds:
									if guild.id == event['d']['guild_id']:
										for presence in guild.presences:
											if presence.user.id == event['d']['user']['id']:
												new_presence = Presence(event['d'],event['d']['guild_id'],self)
												self.guilds[guild_idx].presences[presence_idx] = new_presence
												thread.start_new_thread(asyncio.run,(self.on_presence_update(presence,new_presence),))
												break
											presence_idx += 1
										break
									guild_idx += 1
							else:
								presence_idx = 0
								for presence in self.state.presences:
									if presence.user.id == event['d']['user']['id']:
										self.state.presences[presence_idx] = Presence(event['d'],None,self)
										thread.start_new_thread(asyncio.run,(self.on_presence_update(presence,self.state.presences[presence_idx]),))

						if event['t'] == "GUILD_CREATE":
							guild = Guild(event['d'],self)
							self.guilds.append(guild)
							thread.start_new_thread(asyncio.run,(self.on_guild_create(guild),))

						if event['t'] == "GUILD_DELETE":
							idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['id']:
									self.guilds.pop(idx)
									thread.start_new_thread(asyncio.run,(self.on_guild_delete(guild),))
									break
								idx += 1

						if event['t'] == "GUILD_MEMBER_ADD":
							member = Member(event['d'],event['d']['guild_id'],self)
							idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									self.guilds[idx].members.append(member)
									thread.start_new_thread(asyncio.run,(self.on_guild_member_add(guild,member),))
									break
								idx += 1

						if event['t'] == "GUILD_MEMBER_REMOVE":
							member = User(event['d']['user'],self)
							idx = 0
							for guild in self.guilds:
								if guild.id == event['d']['guild_id']:
									midx = 0
									for member in self.guilds[idx].members:
										if member.id == event['d']['user']['id']:
											self.guilds[idx].members.pop(midx)
											thread.start_new_thread(asyncio.run,(self.on_guild_member_remove(guild,member),))
											break
										midx += 1
									break
								idx += 1

						if event['t'] == "MESSAGE_DELETE":
							guild = None
							if event['d'].get('guild_id'):
								guild_idx = 0
								for g in self.guilds:
									if g.id == event['d']['guild_id']:
										guild = g
										break
								thread.start_new_thread(asyncio.run,(self.on_message_delete(event['d']['id'],event['d']['channel_id'],guild),))

						if event['t'] == "MESSAGE_UPDATE":
							thread.start_new_thread(asyncio.run,(self.on_message_update(Message(event['d'],self)),))

						if event['t'] == "MESSAGE_CREATE":
							message = Message(event['d'],self)
							can_respond = True
							if not self.settings.reply_to_self and message.author.id == self.user.id:
								can_respond = False
							if not self.settings.reply_to_bots and message.author.bot:
								can_respond = False
							if can_respond or not self.settings.apply_to_events:
							    try:
							        await self.on_message_create(message)
							    except Exception as e:
							        print(f"\033[31mIgnoring exception: {e}\nTraceback:\033[0m")
							        traceback.print_exc()

							prefix = await self.get_prefix(message)
							if self.commands and prefix and event['d']['content'].startswith(prefix): #problem with uptime
								context = Context(message,self)
								func = message.content[len(prefix):]
								args = func.split()
								can_respond = True
								if len(args) < 1:
									can_respond = False
								if not self.settings.reply_to_self and message.author.id == self.user.id:
									can_respond = False
								if not self.settings.reply_to_bots and message.author.bot:
									can_respond = False
								if can_respond:
									try:
										command = getattr(self.commands, args[0])
										if callable(command) and not "__" in args[0]:
											try:
												command_args = await splitArgs(command,message,self)
												try:
													thread.start_new_thread(asyncio.run,(command(context,*command_args),))
												except TypeError as e:
													if "required positional argument" in str(e):
														args = str(e).split(": '")[1].replace("'","").replace(",","").replace("and","").split()
														await self.custom_exceptions.onMissingArguments(args,context)
											except Exception as ex:
												print(f"\033[31mIgnoring exception: {ex}\nTraceback:\033[0m")
												traceback.print_exc()
									except AttributeError as e:
										if self.commands.aliases and self.commands.aliases.aliases.get(args[0]):
											command = self.commands.aliases.aliases[args[0]]
											command = getattr(self.commands, command.__name__)
											try:
												command_args = await splitArgs(command,message,self)
												try:
													thread.start_new_thread(asyncio.run,(command(context,*command_args),))
												except TypeError as e:
													if "required positional argument" in str(e):
														args = str(e).split(": '")[1].replace("'","").replace(",","").replace("and","").split()
														await self.custom_exceptions.onMissingArguments(args,context)
											except Exception as e:
												print(f"\033[31mIgnoring exception: {e}\nTraceback:\033[0m")
										else:
											if args[0] in str(e):
												print(f"\033[31mCommand '{args[0]}' not found as a command or alias.\033[0m")
			except websockets.exceptions.ConnectionClosedOK as e:
			    print(f"heartbeat expiry close, {e}\nLast event: {last_event}\nAt: {datetime.now()}")
			    traceback.print_exc()
			    reconnect = True
			except Exception as e:
				print(f"\033[31mDisconnected with error {e}, reconnecting...\033[0m")
				traceback.print_exc()
				reconnect = True
				time.sleep(5)

	async def get_prefix(self,message):
		return self.prefix

	#events
	async def on_ready(self, bot):
		pass

	async def channel_pins_update(self, channel_id, last_pin_timestamp):
		pass

	async def on_message_create(self, message):
		pass

	async def on_message_delete(self, message_id, channel_id, guild): #channel id in case this is in a dm or gc and we cannot get the channel object from the corresponding guild object, guild will be None if so
		pass

	async def on_message_update(self, message):
		pass

	async def on_presence_update(self, before, presence):
		pass

	async def on_guild_ban_add(self, guild, user):
		pass

	async def on_guild_ban_remove(self, guild, user):
		pass

	async def on_guild_member_add(self, guild, member):
		pass

	async def on_guild_member_remove(self, guild, member): #unlike other events, a member object actually gets passed through! discord is not being obscure with info for once!?!?!?
		pass

	async def on_guild_member_update(self, before, after):
		pass

	async def on_guild_create(self, guild):
		pass

	async def on_guild_delete(self, guild):
		pass

	async def on_guild_update(self, before, after):
		pass

	async def on_guild_role_create(self, guild, role):
		pass

	async def on_guild_role_delete(self, guild, role):
		pass

	async def on_guild_role_update(self, guild, before, after):
		pass

	async def on_guild_emojis_update(self, guild, before, after):
		pass

	async def on_typing_start(self, is_guild, channel, user, when):
		pass

	async def on_channel_create(self, guild, channel):
		pass

	async def on_channel_delete(self, guild, channel):
		pass

	async def on_channel_update(self, guild, before, after):
		pass
