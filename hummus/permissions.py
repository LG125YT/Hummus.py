import discord
from .role import Role

class Permissions(discord.Permissions):
  def __init__(self,role=None):
    if type(role) == Role:
      role.permissions.update()
      super().__init__(role.permissions.value) #yeah no lets just skid discord.py :trol:
    elif type(role) == int:
      super().__init__(role)
    elif type(role) == str:
      super().__init__(int(role))
    elif not role: #None
      super().__init__(0) #creation of a fake role