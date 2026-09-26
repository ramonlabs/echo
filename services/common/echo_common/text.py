import mistune

_parse = mistune.create_markdown(renderer=None, plugins=["strikethrough", "table"])

_BLOCK = {"paragraph", "heading", "list_item", "block_quote"}

_ROW = {"table_head", "table_row"}


def _render(tokens):
    out = []
    for token in tokens:
        kind = token["type"]

        if kind in ("text", "codespan", "block_code"):
            out.append(token["raw"])
        elif kind == "softbreak":
            out.append(" ")
        elif kind == "linebreak":
            out.append("\n")
        elif kind in _ROW:
            # commas so the cells do not run together when spoken
            out.append(", ".join(_render([cell]) for cell in token["children"]))
            out.append("\n")
        elif "children" in token:
            out.append(_render(token["children"]))
            if kind in _BLOCK:
                out.append("\n")

    return "".join(out)


def speakable(text):
    """Punctuation with no sound never survives to speech."""
    if not text:
        return text

    return text.replace(";", ",").replace("\u2014", ", ")


def strip_markdown(text):
    if not text:
        return text
    return _render(_parse(text)).strip()
