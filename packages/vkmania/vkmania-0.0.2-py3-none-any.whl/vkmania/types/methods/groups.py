import typing
import aiohttp

from vkmania.const import API_VERSION, API_URL
from vkmania.types.responses.groups import *
from vkmania.framework.request import Request

class GetLongpollServer():
    def __init__(self, api):
        self._api = api
    async def __call__(self, group_id: int) -> dict:
        params = {'group_id': group_id, 'access_token': self._api._token, 'v': API_VERSION}
        response = await Request.post(self._api._session, '{}{}'.format(API_URL, 'groups.getLongPollServer'), params)
        return GetLongpollServerData(response)

class Groups:
    def __init__(self, api):
        self.get_longpoll_server = GetLongpollServer(api)