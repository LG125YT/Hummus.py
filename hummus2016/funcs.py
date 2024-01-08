#quick functions for doing some actions such as getting guild user or role objects and/or comparing them

from .permissions import Permissions
from .allguild import AllGuild
from .member import Member
from .role import FakeRole

async def checkPerms(ctx,allGuilds,perm):
  for guild in allGuilds:
    if guild.guild.id == ctx.guild_id:
      selected = guild
  gmember = await ctx.getGuildUser(ctx.author.id)
  for mrole in gmember.roles:
    for role in selected.roles:
      if role.id == mrole:
        temp = Permissions(role)
        try:
          return getattr(temp, perm)
        except AttributeError:
          raise AttributeError(f"{perm} is not a valid permission!")
  return False

async def getRole(role_id,guild:AllGuild):
  for role in guild.roles:
    if role.id == role_id:
      return role

async def checkPositions(user1:Member,user2:Member,allGuilds):
  for guild in allGuilds:
    if guild.guild.id == user1.guild:
      selected = guild
  if len(user1.roles) > 0:
    highest1 = await getRole(user1.roles[0],selected)
    for role in user1.roles:
      fetched = await getRole(role,selected)
      if fetched.position < highest1.position:
        highest1 = fetched
  else:
    highest1 = FakeRole(999999) #who the hell in their right mind is going to make 999999 roles just to fuck with this

  if len(user2.roles) > 0:
    highest2 = await getRole(user2.roles[0],selected)
    for role in user2.roles:
      fetched = await getRole(role,selected)
      if fetched.position < highest1.position:
        highest1 = fetched
  else:
    highest2 = FakeRole(999999)
      
  return highest1.position < highest2.position

async def fullPermsCheck(ctx,instance,perm,target_id=None):
    perms = await checkPerms(ctx,instance.allGuilds,perm)
    if perms:
      if target_id is not None:
          member = await ctx.getGuildUser(target_id)
          author = await ctx.getGuildUser(ctx.author.id)
          pos = await checkPositions(author,member,instance.allGuilds)
          if pos:
            return True
      else:
        return True #perm checking does not have a target user, no comparison necessary
    return False