from .utils import Exceptions, CustomStatus
from .internal import http

from aiohttp import ClientResponse
import asyncio
import json


class HTTPStatus:
    def __init__(self, response: ClientResponse):
        self.success = False
        self.response: ClientResponse = response
        if 199 < response.status < 300:  # i think some 300-range status codes can be considered "successful", but I don't think Hummus ever returns them
            self.success = True
            return
        if response.status == 400:
            self.reason = "Client formatted the request incorrectly!"
            self.exception = Exceptions.BadRequest
            return
        if response.status == 401:
            self.reason = "Client is not allowed to perform this action! (likely because invalid token)"
            self.exception = Exceptions.NotAllowed
            return
        if response.status == 403:
            self.reason = "Client does not have permissions to perform this action!"
            self.exception = Exceptions.InvalidPermissions
            return
        if response.status == 404:
            self.reason = "Client could not find the requested resource!"
            self.exception = Exceptions.NotFound
            return
        if response.status > 499:
            self.reason = "Server had an internal error!"
            self.exception = Exceptions.InternalServerError
            return
        try:
            if "unknown" in asyncio.run(response.json())['message'].lower():
                self.reason = "Client could not find the requested resource!"
                self.exception = Exceptions.NotFound
                return
        except:
            pass
        self.reason = "An unknown error occurred!"
        self.exception = Exceptions.UnknownError


class HTTP(http.hChannel, http.hGuild, http.hMessage, http.hSelf, http.hUser):
    def __init__(self, instance):
        self.instance = instance
        self.s = instance.s

    # no need to create a whole file for one function
    async def update_status(self, status: CustomStatus) -> None:
        self.instance.connection.send(json.dumps({"op": 3, "d": status._toJson()}))
