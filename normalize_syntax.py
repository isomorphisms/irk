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

    for character in source:
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
            output.append(REPLACEMENTS.get(character, character))

    return "".join(output)
