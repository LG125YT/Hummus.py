# Objects

This page contains the list of all objects accessible to you and their attributes in Hummus.py.

## Notes:

1. **Important:** The entire "features" section of the documentation is very incomplete! I have not started on a lot of these! You will see that the existing objects here are **listed** but not **explained.** Sorry for the inconvenience, I haven't had the motivation to finish this very lengthy process. If you need info on matters that these pages are supposed to address, you are most likely better off contacting me for help or inspecting the code yourself to see how it works.

2. The following objects are not mentioned in this page (likely because they are covered in other pages):
- `hummus.utils.Exceptions` and `.CustomizableExceptions`
- `hummus.utils.ClientSettings`
- `hummus.utils.CustomStatus`
- `hummus.utils.Commands`
- `hummus.utils.Aliases`
- `hummus.utils.Enums`
- `hummus.internal.*`
- `hummus.FakeRole`

3. Objects listed here that do not list parameters are likely because they are created internally and not meant to be created by the user (unless stated otherwise).

### hummus.\_\_version\_\_

The version of Hummus.py, ex: `'1.0.0'`.

## hummus.Client
```py
class hummus.Client(
    token : str,
    commands : Commands = None,
    url : str = "https://hummus.sys42.net/api/v6/",
    cdn : str = None,
    custom_status : CustomStatus = default_status,
    exception_handler : CustomizableExceptions = default_exceptions,
    settings : ClientSettings = default_settings
    )
```
***
This is meant to be inherited to modify the functions of this class (you can also not inherit and use the original if you only want to create commands with the `Commands` class).

You create an instance and pass in the required `token` parameter, and you may also pass in other optional parameters to configure your project.

### Parameters:
- `token` (`str`)
    - Required, logs into the account.
- `commands` (Optional[`Commands`])
    - Optional, registers commands you create to execute them when a user activates a command. Only accepts a `Commands` object.
- `url` (Optional[`str`])
    - Optional, connect to a different website instead of Hummus. Site must run API v6 and have the `/gateway` endpoint available.
- `cdn` (Optional[`str`])
    - Optional, set a cdn url. Do not set if site cdn url is `"https://{domain}-cdn.{rest of domain}"` (example: `"https://hummus-cdn.sys42.net"`)
- `custom_status` (Optional[`CustomStatus`])
    - Optional, set the account status on login. Only accepts a `CustomStatus` object.
- `exception_handler` (Optional[`CustomizableExceptions`])
    - Optional, set actions to execute on specific exceptions using an inherited `CustomizableExceptions` class. See the Exceptions page of the Utilities section for more info.
- `settings` (Optional[`ClientSettings`])
    - Optional, set specific client settings for how the package behaves. See the Settings page of the Utilities section for more info. Only accepts a `ClientSettings` object.

### Attributes:
- `websocket` (`str`)
    - The websocket url for the site.
- `base_url` (`str`)
    - The base API url for the site.
- `cdn` (`str`)
    - The cdn url for the site.
- `token` (`str`)
    - The token passed in on initialization.
- `guilds` (List[`Guild`])
    - List of `Guild` objects received either on `READY` or through `GUILD_CREATE` events. Only filled in after bot login.
- `ping` (`str`)
    - The gateway ping, measured in milliseconds. Formatted as `f"{ping} ms"`
- `state` (`Ready`)
    - A `Ready` object containing info received on the `READY` event.
- `user` (`Self`)
    - A `Self` (user-based) object received on the `READY` event, can also be found as an attribute in `Client.state`.
- `custom_exceptions` (`CustomizableExceptions`)
    - The modified `CustomizableExceptions` object you passed through on object initialization, or the preset default if none was passed through.
- `commands` (`Commands`)
    - The modified `Commands` object you passed through on object initialization, or `None` if none was passed through.
- `settings` (`ClientSettings`)
    - The modified `ClientSettings` object you passed through on object initialization, or the preset default if none was passed through.
- `prefix` (`str`)
    - The set prefix for the client, is `None` if you did not create and pass in a `Commands` object to `Client`.
- `s` (`requests.Session`)*
    - The requests session object for the client. Meant for internal use.
- `http` (`HTTP`)
    - The HTTP object containing all HTTP-related functions, see [the HTTP page](http.md) for usage.
- `status` (`CustomStatus`)
    - JSON format of the `CustomStatus` object passed in on initialization.
- `connection` (`websockets.sync.client.ClientConnection`)*
    - The websocket connection to the server.

*This object is outside of Hummus.py.

### Functions:
- `async run()`
    - Runs the client.

__Note:__ For information on the `on_{event}` functions meant to be modified with this class, please see the [Events page.](events.md)

## hummus.utils.Context

```py
class hummus.utils.Context(...)
```

This is an object that is created internally and given to you either from a command function (on message) or an customizable exception function. You should not have to create an instance of this class for any reason.

### Attributes:
- `instance` (`Client`)
    - The `Client` object of the current session.
- `message` (`Message`)
    - The message object.
- `channel` (`Channel`)
    - The channel object.
- `guild` (Optional[`Guild`])
    - The guild object, can be `None` if message is in a gc/dm rather than in a guild channel.
- `author` (`User`)
    - The user object of the person who created the message.
- `http` (`HTTP`)
    - See the [HTTP page](http.md) for how to use this object.
- `typing` (`Typing`)
    - Made for `async with` usage (`async with ctx.typing():`)

### Functions:
- `async reply(content = "", embeds = [], file = None)`
    - Sends a message replying to the current message.
    - **Parameters:**
        - `content` - The message content.
        - `embeds` - A list of `Embed` objects.
        - `file` - A `File` object.
    - **Returns:**
        - A `Message` object.
- `async sendMessage(content = "", embeds = [], file = None)`
    - Sends a message in the current channel (same channel as current message).
    - **Parameters:**
        - `content` - The message content.
        - `embeds` - A list of `Embed` objects.
        - `file` - A `File` object.
    - **Returns:**
        - A `Message` object.
- `async startTyping()`
    - Makes the client show as typing in the current channel.
- `async getPins()`
    - Gets the pinned messages of the current channel.
    - **Returns:**
        - A list of `Message` objects.
- `async createInvite()`
    - Creates an invite for the current channel/guild.
    - **Returns:**
        - An `Invite` object.
- `async getClientMember()`
    - Gets the `Member` object of the current client for the current guild.
    - **Returns:**
        - `Member` of current client user.

***

## hummus.Embed

```py
class Embed(
    title : str,
    description : str,
    color : int = 0,
    url : str = None,
    timestamp : str = None
    )
```

Create an instance of the `Embed` object to create an embed that you can attach to messages. Pass in a list of these objects when using any message sending-related function in Hummus.py (`Context.sendMessage(embed=[embed])`).

### Parameters:
- `title` (`str`)
    - The title of the embed.
- `description` (`str`)
    - The description of the embed.
- `color` (`int`)
    - The color bordering the left side of the embed.
- `url` (`str`)
    - The masked url of the title of the embed, click the title to redirect to this url.
- `timestamp` (`str`)
    - Timestamp in ISO 8601 format, displays next to embed footer.

### Attributes:
- `title` (`str`)
    - The title of the embed.
- `description` (`str`)
    - The description of the embed.
- `color` (`int`)
    - The color bordering the left side of the embed.
- `fields` (list[`Field`])
    - A list of embed field objects, will be an empty list if there are no fields.
- `url` (`str`)
    - The masked url of the title of the embed, click the title to redirect to this url.
- `timestamp` (`str`)
    - Timestamp in ISO 8601 format, displays next to embed footer.
- `author` (`EmbedAuthor`)
    - An author section, shows right above the title of the embed.
- `footer` (`Footer`)
    - The embed footer, shows below everything.
- `thumbnail` (`Thumbnail`)
    - An image that displays on the top right corner of the embed.
- `image` (`Image`)
    - A large image that displays on the bottom (right above the footer) of the embed.

### Functions:
- `async addAuthor(name, url = None, icon_url = None)`
    - Adds an `EmbedAuthor` object to the embed.
    - **Parameters:**
        - `name` - The text showing in the author section of the embed.
        - `url` - The link go to if the author section is clicked on.
        - `icon_url` - The CDN url to the image, shows next to the name in the author section.
- `async addFooter(text, icon_url = None)`
    - Adds a `Footer` object to the embed.
    - **Parameters:**
        - `text` - The text to show at the footer section of the embed.
        - `icon_url` - The CDN url to the image, shows next to the text of the footer.
- `async addField(name, value, inline = False)`
    - Adds a `Field` object to the embed, can be done multiple times.
    - **Parameters:**
        - `name`
        - `value`
        - `inline`

async def addField(self,name:str,value:str,inline:bool=False):
    self.fields.append(Field(name,value,inline))

async def addThumbnail(self,url:str):
    self.thumbnail = Thumbnail(url)

async def addImage(self,url:str):
    self.image = Image(url)

## hummus.ImageEmbed

## hummus.Field

## hummus.Footer

## hummus.EmbedAuthor

## hummus.Thumbnail

## hummus.Image

## hummus.Provider

## hummus.Video

stuff

***

## hummus.File

## hummus.Attachment

## hummus.Icon

stuff

***

## hummus.PermissionOverwrite

## hummus.InvitePartialGuild

## hummus.Typing

## hummus.PartialChannel

## hummus.Invite

## hummus.PartialGuild

## hummus.Channel

## hummus.Emoji

## hummus.Guild

## hummus.Ban

stuff

***

## hummus.HTTPStatus

## hummus.HTTP

stuff

***

## hummus.Message

stuff

***

## hummus.Ready

## hummus.Self

## hummus.Relationship

## hummus.Application

stuff

***

## hummus.Role

## hummus.Permissions

stuff

***

## hummus.Profile

## hummus.Member

## hummus.Presence

## hummus.User