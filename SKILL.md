---
name: paper-reading-guide
description: Turn a local academic PDF into an English close-reading guide plus a short academic-writing lesson. Three stages - a local script extracts text, figures and metadata at zero token cost; the model builds an evidence card; the guide is written from the card. Use when the user points at a PDF and wants to understand it, study how it is written, or build domain judgment. Not a summarizer, not a translator, not a reference manager.
---

# Paper → English reading guide

Reader profile this is built for: writing a paper in developmental cognitive neuroscience,
~200 local PDFs, low domain confidence, does not sit down and read the originals. The product
is **their** judgment, not a report that looks complete. Everything below serves that.

Install: this folder is the skill. Copy it to `~/.claude/skills/paper-reading-guide/`, or run
the stages from the repo.

## Do not

- Connect the paper to the user's own research or data. They want to make those links themselves.
- Recommend what to read next.
- Translate the paper, or write a peer-review report.
- Add a section because the structure looks incomplete without it. No comprehension quiz.
- Embed figures. Point at them (see *Conventions*).

## Stage 1 — extract (script, 0 model tokens)

```bash
"/d/2/software/python.exe" pdf2md.py "<paper>.pdf" --out out
```

**That interpreter path is not optional.** `python` on PATH is LibreOffice's bundled build and
has none of the dependencies. `D:\2\software\python.exe` (3.10.11) has `pdf-inspector`.

Writes `out/<slug>/`:

| File | Contents |
|---|---|
| `body.md` | Text, `<!-- Page N -->` markers, running heads/feet dropped, references cut |
| `refs.md` | References. **Never enters model context.** 29–40% of extracted text |
| `figures.json` | id, PDF page, caption. No images |
| `meta.json` | sha256, pages, text/scanned, `has_primary_data`, headings, `warnings` |

Idempotent by sha256; `--force` re-runs. Self-check: `test_pdf2md.py`.

**Read the `!!` warning lines before spending stage-2 tokens.** Four silent stage-1 failures have
each cost real time. A warning means one of: references not split (body.md still carries them —
30–40% of your stage-2 tokens wasted), zero figures indexed, `has_primary_data` false, headings
shredded by the extractor. A shredded-heading paper still has clean body prose; only heading-styled
runs break. Confirm the branch by hand when warned.

`has_primary_data` is the branch flag. The question it answers is **"did the authors collect the
data?"** — not "is this a review?". A meta-analysis lands on the primary-data side, where it
belongs: it has its own data, its own analysis and a forest plot. A synthesis review with no
pooled statistics lands on the other side. A paper that reviews and then reports new data is
primary-data; there is no third branch.

## Stage 2 — evidence card

Read `body.md` in full, once. Write `out/<slug>/evidence-card.json`. This is an internal artifact;
the reader never sees it.

**It exists for accuracy, not for token savings.** Writing fluent English and holding citation
discipline are two jobs competing for attention, and fluency wins. Building the ledger first
separates them. Everything downstream trusts this file, so a wrong card produces a guide that is
quietly wrong — and it is the least delegatable step in the pipeline.

Rules:

1. Every substantive entry carries `page` (PDF page) and `where` (section, table or figure).
2. Keep the layers in separate arrays and never merge them: what was measured, what the authors
   concluded from it, what the authors admit as a limit, what you as analyst raise.
3. Never invent a page, figure or number. Missing or unreliable → say so in `extraction_warnings`.
4. Locating a source correctly does not mean the reading is correct. Check that the claim is
   actually supported by the evidence you attached to it.
5. When a table's numbers survive extraction badly (detached superscripts, merged cells), record it
   in `extraction_warnings` and tell stage 3 to read those values off the PDF.

### Schema — primary data (`evidence-card/primary-data/v2`)

Worked example: `out/effect-of-aging-on-erp-components-of-cognitive-control/evidence-card.json`.

```
schema, note, paper{cite, doi, branch, sample}
questions[]                       id, text, page, note
design[]                          id, layer:method, page, where, text, why_it_matters
results[]                         id, layer:result, page, where, text, why_it_matters, supports[]
author_interpretations[]          id, layer:author_interpretation, page, where, text,
                                  rests_on[], boundary
limitations_author_acknowledged[] id, page, where, text
limitations_analyst_raised[]      id, text, targets[]
extraction_warnings[]             text, affects[]
writing_samples[]                 see below
figure_pointers[]                 id, page, use
```

### Schema — synthesis (`evidence-card/synthesis/v2`)

Same envelope; `design` / `results` / `author_interpretations` collapse into one array:

```
claims[]  id, page, where, text,
          tier: original_result | review_author_position | field_consensus,
          cited_as     (the citation this review gives for it; null for tier b),
          read_source  (true only if the original paper was actually opened)
disagreements[]  id, text, sides[]
```

**The tier is the whole point of this branch.** A review adds a layer of interpretation on top of
the papers it cites: original data → original authors' reading → this author's selection and
framing. Tagging a review author's position as field consensus is the specific failure this array
exists to prevent. `read_source: false` on everything is honest and expected; do not let a
second-hand summary pass as independent verification.

### `writing_samples[]` — harvest while the body is open

5–6 entries. `id`, `page`, `section`, `where`, `quote` (verbatim), `move`, `why_it_works`,
`conditions` (optional). At least one marked `AVOID` — teaching by contrast is cheap and the
failure modes are what the user needs to see.

**Store the move, not a template.** Record what the author *did* ("report a null result as a
licence, not as an absence"). Stage 3 derives any transferable pattern from that. A card full of
fill-in-the-blank sentence frames turns Part four into a phrasebook, which is the one thing it must
not become.

Without this array Part four is impossible from the card and stage 3 has to re-read the whole body.
Stage 2 already has it open, so this costs nothing.

## Stage 3 — the reading guide

Read the card. Re-read `body.md` only through targeted windows (`sed -n '340,380p'`) and only when
the card is genuinely short of something — never in full. Measured: card 7.7k tokens against
21.9k for the body.

Write to `output/reading-guides/<author>-<year>-reading-guide.md`.

**If that file already exists, write `<name>-r2.md` instead.** The reader's own notes live in the
guide (`> [!note] 我` under a paragraph, and a `## My Notes` section they append at the end, in
Obsidian). Regeneration is cheap and will happen often. Never clobber their thinking.

### Front matter

Title (short, not the paper's own title) · full citation · a three-row table: **What it asks** /
**What it found** / **What is new** · the conventions sentence · the evaluation-quarantine sentence
· any `> ⚠ **EXTRACTION WARNING**` · `---`.

### The five parts

| Part | Job |
|---|---|
| **Before You Read** | What the paper studies, and the background it assumes you already have |
| **Understanding the Paper** | The body. Concepts, argument, method, findings, in prose |
| **What the Evidence Supports** | See the branch table. All evaluation lives here |
| **Learning to Write** | 4 moves from this paper, with their conditions |
| **Key Takeaways** | Bolded one-line claims, each with 2–3 sentences under it |

Two things — and only two — differ by branch:

| | Understanding the Paper, spine | What the Evidence Supports, job |
|---|---|---|
| primary data | question → theoretical expectation → design logic → what was observed → how the authors explain it | separate result from interpretation; state where the conclusions stop |
| synthesis | core question → conceptual frame → the evidence on each side → where they disagree → the author's own position | what is established against what is this author's claim |

Everything else is identical. Do not build parallel templates per paper type.

**Part three is quarantined and labelled.** Parts one and two report what the paper says; Part three
is where you evaluate it. Evaluation woven through the narrative makes the reader absorb your
judgment instead of forming their own — the exact failure this project exists to prevent. Three
sub-headings: *Well supported* / *Supported, but reaching past the design* / *Interpretation, not
result*, then a `> **BOUNDARIES THE AUTHORS STATE**` blockquote. Keep the authors' own admissions
visibly separate from your objections.

**A primary-data paper's Introduction gets the synthesis treatment** in Part two. It is a
mini-review and it is where the user most needs to learn. Do not compress it to background.

**Part four follows the branch, but the Introduction is always fair game.** Primary data → Methods
and Results moves: reporting a statistic, reporting a null as a licence, stating a data-driven
choice without defending it, bounding a conclusion. Synthesis → Introduction and Discussion moves:
building a gap, attributing a claim to the literature, setting two positions side by side. The user
is weakest on Introduction and Discussion, so reviews are the *main* source of writing material,
not the secondary one — but never write a Part four for a primary-data paper that only collects
Introduction phrases, because its Methods and Results are the part they cannot learn elsewhere.

Per move: name it, point at `§Section, p. N`, quote **at most one sentence** verbatim, say what it
does and when it applies. Any sentence frame you invent goes in a blockquote labelled
`> **PATTERN — my example, not the authors'**`. Never let an example be mistaken for a finding.

### Conventions

Markdown cannot set fonts or sizes. Seven levers do the work:

- `` `F[4, 449]` ``, `` `p < 10⁻³` ``, `` `N = 454` `` — code spans for every statistic, so they
  stay findable in prose.
- `→ FIGURE 4 · p. 9` at the point of use, plus **what to look at and what to compare**. The guide
  must not replace the paper. Tables get the same treatment as figures; do not point at figures and
  skip the evidence sitting in a table.
- Blockquotes are reserved voices and every one carries a bold ALL-CAPS label. Bare `>` and
  `> [!note]` belong to the reader.
- Tables only for a comparison that is genuinely two-dimensional.
- Heading density ≈ 1 per 130 words. Paragraphs 3–4 sentences.
- Standalone bolded sentences for the instruction the reader should act on.
- Page numbers are **PDF pages**, stated once in the front matter.

English throughout, readable but not dumbed down — keep the technical terms. Background goes where
it is needed, not stacked at the front. Target **2,900–3,250 words**; both worked examples land
there.

### Worked examples

- `output/reading-guides/kropotov-2016-reading-guide.md` — primary data, Frontiers, carries an
  extraction warning and eight analyst notes
- `output/reading-guides/sorsa-2026-reading-guide.md` — primary data, Elsevier

`horowitz-kraus-2026-reading-guide.md` predates every rule above. **Do not use it as a model.**
The synthesis branch has never been run end to end under these rules.
