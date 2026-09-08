"""Data preservation and repeat-run regressions; no PDF dependency required."""
import contextlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import pdf2md
from save_guide import save_guide


class ExtractionTests(unittest.TestCase):
    def test_short_documents_preserve_all_text(self):
        for pages in (["# Paper\nWe measured 42 participants.\nNo effect."],
                      ["Title\nRepeated result", "Title\nRepeated result"]):
            self.assertEqual(pdf2md.strip_running(pages), (pages, set()))

    def test_repeated_interior_text_is_not_a_running_header(self):
        pages = [f"Journal\nfirst {i}\nShared result\nlast {i}\nFooter"
                 for i in range(5)]
        cleaned, junk = pdf2md.strip_running(pages)
        self.assertEqual(junk, {"Journal", "Footer"})
        self.assertTrue(all("Shared result" in page for page in cleaned))

    def test_header_text_in_body_survives(self):
        pages = [f"Journal\nfirst {i}\nJournal\nlast {i}\nFooter" for i in range(5)]
        cleaned, _ = pdf2md.strip_running(pages)
        self.assertTrue(all(page.count("Journal") == 1 for page in cleaned))

    def test_appendix_after_references_preserves_page_numbers(self):
        pages = ["# Results\nObserved result.",
                 "**References**\nSmith, A. (2020). A paper.",
                 "## Appendix A\nExclusion threshold was 100 microvolts.",
                 "**Table 1.** Sample sizes\n42 participants"]
        body, refs = pdf2md.split_refs(pages)
        self.assertEqual(len(body), 4)
        self.assertIn("Exclusion threshold", body[2])
        self.assertNotIn("Exclusion threshold", refs)
        self.assertIn("<!-- Page 2 -->", refs)
        self.assertIn("<!-- Page 3 -->\n## Appendix A", pdf2md.page_markdown(body))
        self.assertEqual(pdf2md.index_figures(body)[0]["page"], 4)

    def test_same_page_figure_after_references_is_retained(self):
        body, refs = pdf2md.split_refs([
            "Conclusion.\n**References**\nSmith, A. (2020). A paper.\n"
            "**Figure 1.** Main result\nPanel A: response difference."])
        self.assertIn("Conclusion.", body[0])
        self.assertIn("Panel A", body[0])
        self.assertNotIn("Panel A", refs)

    def test_shape_split_restores_post_reference_table(self):
        prose = "\n".join(f"Body line {i}" for i in range(10))
        entries = "\n".join(
            f"{i}. Smith A, Jones B (2020) A study. Journal 2: 100-120."
            for i in range(1, 15))
        pages = [prose] * 4 + [entries, "Table 1. Results\nForty-two cases"]
        body, refs = pdf2md.split_refs(pages)
        self.assertIn("A study", refs)
        self.assertIn("Forty-two cases", body[5])


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pdf = self.root / "paper.pdf"
        self.pdf.write_bytes(b"fixture bytes; extraction is mocked")
        self.extractor = Mock()
        self.extractor.classify_pdf.return_value = SimpleNamespace(
            page_count=4, pdf_type="mixed", confidence=0.8, pages_needing_ocr=[2])
        self.pages = ["Journal\n# Results\n42 participants\nFooter",
                      "Journal\nUnrecognized extracted material\nFooter",
                      "Journal\n**References**\nSmith, A. (2020). A paper.\nFooter",
                      "Journal\n## Appendix A\nTable 1. Sample\n42 participants\nFooter"]
        self.extractor.extract_pages_markdown.return_value = SimpleNamespace(
            pages=[SimpleNamespace(markdown=p) for p in self.pages],
            pages_with_columns=[], pages_with_tables=[4])
        patcher = patch.object(pdf2md, "load_extractor", return_value=self.extractor)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_pipeline(self, force=False):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            dest = pdf2md.run(self.pdf, self.root / "out", force)
        return dest, output.getvalue()

    def test_raw_text_and_tail_figure_are_preserved(self):
        dest, output = self.run_pipeline()
        self.assertEqual((dest / "raw.md").read_text("utf-8"),
                         pdf2md.page_markdown(self.pages))
        self.assertIn("Appendix A", (dest / "body.md").read_text("utf-8"))
        self.assertEqual(json.loads((dest / "figures.json").read_text("utf-8"))[0]["page"], 4)
        self.assertIn("need OCR", output)

    def test_cache_hit_repeats_warnings(self):
        self.run_pipeline()
        _, output = self.run_pipeline()
        self.assertEqual(self.extractor.extract_pages_markdown.call_count, 1)
        self.assertIn("cached", output)
        self.assertIn("need OCR", output)

    def test_old_extractor_fingerprint_invalidates_cache(self):
        dest, _ = self.run_pipeline()
        meta_file = dest / "meta.json"
        meta = json.loads(meta_file.read_text("utf-8"))
        meta["extractor_sha256"] = "old implementation"
        meta_file.write_text(json.dumps(meta), "utf-8")
        self.run_pipeline()
        self.assertEqual(self.extractor.extract_pages_markdown.call_count, 2)

    def test_missing_output_is_regenerated(self):
        dest, _ = self.run_pipeline()
        (dest / "body.md").unlink()
        self.run_pipeline()
        self.assertTrue((dest / "body.md").exists())
        self.assertEqual(self.extractor.extract_pages_markdown.call_count, 2)

    def test_force_bypasses_cache(self):
        self.run_pipeline()
        self.run_pipeline(force=True)
        self.assertEqual(self.extractor.extract_pages_markdown.call_count, 2)


class SaveTests(unittest.TestCase):
    def test_three_regenerations_preserve_notes_and_drafts(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = root / "draft.md"
            target = root / "guides" / "author-year.md"
            paths = []
            for text in ("Original\n> My notes", "Second draft", "Third draft"):
                draft.write_text(text, "utf-8")
                paths.append(save_guide(draft, target))
            self.assertEqual([p.name for p in paths],
                             ["author-year.md", "author-year-r2.md", "author-year-r3.md"])
            self.assertEqual([p.read_text("utf-8") for p in paths],
                             ["Original\n> My notes", "Second draft", "Third draft"])


if __name__ == "__main__":
    unittest.main()
