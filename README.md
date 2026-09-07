# easy-paper

An [Agent Skill](https://code.claude.com/docs/en/skills) that turns a local academic PDF into an
English close-reading guide, plus a short lesson in how that paper is written.

It is built for one specific problem: you have a few hundred PDFs, limited confidence in the field,
and you do not actually sit down and read them. **The product is your own judgment**, not a summary
that saves you from the paper. The guide points you back at the figures and pages rather than
replacing them, and several rules exist purely to stop it handing you a verdict instead of evidence.

Not a summariser, not a translator, not a reference manager.

## What you get

For each paper, a five-part Markdown guide:

| Part | Job |
|---|---|
| Before You Read | The background the paper assumes you already have |
| Understanding the Paper | Concepts, argument, **how the data were actually collected and processed**, findings |
| What the Evidence Supports | Each claim, what it rests on, where the paper says it stops |
| Learning to Write | How this paper builds a gap, states a method, reports a result, and crosses from result to interpretation — in its own sentences |
| Key Takeaways | What to carry to the next paper |

## How it works

Three stages. The first is free.

```
stage 1   pdf2md.py            0 model tokens    text, references, figure index, metadata
stage 2   model reads once     one full pass     evidence-card.json
stage 3   model reads the card card-sized        the guide
```

**Stage 1 never sends the PDF to a model.** A local script splits the paper into body text,
references (29–40% of the extracted characters, kept out of context entirely), a figure and table
index with page numbers, and metadata.

**Stage 2 builds an evidence ledger** before any prose is written. This exists for accuracy, not to
save tokens: writing fluent English and holding citation discipline are two jobs competing for
attention, and fluency wins. Separating them is the whole design.

**Stage 3 writes from the card**, not from the paper. Measured on one paper: 21.9k tokens to read
the body against 7.7k to read the card, and the guide can be regenerated after a rule change without
re-parsing anything.

## Install

```bash
git clone https://github.com/kyrieove/easy-paper ~/.claude/skills/easy-paper
pip install pdf-inspector
```

That is the only dependency. Then, in Claude Code:

```
read paper.pdf with easy-paper
```

Or run stage 1 yourself and let the model pick up from there:

```bash
python pdf2md.py "paper.pdf"
```

> If `pdf-inspector` is missing, the script exits with the interpreter it ran under and the exact
> `pip install` line for it. The usual cause is the wrong Python, not a missing package: LibreOffice,
> Anaconda and the Windows Store stub all shadow the one on `PATH`.

Everything lands under one folder:

```
output/
  extracted/<slug>/    body.md, refs.md, figures.json, meta.json, evidence-card.json
  reading-guides/      the guides
```

Self-check: `python test_pdf2md.py`.

## Two branches, one question

The guide adapts on a single test: **did the authors collect the data themselves?** Not "is this a
review?" — that question puts meta-analyses on the wrong side. A meta-analysis has its own data, its
own analysis and a forest plot, so it goes with the experimental papers. The flag is set by stage 1
from the section headings, at no model cost.

Only two things differ between the branches: the spine of *Understanding the Paper*, and the job of
*What the Evidence Supports*. There is no third branch and no per-type template.

## Design decisions worth knowing before you use it

- **Figures are pointed at, never reproduced.** `→ FIGURE 4 · p. 9` plus what to look at. If the
  guide contained the figures it would replace the paper, and not opening the paper is the problem
  being solved.
- **Evaluation is confined to one part, and it is a map, not a verdict.** An earlier version scored
  13 evaluative judgements in 3,553 words; the reader absorbs the analyst's opinion instead of
  forming their own, which is the exact failure this skill exists to avoid. Part three now lists
  claim → what it rests on → where it stops, and leaves the conclusion to you.
- **Methods detail is the last thing cut.** If you are running your own experiments, the methods
  section is the most directly usable part of any paper and the part a summary destroys most
  completely. The guide carries the real parameters — filter cutoffs, rejection thresholds, trial
  timings, the statistical model and its factors.
- **The guide never overwrites itself.** Your notes live in it (it is designed to be read in an
  Obsidian vault), so regeneration writes a new file and lets you merge.

## Limits, honestly

- Scanned PDFs are detected but not OCR'd.
- Reference splitting fails on some two-column layouts whose `REFERENCES` heading is shredded by the
  extractor; stage 1 warns you, and that paper costs 30–40% more in stage 2.
- The synthesis branch and the meta-analysis case have each been exercised on very few papers.
- Guide length lands around 3,000–3,300 words for an experimental paper. That is a ceiling with a
  documented cut order, not a target.

## Credits

Stage 1 is built on [pdf-inspector](https://github.com/firecrawl/pdf-inspector) (Rust core, fully
local, no API key). Its two-column reading order is the capability the whole pipeline rests on.

The prose rules in *Prose constraints* are adapted from the S1–S16 catalogue of the
`academic-ai-pattern` skill, which audits academic manuscripts for AI-writing signals. They are
reproduced in full in `SKILL.md`, so this skill has no dependency on it.

## License

MIT. See [LICENSE](LICENSE).
