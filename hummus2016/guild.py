from .member import Avatar

class Guild:
  def __init__(self,data,cdn):
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

class Channel:
  def __init__(self,data):
    self.type = data['type']
    self.id = data['id']
    self.guild_id = data['guild_id']
    self.topic = data['topic']
    self.last_message_id = data['last_message_id']
    self.name = data['name']
    self.permission_overwrites = []
    for overwrite in data['permission_overwrites']:
      self.permission_overwrites.append(PermOverwrites(overwrite))
    self.position = data['position']

class PermOverwrites:
  def __init__(self,data):
    self.id = data['id']
    self.type = data['type']
    self.allow = data['allow']
    self.deny = data['deny']