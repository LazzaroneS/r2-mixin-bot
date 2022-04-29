import asyncio

import message_handler
from mixinsdk.clients.blaze_client import BlazeClient
from thisbot.init import logger, mixin_bot_config, mixin_client

mixin_client.blaze = BlazeClient(
    mixin_bot_config,
    on_message=message_handler.handle,
    on_message_error_callback=message_handler.error_callback,
    logger=logger,
)

asyncio.run(mixin_client.blaze.run_forever(5))
