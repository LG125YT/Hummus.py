class Events:
  def __init__(self,instance):
    self.instance = instance

  async def on_ready(self, bot):
    pass

  async def on_message_create(self, message):
    pass

  async def on_message_delete(self, message_id, channel_id, guild_id):
    pass

  def on_message_delete_bulk(self, channel, messages):
    pass

  async def on_message_update(self, message, author):
    pass

  async def on_guild_member_add(self, guild, member):
    pass

  async def on_guild_member_remove(self, guild, member): #unlike other events, a member object actually gets passed through! discord is not being obscure with info for once!?!?!?
    pass

  def on_member_update(self, guild, before, after):
    pass

  async def on_guild_create(self, guild):
    pass

  def on_guild_join(self, guild):
    pass

  async def on_guild_delete(self, guild):
    pass

  def on_guild_update(self, bot, before, after):
    pass

  def on_guild_role_create(self, bot, role):
    pass

  def on_guild_role_delete(self, bot, role):
    pass

  def on_guild_role_update(self, bot, before, after):
    pass

  def on_guild_emojis_update(self, bot, guild, before, after):
    pass

  def on_typing_start(self, bot, channel, user, when):
    pass

  def on_channel_create(self, bot, channel):
    pass

  def on_channel_delete(self, bot, channel):
    pass

  def on_channel_update(self, bot, before, after):
    pass