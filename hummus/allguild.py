from .guild import Guild, Channel, Emoji
from .role import Role
from .member import Member, Presence

class AllGuild(Guild):
  def __init__(self,instance,guild,cdn,token,url):
    super().__init__(guild,cdn,instance)
    self.instance = instance
    self.channels = []
    for channel in guild['channels']:
      self.channels.append(Channel(channel,instance))
    self.emojis = []
    for emoji in guild['emojis']:
      self.emojis.append(Emoji(emoji,instance))
    self.roles = []
    for role in guild['roles']:
      self.roles.append(Role(role))
    self.members = []
    for member in guild['members']:
      self.members.append(Member(instance,member,cdn,token,url,self.id))
    self.large = guild['large']
    self.member_count = guild['member_count']
    self.presences = []
    for presence in guild['presences']:
      self.presences.append(Presence(instance,presence,cdn,token,url,self.id))
    self.unavailable = guild.get('unavailable') #nonexistent on guild join mid-session

  async def toDict(self):
    return {"channels":[channel.toDict() for channel in self.channels], "emojis":[emoji.toDict() for emoji in self.emojis], "roles":[role.toDict() for role in self.roles], "members":[member.toDict() for member in self.members], "large":self.large, "member_count":self.member_count, "presences":[presence.toDict() for presence in self.presences],"unavailable":self.unavailable}