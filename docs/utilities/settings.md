# Client Settings

Hummus.py can process some events differently, depending on the client settings provided. These settings are client-side and allow for easier bot development.

Start off by importing the `ClientSettings` class from `hummus.utils` and creating an object:
```py
from hummus.utils import ClientSettings

settings = ClientSettings(reply_to_bots=True) #param would default to False otherwise

bot = Client(token="token",settings=settings)

asyncio.run(bot.run())
```

All parameters in the `ClientSettings` object are optional booleans.

## Available settings:

- `split_by_quotations`
	- Determines whether arguments can be split by quotation marks and spaces instead of just spaces (see the Arguments section in the Commands page for more info).
	- Defaults to `True`.
- `reply_to_bots`
	- Determines whether commands will be executed if the command is run by a bot account.
	- Defaults to `False`.
- `reply_to_self`
	- Determines whether commands will be executed if the command is run by the client.
	- Defaults to `False`.
- `apply_to_events`
	- Determines whether `reply_to_bots` and `reply_to_self` is also enforced in the `on_message_create` function.
	- Defaults to `True`.
- `logging`
	- Determines whether statements like "restarting..." and "ready" are automatically printed to console or not. Does not apply to exceptions.
	- Defaults to `True`.