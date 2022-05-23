from mixinsdk.utils import is_group_conversation
from thisbot.constants import USER_TYPES
from thisbot.init import mixin_bot_config, mixin_client
from thisbot.types import MessageUser

temp_map_user_id_to_ext_user_type = {}


def get_mixin_user_type_and_id(conv_id, user_id):
    """return ext_user_type and ext_user_id"""
    if not conv_id or not user_id:
        return None, None
    if is_group_conversation(conv_id, user_id, mixin_bot_config.client_id):
        return USER_TYPES.MIXIN_GROUP, conv_id
    else:
        ext_utype = temp_map_user_id_to_ext_user_type.get(user_id)
        if ext_utype:
            return ext_utype, user_id

        r = mixin_client.http.api.user.get_user(user_id)
        identity_number = r.get("data", {}).get("identity_number")
        if not identity_number:
            ext_utype = None
        if identity_number == "0":  # Network user
            ext_utype = None  # Unsupported
        if identity_number.startswith("7000"):  # Mixin App
            ext_utype = USER_TYPES.MIXIN_APP
        else:
            ext_utype = USER_TYPES.MIXIN_USER

        temp_map_user_id_to_ext_user_type[user_id] = ext_utype
        return ext_utype, user_id


def get_mixin_group_profile(msguser: MessageUser, group_conv_id):
    """no return. assign to msguser"""
    r = mixin_client.http.api.conversation.get_info(group_conv_id)
    if not isinstance(r, dict):
        raise ConnectionError(f"Cannot get group profile: {group_conv_id}")
    data = r.get("data")
    if not data:
        raise ConnectionError(f"Cannot get group profile: {group_conv_id}")
    if data.get("category") != "GROUP":
        raise ValueError(f"Not a group conversation: {group_conv_id}")
    msguser.group_owner_id = data.get("creator_id")
    msguser.group_name = data.get("name")
