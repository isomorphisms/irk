#!/usr/bin/env python3
"""Compile one readable IRK experiment to ordinary R."""

import argparse
from pathlib import Path
import sys

from emit_r import emit_r
from name_types import NameTypeError, check_signature
from read_source import SourceError, read_binding


def main() -> int:
    arguments = argparse.ArgumentParser()
    arguments.add_argument("source", type=Path)
    arguments.add_argument("-o", "--output", type=Path)
    request = arguments.parse_args()

    try:
        binding = read_binding(request.source.read_text(encoding="utf-8"))
        report = check_signature(
            binding.name, binding.input_kind, binding.output_kind
        )
    except (OSError, SourceError, NameTypeError) as problem:
        arguments.error(str(problem))

    generated = emit_r(binding)
    if request.output:
        request.output.write_text(generated, encoding="utf-8")
    else:
        print(generated, end="")

    print(
        f"{report.claim.word} → {report.claim.kind} "
        f"({report.claim.method}); {report.operation} behavior remains unchecked",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
