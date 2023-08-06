import aiohttp
import asyncio
import json

class Request:
    @staticmethod
    async def post(session, url, content = {}):
        async with session.post(url, data=content) as response:
            return await response.json()