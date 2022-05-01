from typing import List

from mixinsdk.types.message import MessageView
from thisbot.types import MessageUser


class CommandContext:
    def __init__(self, msguser: MessageUser, msgview: MessageView):
        self.msguser = msguser
        self.msgview = msgview
        self.cur_prog_name = ""
        self.pipe_data = None
        self.replying_msgs: List[dict] = []


class CommandError(BaseException):
    def __init__(self, prog_name: str, message: str):
        self.prog_name = prog_name
        self.message = message
        super().__init__(f"{prog_name} : {message}")
