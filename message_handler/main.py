from mixinsdk.types.message import MESSAGE_CATEGORIES, MessageView
from thisbot.init import logger, mixin_client
from thisbot.types import MessageUser
from thisbot.constants import USER_TYPES

from . import from_operator, from_user
from .methods import get_ext_user_type_and_id, get_mixin_group_profile


def error_callback(error, details):
    logger.error(error)
    logger.error(details)


async def handle(message):
    action = message["action"]

    if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
        # mixin blaze server received the message
        return

    if action == "LIST_PENDING_MESSAGES":
        print("Mixin blaze server: 👂")
        return

    if action == "ERROR":
        logger.warn("--- received error message ---")
        logger.warn(message)
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
            logger.warn("--- received error message ---")
            logger.warn(message)
            return

        data = message["data"]
        msgview = MessageView.from_dict(data)

        if msgview.conversation_id == "":
            # is response status of send message, ignore
            return

        if msgview.type == "message":
            # === from system message
            if msgview.user_id == "00000000-0000-0000-0000-000000000000":
                logger.debug("received system message")
                logger.debug(msgview.to_dict())
                if msgview.category == MESSAGE_CATEGORIES.SYSTEM_CONVERSATION:
                    await from_user.handle_conversation_actions(msgview)
                    await mixin_client.blaze.echo(msgview.message_id)
                    return

                logger.warn(f"unknown system message category: {msgview.category}")
                return

            msguser = MessageUser()
            (
                msguser.ext_user_type,
                msguser.ext_user_id,
            ) = get_ext_user_type_and_id(msgview.conversation_id, msgview.user_id)
            logger.debug(
                f"{msgview.category} message from: {msguser.ext_user_type} - {msguser.ext_user_id}"
            )

            if msgview.category == MESSAGE_CATEGORIES.SYSTEM_ACCOUNT_SNAPSHOT:
                # logger.debug(msgview.data_decoded)
                try:
                    await from_user.handle_transfer(msguser, msgview)
                    await mixin_client.blaze.echo(msgview.message_id)
                except Exception as e:
                    logger.exception("at snapshot message", exc_info=True)
                    raise e from None
                return

            # === from user

            # preprocess group message
            if msguser.ext_user_type == USER_TYPES.MIXIN_GROUP:
                msguser.is_group = True
                get_mixin_group_profile(msguser, msgview.conversation_id)
                if msguser.group_owner_id != msgview.user_id:
                    # filter out group messages not from owner
                    logger.debug(
                        f"Ignore group message:{msgview.message_id} not from owner"
                    )
                    await mixin_client.blaze.echo(msgview.message_id)
                    return

            if msgview.category == MESSAGE_CATEGORIES.TEXT:
                msg_text = msgview.data_decoded
                if msg_text.startswith(":"):  # consider it is admin command
                    await from_operator.handle_command(msguser, msgview)
                else:
                    await from_user.handle_command(msguser, msgview)
                await mixin_client.blaze.echo(msgview.message_id)
                return

            if msgview.category == MESSAGE_CATEGORIES.POST:
                await mixin_client.blaze.echo(msgview.message_id)
                return

            if msgview.category in [
                MESSAGE_CATEGORIES.IMAGE,
                MESSAGE_CATEGORIES.AUDIO,
                MESSAGE_CATEGORIES.VIDEO,
                MESSAGE_CATEGORIES.FILE,
            ]:
                await from_user.handle_media(msguser, msgview)
                await mixin_client.blaze.echo(msgview.message_id)
                return

            if msgview.category in [
                MESSAGE_CATEGORIES.STICKER,
                MESSAGE_CATEGORIES.APP_CARD,
                MESSAGE_CATEGORIES.LIVE,
            ]:
                # ignore
                logger.info(
                    f"Ignore message category: {msgview.category}, {msgview.message_id}"
                )
                await mixin_client.blaze.echo(msgview.message_id)
                return

            logger.warn(f"Unknown/Ignore message category: {message}")
            await mixin_client.blaze.echo(msgview.message_id)
            return

    logger.warn("Unknown message:", message)
