from ...guild import PartialGuild, Ban, Emoji
from ...role import Role, Permissions
from ...user import Member
from ...file import File

from aiohttp import ClientSession
from typing import *
import base64


class hGuild:
    def __init__(self, instance):
        self.instance = instance
        self.s: ClientSession = instance.s

    async def get_guild(self, id: str) -> PartialGuild:
        from ... import HTTPStatus
        r = await self.s.get(url=f"{self.instance.base_url}guilds/{id}")
        s = HTTPStatus(r)
        if s.success:
            return PartialGuild(await r.json(), self.instance)
        else:
            raise s.exception(s.reason)

    async def leave_guild(self, guild_id: str) -> None:
        from ... import HTTPStatus
        r = await self.s.delete(f"{self.instance.base_url}users/@me/guilds/{guild_id}")
        s = HTTPStatus(r)
        if not s.success:
            raise s.exception(s.reason)

    async def delete_guild(self, guild_id: str) -> None:
        from ... import HTTPStatus
        r = await self.s.post(f"{self.instance.base_url}guilds/{guild_id}/delete")  # clowning on the discord docs rn cause theyre WRONG (they said it was DELETE /guilds/{guild_id})
        s = HTTPStatus(r)
        if not s.success:
            raise s.exception(s.reason)

    async def kick(self, guild_id: str, user_id: str, reason: str = "") -> None:
        from ... import HTTPStatus
        self.s.headers.add('X-Audit-Log-Reason', reason)
        r = await self.s.delete(url=f"{self.instance.base_url}guilds/{guild_id}/members/{user_id}")
        self.s.headers.pop('X-Audit-Log-Reason')
        s = HTTPStatus(r)
        if not s.success:
            raise s.exception(s.reason)

    async def get_bans(self, guild_id: str) -> List[Ban]:
        from ... import HTTPStatus
        r = await self.s.get(url=f"{self.instance.base_url}/guilds/{guild_id}/bans")
        s = HTTPStatus(r)
        if s.success:
            return [Ban(ban, guild_id, self.instance) for ban in await r.json()]
        else:
            raise s.exception(s.reason)

    async def ban(self, guild_id: str, user_id: str, reason: str = "", delete_message_days: int = 0) -> None:
        from ... import HTTPStatus
        self.s.headers.add('X-Audit-Log-Reason', reason)
        r = await self.s.put(url=f"{self.instance.base_url}guilds/{guild_id}/bans/{user_id}", json={'delete-message-days': int(delete_message_days), 'reason': reason})
        self.s.headers.pop('X-Audit-Log-Reason')
        s = HTTPStatus(r)
        if not s.success:
            raise s.exception(s.reason)

    async def unban(self, guild_id: str, user_id: str) -> None:
        from ... import HTTPStatus
        r = await self.s.delete(url=f"{self.instance.base_url}guilds/{guild_id}/bans/{user_id}")
        s = HTTPStatus(r)
        if not s.success:
            raise s.exception(s.reason)

    # mute,deaf,channel_id params are for voice, which doesn't exist on hummus yet
    async def update_guild_member(self, guild_id: str, user_id: str, nick: str | None = None, roles: Sequence[Role | str] | None = None) -> None:
        from ... import HTTPStatus
        data = {}
        if roles:
            data['roles'] = [role.id if isinstance(role, Role) else role for role in roles]
            if guild_id in data['roles']:
                data['roles'].remove(guild_id)
        if nick:
            data['nick'] = nick
        r = await self.s.patch(url=f"{self.instance.base_url}guilds/{guild_id}/members/{user_id}", json=data)
        s = HTTPStatus(r)
        if not s.success:
            raise s.exception(s.reason)

    async def create_guild(self, name: str, region: Union[str, None] = None, icon: Union[File, None] = None) -> PartialGuild:
        data = {}
        if icon:
            data["icon"] = f"data:image/png;base64,{base64.b64encode(await icon.get_file_data()).decode('utf-8')}"
        if region:
            data['region'] = region
        data['name'] = name
        from ... import HTTPStatus
        r = await self.s.post(url=f"{self.instance.base_url}guilds", json=data)
        s = HTTPStatus(r)
        if s.success:
            return PartialGuild(await r.json(), self.instance)
        else:
            raise s.exception(s.reason)

    async def update_client_nick(self, guild_id: str, nick: str = "") -> Member:
        from ... import HTTPStatus
        if not nick:  # user attempts to pass in None to reset nick
            nick = ""
        r = await self.s.patch(url=f"{self.instance.base_url}guilds/{guild_id}/members/@me/nick", json={"nick": nick})
        s = HTTPStatus(r)
        if s.success:
            return Member(await r.json(), guild_id, self.instance)
        else:
            raise s.exception(s.reason)

    async def delete_role(self, guild_id: str, id: str) -> None:
        from ... import HTTPStatus
        r = await self.s.delete(url=f"{self.instance.base_url}guilds/{guild_id}/roles/{id}")
        s = HTTPStatus(r)
        if not s.success:
            raise s.exception(s.reason)

    async def create_role(self, guild_id: str) -> Role:
        from ... import HTTPStatus
        r = await self.s.post(url=f"{self.instance.base_url}guilds/{guild_id}/roles")  # when the json doesnt fucking work so people have to rely on Role.edit() lol! (fuck you ziad)
        s = HTTPStatus(r)
        if s.success:
            return Role(await r.json(), guild_id, self.instance)
        else:
            raise s.exception(s.reason)

    async def modify_role(self, guild_id: str, id: str, name: Union[str, None] = None, permissions: Union[Permissions, int, None] = None, color: Union[int, None] = None, hoist: Union[bool, None] = None, mentionable: Union[bool, None] = None) -> Role:
        data = {}
        if name:
            data['name'] = name
        if permissions:
            if type(permissions) == Permissions:
                permissions.update()
                permissions = permissions.value
            data['permissions'] = permissions
        if color:
            data['color'] = int(color)
        if hoist != None:
            data['hoist'] = hoist
        if mentionable != None:
            data['mentionable'] = mentionable
        from ... import HTTPStatus
        r = await self.s.patch(url=f"{self.instance.base_url}guilds/{guild_id}/roles/{id}", json=data)
        s = HTTPStatus(r)
        if s.success:
            return Role(await r.json(), guild_id, self.instance)
        else:
            raise s.exception(s.reason)

    async def modify_role_position(self, guild_id: str, id: str, position: int) -> List[Role]:
        from ... import HTTPStatus
        r = await self.s.patch(url=f"{self.instance.base_url}guilds/{guild_id}/roles", json=[{"id": id, "position": int(position)}])
        s = HTTPStatus(r)
        if s.success:
            return [Role(role, guild_id, self.instance) for role in await r.json()]
        else:
            raise s.exception(s.reason)

    async def modify_guild(self, guild_id: str, name: Union[str, None] = None, icon: Union[File, None] = None) -> PartialGuild:
        data = {}
        if name:
            data['name'] = name
        if icon:
            if not icon.empty:
                data["icon"] = f"data:image/png;base64,{base64.b64encode(await icon.get_file_data()).decode('utf-8')}"
        else:
            e = await (await self.s.get(f"{self.instance.base_url}guilds/{guild_id}")).json()
            icondata = await (await self.s.get(f"{self.instance.cdn}icons/{e['id']}/{e['icon']}.png")).content.read()
            data["icon"] = f"data:image/png;base64,{base64.b64encode(icondata).decode('utf-8')}"
        from ... import HTTPStatus
        r = await self.s.patch(url=f"{self.instance.base_url}guilds/{guild_id}", json=data)
        s = HTTPStatus(r)
        if s.success:
            return PartialGuild(await r.json(), self.instance)
        else:
            raise s.exception(s.reason)

    async def get_emojis(self, guild_id: str) -> List[Emoji]:
        from ... import HTTPStatus
        r = await self.s.get(f"{self.instance.base_url}guilds/{guild_id}/emojis")
        s = HTTPStatus(r)
        if s.success:
            return [Emoji(emoji, self.instance) for emoji in await r.json()]
        else:
            raise s.exception(s.reason)

    async def get_emoji(self, guild_id: str, id: str) -> Emoji:
        from ... import HTTPStatus
        r = await self.s.get(f"{self.instance.base_url}guilds/{guild_id}/emojis/{id}")
        s = HTTPStatus(r)
        if s.success:
            return Emoji(await r.json(), self.instance)
        else:
            raise s.exception(s.reason)

    async def create_emoji(self, guild_id: str, name: str, image: File) -> Emoji:
        from ... import HTTPStatus
        r = await self.s.post(f"{self.instance.base_url}guilds/{guild_id}/emojis", json={"name": name, "image": f"data:image/png;base64,{base64.b64encode(await image.get_file_data()).decode('utf-8')}"})
        s = HTTPStatus(r)
        if s.success:
            return Emoji(await r.json(), self.instance)
        else:
            raise s.exception(s.reason)

    async def edit_emoji(self, guild_id: str, id: str, name: str) -> Emoji:
        from ... import HTTPStatus
        r = await self.s.patch(f"{self.instance.base_url}guilds/{guild_id}/emojis/{id}", json={"name": name})
        s = HTTPStatus(r)
        if s.success:
            return Emoji(await r.json(), self.instance)
        else:
            raise s.exception(s.reason)

    async def delete_emoji(self, guild_id: str, id: str) -> None:
        from ... import HTTPStatus
        r = await self.s.delete(url=f"{self.instance.base_url}guilds/{guild_id}/emojis/{id}")
        s = HTTPStatus(r)
        if not s.success:
            raise s.exception(s.reason)
