import logging
from html import unescape

from markdownify import markdownify

from commander.types import CommandContext, CommandError
from mixinsdk.constants import BUTTON_COLORS
from pkgs.google_translator import translater
from pkgs.wikipedia import query as wiki_query
from pkgs.wikipedia.constants import PAGE_PROPS as PAGE_PROPS
from mixinsdk.types.messenger_schema import pack_input_action
from thisbot.init import mixin_bot_config

from ..methods import (
    add_response_buttons_message,
    add_response_markdown_message,
    add_response_text_message,
    parse_arguments,
)


def get_doc():
    return """
### Command `wiki`
Search wikipedia.

### Examples:
**`wiki apple`**
**`wiki 苹果`**

### Syntax:
**`wiki <title> [-l|--lang]`**
**`wiki page <pageid> [-l|--lang]`**

### Options:
- `-h`: show help
- `-l,-lang`: set language
    `-lang=zh` ,set language as 中文
    `-lang=en` ,set language as English
    """


async def handle(ctx: CommandContext, args):
    # parser arguments
    actions, options = parse_arguments(args, {"lang": ["l"]})

    if options.get("help"):
        add_response_markdown_message(ctx, get_doc())
        return

    if not actions:
        add_response_text_message(ctx, "✗ wiki: No action")
        add_response_markdown_message(ctx, get_doc())
        return

    if len(actions) == 1:
        sub_cmd = "search"
        act_value = actions[0]
    else:
        sub_cmd = actions[0]
        act_value = actions[1]

    opt_lang = options.get("lang")

    if sub_cmd == "search":
        title = act_value
        search_title(ctx, title, opt_lang)
    elif sub_cmd == "page":
        pageid = act_value
        query_page(ctx, pageid, opt_lang)


def search_title(ctx: CommandContext, title, opt_lang):
    lang = opt_lang if opt_lang else get_lang(title)
    rsp = wiki_query.search(title, lang)
    if rsp.get("error"):
        raise CommandError(ctx.cur_prog_name, rsp.get("error"))
    found_pages = rsp.get("data", [])
    if not found_pages:
        add_response_text_message(ctx, f"wiki: No result of {title}")
        return

    # for pack button
    mixin_number = None
    if ctx.msguser.is_group:
        mixin_number = mixin_bot_config.mixin_id

    # [{ns, title, pageid, size, wordcount, snippet, timestamp}]
    if len(found_pages) == 1:
        page = found_pages[0]
        pageid = page.get("pageid")
        query_page(ctx, pageid, lang)
    else:  # multiple results, let user to select one
        button_tuples = []
        for page in found_pages:
            title = page.get("title")
            pageid = page.get("pageid")
            action = pack_input_action(f'wiki page "{pageid}" -l={lang}', mixin_number)
            button_tuples.append((title, action, BUTTON_COLORS[3]))

        add_response_buttons_message(ctx, button_tuples)


def query_page(ctx: CommandContext, pageid: str, opt_lang: str):
    lang = opt_lang if opt_lang else "en"
    logging.info(f"wiki query page: [{lang}] {pageid}")

    rsp = wiki_query.page(pageid, lang, [PAGE_PROPS.extracts, PAGE_PROPS.description])
    error = rsp.get("error")
    if error:
        raise CommandError(ctx.cur_prog_name, error)
    data = rsp.get("data")
    title = data.get("title")
    url = data.get("url")
    extract = data.get("extract")
    description = data.get("description")

    if not title:
        add_response_text_message(ctx, f"wiki: Not found page: {title}")
        return

    # html to markdown
    content = markdownify(unescape(extract))
    md = f"**[{title}]({url})**\n\n"
    md += description + "\n\n"
    md += content
    md += f"\n\n🔗[{url}]({url})"
    add_response_markdown_message(ctx, md)


def get_lang(text: str):
    lang = translater.detect(text)[:2]
    return lang
