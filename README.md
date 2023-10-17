# Hummus.py

This is an asynchronous wrapper currently in version 0.2.0!

## Getting started

Download these files and put them in a folder named "hummus". Next to the hummus folder, create your main file. You can use the following code in the main file to connect to Hummus:
```py
import hummus
from hummus.main import Client
import asyncio

class Commands(Client):
    async def test(self,ctx:hummus.message.Message):
        print(ctx.content)
        await ctx.reply(f"<@{ctx.author.id}> activated test!")


Client = Commands(prefix="!",bottoken="INSERT TOKEN HERE", status="online", game="!test")

asyncio.run(Client.run())
```

Adding new commands is as simple as creating new functions under the `Commands` class. Adding custom arguments is as simple as adding **optional** kwargs in a function, as seen below (remember: In every function, you must have the `self` and `ctx:hummus.message.Message` args!):

```py
class Commands(Client):
    async def test(self,ctx:hummus.message.Message,test=None): #extra "test" arg
        print(test)
        print(ctx.content)
        await ctx.reply(f"<@{ctx.author.id}> activated test! Provided args: {test}")
        if not ctx.dm:
          await ctx.getGuild(ctx.guild)
```

You **must** make custom arguments **optional**, or they will not work. Read the "Arguments" section of the README (right below this) for more information on how arguments work.

## Arguments

There are 2 ways to have arguments in a Hummus.py command:
1. Add custom optional arguments to your function
2. Use `.split(" ")` to split words in a command into different items on a list

Custom arguments in a function will function differently than using `.split(" ")`. The argument system looks for quotation marks in a message, and if there is text within quotation marks, no matter if there are spaces, the entire text (within the quotations!) will be considered as a **single** argument. This allows for easier usage of commands like `!nickname` where you can specify a nickname with spaces, as long as the nickname is within quotation marks.

Quotation marks are not necessary for arguments with no spaces!

## Installation

Once this actually becomes decent enough I'll push it to pypi so you can install with pip. For now just download the files and import them locally.

## Usage

### Commands

Currently there is little to no functions on Hummus.py. For now, you can use a getUser function where you can get any user with their ID. Here's an example:
```py
class Commands(Client):
    async def avatar(self,ctx:hummus.message.Message):
      print(len(ctx.mentions))
      print(ctx.mentions)
      if len(ctx.mentions) > 0:
        member = ctx.getUser(ctx.mentions[0].id)
        await ctx.reply(member.avatar.url)
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
  async def kick(self,ctx:hummus.message.Message):
    if len(ctx.mentions) > 0:
      perms = await fullPermsCheck(ctx,self,"kick_members",ctx.mentions[0])
      member = await ctx.getUser(ctx.mentions[0])
      if perms:
        e = await member.kick()
        if e.staus_code == 200 or e.status_code == 204:
          await ctx.reply(f"i have kicked <@{member.id}>!")
        else:
          await ctx.reply(f"Error kicking user. Status code: {e.status_code}")
      else:
        await ctx.reply(f"You do not have the perms to kick {member.user.username}!")
    else:
      await ctx.reply("Please ping someone to kick them.")
```

Hummus's API is very unfinished, which means fetching a guild member with the endpoint doesn't exist, as is with many other endpoints. Therefore, Hummus.py has to rely on login information for necessary info such as role permissions. Because I am lazy and don't know how Hummus/Discord's permissions integers works, Hummus.py now uses Discord.py as a dependency (it has a needed permissions function). However, this is mainly a package process, which means you don't need to manually import Discord.py in your main bot code, you just need to have it installed.

### Events

You can use events to execute code, as demonstrated below.

```py
from .events import Events

class Events(Events):
        async def on_message_create(self, message):
            if message.content.startswith("!ping"):
                await message.reply("pong")
```

Make sure to put this in your main file, before your `Client` class. You will also want to include this class as the `events` parameter when running the `Client` class, as shown below:

```py
Commands(prefix="!",bottoken=token, status="online", game="!test", events=Events())
```

Events are a WIP, expect some bugs and a lot of missing events.

## Support
I am LG125YT#2241 on Hummus, @ytlg on Discord, and @lg125yt on Replit.

## Roadmap
Currently attempting to add all endpoints from the [Hummus API docs](https://hummus.sys42.net/developers/docs/intro) beginning with most important for bot development.

## Contributing
Contribute if you want, you can make a pull request here, comment on the [Replit project](https://replit.com/@LG125YT/Classes-or-something-ig#main.py)

## Authors
This wrapper was made by LG125YT.