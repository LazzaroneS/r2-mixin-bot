import logging

from mixinsdk.clients.blaze_client import BlazeClient
from mixinsdk.types.message import MESSAGE_CATEGORIES, MessageView
from thisbot.constants import USER_TYPES
from thisbot.types import MessageUser

from . import from_operator, from_user
from .methods import get_mixin_group_profile, get_mixin_user_type_and_id


def handle(blaze: BlazeClient, message):
    action = message["action"]

    if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
        # mixin blaze server received the message
        return

    if action == "LIST_PENDING_MESSAGES":
        print("Mixin blaze server: 👂")
        return

    if action == "ERROR":
        logging.warn("--- received error message ---")
        logging.warn(message)
        return
        """example message={
            "id": "00000000-0000-0000-0000-000000000000",
            "action": "ERROR",
            "error": {
                "status": 202,
                "code": 400,
                "description": "The request body can't be parsed as valid data.",
            },
        }"""

    if action == "CREATE_MESSAGE":
        error = message.get("error")
        if error:
            logging.warn("--- received error message ---")
            logging.warn(message)
            return

        data = message["data"]
        msgview = MessageView.from_dict(data)

        if msgview.conversation_id == "":
            # is response status of send message, ignore
            return

        if msgview.type == "message":
            # === from system message
            if msgview.user_id == "00000000-0000-0000-0000-000000000000":
                logging.debug("received system message")
                logging.debug(msgview.to_dict())
                if msgview.category == MESSAGE_CATEGORIES.SYSTEM_CONVERSATION:
                    from_user.handle_conversation_actions(msgview)
                    blaze.echo(msgview.message_id)
                    return

                logging.warn(f"unknown system message category: {msgview.category}")
                return

            msguser = MessageUser()
            (
                msguser.ext_user_type,
                msguser.ext_user_id,
            ) = get_mixin_user_type_and_id(msgview.conversation_id, msgview.user_id)
            msg = f"Message {msgview.category} - {msgview.message_id} From: {msguser.ext_user_type} - {msguser.ext_user_id}"
            logging.info(msg)
            print(msg)

            if not msguser.ext_user_type:
                logging.warn(f"Ignore unsupported user's message: {msgview.to_dict()}")
                blaze.echo(msgview.message_id)
                return
            if msguser.ext_user_type == USER_TYPES.MIXIN_APP:
                # 过滤 APP USER 消息。不然机器人直接可能相互收发消息无止境
                logging.info("Ignore mixin app user's message")
                blaze.echo(msgview.message_id)
                return

            if msgview.category == MESSAGE_CATEGORIES.SYSTEM_ACCOUNT_SNAPSHOT:
                # logging.debug(msgview.data_decoded)
                try:
                    from_user.handle_transfer(msguser, msgview)
                    blaze.echo(msgview.message_id)
                except Exception as e:
                    logging.exception("at snapshot message", exc_info=True)
                    raise e from None
                return

            # === from user

            # preprocess group message
            if msguser.ext_user_type == USER_TYPES.MIXIN_GROUP:
                msguser.is_group = True
                get_mixin_group_profile(msguser, msgview.conversation_id)
                if msguser.group_owner_id != msgview.user_id:
                    # filter out group messages not from owner
                    logging.debug(
                        f"Ignore group message:{msgview.message_id} not from owner"
                    )
                    blaze.echo(msgview.message_id)
                    return

            if msgview.category == MESSAGE_CATEGORIES.TEXT:
                msg_text = msgview.data_decoded
                if msg_text.startswith(":"):  # consider it is admin command
                    from_operator.handle_command(msguser, msgview)
                else:
                    from_user.handle_text(msguser, msgview)
                blaze.echo(msgview.message_id)
                return

            if msgview.category == MESSAGE_CATEGORIES.POST:
                blaze.echo(msgview.message_id)
                return

            if msgview.category in [
                MESSAGE_CATEGORIES.IMAGE,
                MESSAGE_CATEGORIES.AUDIO,
                MESSAGE_CATEGORIES.VIDEO,
                MESSAGE_CATEGORIES.FILE,
                MESSAGE_CATEGORIES.STICKER,
            ]:
                from_user.handle_media(msguser, msgview)
                blaze.echo(msgview.message_id)
                return

            if msgview.category in [
                MESSAGE_CATEGORIES.APP_CARD,
                MESSAGE_CATEGORIES.LIVE,
            ]:
                # ignore
                logging.info(
                    f"Ignore message category: {msgview.category}, {msgview.message_id}"
                )
                blaze.echo(msgview.message_id)
                return

            logging.warn(f"Unknown/Ignore message category: {message}")
            blaze.echo(msgview.message_id)
            return

    logging.warn("Unknown message:", message)
