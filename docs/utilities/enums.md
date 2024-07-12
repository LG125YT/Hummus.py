# Enums

Sometimes users don't know what is available in terms of permissions, colors, presence types, etc. Hummus.py provides some enums to assist with that.

If you know most or all of these values, it is not necessary to use enums. This is just to provide assistance to other people.

To begin, simply import `Enums` from `hummus.utils`:
```py
from hummus.utils import Enums

Enums.Presence.do_not_disturb #do not disturb presence

Enums.Status.playing #"playing" custom status

Enums.Channel.text #text channel type

Enums.DefaultAvatars.gray #Hummus gray default avatar

Enums.Permissions.administrator #permissions are not integers

Enums.Colors.red #red color (for embeds and roles)
```

## Presences

Access these enums through `Enums.Presence`.

There are 4 different presence types:
1. `online`
2. `idle`
3. `do_not_disturb`
4. `invisible`

The attributes all reflect the hardcoded value assigned to them, except for `do_not_disturb` (which has the value of `"dnd"`).

## Statuses

Access these enums through `Enums.Status`. These are the status types that appear on a profile like "Playing {game}".

There are 3 available status types:
1. `playing` (value of `1`)
2. `listening to` (value of `2`)
3. `watching` (value of `3`)

## Channels

Access these enums through `Enums.Channel`. These are the different available channel types on Hummus.

There are 4 channel types:
1. `text` (value of `0`)
2. `dm` (value of `1`)
3. `voice` (value of `2`)
4. `gc` (value of `3`)

## Default Avatars

Access these enums through `Enums.DefaultAvatars`. These are the different default avatars available on Hummus.

- `all` (contains a tuple of all 5 default avatars, already sorted so you can determine the avatar from the discriminator: `DefaultAvatars.all[int(User.discriminator) % 5]`)
- `blue` (value of `"https://hummus.sys42.net/assets/6debd47ed13483642cf09e832ed0bc1b.png"`)
- `gray` (value of `"https://hummus.sys42.net/assets/322c936a8c8be1b803cd94861bdfa868.png"`)
- `green` (value of `"https://hummus.sys42.net/assets/dd4dbc0016779df1378e7812eabaa04d.png"`)
- `yellow` (value of `"https://hummus.sys42.net/assets/0e291f67c9274a1abdddeb3fd919cbaa.png"`)
- `red` (value of `"https://hummus.sys42.net/assets/1cbd08c76f8af6dddce02c5138971129.png"`)

## Permissions

Access these enums through `Enums.Permissions`. Please note that these enums are **not** permission integers, but str values that match the attributes of the `Permissions` class from Discord.py.

All attribute names reflect the string value assigned to them. Here is the list of attributes:
- `add_reactions`
- `administrator`
- `attach_files`
- `ban_members`
- `change_nickname`
- `connect`
- `create_instant_invite`
- `deafen_members`
- `embed_links`
- `external_emojis`
- `kick_members`
- `manage_channels`
- `manage_emojis`
- `manage_guild`
- `manage_messages`
- `manage_nicknames`
- `manage_roles`
- `manage_webhooks`
- `mention_everyone`
- `move_members`
- `mute_members`
- `read_message_history`
- `read_messages`
- `send_messages`
- `send_tts_messages`
- `speak`
- `use_voice_activation`

## Colors

Color enums are hexadecimals assigned to their respective attribute names. Note that not all existing colors are included (obviously), but these enums are a list of the most common colors used.

These enums can be used to assign role colors or embed colors.

List of colors:
- `default` (value of `0`)
- `aqua` (value of `0x1ABC9C`)
- `dark_aqua` (value of `0x11806A`)
- `green` (value of `0x2ECC71`)
- `dark_green` (value of `0x1F8B4C`)
- `blue` (value of `0x3498DB`)
- `dark_blue` (value of `0x206694`)
- `purple` (value of `0x9B59B6`)
- `dark_purple` (value of `0x71368A`)
- `magenta` (value of `0xE91E63`)
- `dark_magenta` (value of `0xAD1457`)
- `gold` (value of `0xF1C40F`)
- `dark_gold` (value of `0xC27C0E`)
- `orange` (value of `0xE67E22`)
- `dark_orange` (value of `0xA84300`)
- `red` (value of `0xE74c3C`)
- `dark_red` (value of `0x992D22`)
- `light_gray` (value of `0xBCC0C0`)
- `gray` (value of `0x95A5A6`)
- `dark_gray` (value of `0x979C9F`)
- `darker_gray` (value of `0x7F8C8D`)
- `og_blurple` (value of `0x7289DA`)
- `ruined_blurple` (value of `0x586AEA`)
- `blurple` (value of `0x5865F2`)
- `greyple` (value of `0x99AAB5`)
- `dark_them` (value of `0x36393F`)
- `not_quite_black` (value of `0x23272A`)
- `dark_but_not_black` (value of `0x2C2F33`)
- `white` (value of `0xFFFFFE`)
- `fuchsia` (value of `0xEB459E`)
- `yellow` (value of `0xFEE75C`)
- `navy` (value of `0x34495E`)
- `dark_navy` (value of `0x2C3E50`)

The `Colors` class also includes functions you can use in relation to colors.

### Get Random Color:

`def get_random_color()`
- Returns a random color.

### Get Byte

`def get_byte(value,byte)`
- Returns the index of the byte (`byte`) from the provided integer (`value`).

### Color From RGB

`def from_rgb(rgb_values)`
- Returns the integer value of the provided rgb values. `rgb_values` must either be a list or tuple.

### Color From Integer

`def to_rgb(color)`
- Returns a tuple containing the RGB equivalent of the integer color provided. This uses the `get_byte` function mentioned before.

### Get Color

`def get(args)`
- Returns the hexadecimal value of the provided color.
- `args` can be a list/tuple containing RGB values, a hexadecimal, or a color name (attempts to get the attribute with the same name).