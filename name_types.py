"""Turn words in a binding name into type claims, then check the signature."""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re

from model2vec import StaticModel


MODEL_DIRECTORY = Path(__file__).with_name("model")

KINDS = {
    "Image": "image picture photograph bitmap pixels width height",
    "Table": "table data frame rows columns tabular records",
    "Text": "text character string words letters",
    "Number": "number numeric integer real quantity",
    "Model": "statistical fitted model predictions coefficients",
}

OBJECT_FLOW = {
    "downsize": ("argument", "result"),
    "resize": ("argument", "result"),
    "rotate": ("argument", "result"),
    "crop": ("argument", "result"),
}


class NameTypeError(ValueError):
    pass


@dataclass(frozen=True)
class KindClaim:
    word: str
    kind: str | None
    score: float
    margin: float
    method: str


@dataclass(frozen=True)
class SignatureCheck:
    claim: KindClaim
    operation: str
    behavior_checked: bool = False


def name_words(name: str) -> list[str]:
    separated = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return [word.lower() for word in re.split(r"[._]+", separated) if word]


@lru_cache(maxsize=4)
def _model(directory: str) -> StaticModel:
    return StaticModel.from_pretrained(directory)


def infer_kind(word: str, model_directory: Path = MODEL_DIRECTORY) -> KindClaim:
    for kind in KINDS:
        if word.lower() == kind.lower():
            return KindClaim(word, kind, 1.0, 1.0, "exact")

    model = _model(str(model_directory))
    query = model.encode([word])[0]
    descriptions = model.encode(list(KINDS.values()))
    ranked = sorted(
        zip(query @ descriptions.T, KINDS), reverse=True
    )
    best_score, best_kind = ranked[0]
    margin = float(best_score - ranked[1][0])
    score = float(best_score)

    if score < 0.50 or margin < 0.15:
        return KindClaim(word, None, score, margin, "unresolved")
    return KindClaim(word, best_kind, score, margin, "vector")


def check_signature(
    name: str,
    input_kind: str,
    output_kind: str,
    model_directory: Path = MODEL_DIRECTORY,
) -> SignatureCheck:
    words = name_words(name)
    if len(words) < 2:
        raise NameTypeError(f"{name!r} does not yet expose an operation and object")

    operation, object_word = words[0], words[-1]
    claim = infer_kind(object_word, model_directory)
    if claim.kind is None:
        raise NameTypeError(
            f"{object_word!r} does not resolve confidently to a known kind "
            f"(score {claim.score:.3f}, margin {claim.margin:.3f})"
        )

    actual = {"argument": input_kind, "result": output_kind}
    if input_kind != claim.kind:
        raise NameTypeError(
            f"{name} says it acts on {claim.kind}, but its argument is "
            f"declared {input_kind}"
        )

    positions = OBJECT_FLOW.get(operation)
    if positions is None:
        raise NameTypeError(f"the operation {operation!r} has no type rule yet")

    for position in positions:
        if actual[position] != claim.kind:
            raise NameTypeError(
                f"{name} says {claim.kind}, but its {position} is "
                f"declared {actual[position]}"
            )

    return SignatureCheck(claim=claim, operation=operation)
