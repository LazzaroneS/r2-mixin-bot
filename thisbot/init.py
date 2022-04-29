import json
import logging
import os
from logging.handlers import RotatingFileHandler

from mixinsdk.clients.bot_config import BotConfig
from mixinsdk.clients.http_client import HttpClient_BotAuth, HttpClient_WithoutAuth
from thisbot.types import MixinBotClient, OperationObject


os.environ["TZ"] = "UTC+00:00"  # fix timezone


# --- Logging
log_handler = RotatingFileHandler(
    "../oogway.log", mode="a", maxBytes=5 * 1024 * 1024, backupCount=2, encoding="utf-8"
)
log_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s - %(message)s"
    )
)
# log_handler.setLevel(logging.DEBUG)
logger = logging.getLogger("root")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


# --- operation
operation_config = json.load(open("./data/operation-config.json"))
operation = OperationObject()
operation.operator_user_id = operation_config.get("operator", {}).get("user_id")
operation.operator_mixin_id = operation_config.get("operator", {}).get("mixin_id")
operation.notice_conv_id = operation_config.get("notice", {}).get("conversation_id")


# --- mixin bot
# mixin_bot_config = BotConfig.from_file("./data/bot-config-oogway.json")
mixin_bot_config = BotConfig.from_file("./data/bot-config-test.json")
mixin_client = MixinBotClient()
mixin_client.http = HttpClient_BotAuth(mixin_bot_config)
mixin_client.noauth = HttpClient_WithoutAuth()
