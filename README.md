# Hummus.py

This is an asynchronous wrapper currently in version 0.6.0!

## Installation

You can do `pip install hummus2016.py` to install Hummus.py as a package, or you can import it manually by downloading the files at [the GitLab repository](https://gitlab.com/lg125yt/hummus.py)

## Getting started

You can use the following code in the main file to connect to Hummus:
```py
import hummus
from hummus import Client
import asyncio

class Commands(Client):
	async def test(self,ctx:hummus.Message):
		print(ctx.content)
		await ctx.reply(f"<@{ctx.author.id}> activated test!")

Client = Commands(prefix="!",bottoken="INSERT TOKEN HERE", status="online", game="!test")

asyncio.run(Client.RUN())
```

Adding new commands is as simple as creating new functions under the `Commands` class. No need for decorators, just because. Adding custom arguments is as simple as adding parameters in a function, as seen below (remember: In every function, you must have the `self` and `ctx` args!):

```py
class Commands(Client):
	async def test(self,ctx:hummus.Message,test=None): #extra "test" arg
		print(test)
		print(ctx.content)
		await ctx.reply(f"{ctx.author.mention} activated test! Arg 1: {test}") #you can also do "<@{ctx.author.id}>" if you want
```

You can make these parameters have annotations (`test: str` or `mention: hummus.User`) or have default values (`test=None`).

## Arguments

There are 2 ways to have arguments in a Hummus.py command:
1. Add extra arguments to your function
2. Use `.split(" ")` to split words in a command into different items on a list

Custom arguments in a function will function differently than using `.split(" ")`. The argument system looks for quotation marks in a message, and if there is text within quotation marks, no matter if there are spaces, the entire text (within the quotations!) will be considered as a **single** argument. This allows for easier usage of commands like `!nickname` where you can specify a nickname with spaces, as long as the nickname is within quotation marks.

Quotation marks are not necessary for arguments with no spaces!

## Usage

### Commands

Hummus.py is in development, so it will not have all the functions existing. Also, please note that the Hummus API itself is unfinished and is missing endpoints, so I cannot have every function either.

Here's an example on how to use the `ctx.getUser()` function where you can get any user with their ID:

Without parameter and annotation:
```py
class Commands(Client):
	async def avatar(self,ctx:hummus.Message):
		if len(ctx.mentions) > 0:
			member = ctx.getUser(ctx.mentions[0].id)
			await ctx.reply(member.avatar.url)
		else:
			await ctx.reply(ctx.author.avatar.url)
```

With parameter and annotation:
```py
class Commands(Client):
	async def avatar(self,ctx:hummus.Message,mention:hummus.User=None):
		if mention: #"None" is equivalent to "False"
			await ctx.reply(mention.avatar.url)
		else:
			await ctx.reply(ctx.author.avatar.url)
```

As you can see, the above code fetches a member based on the first mention that is in the recieved command, and uses the Member object to get their avatar url.

### Moderation Commands (or commands requiring permissions)

You can get access to Hummus.py's permissions checking feature with `from hummus.funcs import fullPermsCheck`. Its arguments are the `Message` object you recieve on command, your class instance aka `self`, the permission you want to check, and **optionally,** the target user ID to compare permissions with. What the `fullPermsCheck()` function does is that it checks to see if the user has the required permission, and it also checks whether it has a higher role than the target ID when specified (permissions comparing). You would use the function like this:

```py
perms = await fullPermsCheck(ctx,self,"kick_members",ctx.mentions[0]) #assume this is in a command function
```

The code would return a `bool` object which you could use to verify that the user executing the command has the required permissions.

So, for commands that require permissions such as kicking members, the **optimal** code would be the following:

```py
class Commands(Client):
	async def kick(self,ctx:hummus.Message,mention:hummus.User=None):
		if not mention:
			await ctx.reply("Please mention a user to kick them.")
			return
		perms = await fullPermsCheck(ctx,self,"kick_members",mention)
		member = await ctx.getUser(mention)
		if perms:
			e = await member.kick()
			if e.staus_code == 200 or e.status_code == 204: #i dont remember which status code it is lol
				await ctx.reply(f"i have kicked <@{member.id}>!")
			else:
				await ctx.reply(f"Error kicking user. Status code: {e.status_code}")
		else:
			await ctx.reply(f"You do not have the perms to kick {member.user.username}!")
```

Existing moderation commands you can use:
- `member.kick()`
- `member.nick()`
- `ctx.deleteMessage()`
- `ctx.bulkDelete()`
- `ctx.delete()`

Hummus's API is very unfinished, which means fetching a guild member with the endpoint doesn't exist, as is with many other endpoints. Therefore, Hummus.py has to rely on login information for necessary info such as role permissions. Because I am lazy and don't know how Hummus/Discord's permissions integers works, Hummus.py now uses Discord.py as a dependency (it has a needed permissions function). However, this is mainly a package process, which means you don't need to manually import Discord.py in your main bot code, you just need to have it installed.

### Editing Channel Permissions

You can modify channel permissions like so. The code below adds "mention everyone" permissions to a role.

```py
	async def pingEveryone(self,ctx:hummus.Message,role:hummus.Role):
		overwrite = PermOverwrites(role)
		overwrite.allow.mention_everyone = True
		e = await ctx.channel.changePerms(role,overwrite)
		print(e)
		await ctx.send("@everyone")
```

Note: Only using the above code is not recommended, it does **not** have permissions checking. See the section directly above this section on permissions checking.

### Events

You can use events to execute code, as demonstrated below.

```py
from hummus import Events

class Events(Events):
	async def on_message_create(self, message): #activates every time a message is sent in a channel a bot can see
		if message.content.startswith("ping"):
			await message.reply("pong")
```

Make sure to put this in your main file, before your `Client` class. You will also want to "listen" for this class before running the `Client` class, as shown below:

```py
Client = Commands(prefix="!", bottoken=token, status="online", game="!test")

async def bot():
	await Client.LISTEN(Events())
	await Client.RUN()

asyncio.run(bot())
```

Events are a WIP, expect some bugs and a **lot** of missing events.

### Embeds

You can create an embed object by importing the `Embed` class from `hummus`.

```py
from hummus import Embed

class Commands(Client):
async def test(self,ctx:hummus.Message):
	embed = Embed(title="Test",description="something")
```

The `Embed` class supports 4 parameters: `title`, `description`, `color`, and `timestamp`. The `color` parameter uses Discord's integer colors, view the list [here.](https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812) The `timestamp` parameter uses the ISO8601 format (what Hummus accepts), so here's the code to get the current time in that format.

```py
from datetime import datetime,timezone
current_time_utc = datetime.now(timezone.utc)
formatted_timestamp = current_time_utc.isoformat()
```

You can add attributes to the embed such as fields, footers, a thumbnail, an image, or an author like this:

```py
class Commands(Client):
async def test(self,ctx:hummus.Message):
	embed = Embed(title="Test",description="something")
	await embed.addField(name="field title",value="field value")
	await embed.addAuthor(name="author",url="https://google.com/",icon_url="https://www.google.com/favicon.ico")
	await embed.addFooter(text="foot",icon_url="https://www.google.com/favicon.ico")
	await embed.addThumbnail(url="https://google.com/favicon.ico")
```

Sending an embed is as expected, you would include it in the `ctx.send()` or `ctx.reply()` function like this:

```py
class Commands(Client):
async def test(self,ctx:hummus.Message):
	embed = Embed(title="Test",description="something")
	await embed.addField(name="field title",value="field value")
	await ctx.reply("its an embed!",embed=embed)
```

**__Note:__ Embeds will be ignored if an attachment is also passed!**

### Attachments

Attachments are quite simple. Create a `File` object instance, and pass it through the `file` parameter in `ctx.send()` or `ctx.reply()`.

A `File` object can take 4 different types of parameters. Here is a list of them and their examples:

1. `str`: `file = hummus.File("path/to/file.here")`
2. `io.BufferedReader`: `file = hummus.File(open("file.png","rb"))`
3. `bytes`: `file = hummus.File(open("file.png","rb").read())` (`.read()` returns a `bytes` object)
4. `BytesIO`: `file = hummus.File(BytesIO(b""))` (BytesIO accepts a `bytes` object, `File` gets it)

A use case is the following:
```py
class Commands(Client):
async def test(self,ctx:hummus.Message):
	await ctx.reply("its an image!",file=hummus.File("image.png"))
```

**__Note:__ Embeds will be ignored if an attachment is passed!**

## Support
I am LG125YT#2241 on Hummus, @ytlg on Discord, LG125YT#3014 on Oldground, and @lg125yt on Replit. My email is lg125yt@gmail.com, but you might want to let me know somewhere else that you sent me an email.

## Roadmap
Currently attempting to add all endpoints from the [Hummus API docs](https://hummus.sys42.net/developers/docs/intro) beginning with most important for bot development.

## Changelog

Version 0.6.0:
- `AllGuild` now inherits from `Guild` instead of making a `Guild` attribute in the class.
- New `Channel` and `Emoji` objects exist, which arw available in an `AllGuild` object. `PermOverwrites` is also a new object that you can create instances of to edit channel permissions.
- ~~All~~ Most events are added. In the middle of this update, banning has been added to Hummus and Oldground, and the events and functions do not exist for it yet.
- Hummus.py now supports catching websocket errors, and auto-restarts if an error occurs (such as heartbeat expiring).
- `fullPermsCheck()` now correctly checks for server owner ID before returning whether the user has a specific permission.
- `Channel` object attributes now have support for both voice and text channels.
- `User` and `Member` now have role-related functions (`addRoles`, `removeRoles`, and `setRoles`)
- Many of these new objects have a `toDict()` function, however, this should be mainly internal.
- `Message` objects now have a `guild` and `channel` attribute containing the entire `Guild` and `Channel` objects (respectively). The old attributes that only had the ID are now called `guild_id` and `channel_id`.
- `getGuildChannels()` exists as a function in a `Message` object.
- The `Permissions` object now supports empty/fake role creation and the creation of a role with only a permissions integer.
- The `Role` object now has a `Permissions` object for their `permissions` attribute.
- The `bottoken` parameter name has been changed to `token` when creating a `Client`/`Commands` object.
- Hummus.py will now get the cdn url from the base url provided, no need to provide a cdn url when creating a `Client`/`Commands` object now.

Version 0.5.2:
- Again, no real changes to hummus.py, but I'm pretty sure I figured out how to fix the previous error. Also, `hmus` exists as a mirror package now if you don't want to type in `hummus2016.py` to install the package.

Version 0.5.1:
- No real changes, I'm just trying to fix the pypi issue where `import hummus` doesnt work. Also updating this file a little to be more up-to-date.

Version 0.5.0:
- You now need to upload files by creating a `File` object with your file in it. This allows for less cluttering in `message.py` for the `send` function, and it allows me to easily add more freedom to uploading files.
- Continuation of above note, you can now provide a file path, `bytes` object, `BytesIO` object, or an `io.BufferedReader` object (the object you get when you assign a variable to `open("name.ext","rb")`)
- All `Message` objects now have a `delete()` function, which sends a request to delete that message on Hummus. (Previously, we only had `deleteMessage(id)`, where you needed to provide a message ID to delete.)
- For some reason, the v0.4.x versions have not been updating the `hummus` folder, and only the `hummus2016` folder. If it persists, consider switching all `from hummus import *` and `import hummus` to `from hummus2016 import *` and `import hummus2016`. This may also require changing some other lines, or you can use `import hummus2016 as hummus`.

Version 0.4.1:
- Updates in 0.4.0 didn't push for some reason lol. Here they are (again).
- Turns out that the Image and Thumbnail objects *do* work, they just require `width` and `height` parameters that Hummus.py will automatically take care for you. Nothing has changed, you can continue uploading files as before.
- Fixed bug not letting Hummus.py work, its just me forgetting to include headers when making the request to get the websocket url.

Version 0.4.0:
- Added embed support (Image and Thumbnail objects to not work on Hummus, so they are not included in Hummus.py)
- Added attachment support (You only have to include the filepath)

Version 0.3.4:
- Fixed `ctx.edit()` so that it edits only the "content" section of the "reply" from `ctx.reply()` (basically it doesn't edit the whole message)
- Added a new `is_reply` (boolean), `original_reply` (content of the message being replied to), and `original_author` (`User` class) attributes to the `Message` object
	- `is_reply` is entirely local, it is only true for a message object where the `ctx.reply()` function is used, and cannot detect replies outside of `ctx.reply()`
- Errors caught by the package exception handler now print out the traceback
- Minor changes to the README

Version 0.3.3:
- Updated the README (this thingy you're reading!) to not have the wackiest indents (frick you replit)

Version 0.3.2:
- Fixed hummus.py not working when you didn't manually register an `Events` class to listen.

Version 0.3.1:
- Quick update just added `ctx.deleteMessage(id)` because i forgor to add it before :sku:

Version 0.3.0:
- More events in the `Events` class work now, also `self.allGuilds` in the `Client` class now updates on related events like guild member join/leave and guild add/remove
- `Client` class initialization redone a little, see the "Getting Started" and "Events" section in this README
- Command args should now fully work, you do not need to add a default value to parameters and some annotations (namely `str`,`int`, and `hummus.member.User`) now work
- The `Author` class has been renamed to the `User` class because most use cases within the package do not reflect the "Author" status of a user (this should not affect much of anything since annotations did not work before this update)


Too lazy to like do anything from before, if you want to do it for me, go for it.

## Contributing
Contribute if you want, you can make a pull request on the [GitLab repository](https://gitlab.com/lg125yt/hummus.py), comment on the [Replit project.](https://replit.com/@LG125YT/Classes-or-something-ig#main.py) Note that the Replit project is the most recent version of Hummus.py, because it is where I test new features. You can see upcoming features on the Replit project if you want.

## Authors
This wrapper was made by LG125YT. Contact me on Hummus (LG125YT#2241) or Discord (@ytlg)