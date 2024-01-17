import discord
from .role import Role

class Permissions(discord.Permissions):
  def __init__(self,role:Role):
    super().__init__(role.permissions) #yeah no lets just skid discord.py :trol: