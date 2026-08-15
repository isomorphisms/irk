"""Normalize IRK's R spellings without changing strings or comments."""


REPLACEMENTS = {
    "←": "<-",
    "λ": "function",
    "÷": "/",
    "×": "*",
    "•": "*",
    "·": "*",
}


def normalize_syntax(source: str) -> str:
    output = []
    quote = None
    escaped = False
    comment = False

    for position, character in enumerate(source):
        if comment:
            output.append(character)
            comment = character != "\n"
        elif quote:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
        elif character in "'\"`":
            quote = character
            output.append(character)
        elif character == "#":
            comment = True
            output.append(character)
        else:
            previous = source[position - 1] if position else ""
            following = source[position + 1] if position + 1 < len(source) else ""
            lambda_is_in_a_name = character == "λ" and (
                (previous and (previous.isalnum() or previous in "._"))
                or (following and (following.isalnum() or following in "._"))
            )
            output.append(
                character if lambda_is_in_a_name else REPLACEMENTS.get(character, character)
            )

    return "".join(output)
