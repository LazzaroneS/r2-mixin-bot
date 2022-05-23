import message_handler
from mixinsdk.clients.blaze_client import BlazeClient
from thisbot.init import logger, mixin_bot_config, mixin_client


def on_error(blaze, error):
    logger.error(error)


mixin_client.blaze = BlazeClient(
    mixin_bot_config,
    on_message=message_handler.handle,
    on_error=on_error,
)

mixin_client.blaze.run_forever(3)
