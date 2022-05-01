import basic_reply
from commander.types import CommandContext
from mixinsdk.types.message import (
    pack_button_group_data,
    pack_message,
    pack_post_data,
    pack_text_data,
)


async def hi(ctx: CommandContext, args):
    text = basic_reply.get_welcome()
    msg1 = pack_message(pack_text_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg1)

    btn = basic_reply.get_button_of_help(ctx.msguser)
    msg2 = pack_message(pack_button_group_data(btn), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg2)


async def command_not_found(ctx: CommandContext, args):
    text = basic_reply.get_unknown_command(ctx.cur_prog_name)
    msg1 = pack_message(pack_text_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg1)


async def help(ctx: CommandContext, args):
    text = basic_reply.get_help_doc()
    msg1 = pack_message(pack_post_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg1)


async def current_user_info(ctx: CommandContext, args):
    text = f"Your mixin user id: {ctx.msgview.user_id}"
    msg1 = pack_message(pack_text_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg1)


async def current_conversation_info(ctx: CommandContext, args):
    text = f"This conversation id: {ctx.msgview.conversation_id}"
    msg1 = pack_message(pack_text_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg1)


async def master_pearls(ctx: CommandContext, args):
    text = basic_reply.master_pearls()
    msg1 = pack_message(pack_text_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg1)
