class ReplyMessage:
    def __init__(
        self, 
        user_id:int = None,
        peer_id:int = None,
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
        disable_mentions: bool = False) -> None:
        self.data = dict((k, v) for k, v in locals().items() if k is not "self" and v is not None)
    
    def get(self):
        return self.data
