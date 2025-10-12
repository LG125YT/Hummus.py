from ...user import User, Profile

class hUser:
	def __init__(self,instance):
		self.instance = instance
		self.s = instance.s

	async def get_user(self,id:str) -> User:
		from ... import HTTPStatus
		r = self.s.get(url=f"{self.instance.base_url}users/{id}/")
		s = HTTPStatus(r)
		if s.success:
			return User(r.json(),self.instance)
		else:
			raise s.exception(s.reason)

	async def get_user_profile(self,id:str) -> Profile:
		from ... import HTTPStatus
		r = self.s.get(url=f"{self.instance.base_url}users/{id}/profile")
		s = HTTPStatus(r)
		if s.success:
			return Profile(r.json(),self.instance)
		else:
			raise s.exception(s.reason)

"""
	async def create_dm(self,id):
		r = self.s.post(url=f"{self.instance.base_url}users/@me/channels" ,json={"recipient_id":id})
		print(r)
		print(r.json())
""" #returns 400, does not work at all, cannot figure out how to make it work