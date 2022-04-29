from thisbot.init import operation
from mixinsdk.types.message import MessageView
from thisbot.types import MessageUser


async def handle_command(msguser: MessageUser, msgview: MessageView):
    if msguser.is_group:
        return  # ignore command from group
    if not operation.operator_user_id:
        return
    if msgview.user_id != operation.operator_user_id:
        return

    cmd = msgview.data_decoded.lower()
    if cmd == ":balance":
        pass
