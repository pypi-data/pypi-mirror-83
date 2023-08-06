import typing
import aiohttp
import random
import requests

from vkmania.const import API_VERSION, API_URL
from vkmania.types.responses.messages import SendMessageData
from vkmania.framework.request import Request

class Send:
    def __init__(self, api):
        self._api = api
    async def __call__(
        self, 
        user_id:int = None,
        peer_id: int = None,
        peer_ids: str = None,
        domain: str = None,
        chat_id: int = None,
        message: int = None,
        lat: float = None,
        long: float = None,
        attachment: str = None,
        reply_to: int = None,
        forward_messages: str = None,
        group_id: int = None,
        dont_parse_links: bool = False,
        disable_mentions: bool = False
    ) -> dict:
        params = dict((k, v) for k, v in locals().items() if k is not "self" and v is not None)
        params['random_id'] = random.randint(0, 99999999999999999999)
        params['access_token'] = self._api._token
        params['v'] = API_VERSION
        response = await Request.post(self._api._session, '{}{}'.format(API_URL, 'messages.send'), params)
        return SendMessageData(response)

class Messages:
    def __init__(self, api):
        self.send = Send(api)