from vkmania.api import API
from vkmania.types.reply import ReplyMessage

class GetAPI:
    @property
    def api(self) -> API:
        return API.get_instance()

class Message(GetAPI):
    def __init__(self, message):
        self.date:int = message['date']
        self.from_id:int = message['from_id']
        self.id:int = message['id']
        self.out:int = message['out']
        self.peer_id:int = message['peer_id']
        self.text:str = message['text']
        self.attachments:list = message['attachments']

    @property
    def chat_id(self) -> int:
        return self.peer_id - 2000000000

    @property
    def from_chat(self) -> bool:
        return self.peer_id > 2e9

    @property
    def from_user(self) -> bool:
        return self.from_id > 0

    async def reply(
        self,
        reply: ReplyMessage
    ) -> None:
        await self.api.messages.send(**reply.get())

    async def reply(self, text: str, attachment: str = None) -> None:
        reply = ReplyMessage(peer_id = self.peer_id, message = text, attachment = attachment)
        await self.api.messages.send(**reply.get())