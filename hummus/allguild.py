from .guild import Guild
from .role import Role
from .member import Member, Presence

class AllGuild: #i might acutally revamp this to inherit from the Guild class instead of making a new one with a Guild object in it (its kinda stupid having to do "guild.guild.name" tbh)
  def __init__(self,guild,cdn,token,url):
    self.guild = Guild(guild,cdn)
    self.roles = []
    for role in guild['roles']:
      self.roles.append(Role(role))
    self.members = []
    for member in guild['members']:
      self.members.append(Member(member,cdn,token,url,self.guild.id))
    self.large = guild['large']
    self.member_count = guild['member_count']
    self.presences = []
    for presence in guild['presences']:
      self.presences.append(Presence(presence,cdn,token,url,self.guild.id))
    self.unavailable = guild.get('unavailable') #nonexistent on guild join mid-session