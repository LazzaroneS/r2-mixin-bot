from mixinsdk.types.message import pack_button
from mixinsdk.constants import BUTTON_COLORS
from thisbot.types import MessageUser
from thisbot.init import mixin_bot_config


def master_pearls():
    return '"Yesterday is history, tomorrow is a mystery, but today is a gift. That is why it is called present." -- Oogway Master'


def get_welcome():
    return "🐢 Oogway, a querier"


def get_unknown_command(cmd: str):
    return f"> Command not found: {cmd}"


def get_button_of_help(msguser: MessageUser):
    action = "input:"
    if msguser.is_group:
        action += f"@{mixin_bot_config.mixin_id} "
    action += "help"
    pld = pack_button("Help", action, BUTTON_COLORS[7])
    return pld


def get_help_doc():
    text = "## Help\n"
    text += "> Oogway, it is a querier. Be used by Mixin MUI(Message User Interface) as yet.\n"
    text += "#### MUI commands:\n"
    text += "* `help`, show this help\n"
    text += "* `user`, show your mixin network user id\n"
    text += "* `conv`, show current conversation id\n"
    text += "* `asset <symbol>`, search asset by symbol. e.g. `asset btc`\n"
    text += "* `wiki <title>`, search wikipedia"
    return text
