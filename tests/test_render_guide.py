import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import render_guide
import validate_v4

SAMPLE = '# A verified paper\n\n*Citation.*\n\n## Why this contrast?\n\nEvery result in **full**. → Fig. 2 · p. 5.\n\n## Writing\n\n> Original quote.\n'

class RendererTests(unittest.TestCase):
    def test_complete_markdown_and_navigation(self):
        page = render_guide.generate(SAMPLE)
        for expected in ('Every result in', 'Original quote.', 'Why this contrast?', 'href="#why-this-contrast"', 'print-color-adjust'):
            self.assertIn(expected, page)
        self.assertIn('Complete guide', page)

    def test_no_word_quota_or_fixed_heading_count(self):
        page = render_guide.generate('# Short paper\n\nOne sentence.')
        self.assertIn('One sentence.', page)
        self.assertNotIn('toc-link" href=', page)

    def test_figures_are_embedded_once_and_from_checked_manifest(self):
        with TemporaryDirectory() as root:
            path = Path(root)
            (path/'figure.png').write_bytes(b'\x89PNG\r\n\x1a\n' + b'example')
            manifest = path/'figures.json'
            manifest.write_text(json.dumps({'schema':'easy-paper-figures/v1','figures':[
                {'id':'Fig. 2','page':5,'path':'figure.png','caption':'Original panel', 'inspected':True}]}))
            page = render_guide.generate(SAMPLE+'\nAnother Fig. 2.', render_guide.load_figures(manifest))
            self.assertEqual(page.count('class="paper-figure"'), 1)
            self.assertIn('data:image/png;base64,', page)
            self.assertIn('Original PDF · p. 5', page)

    def test_legacy_explicit_figure_marker(self):
        with TemporaryDirectory() as root:
            folder = Path(root)
            (folder/'image.png').write_bytes(b'\x89PNG\r\n\x1a\n' + b'example')
            manifest = folder/'figures.json'
            manifest.write_text(json.dumps({'schema':'easy-paper-figures/v1','figures':[
                {'id':'Fig. 2','key':'sorsa_fig2','page':5,'path':'image.png','inspected':True}]}))
            page = render_guide.generate('# Guide\n\n→ Fig. 2 · p. 5.\n\n[[FIG:sorsa_fig2]]', render_guide.load_figures(manifest))
            self.assertEqual(page.count('class="paper-figure"'), 1)
            self.assertNotIn('[[FIG:', page)

    def test_rejects_fake_image_payload(self):
        with TemporaryDirectory() as root:
            folder = Path(root)
            (folder/'image.png').write_bytes(b'not an image')
            manifest = folder/'figures.json'
            manifest.write_text(json.dumps({'schema':'easy-paper-figures/v1','figures':[{'id':'Fig. 1','page':1,'path':'image.png','inspected':True}]}))
            with self.assertRaises(ValueError):
                render_guide.load_figures(manifest)

    def test_repeated_explicit_marker_only_embeds_once(self):
        with TemporaryDirectory() as root:
            folder = Path(root)
            (folder/'image.png').write_bytes(b'\x89PNG\r\n\x1a\nexample')
            manifest = folder/'figures.json'
            manifest.write_text(json.dumps({'schema':'easy-paper-figures/v1','figures':[{'id':'Fig. 2','key':'f2','page':5,'path':'image.png','inspected':True}]}))
            page = render_guide.generate('# Guide\n\n[[FIG:f2]]\n\n[[FIG:f2]]', render_guide.load_figures(manifest))
            self.assertEqual(page.count('class="paper-figure"'), 1)

    def test_refuses_uninspected_figures(self):
        with TemporaryDirectory() as root:
            path=Path(root)/'figures.json'
            path.write_text(json.dumps({'schema':'easy-paper-figures/v1','figures':[{'id':'Fig. 1','page':1,'path':'missing.png','inspected':False}]}))
            with self.assertRaises(ValueError):
                render_guide.load_figures(path)

    def test_versioned_output_does_not_overwrite(self):
        with TemporaryDirectory() as folder:
            p=Path(folder)
            guide=p/'guide.md'
            guide.write_text(SAMPLE)
            first,_=render_guide.run(guide)
            first.write_text('My annotations')
            second,_=render_guide.run(guide)
            self.assertEqual(first.read_text(), 'My annotations')
            self.assertEqual(second.name, 'guide-r2.html')

    def test_malformed_locations_returns_failure_not_exception(self):
        with TemporaryDirectory() as folder:
            card = Path(folder)/'card.json'
            card.write_text(json.dumps({'schema':'evidence-card/v4','source':{'n_pages':2,'pdf_sha256':'x','extractor_sha256':'x'},'paper':{'title':'T'},'questions':[{'locations':None}]}))
            self.assertTrue(any('locations must be an array' in x for x in validate_v4.validate(card)))

    def test_schema_validation_rejects_old_cards(self):
        with TemporaryDirectory() as folder:
            card=Path(folder)/'card.json'
            card.write_text('{"schema":"v3"}')
            errors=validate_v4.validate(card)
            self.assertTrue(any('schema' in e for e in errors))

if __name__ == '__main__':
    unittest.main()