import re
import traceback

from mixinsdk.types.message import (
    MessageView,
    pack_button_group_data,
    pack_post_data,
    pack_text_data,
)
from mixinsdk.types.transfer import TransferView
from thisbot.init import (
    logger,
    mixin_bot_config,
    mixin_client,
    operation,
)
from thisbot.types import MessageUser
from thisbot.constants import USER_TYPES, APP_NAME
from . import methods

from . import reply_template


async def send_text_to_user(text, conversation_id, quote_message_id=None):
    await mixin_client.blaze.send_message(
        pack_text_data(text), conversation_id, quote_message_id=quote_message_id
    )


async def send_post_to_user(text, conversation_id, quote_message_id=None):
    await mixin_client.blaze.send_message(
        pack_post_data(text), conversation_id, quote_message_id=quote_message_id
    )


async def notice_operator(text):
    logger.warn(f"notice operator: {text}")
    text = f"{APP_NAME}:\n```" + text + "\n```"
    await mixin_client.blaze.send_message(
        pack_post_data(text), operation.notice_conv_id
    )


async def handle_command(msguser: MessageUser, msgview: MessageView):
    msg_text = msgview.data_decoded

    """ ===== Process command ===== """

    # clean text command
    cmd = msg_text.lower().strip()
    cmd = cmd.lstrip("/")
    sign_str = "@" + mixin_bot_config.mixin_id + " "
    cmd = cmd.replace(sign_str, "")

    logger.debug(f"user command: {cmd}")

    if cmd in ["hi", "hello", "你好"]:
        text = reply_template.get_welcome()
        await send_text_to_user(text, msgview.conversation_id)

        btn = reply_template.get_button_of_help(msguser)
        await mixin_client.blaze.send_message(
            pack_button_group_data(btn), msgview.conversation_id
        )

        return

    if cmd in ["help", "帮助"]:
        text = reply_template.get_help_doc()
        await send_post_to_user(text, msgview.conversation_id)
        return

    if re.match(r"^user\b", cmd):
        await send_text_to_user(
            f"Your mixin user id: {msgview.user_id}", msgview.conversation_id
        )
        return
    if re.match(r"^conv\b", cmd):
        await send_text_to_user(
            f"This conversation id: {msgview.conversation_id}", msgview.conversation_id
        )
        return

    if re.match(r"^asset ", cmd):
        symbol = cmd.split(" ")[1]
        markdown = methods.query_mixin_asset_by_symbol(symbol)
        await send_post_to_user(markdown, msgview.conversation_id)
        return

    if cmd in ["oogway", "master"]:
        await send_text_to_user(reply_template.master_pearls(), msgview.conversation_id)
        return

    # else
    text = reply_template.get_unknown()
    await send_text_to_user(
        text, msgview.conversation_id, quote_message_id=msgview.message_id
    )


async def handle_media(msguser: MessageUser, msgview: MessageView):
    text = f"{msgview.category}\n\n```\n{msgview.data_decoded}\n```"
    await send_post_to_user(text, msgview.conversation_id)


async def handle_conversation_actions(msgview: MessageView):
    # print(msgview.data_decoded)
    participant_id = msgview.data_decoded.get("participant_id")
    if participant_id != mixin_client.blaze.config.client_id:
        return
    # 是对本机器人账号的操作才关心和处理
    action = msgview.data_decoded.get("action")
    if action == "ADD":
        logger.info(f"被加入了群聊会话: {msgview.conversation_id}")

        text = reply_template.get_welcome()
        await send_text_to_user(text, msgview.conversation_id)

        return
    elif action == "REMOVE":
        logger.info(f"被加入了群聊会话: {msgview.conversation_id}")
        # log to db?
        return
    else:
        logger.warn(f"未知的会话操作: {action}")
        return
