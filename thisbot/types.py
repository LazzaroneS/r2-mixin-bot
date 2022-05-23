from mixinsdk.clients.blaze_client import BlazeClient
from mixinsdk.clients.http_client import HttpClient_AppAuth, HttpClient_WithoutAuth


class MixinBotClient:
    def __init__(self):
        self.blaze: BlazeClient = None
        self.http: HttpClient_AppAuth = None
        self.noauth: HttpClient_WithoutAuth = None


class MessageUser:
    def __init__(self):
        self.conversation_id = None
        self.user_id = None
        self.ext_user_type = None
        self.ext_user_id = None
        self.is_group = None
        self.group_owner_id = None
        self.group_name = None


class OperationObject:
    def __init__(self):
        self.operator_user_id: str = None
        self.operator_mixin_id: str = None
        self.notice_conv_id: str = None
