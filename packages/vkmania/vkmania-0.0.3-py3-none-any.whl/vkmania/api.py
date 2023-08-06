import typing
import aiohttp

from .types.methods import Groups, Messages

class API:
    instance = None
    def __init__(self, token:str = None, session: aiohttp.client.ClientSession = None):
        """Initialization of the main class for accessing to the vk api

        Args:
            token (str, optional): bot token. Defaults to None.
            session (aiohttp.client.ClientSession, optional): aiohttp session. Defaults to None. 
        """
        if not API.instance and not token:
            raise TypeError("token must be specified for the first instance")

        if API.instance:
            self = API.instance
            return

        self._token = token
        self._session = session or aiohttp.ClientSession()
        self.groups = Groups(self)
        self.messages = Messages(self)
        API.instance = self

    @staticmethod
    def get_instance():
        return API.instance