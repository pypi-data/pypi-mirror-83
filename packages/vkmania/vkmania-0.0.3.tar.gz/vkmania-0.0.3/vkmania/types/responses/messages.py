class SendMessageData:
    def __init__(self, response:dict) -> None:
        self.ok:bool = False

        if 'response' in response:
            self.ok = True
