import typing
import asyncio
import re
import random
import json
import aiohttp

from .framework.request import Request
from .framework.handlers.message import MessageHandler
from .framework import Longpoll
from . import API

class Bot(Longpoll):
    """The main class of the library"""
    long_poll_server: dict
    
    def __init__(self, token: str, group_id: int, wait: int = 25):
        self._token:str = token
        self._group_id:int = group_id
        self._wait:int = wait
        self._session = aiohttp.ClientSession()
        self._stop:False = False
        self.api:API = API(token = token, session = self._session)
        self.loop:asyncio.AbstractEventLoop = None
        self.handler = MessageHandler()
        self.command = self.handler.command

    async def get_server(self) -> dict:
        """Get longpoll server

        Returns:
            dict: [description]
        """
        self.long_poll_server = await self.api.groups.get_longpoll_server(self._group_id)
        return self.long_poll_server

    async def longpoll_request(self) -> dict:
        """Make a request to the server

        Returns:
            dict: Updates
        """
        url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
            self.long_poll_server.server,
            self.long_poll_server.key,
            self.long_poll_server.ts,
            self._wait,
        )
        return await Request.post(self._session, url)

    async def run(self) -> None:
        """
        Run bot polling
        Can be manually stopped with:
        bot.stop()
        """
        await self.get_server()

        while not self._stop:
            event:dict = await self.longpoll_request()
            if isinstance(event, dict) and event.get("ts"):
                await self.distribute(event)
                self.long_poll_server.ts = event.get("ts")
            else:
                await self.get_server()

        await self._session.close()

    async def distribute(self, event:dict):
        """Distribution of updates to handlers.

        Args:
            event (dict): update
        """
        updates = event.get("updates", [event])

        for update in updates:
            if not update.get("object"):
                return
            if update.get("type") == "message_new":
                await self.loop.create_task(self.handler.handle_message(update.get("object")))

    def start_longpoll(self) -> None:
        """Start asyncio loop of the bot"""
        self._stop = False
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.run())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()
    
    def stop(self) -> None:
        """Stop longpoll (only after the end of the current request)
        """
        self._stop = True
