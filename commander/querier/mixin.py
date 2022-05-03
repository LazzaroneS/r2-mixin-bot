import json

from commander.types import CommandContext, CommandError
from mixinsdk.types.message import pack_message, pack_post_data, pack_text_data
from thisbot.init import mixin_client

from ..methods import (
    add_response_buttons_message,
    add_response_markdown_message,
    add_response_text_message,
    parse_arguments,
)


def get_asset_doc():
    return """
Query Mixin network assets

`asset <symbol> [-nt|-no-table]`

Example: `asset btc`
    """


async def asset(ctx: CommandContext, args):
    # parser arguments
    actions, options = parse_arguments(args, {"no-table": ["nt"]})

    if options.get("help"):
        add_response_markdown_message(ctx, get_asset_doc())
        return

    if not actions:
        raise CommandError(ctx.cur_prog_name, "missing symbol")

    symbol = actions[0]
    opt_no_table = options.get("no-table")

    # query
    text = query_mixin_asset_by_symbol(symbol, opt_no_table)
    if not text:
        text = f"Cannot find asset by symbol: {symbol}"
        msg = pack_message(pack_text_data(text), ctx.msgview.conversation_id)
        ctx.replying_msgs.append(msg)
        return
    msg = pack_message(pack_post_data(text), ctx.msgview.conversation_id)
    ctx.replying_msgs.append(msg)


def query_mixin_asset_by_symbol(symbol: str, opt_no_table: bool):
    rsp = mixin_client.noauth.api.network.search_asset_by_symbol(symbol)
    assets = rsp.get("data", [])
    if not assets:
        return None
    # render
    markdown = f"Mixin Assets of query symbol: **{symbol.upper()}**\n"
    if not opt_no_table:
        markdown += "\n|Icon|Symbol|Name|Asset ID|Price in USD|Capitalization\n|:---:|:---:|:---:|:---:|:---:|:---:|\n"
        for item in assets:
            icon_url = item.get("icon_url")
            markdown += f"|![]({icon_url})"
            # markdown += f'|<img src="{icon_url}" width="25" height="25">'
            markdown += (
                f"|{item.get('symbol')}|{item.get('name')}|{item.get('asset_id')}|"
            )
            markdown += f"{item.get('price_usd')}|{item.get('capitalization')}|\n"

    # json
    markdown += "\nRaw data\n"
    markdown += "```\n" + json.dumps(assets, indent=2) + "\n```\n"
    markdown += f"Data from: {mixin_client.http.http.api_base}"

    return markdown
