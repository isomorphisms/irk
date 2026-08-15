from pathlib import Path
import unittest

from emit_r import emit_r
from name_types import NameTypeError, check_signature, infer_kind
from normalize_syntax import normalize_syntax
from read_source import SourceError, read_binding


ROOT = Path(__file__).parents[1]
MODEL = ROOT / "model"


class NameTypesTest(unittest.TestCase):
    def test_image_name_agrees_with_image_signature(self):
        report = check_signature("downsize_image", "Image", "Image", MODEL)
        self.assertEqual(report.claim.kind, "Image")
        self.assertFalse(report.behavior_checked)

    def test_name_rejects_a_decorative_wrong_type(self):
        with self.assertRaisesRegex(NameTypeError, "acts on Image"):
            check_signature("downsize_image", "Table", "Table", MODEL)

    def test_noun_type_is_checked_before_an_unknown_verb(self):
        with self.assertRaisesRegex(NameTypeError, "acts on Image"):
            check_signature("flarb_image", "Table", "Image", MODEL)

    def test_vector_resolves_photo_to_image(self):
        claim = infer_kind("photo", MODEL)
        self.assertEqual((claim.kind, claim.method), ("Image", "vector"))

    def test_reader_and_emitter_keep_the_top_level_small(self):
        source = (ROOT / "examples/downsize_image.irk").read_text(encoding="utf-8")
        generated = emit_r(read_binding(source))
        self.assertIn(".irk_impl_downsize_image <- function(image)", generated)
        self.assertIn('irk_expect_kind(image, "Image"', generated)
        self.assertIn('irk_expect_kind(result, "Image"', generated)
        self.assertIn("image$pixels <- image$pixels[rows, columns", generated)
        self.assertIn("irk_expect_kind <- function", generated)

    def test_syntax_normalization_leaves_strings_and_comments_alone(self):
        source = 'λ(x) { x ← 8 ÷ 2; "← λ ÷" # ← λ ÷\n }'
        normalized = normalize_syntax(source)
        self.assertIn('function(x) { x <- 8 / 2; "← λ ÷"', normalized)
        self.assertIn("# ← λ ÷", normalized)
        self.assertEqual(normalize_syntax("αλvalue ← λ(x) x"), "αλvalue <- function(x) x")

    def test_reader_rejects_a_second_function(self):
        source = (ROOT / "examples/downsize_image.irk").read_text(encoding="utf-8")
        with self.assertRaisesRegex(SourceError, "exactly one function"):
            read_binding(source + "\nother ← λ(x) { x }\n")


if __name__ == "__main__":
    unittest.main()
