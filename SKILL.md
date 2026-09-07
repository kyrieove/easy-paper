---
name: easy-paper
description: Turn a local academic PDF into an English close-reading guide plus a short academic-writing lesson. Three stages - a local script extracts text, figures and metadata at zero token cost; the model builds an evidence card; the guide is written from the card. Use when the user points at a PDF and wants to understand it, study how it is written, or build domain judgment. Not a summarizer, not a translator, not a reference manager.
---

# Paper → English reading guide

Built for a reader who has a large local PDF library, limited confidence in the field, and does not
sit down and read the originals — a graduate student or early-career researcher writing their first
papers. **The product is their judgment, not a report that looks complete.** Everything below serves
that, and several rules exist specifically to stop the guide from handing them a verdict instead.

Install: copy this folder to `~/.claude/skills/easy-paper/`, or run the stages from a clone.
Stage 1 needs `pip install pdf-inspector` and nothing else.

## Do not

- Connect the paper to the user's own research or data. They want to make those links themselves.
- Recommend what to read next.
- Translate the paper, or write a peer-review report.
- Add a section because the structure looks incomplete without it. No comprehension quiz.
- Embed figures. Point at them (see *Conventions*).

## Stage 1 — extract (script, 0 model tokens)

```bash
python pdf2md.py "<paper>.pdf"
```

**On the first run, the script checks its own dependency.** If `pdf-inspector` is missing it exits
with the interpreter path it is running under and the exact `pip install` line for that interpreter.
Relay that message to the user and stop — do not try to install it yourself, and do not fall back to
reading the PDF directly, which sends the whole document into context and defeats the pipeline.

The usual cause is not a missing package but the wrong Python: LibreOffice, Anaconda and the Windows
Store stub all shadow the one on `PATH`. The error message says which interpreter ran, so compare it
against the one the user installed into before advising a reinstall.

Everything the skill produces lives under one `output/` folder:

```
output/
  extracted/<slug>/      stage 1 -- body.md, refs.md, figures.json, meta.json
                         stage 2 -- evidence-card.json lands here too
  reading-guides/        stage 3 -- the deliverable
```

`output/extracted/<slug>/` holds:

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

Read `body.md` in full, once. Write `output/extracted/<slug>/evidence-card.json`. This is an internal artifact;
the reader never sees it.

**It exists for accuracy, not for token savings.** Writing fluent English and holding citation
discipline are two jobs competing for attention, and fluency wins. Building the ledger first
separates them. Everything downstream trusts this file, so a wrong card produces a guide that is
quietly wrong — and it is the least delegatable step in the pipeline.

Rules:

1. Every substantive entry carries `page` (PDF page) and `where` (section, table or figure).
2. Keep the layers in separate arrays and never merge them: what was measured, what the authors
   concluded from it, what the authors admit as a limit, what the paper does not state.
3. Never invent a page, figure or number. Missing or unreliable → say so in `extraction_warnings`.
4. Locating a source correctly does not mean the reading is correct. Check that the claim is
   actually supported by the evidence you attached to it.
5. When a table's numbers survive extraction badly (detached superscripts, merged cells), record it
   in `extraction_warnings` and tell stage 3 to read those values off the PDF.
6. **Carry the paper's own wording.** Where the paper states something in one sentence, the card's
   `text` / `what_was_done` **is that sentence**, not your restatement of it. Paraphrase only when
   you are compressing several sentences, and mark those entries `"paraphrase": true`. Stage 3
   cannot quote what stage 2 did not keep, and it will not re-read the body to find it — a card full
   of restatements forces a guide written entirely in your voice, which is the failure the user
   named: a guide that reads as an opinion piece. Hyphenation debris from extraction may be
   repaired silently; nothing else.

### `methods[]` — the part the reader cannot get anywhere else

This array replaces the old `design[]`, which stored *why a choice mattered* and almost nothing
about *what was actually done*. The reader is running their own experiments and analysing their own
data; the methods section is the most directly usable part of any paper they will read, and the part
a summary destroys most completely. **Harvest it in detail. This is the one place where more is
better.**

`stage` is one of `participants`, `materials`, `procedure`, `acquisition`, `processing`, `analysis`.
A paper without an acquisition step simply has no entries at that stage — do not invent buckets.

- **`what_was_done`** — the paper's own sentence wherever it states the thing in one sentence.
- **`parameters`** — the actual numbers, in the paper's own units. Sample sizes per group and how
  they were recruited; inclusion and exclusion criteria; trial counts, timings, stimulus durations;
  equipment, sampling rate, electrode count, montage, scanner sequence; filter cutoffs, artifact
  rejection thresholds, epoch windows, baseline correction, referencing, interpolation; the
  statistical model with its factors, the correction applied, the software and version.
  **A parameter the paper gives and the card drops is gone** — stage 3 will never re-read for it.
- **`unclear`** — a step the paper does not specify well enough to reproduce. State what is missing,
  do not guess, and do not turn it into a criticism; if it is genuinely a hole, it belongs in
  `unstated_by_the_paper[]` as `missing_method`.

Order the entries as the study ran, not as the paper presents them. Papers routinely put
preprocessing after analysis or bury acquisition in a figure caption.

### `unstated_by_the_paper[]` — the pointing test

Every entry must be settleable by **pointing**: at two places in the paper that do not agree, at a
number that does not match another number, at a citation that is missing, or at a thing the paper
never states. `kind` is one of `contradiction`, `missing_method`, `number_mismatch`,
`unsourced_claim`, `location` (a claim that appears only where a reader will miss it).

If an entry cannot be settled by pointing, it is your opinion and it does not go in the card.
**An empty array is a good outcome, not a gap.** This array used to be called
`limitations_analyst_raised` and it produced nine entries on the first synthesis paper, several of
which were verdicts about which sections were worth reading. That is the failure this rename exists
to stop: a first-class container for opinions gets filled with opinions, and stage 3 then has
nothing else to write with.

### Schema — primary data (`evidence-card/primary-data/v3`)

```
schema, note, paper{cite, doi, branch, sample}
questions[]                       id, text, page, note
methods[]                         id, stage, page, where, what_was_done, parameters,
                                  why_it_matters (optional), unclear (optional)
results_reporting{}               convention, example, what_is_omitted, where
results[]                         id, layer:result, page, where, text, why_it_matters, supports[]
author_interpretations[]          id, layer:author_interpretation, page, where, text,
                                  rests_on[], boundary
limitations_author_acknowledged[] id, page, where, text
unstated_by_the_paper[]           id, kind, text, targets[]   -- see the pointing test
extraction_warnings[]             text, affects[]
writing_samples[]                 see below
figure_pointers[]                 id, page, use
```

`[]` is an array, `{}` a single object. **The key names above are exact and the set is closed**,
in both schemas. A card that shortens `limitations_author_acknowledged` to `limitations`, or folds
`results[]` and `author_interpretations[]` into `results_reporting`, is a different schema wearing
a v3 label: stage 3 reads the declared field names and finds nothing. The two arrays stay separate
even though both carry a `layer` tag — that tag exists to keep them apart in the guide, not to
merge them here.

`page` is an integer. When an item spans pages, quote it — `"page": "10-12"`. A bare `10-12` is
not JSON and the whole card fails to parse.

### Schema — synthesis (`evidence-card/synthesis/v3`)

Same envelope; `methods` / `results` / `author_interpretations` collapse into one array. A synthesis
paper has no methods of its own — if it turns out to have any (a stated search strategy, inclusion
criteria, a coding scheme), that is a systematic review and it keeps `methods[]` as well:

```
claims[]  id, page, where, text,
          tier: original_result | review_author_position | field_consensus,
          cited_as     (the citation this review gives for it; null for tier b),
          read_source  (true only if the original paper was actually opened)
disagreements[]  id, text, sides[]
structure_note   (optional string; only when the paper is not one voice)
```

`structure_note` exists because the first synthesis paper run through this schema was a workshop
write-up whose sections each had a different named author, and those authors contradicted each other
in four places. Where that is true, tier (b) means *the position of that section's author*, not
*the position of the review*, and stage 3 must attribute positions to sections rather than to
"the authors". Multi-author reviews and edited collections are common enough to be worth the field.

**The tier is the whole point of this branch.** A review adds a layer of interpretation on top of
the papers it cites: original data → original authors' reading → this author's selection and
framing. Tagging a review author's position as field consensus is the specific failure this array
exists to prevent. `read_source: false` on everything is honest and expected; do not let a
second-hand summary pass as independent verification.

### `writing_samples[]` — harvest while the body is open

`id`, `page`, `section`, `where`, `quote` (verbatim), `move`, `why_it_works`, `conditions`
(optional). **As many as the paper actually offers — 3 to 6 is typical, and two good ones beat six
padded ones.** Mark any that is a failure mode `AVOID`: teaching by contrast is cheap and the
failure modes are what the user needs to see. But only if the paper contains one — **do not
manufacture a bad example to fill a slot.**

**Store the move, not a template.** Record what the author *did* ("report a null result as a
licence, not as an absence"). Stage 3 derives any transferable pattern from that. A card full of
fill-in-the-blank sentence frames turns Part four into a phrasebook, which is the one thing it must
not become.

Without this array Part four is impossible from the card and stage 3 has to re-read the whole body.
Stage 2 already has it open, so this costs nothing.

**Coverage, for a primary-data paper.** No fixed count, but four things must be covered, because
these are the four the reader is trying to learn:

1. **How the gap is built** — Introduction. Even on an experimental paper: its Introduction is a
   mini-review and it is where the reader is weakest.
2. **How a design or analysis choice is stated** — Methods.
3. **How a result is reported** — the statistical format itself, see below.
4. **How the paper gets from a result to an interpretation** — the Results→Discussion joint.

One sample can cover two of these. If the paper does one of them badly, teach it as `AVOID`; if it
genuinely does not do one at all, say so in a line rather than inventing a sample. A synthesis paper
covers 1 and 4 only, and the disagreement moves in place of 2 and 3.

### `results_reporting` — how this literature writes a result

One object, not an array. Required on the primary-data branch; omit it only on a synthesis paper
that reports no results of its own:

```
results_reporting{}  convention, example (verbatim), what_is_omitted, where
```

The reader is about to write their own Results section and does not know what a result sentence in
this field contains. Record the paper's actual convention: which statistic, the degrees-of-freedom
notation, whether effect sizes appear, whether the numbers sit in the prose or in a table, and what
the field would normally include that this paper leaves out.

Conventions differ sharply and the difference matters. An ERP paper may state direction verbally and
push every `F` into a table; a mixed-model paper states `β`, `SE`, `t` or `z`, `df` and `p` inline
for each fixed effect and reports the random-effects structure separately; a meta-analysis reports a
pooled estimate with its confidence interval and a heterogeneity statistic. **Name the convention
this paper follows and quote one sentence of it.** Naming an alternative convention as background is
allowed and useful, but label it as background — it did not come from this paper.

### Before stage 3, on a batch run

```
python check_guides.py <run-dir>
```

Checks every card's key set against the two schemas above, flags cards that are not valid JSON or
that are byte-identical to another card, and traces every statistic in a finished guide back to
`body.md` or `refs.md`. A card written by an agent that never opened this file is fluent, correctly
structured, in the right language, and wrong; the key set is the only thing it cannot fake.

## Stage 3 — the reading guide

Read the card. Re-read `body.md` only through targeted windows (`sed -n '340,380p'`) and only when
the card is genuinely short of something — never in full. Measured: card 7.7k tokens against
21.9k for the body.

Write to `output/reading-guides/<author>-<year>-reading-guide.md`.

**If that file already exists, write `<name>-r2.md` instead.** The reader's own notes live in the
guide (a `> [!note]` callout under the paragraph it answers, and a `## My Notes` section at the end, in
Obsidian). Regeneration is cheap and will happen often. Never clobber their thinking.

### Front matter

Title (short, not the paper's own title) · full citation · a three-row table: **What it asks** /
**What it found** / **What is new** · `---`.

**Nothing else.** The top of the page is where the reader is paying most attention, and it is spent
on the paper. Anything that is about *the pipeline* rather than about the paper moves out:

- **The conventions sentence and the evaluation-quarantine sentence** go in a short
  `## About this guide` footer after Key Takeaways. They are identical in every guide, so the reader
  learns them once and skips them forever after. At the top they are boilerplate standing between
  the reader and the first sentence about the paper.
- **Extraction warnings** are recorded in the card's `extraction_warnings[]` — that is their
  permanent home — and appear in the guide **only inline, attached to the number, table or figure
  they affect**. One clause at the point of use, never a block at the top. A warning about scrambled
  table columns, met before the reader knows what the table contains, teaches nothing; the same
  warning beside the cell they were about to quote stops the mistake.

The one exception: if extraction damaged the **body prose** rather than a table or a heading, so that
the whole guide is suspect, say that in one line under the citation. Nothing less earns front-matter
space.

### The five parts

| Part | Job |
|---|---|
| **Before You Read** | What the paper studies, and the background it assumes you already have |
| **Understanding the Paper** | The body. Concepts, argument, what was actually done, findings |
| **What the Evidence Supports** | See the branch table. Claims mapped onto their evidence, no verdicts |
| **Learning to Write** | The moves this paper actually offers, with their conditions |
| **Key Takeaways** | Bolded one-line claims, each with 2–3 sentences under it |

**No section has a fixed item count.** Write the moves the paper offers and the takeaways that
survive — two of each is a correct outcome for a thin paper, and padding to a number is how a guide
starts inventing content. Typical is 2–5 moves and 3–5 takeaways; neither is a target.

Two things — and only two — differ by branch:

| | Understanding the Paper, spine | What the Evidence Supports, job |
|---|---|---|
| primary data | question → theoretical expectation → design logic → **how the data were collected and processed** → what was observed → how the authors explain it | separate result from interpretation; state where the conclusions stop |
| synthesis | core question → conceptual frame → the evidence on each side → where they disagree → the author's own position | what is established against what is this author's claim |

Everything else is identical. Do not build parallel templates per paper type.

**Part three maps claims onto their evidence. It does not deliver a verdict.** Three sub-headings —
*Well supported* / *Supported, but reaching past the design* / *Interpretation, not result* — then a
`> **BOUNDARIES THE AUTHORS STATE**` blockquote. Under each claim, say what supports it and what the
authors themselves say it does not establish, and stop. The reader draws the conclusion; that is the
only way they build judgment of their own, which is the entire point of the project.

Concretely: **never rank sections, authors, ideas or sentences against each other.** No "the most
sceptical section", no "the strongest move in the paper", no "worth reading twice", no "in my view".
See *Prose constraints*, which is not a style note — it is the rule this part most often breaks.

**A primary-data paper's Introduction gets the synthesis treatment** in Part two. It is a
mini-review and it is where the user most needs to learn. Do not compress it to background.

**A primary-data paper gets a full sub-section on how the data were collected and processed**, built
from `methods[]` and running in the order the study ran: who the participants were and how they were
selected, what they were shown and for how long, what was recorded and with what equipment and
settings, then every processing step in sequence — filters, referencing, artifact rejection,
epoching, baseline — then the statistical model with its factors and correction.

Give the numbers. `0.1–30 Hz`, `±100 µV`, `−200 to 800 ms`, `N = 17 / 37 / 37`, `p < .05 FDR` are
the content of this sub-section, not decoration on it. The reader is designing their own experiments
and analysing their own data: this is the part of a paper they can use directly and the part a
summary destroys. Where the paper does not specify a step well enough to reproduce, say so plainly
in one clause and move on. **When the guide runs long, this sub-section is the last thing you cut.**

**Show the joint between result and interpretation, do not just report both.** For each substantive
interpretation, name the result it rests on and the step the authors took to get there — an
inference, an analogy to another literature, a label imported from earlier work. The card's
`rests_on` and `boundary` fields hold this. A reader who sees a Results section and a Discussion
section, with nothing linking them, learns that interpretations follow results automatically, which
is the opposite of what they need.

**Part four covers four things for a primary-data paper**, in this order, matching the coverage rule
in stage 2. The reader is trying to learn how to write each of them:

1. **Building the gap** — from the Introduction, which on an experimental paper is a mini-review.
2. **Stating a design or analysis choice** — from the Methods.
3. **Reporting a result** — with the paper's actual statistical format, from `results_reporting`.
   Say which statistic, in what notation, with what omitted, and whether the numbers live in the
   prose or in a table. This is the section the reader will imitate most literally.
4. **Getting from a result to an interpretation** — the sentence where the paper crosses from what
   it measured to what it means, and what that crossing costs.

A synthesis paper covers 1 and 4, plus how a claim is attributed to the literature and how two
positions are set side by side. No fixed number of moves: one sample may cover two of the four, and
a move the paper performs badly is taught as `AVOID`.

Per move: name it, point at `§Section, p. N`, quote the sentence verbatim in a blockquote labelled
`> **THE AUTHORS' SENTENCE** — §N, p. N`, then say what it does and when it applies. One sentence
per move is the norm; two only when the move *is* the pair, as when a null result and its
attribution are split across consecutive sentences. Any sentence frame you invent goes in a
separate blockquote labelled `> **PATTERN — my example, not the authors'**`. Never let an example be
mistaken for a finding.

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
it is needed, not stacked at the front.

### Use the paper's words

The reader is here to learn the field's vocabulary and the field's English. Your restatement teaches
them neither.

**Quote, do not paraphrase:** the claim itself, definitions, hedges and epistemic verbs, every
number and statistic, and the sentence in which a limitation is stated. These are the places where
the exact wording *is* the content — `may reflect` and `demonstrates` are different findings.

**Paraphrase:** connective narrative, background the reader needs supplied, and anything you are
compressing from several sentences into one.

**If you replaced one of the paper's terms with a synonym you preferred, you have broken S10** and
taught the wrong word. See *Prose constraints*.

Keep total verbatim quotation to a small fraction of the source — roughly a sentence per section,
never a whole paragraph, never a table, never a run of figure captions. This is a study aid that
sends the reader to the paper, not a replacement for it.

### Length

**Ceiling: 3,300 words for a primary-data paper, 3,000 for a synthesis paper. No target, and no
lower bound.** The `## About this guide` footer does not count — the ceiling exists to stop the guide
inventing content about the paper, and the footer contains none. A short guide for a thin paper is correct output. Padding to a number is how a guide
starts inventing content, and the original 2,900–3,250 *target* — calibrated on two single-experiment
papers — did exactly that, then made a coherent synthesis guide worse when it was shaved to fit.

The two ceilings differ because the branches carry different obligations, measured not guessed: the
methods sub-section runs about 520 words and the results-reporting move about 400, and a synthesis
paper spends neither. Kropotov lands at 3,150 with both; Horowitz-Kraus at 2,989 with neither.
**Do not shave a required section to hit the number** — cut in the order below, and if that is not
enough, the guide is as long as the paper requires and the ceiling is the thing that is wrong.

When you are over the ceiling, cut in this order:

1. Part one, anything the reader can get from the paper's own Introduction.
2. Part three's prose, compressed into a claim → evidence → boundary table.
3. Part two's narrative, but never its content — and never the methods sub-section.
4. Anything Part two says that Part four now quotes directly. Adding a writing move about the
   Introduction makes Part two's account of the same paragraph redundant; point across instead.

**Never cut:** the methods parameters, the results-reporting format, the four coverage areas in
Part four, the figure and section pointers, the extraction warnings, or the authors' stated
boundaries. Those are why the guide is trustworthy; the prose around them is negotiable.

### Worked examples

- `output/reading-guides/kropotov-2016-reading-guide.md` — primary data, Frontiers, carries an
  extraction warning and eight analyst notes
- `output/reading-guides/sorsa-2026-reading-guide.md` — primary data, Elsevier

- `output/reading-guides/horowitz-kraus-2026-reading-guide.md` — synthesis, Elsevier, a
  multi-author workshop review with no figures and no tables at all. Worked example of the
  disagreement table and of attributing positions to sections rather than to "the authors".

## Prose constraints

Applies to the card and the guide alike. The rules below are borrowed, with thanks, from the
S1–S16 catalogue in the [academic-ai-pattern](https://github.com/topics/academic-ai-pattern) skill,
which audits academic manuscripts for AI-writing signals. **They are reproduced here in full, so
this skill has no dependency on it.**

If you do have that skill installed, still do not invoke it from here: its scanner, report schema
and validator are built for auditing a manuscript you intend to submit, cost 15–20k tokens per run,
and produce an audit report nobody in this workflow asked for. Borrow the rules, not the pipeline.

The governing sentence, from S8, states this project's thesis better than the design doc does:

> A scholar does not decide importance on the reader's behalf. Whether the argument holds and the
> evidence suffices, the reader can see for themselves.

### Never write these

1. **Evaluative sentences and superlatives (S8).** No "the most sceptical section", "the strongest
   move", "the paper's hardest fact", "worth reading twice", "in my view", "deserves to be quoted".
   Delete the evaluation and keep the content. *Evidence ranking is not evaluation* — "primary
   outcome" is information when the paper established that hierarchy; "important finding" is not.
2. **Verb and list stacking (S1)**, **enumeration that argues by count (S2)**, **abstraction with no
   referent (S3)**.
3. **Colon-plus-expansion used for rhythm (S4)**; **`that` pointing at nothing specific (S5)**.
4. **Template scaffolding (S13)**, **self-answered rhetorical questions (S15)**, **navigational
   meta-talk (S16)** — "in this section we will", "as noted above", "it is worth noting that".

Measured on the first synthesis guide: thirteen S8 violations in 3,553 words, and S8's own keyword
grep caught one of the thirteen. **They hide in superlatives, so a scan will not save you** — this
has to be obeyed while writing.

### Check against the card as you write — the card is already open, so this is free

- **Term identity (S10).** Use the paper's own term, never a synonym you prefer. This is a hard
  requirement, not a style preference: the reader is here to learn the vocabulary, and a swapped
  word teaches them the wrong one.
- **Epistemic strength (S11).** The tier licenses the verb. Never give a tier-(b) position the
  grammar of a tier-(c) consensus.
- **Attribution (S12).** Carry the citation the paper gave (`cited_as`), or carry none and say so.
- **No phantom opposition (S9).** Do not manufacture a contrast the paper does not make.

### Read the finished guide back once

You just wrote it, so it costs almost nothing. Check three things only: the same functional slot
filled the same way twice (S6), paragraph joins that do not hold (S7), abstractions given dramatic
verbs (S14).

### Do not chase these — the manual's §7 says they make writing worse

Three-item lists, sentences over 35 words, passive voice, nominalisation, first-person plural,
`however` / `moreover`, metaphor as such, questions as such, punctuation patterns.
**Methods prose is passive by genre and stays passive.**
