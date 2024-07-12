# Aliases

Command aliases exist primarily to link multiple command names to one command, and also to allow for commands that start with numbers.

Alias management is the only feature in Hummus.py that involve decorators. To begin, create an instance of a `hummus.utils.Aliases` class.

```py
from hummus.utils import Aliases
aliases = Aliases()
```

Adding an alias to a command is as simple as adding a decorator with the created `Aliases` instance and the `add_alias` function.

```py
import hummus
from hummus.utils import Aliases
aliases = Aliases()

class Commands(hummus.utils.Commands):
	@aliases.add_aliases(['altname'])
	async def test(self,ctx):
		await ctx.sendMessage("test command, you can use `test` or `altname` as the command name!")
```

Note that the parameter is a list of strings. Hummus.py requires that you put your aliases in a list.