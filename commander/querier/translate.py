from commander.types import CommandContext
from pkgs.google import translator

from ..methods import add_response_markdown_message, parse_arguments


def get_doc():
    return """
### Command `translate`
Translate text to other languages.

- `tr <text>` translate text to English
- `翻 <文本>` 翻译成中文
- `tr -l=jp <text>` translate text to Japanese

### Options:
- `-h`: show help
- `-l,-lang`: set target language
    `-l=zh` set target language as 中文
    `-l=en` set target language as English
    """


def handle(ctx: CommandContext, args):
    # parser arguments
    actions, options = parse_arguments(args, {"lang": ["l"]})

    if options.get("help") or not actions:
        add_response_markdown_message(ctx, get_doc())
        return

    dest_lang = options.get("lang")
    if not dest_lang:
        if ctx.cur_prog_name.startswith("tr"):
            dest_lang = "en"
        else:
            dest_lang = "zh"

    text = " ".join(actions)
    result, original_lang = translator.translate(text, dest_lang=dest_lang)

    md = f"**------ [{dest_lang}] ------**\n\n{result}\n\n\n"
    md += f"**------ [{original_lang}] ------**\n\n{text}"
    add_response_markdown_message(ctx, md)
