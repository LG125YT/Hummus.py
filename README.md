# Hummus.py

## Getting started

Download these files and put them in a folder named "hummus". Next to the hummus folder, create your main file. You can use the following code in the main file to connect to Hummus:
```py
import hummus
from hummus.main import Client

class Commands(Client):
    def test(self,ctx:hummus.message.Message):
        print(ctx.content)
        ctx.reply(f"<@{ctx.author.id}> activated test!")


Commands(prefix="!",bottoken="INSERT TOKEN HERE", status="online", game="!test")
```

Adding new commands is as simple as creating new functions under the `Commands` class. You cannot add custom arguments to your functions yet, so they will have to only have the arguments of `self` and `ctx:hummus.message.Message`.

## Installation
Once this actually becomes decent enough I'll push it to pypi so you can install with pip. For now just download the files and import them locally.

## Usage

Currently there is little to no functions on Hummus.py. For now, you can use a getUser function where you can get any user with their ID. Here's an example:
```py
    def avatar(self,ctx:hummus.message.Message):
      print(len(ctx.mentions))
      print(ctx.mentions)
      if len(ctx.mentions) > 0:
        member = ctx.getUser(ctx.mentions[0])
        ctx.reply(member.avatar.url)
      else:
        ctx.reply(ctx.author.avatar.url)
```

As you can see, the above code fetches a member based on the first mention that is in the recieved command, and uses the Member object to get their avatar url.

## Support
I am LG125YT#2241 on Hummus, @ytlg on Discord, and @lg125yt on Replit.

## Roadmap
Currently attempting to add all endpoints from the [Hummus API docs]() beginning with most important for bot development.

## Contributing
Contribute if you want, you can make a pull request here, comment on the [Replit project](https://replit.com/@LG125YT/Classes-or-something-ig#main.py)

## Authors
This wrapper was made by LG125YT.