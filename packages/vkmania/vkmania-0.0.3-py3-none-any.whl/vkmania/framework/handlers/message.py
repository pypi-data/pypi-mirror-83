import re

from vkmania.types.responses.groups import *
from vkmania.types.message import Message
from vkmania.types.reply import ReplyMessage

class MessageHandler:
    def __init__(self) -> None:
        self.commands = {}

    def command(self, text, lower = True) -> None:
        """Decorator for commands

        Args:
            text ([type]): Command text
            lower (bool, optional): Convert text to lowercase? Defaults to True.
        """
        if text in self.commands:
            raise AssertionError("Such command already exists")

        def wrapper(handler):
            self.commands[text] = {}
            self.commands[text]['handler'] = handler
            self.commands[text]['lower'] = lower
            return handler
        
        return wrapper
    
    async def handle_message(self, event: dict):
        """Call the desired handler for the message

        Args:
            event (dict): Raw dict of the message
        """
        message:Message = Message(event['message'])

        for command, content in self.commands.items():
            matches = None

            if content['lower']: 
                command = command.lower()
                message.text = message.text.lower()
            command = "^{}$".format(command)

            try:
                matches = re.match(re.compile(command), message.text)
            except:
                raise AssertionError("The regex is invalid")

            if not matches: continue
            try: 
                await content['handler'](message)
            except:
                raise RuntimeError("Command handler error")