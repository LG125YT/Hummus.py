from .utils import Exceptions, CustomStatus
from .internal import http

import json

class HTTPStatus:
	def __init__(self,response):
		self.success = False
		self.response = response
		if 199 < response.status_code < 300: #i think some 300-range status codes can be considered "successful", but I don't think Hummus ever returns them
			self.success = True
			return
		if response.status_code == 400:
			self.reason = "Client formatted the request incorrectly!"
			self.exception = Exceptions.BadRequest
			return
		if response.status_code == 401:
			self.reason = "Client is not allowed to perform this action! (likely because invalid token)"
			self.exception = Exceptions.NotAllowed
			return
		if response.status_code == 403:
			self.reason = "Client does not have permissions to perform this action!"
			self.exception = Exceptions.InvalidPermissions
			return
		if response.status_code == 404:
			self.reason = "Client could not find the requested resource!"
			self.exception = Exceptions.NotFound
			return
		if response.status_code > 499:
			self.reason = "Server had an internal error!"
			self.exception = Exceptions.InternalServerError
			return
		try:
			if "unknown" in response.json()['message'].lower():
				self.reason = "Client could not find the requested resource!"
				self.exception = Exceptions.NotFound
				return
		except:
			pass
		self.reason = "An unknown error occurred!"
		self.exception = Exceptions.UnknownError

class HTTP(http.hChannel,http.hGuild,http.hMessage,http.hSelf,http.hUser):
	def __init__(self,instance):
		super().__init__(instance)

	#no need to create a whole file for one function
	async def update_status(self,status:CustomStatus) -> None:
		self.instance.connection.send(json.dumps({"op":3,"d":status._toJson()}))