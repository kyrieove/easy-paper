# easy-paper

A local PDF reading skill that creates an English close-reading guide and a focused academic-writing
lesson. It explains the path from a research question through design and evidence to interpretation.
Technical detail serves that explanation; there is no fixed five-part template or word quota.

## Install and use

Copy this folder into your agent's skill directory, such as `~/.claude/skills/easy-paper/` or
`~/.codex/skills/easy-paper/`. PDF extraction requires `pdf-inspector` in the interpreter used:

```bash
python -m pip install pdf-inspector
python /path/to/easy-paper/pdf2md.py /path/to/paper.pdf --out output/extracted
```

Then ask the agent to read the paper with easy-paper. Installation of the dependency is a user
setup command, not a side effect of importing or testing the scripts.

## Outputs

- `output/extracted/<filename-hash>/raw.md`: untrimmed extracted text with PDF page markers.
- `body.md`, `refs.md`: heuristic reading/reference split; appendices and tables remain recoverable.
- `figures.json`, `meta.json`: caption index, source identity, OCR flags and extraction warnings.
- `evidence-card.json`: the agent's source-linked record of measurements and interpretations.
- `verification.json`: source locations actually checked and unresolved issues.
- `output/reading-guides/*.md`: explanation and writing lesson, with source pointers.

Caches check PDF and script fingerprints plus required output files; warnings are repeated on cache
hits. Use `--force` after upgrading the extraction dependency. Existing cards require review after
re-extraction. The legacy `has_primary_data` field is only a heading hint, not a paper classifier.

The agent verifies paper identity, core conclusions and teaching quotations against the original
source. Methodological reasoning is welcome when its basis and attribution are clear. Writing
examples must preserve the same evidence boundaries as the explanation.

To save a generated draft without overwriting notes:

```bash
python /path/to/easy-paper/save_guide.py draft.md output/reading-guides/author-year-reading-guide.md
```

If needed this creates `-r2.md`, `-r3.md`, and so on, without replacing an existing file.

## Checks and limits

```bash
python test_pdf2md.py
python -m unittest test_regressions.py
```

These tests use only the standard library. Mock extraction tests check output handling, not actual
PDF parser accuracy. Scanned or damaged PDFs require separate OCR/visual inspection. Reference
splitting and running-header removal are heuristic; `raw.md` retains extracted text before either
operation. Core figures must be inspected rather than inferred from captions alone.

A passed script test does not prove a generated guide is accurate or readable. The final source
checks in `SKILL.md` remain necessary, and a revised guide should be judged on actual reading use.

## Credits and license

PDF extraction uses [pdf-inspector](https://github.com/firecrawl/pdf-inspector). MIT; see `LICENSE`.

## Historical files

Earlier design notes, handoff logs, sample guides and `check_guides.py` are retained from
the previous repository history. They describe v3, not the current v4 workflow. In particular,
`check_guides.py` enforces the old five-part template and must not validate v4 guides.
`SKILL.md` is the current specification; existing sample outputs have not been regenerated.
