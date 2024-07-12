# Custom Statuses

You can make your bot display a custom status when it is online. You can set a presence, activity, and activity name with Hummus.py. Create an instance of the `CustomStatus` object from `hummus.utils` and pass it as an argument when creating a `Client` object instance.

```py
import hummus

status = hummus.utils.CustomStatus(game="with Hummus.py!")

bot = hummus.Client(token="TOKEN",custom_status=status)

asyncio.run(bot.run())
```

## Available parameters:
- `status`
	- Type `str`. Also known as a presence. Determines whether the account is online, idle, DND, or invisible. See the "Presences" sections in the [enums page](enums.md) on how to set them.
	- Defaults to `"online"`.
- `type`
	- Type `int`. Determines whether the account will have a status of "playing", "listening to", "watching", etc. See the "Statuses" sections in the [enums page](enums.md) on how to set them.
	- Defaults to `1`.
- `game`
	- Type `str`. This is the text that goes along with the "playing" (or other) status type. If left empty, the account will not show any status.
	- Defaults to `None`.
- `url`
	- Type `str`. If set along with a "Playing" status (`1`), account will show a "Streaming" status instead. Must provide a valid Twitch url to work.
	- Defaults to `None`.

## Updating status mid-session
You can update an account's status mid-session. The `update_status` function is available in the `HTTP` class, which can be found in any `instance` attribute in almost every class in the package (remember that `instance` is a `hummus.Client` object). This function requires a `CustomStatus` object to be passed through.

Here is an example where an account status updates for every message event it recieves:
```py
import hummus

msgs = 0

class Client(hummus.Client):
	async def on_message_create(self,message:hummus.Message):
		msgs += 1
		status = hummus.utils.CustomStatus(game=f"detected {msgs} messages while online!")
		await self.http.update_status(status)

bot = hummus.Client(token="TOKEN")

asyncio.run(bot.run())
```