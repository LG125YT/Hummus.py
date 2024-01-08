class Role:
  def __init__(self,data):
    self.id = data['id']
    self.name = data['name']
    self.color = data['color']
    self.permissions = data['permissions']
    self.mentionable = data['mentionable']
    self.hoist = data['hoist']
    self.position = data['position']

class FakeRole: #this is really used to provide a placeholder for top role comparison in funcs.py
  def __init__(self,position):
    self.position = position