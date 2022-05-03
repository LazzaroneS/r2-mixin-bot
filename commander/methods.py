from commander.types import CommandContext
from mixinsdk.types.message import (
    pack_button,
    pack_button_group_data,
    pack_message,
    pack_post_data,
    pack_text_data,
)


def parse_process(text: str):
    first_space = text.find(" ")
    if first_space < 0:
        return text, []
    else:
        prog_name = text[:first_space]
        text = text[first_space + 1 :]

    args = []
    arg = ""
    is_in_quotation = False
    for char in text:
        if char == " " and not is_in_quotation:
            # start of a new argument
            args.append(arg)
            arg = ""
            continue

        if char == '"':
            is_in_quotation = not is_in_quotation
            continue

        arg += char

    if arg:
        args.append(arg)

    return prog_name, args


def parse_arguments(args: list, option_name_map: list = {}):
    """
    - option_name_map: {"opt_name":[alias_name1, alias_name2, ...], ...}
    """
    if not args:
        return [], {}

    # add help option
    if "help" not in option_name_map:
        option_name_map["help"] = ["h"]

    actions = []
    options = {}
    option_prefix_char = "-"
    for arg in args:
        if not arg:
            continue
        if not isinstance(arg, str):
            continue
        if arg.startswith(option_prefix_char):
            if "=" in arg:
                opt_name, opt_val = arg.split("=", 1)
            else:
                opt_name = arg
                opt_val = True
            # unify option name
            opt_name = opt_name.lstrip(option_prefix_char)
            if opt_name not in option_name_map:
                for k in option_name_map:
                    alias_names = option_name_map[k]
                    if opt_name in alias_names:
                        opt_name = k
                        break
            options[opt_name] = opt_val
        else:
            actions.append(arg)
    return actions, options


def add_response_text_message(ctx: CommandContext, text):
    msg = pack_message(pack_text_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg)


def add_response_markdown_message(ctx: CommandContext, text):
    msg = pack_message(pack_post_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg)


def add_response_buttons_message(ctx: CommandContext, button_tuple_list):
    """
    button_tuple_list: [(label, action, color), ...]
    """
    count = 0
    buttons = []
    for tup in button_tuple_list:
        count += 1
        label, action, color = tup
        buttons.append(pack_button(label, action, color))
        if count == 6:
            button_group = pack_button_group_data(buttons)
            msg = pack_message(button_group, ctx.msgview.conversation_id)
            ctx.replying_msgs.append(msg)
            buttons = []
            count = 0
    if buttons:
        button_group = pack_button_group_data(buttons)
        msg = pack_message(button_group, ctx.msgview.conversation_id)
        ctx.replying_msgs.append(msg)
