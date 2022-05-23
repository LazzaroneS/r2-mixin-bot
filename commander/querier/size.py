import ijson

from commander.types import CommandContext
from mixinsdk.constants import BUTTON_COLORS
from mixinsdk.types.messenger_schema import pack_input_action
from thisbot.init import mixin_bot_config

from ..methods import (
    add_response_buttons_message,
    add_response_markdown_message,
    add_response_text_message,
    parse_arguments,
)

DATA_FILE_PATH__PAPER = "./data/size/paper.json"
DATA_FILE_PATH__IPHONE = "./data/size/iphone.json"


def get_doc():
    return """
### Command `size`
Query size of Paper, iPhone.

### Examples:
**`size paper`**
**`size paper A4`**
**`size iphone 6`**

### Syntax:
**`size <item> <model>`**

### Options:
- `-h`: show help
    """


def handle(ctx: CommandContext, args):
    # parser arguments
    actions, options = parse_arguments(args, {})

    if options.get("help"):
        add_response_markdown_message(ctx, get_doc())
        return

    # for pack button
    mixin_number = None if not ctx.msguser.is_group else mixin_bot_config.mixin_id

    if not actions:
        # give buttons to select item
        item_names = ["paper", "iphone"]
        button_tuples = []

        # command help button
        tup = (
            "size --help",
            pack_input_action("size -h", mixin_number),
            BUTTON_COLORS[3],
        )
        button_tuples.append(tup)

        for item_name in item_names:
            cmd = f"size {item_name}"
            tup = (cmd, pack_input_action(cmd, mixin_number), BUTTON_COLORS[3])
            button_tuples.append(tup)

        add_response_buttons_message(ctx, button_tuples)
        return

    item_name = actions[0].lower()
    if item_name == "paper":
        if len(actions) == 1:  # no model specified, response all paper sizes table
            response_paper_sizes(ctx)
        else:  # search by specified model name
            response_paper_sizes(ctx, actions[1])
        return
    if item_name == "iphone":
        if len(actions) == 1:
            response_iphone_sizes(ctx)
        else:
            response_iphone_sizes(ctx, actions[1])
        return
    else:
        add_response_text_message(ctx, f"size: Unknown item: {item_name}")
        return


def response_paper_sizes(ctx: CommandContext, query_model: str = None):
    md = "Paper sizes:\n"
    md += "\n|Model|mm|inch|\n|:---:|:---:|:---:|"
    count = 0
    query_model = query_model.upper() if query_model else None
    for obj in ijson.items(open(DATA_FILE_PATH__PAPER), "item"):
        model = obj["model"]
        if not query_model or query_model in model.upper():
            count += 1
            mm = render_paper_unit_size(obj["unit"]["mm"])
            inch = render_paper_unit_size(obj["unit"]["inch"])
            md += f"\n|{model}|{mm}|{inch}|"
    md += "\n\n"

    if count == 0:
        add_response_text_message(ctx, f"Not found paper model: {query_model}")
        return
    add_response_markdown_message(ctx, md)


def render_paper_unit_size(unit_size: dict):
    return f'{unit_size["width"]:.2f}  x  {unit_size["height"]:.2f}'


def response_iphone_sizes(ctx: CommandContext, query_model: str = None):
    md = "iPhone sizes:\n"
    md += "\n|Model|Display|Dimensions|Weight|\n|:---:|:---:|:---:|:---:|"
    count = 0
    query_model = query_model.upper() if query_model else None
    for obj in ijson.items(open(DATA_FILE_PATH__IPHONE), "item"):
        model = obj["model"]
        if not query_model or query_model in model.upper():
            count += 1
            display = obj["display"]["size"] + ", " + obj["display"]["type"]
            dimensions = obj["dimensions"]
            weight = obj["weight"]
            md += f"\n|{model}|{display}|{dimensions}|{weight}|"
    md += "\n\n"
    if count == 0:
        add_response_text_message(ctx, f"Not found iphone model: {query_model}")
        return
    add_response_markdown_message(ctx, md)
