"""Read the one-function IRK subset used by the first experiment."""

from dataclasses import dataclass
import re


NAME = r"[A-Za-z][A-Za-z0-9_.]*"
TYPE = r"[A-Z][A-Za-z0-9_]*"

SIGNATURE = re.compile(
    rf"\A\s*(?P<name>{NAME})\s*:\s*(?P<input>{TYPE})\s*→\s*(?P<output>{TYPE})"
)

DEFINITION = re.compile(
    rf"\s*(?P<name>{NAME})\s*←\s*λ\s*\(\s*(?P<argument>{NAME})\s*\)\s*\{{"
)


class SourceError(ValueError):
    pass


@dataclass(frozen=True)
class Binding:
    name: str
    input_kind: str
    output_kind: str
    argument: str
    implementation: str


def _closing_brace(source: str, opening: int) -> int:
    depth = 0
    quote = None
    escaped = False
    comment = False

    for position in range(opening, len(source)):
        character = source[position]
        if comment:
            comment = character != "\n"
            continue
        if quote:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            continue
        if character in "'\"`":
            quote = character
        elif character == "#":
            comment = True
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return position

    raise SourceError("the function body has no matching }")


def read_binding(source: str) -> Binding:
    signature = SIGNATURE.match(source)

    if not signature:
        raise SourceError("expected: name : Input → Output")
    definition = DEFINITION.match(source, signature.end())
    if not definition:
        raise SourceError("expected: name ← λ(argument) { ... }")
    if signature["name"] != definition["name"]:
        raise SourceError("the signature and definition name different functions")

    closing = _closing_brace(source, definition.end() - 1)
    if source[closing + 1 :].strip():
        raise SourceError("the first experiment accepts exactly one function")

    return Binding(
        name=signature["name"],
        input_kind=signature["input"],
        output_kind=signature["output"],
        argument=definition["argument"],
        implementation=source[definition.start() : closing + 1].strip(),
    )
