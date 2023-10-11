#from .channel import Channel
from .author import Avatar

class Guild:
  def __init__(self,data,cdn):
    print(data)
    self.id = data['id']
    self.name = data['name']
    self.icon = Avatar(self.id,data['icon'],cdn)
    self.owner_id = data['owner_id']
    self.features = data['features']
    self.region = data['region']
    self.roles = []
    for role in data['roles']:
      self.roles.append(role)
    self.cdn = cdn
    self.emojis = []
    for emoji in data['emojis']:
      self.emojis.append(emoji)
    self.voice_states = []
    for voice_state in data['voice_states']:
      self.voice_states.append(voice_state)
    self.afk_timeout = data['afk_timeout']