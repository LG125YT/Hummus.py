class Avatar:
  def __init__(self,id,avatar,cdn):
    self.id = id
    self.avatar = avatar
    self.url = f"{cdn}avatars/{self.id}/{self.avatar}.png"

class Author:
  def __init__(self,data,cdn):
    self.id = data['id']
    self.username = data['username']
    self.discriminator = data['discriminator']
    self.avatar = Avatar(self.id,data['avatar'],cdn)
    self.bot = data['bot']