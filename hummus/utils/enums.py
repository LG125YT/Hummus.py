import random

class Enums:
	class Presence:
		online = "online"
		idle = "idle"
		do_not_disturb = "dnd"
		invisible = "invisible"

	class Status:
		playing = 1
		listening_to = 2
		watching = 3

	class Channel:
		text = 0
		dm = 1
		voice = 2
		gc = 3

	class DefaultAvatars:
		all = ("https://hummus.sys42.net/assets/6debd47ed13483642cf09e832ed0bc1b.png","https://hummus.sys42.net/assets/322c936a8c8be1b803cd94861bdfa868.png","https://hummus.sys42.net/assets/dd4dbc0016779df1378e7812eabaa04d.png","https://hummus.sys42.net/assets/0e291f67c9274a1abdddeb3fd919cbaa.png","https://hummus.sys42.net/assets/1cbd08c76f8af6dddce02c5138971129.png") #cause ziad is stupid and didnt put the default avatars under /embeds/avatars
		blue = "https://hummus.sys42.net/assets/6debd47ed13483642cf09e832ed0bc1b.png"
		gray = "https://hummus.sys42.net/assets/322c936a8c8be1b803cd94861bdfa868.png"
		green = "https://hummus.sys42.net/assets/dd4dbc0016779df1378e7812eabaa04d.png"
		yellow = "https://hummus.sys42.net/assets/0e291f67c9274a1abdddeb3fd919cbaa.png"
		red = "https://hummus.sys42.net/assets/1cbd08c76f8af6dddce02c5138971129.png"

	class Permissions:
		add_reactions = "add_reactions"
		administrator = "administrator"
		attach_files = "attach_files"
		ban_members = "ban_members"
		change_nickname = "change_nickname"
		connect = "connect"
		create_instant_invite = "create_instant_invite"
		deafen_members = "deafen_members"
		embed_links = "embed_links"
		external_emojis = "external_emojis"
		kick_members = "kick_members"
		manage_channels = "manage_channels"
		manage_emojis = "manage_emojis"
		manage_guild = "manage_guild"
		manage_messages = "manage_messages"
		manage_nicknames = "manage_nicknames"
		manage_roles = "manage_roles"
		manage_webhooks = "manage_webhooks"
		mention_everyone = "mention_everyone"
		move_members = "move_members"
		mute_members = "mute_members"
		read_message_history = "read_message_history"
		read_messages = "read_messages"
		send_messages = "send_messages"
		send_tts_messages = "send_tts_messages"
		speak = "speak"
		use_voice_activation = "use_voice_activation"

	#copied from fossbotpy lol
	class Colors:
		default = 0 #just another name for black ig
		aqua = 0x1ABC9C
		dark_aqua = 0x11806A
		green = 0x2ECC71
		dark_green = 0x1F8B4C
		blue = 0x3498DB
		dark_blue = 0x206694
		purple = 0x9B59B6
		dark_purple = 0x71368A
		magenta = 0xE91E63
		dark_magenta = 0xAD1457
		gold = 0xF1C40F
		dark_gold = 0xC27C0E
		orange = 0xE67E22
		dark_orange = 0xA84300
		red = 0xE74c3C
		dark_red = 0x992D22
		light_gray = 0xBCC0C0
		gray = 0x95A5A6
		dark_gray = 0x979C9F
		darker_gray = 0x7F8C8D
		og_blurple = 0x7289DA
		ruined_blurple = 0x586AEA
		blurple = 0x5865F2
		greyple = 0x99AAB5
		dark_them = 0x36393F
		not_quite_black = 0x23272A
		dark_but_not_black = 0x2C2F33
		white = 0xFFFFFE #thx dolfies for noting that 0xFFFFFF doesn't work
		fuchsia = 0xEB459E
		yellow = 0xFEE75C
		navy = 0x34495E
		dark_navy = 0x2C3E50

		@staticmethod
		def get_random_color():
			return random.randint(0x000000, 0xFFFFFF)

		@staticmethod
		def get_byte(value, byte):
			return (value >> (8*byte)) & 0xFF

		@staticmethod
		def from_rgb(*args):
			newArgs = [0,0,0]
			if type(args[0]) in (list, tuple):
				newArgs[0],newArgs[1],newArgs[2] = args[0]
			else:
				newArgs = list(args)
			return (newArgs[0]<<16) + (newArgs[1]<<8) + newArgs[2]

		@staticmethod
		def to_rgb(c):
			return (Enums.Colors.get_byte(c,2), Enums.Colors.get_byte(c,1), Enums.Colors.get_byte(c,0))

		@staticmethod
		def get(*args): #accepts decimal, hex, rgb
			#args -> c
			if len(args) == 3:
				c = args
			elif len(args) == 1:
				c = args[0]
			else:
				raise ValueError("Expected either decimal, hex, or rgb input.")
			#parse c (color input)
			if isinstance(c, tuple) or isinstance(c, list):
				result = Enums.Colors.from_rgb(c)
			elif isinstance(c, str):
				if c.startswith("0x"):
					result = int(c, 0)
				else:
					c = c.lower()
					if c == "random":
						result = Enums.Colors.get_random_color()
					else:
						key = c.replace("grey", "gray")
						if key in dir(Enums.Colors):
							result = getattr(Enums.Colors,key)
						else:
							result = int(c, 16)
			else:
				result = c
			return result