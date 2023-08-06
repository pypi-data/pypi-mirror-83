class GetLongpollServerData:
    def __init__(self, response:dict) -> None:
        self.ok:bool = False
        self.key:str = None
        self.server:str = None
        self.ts:int = None

        if 'response' in response:
            self.ok = True

        if not self.ok: return
        response_content = response['response']
        self.key = response_content['key']
        self.server = response_content['server']
        self.ts = response_content['ts']
