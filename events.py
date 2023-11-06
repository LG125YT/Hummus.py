class Events:
  def __init__(self,instance):
    self.instance = instance

  def on_ready(self, bot): #i dont remember if this works, probably not
    pass

  def on_message_create(self, message):
    pass

  def on_message_delete(self, message_id, channel_id, guild_id):
    pass

  def on_message_update(self, message, author):
    pass

  def on_guild_member_add(self, guild, member):
    pass

  def on_guild_member_remove(self, guild, member): #unlike other events, a member object actually gets passed through! discord is not being obscure with info for once!?!?!?
    pass

#fear not, more shall be added soon!