class Events:
  def __init__(self,instance):
    self.instance = instance

  async def on_ready(self, bot):
    pass

  async def on_message_create(self, message):
    pass

  async def on_message_delete(self, message_id, channel_id, guild_id):
    pass

  async def on_message_update(self, message, author):
    pass

  async def on_presence_update(self, before, presence):
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

  async def on_guild_role_create(self, guild_id, role):
    pass

  async def on_guild_role_delete(self, guild_id, role):
    pass

  async def on_guild_role_update(self, guild_id, before, after):
    pass

  async def on_guild_emojis_update(self, before, after): #emoji object contains guild ID
    pass

  async def on_typing_start(self, channel, user, when):
    pass

  async def on_channel_create(self, channel):
    pass

  async def on_channel_delete(self, channel):
    pass

  async def on_channel_update(self, before, after):
    pass