from .guild import Guild
from .role import Role
from .member import Member, Presence

class AllGuild:
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
    self.unavailable = guild['unavailable']