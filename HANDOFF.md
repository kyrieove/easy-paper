# HANDOFF — easy-paper

Written 2026-09-07 at the end of the design/prototyping session. **Read this first in a new session.**

## What this project is

Build a reusable skill that turns local academic PDFs into readable English study guides, so the user (writing a paper in developmental cognitive neuroscience, ~200 local PDFs, low domain confidence) builds their own judgment and learns academic English writing. Token-light. Evidence traceable. Does not connect papers to the user's own research and does not recommend what to read next.

Full requirements: [paper-learning-skill-design-for-review.md](paper-learning-skill-design-for-review.md) — 261 lines, kept current through this session.

## Where things stand

| | Status |
|---|---|
| Stage 1 — local preprocessing | **Done**, run on 4 papers, self-checked. Now emits `warnings` — read them |
| Stage 2 — evidence card | **Done by hand** (model pass), 2 papers, no automation |
| Stage 3 — English guide | **Done by hand**, 2 papers |
| SKILL.md | **Written 2026-09-07** — 212 lines, all three stages. Never executed as a skill |
| End-to-end token cost | **Measured** in a clean session, 2026-09-07 (see Verification of the card-only route) |

## The pipeline

Three stages. Stage 1 is a script, stages 2–3 are model work.

### Stage 1 — `pdf2md.py`

```bash
"/d/2/software/python.exe" pdf2md.py "<paper>.pdf" --out out
```

⚠ **Use that interpreter path.** The `python` on PATH is **LibreOffice's bundled interpreter** and has none of the dependencies. `D:\2\software\python.exe` (3.10.11) has `pdf_inspector` installed. Only dependency: `pdf-inspector`. PyMuPDF was removed when figures stopped being extracted.

Writes `out/<slug>/`:

| File | Contents |
|---|---|
| `body.md` | Text with `<!-- Page N -->` markers, running heads/feet dropped, references removed |
| `refs.md` | References, split off — 29–40% of extracted text, kept out of model context |
| `figures.json` | Figure/table index: id, PDF page, caption. **No images.** |
| `meta.json` | sha256 (cache key), pages, text/scanned, `has_primary_data`, headings, column/table pages |

Idempotent: re-running skips when the sha256 matches; `--force` overrides. Self-check: `"/d/2/software/python.exe" test_pdf2md.py`.

### Stage 2 — evidence card

Model reads `body.md` in full, writes `out/<slug>/evidence-card.json`. Layers: design / results / author interpretations / author-acknowledged limitations / analyst-raised limitations / extraction warnings / **writing samples** / figure pointers with "what to look at".

**Schema is now `evidence-card/primary-data/v2`.** v2 adds `writing_samples`: 5–6 verbatim sentences harvested while the body is already open, each with `quote`, `move` (the argument move the author is performing), `why_it_works`, and optional `conditions`. Include at least one `AVOID` sample — teaching by contrast is cheap and the failure modes are what the user needs to see.

**Store the move, not a template.** The card carries what the author *did*; stage 3 derives any transferable pattern from that. A card full of fill-in-the-blank sentence frames turns Part 4 into a phrasebook, which is the thing it must not become.

Why v2 exists: without it, Part 4 of the guide is impossible from the card and stage 3 must re-read `body.md`. See *Verification of the card-only route*. Stage 2 already has the body open, so harvesting costs nothing extra.

⚠ **Only the Kropotov card is v2.** `development-of-brain-responses.../evidence-card.json` (Sorsa) is still v1 and needs `writing_samples` backfilled — that requires re-reading its `body.md` (~28.6k tokens), so do it in a session that is opening that paper anyway.

**Why it exists: accuracy, not token savings.** Writing fluent English and holding citation discipline at once is two jobs, and fluency wins. Building the ledger first separates them. It is also the least delegatable step — everything downstream trusts it.

### Stage 3 — reading guide

Model reads the card (plus targeted re-reads of `body.md`), writes `output/reading-guides/<author>-<year>-reading-guide.md`. Five parts, structure in §3 of the design doc.

## Traps already paid for

1. **`python` on PATH is LibreOffice's.** Costs 10 minutes every time it is rediscovered.
2. **pdf-inspector emits section headings as bold runs** (`**3. Results**`), not `#` headings. Anything matching `#` fails *silently* — first implementation reported `has_primary_data: false` and split zero references.
3. **Caption format varies by publisher.** Elsevier `Fig. 1.`, Frontiers `FIGURE 1 |`. The delimiter after the number is what separates a caption from an in-text mention (`as shown in Fig. 1, ...`). `CAPTION` in `pdf2md.py` accepts `. : |` — **add delimiters as new publishers appear**.
4. **Superscripts detach during extraction.** In Kropotov 2016, p-value exponents in Tables 2/3/6/7 land on their own rows: `4.85, 10` then a stray `3` means `p < 10⁻³`. Numeric p values in dense tables must be read from the PDF. Record this in the card's `extraction_warnings` when it happens.
5. **`git add -A` swept in `output/skill-maintenance/`** (1.3 MB zip from an unrelated tool). Now gitignored.
6. **agy delegation failed on this kind of task** — 20 minutes, 0 files, only exploration narration. It did install the deps. Do not re-delegate script-writing here without a much tighter brief; writing it directly took ~15 minutes.
7. **Some PDFs shred their small-caps headings, and it looks like success.** Rieger 2016 (Frontiers) emits `MA D ME TH ODS`, `UL TS`, `RE` + `FERENCES`, `FIG URE 1` — letters spaced and runs out of order. **Body prose is completely unaffected**; only heading-styled runs break. First run reported `figs_indexed=0 primary=False` on a *meta-analysis* and printed a normal success line. Fixed in `index_figures` and the `has_primary_data` fallback by probing the de-spaced form of the line (`line.replace(" ", "")`); the delimiter guard after the figure number still blocks in-text mentions, so this adds no false positives. **The deeper fix is that `meta.json` now carries a `warnings` list** (empty refs / zero figures / not primary / shredded headings) and `pdf2md.py` prints them with `!!`. Third time a silent stage-1 failure has cost real time — see traps 2 and 3. Check the warnings before spending stage-2 tokens.
8. **Reference splitting still fails on Rieger 2016** and is not fixed. The `REFERENCES` heading is shredded into `RE` (line 135) and `FERENCES` (line 168) across a two-column layout, and the reference list starts *before* both. `refs.md` is 0 bytes, so `body.md` (41.6 KB) still carries them — roughly 30-40% of stage-2 tokens wasted on that paper. Fixing it needs a content-shaped detector (a long run of numbered citation lines), not another heading regex. Warned about, deliberately not built.
9. **Do not swap `pdf2md.py` for a different PDF converter without checking its engine.** Evaluated firecrawl/anydoc (2026-09-07): its text-PDF path *is* pdf-inspector, the same library `pdf2md.py` already imports. Same extraction, and switching would drop the paper-specific work on top (reference split, running-head removal, figure index, page markers, `has_primary_data`). More basic: **stage 1 costs 0 model tokens** — the PDF never enters context — so no converter can save tokens there; see the closing paragraph of §6.4 in the design doc. `body.md` has ~1.3% short-line debris, so there is nothing left to compress either. anydoc's one real use would be OCR fallback for scanned PDFs (Firecrawl Parse, API key, paid); `pdf2md.py` already flags those via `pages_needing_ocr`. Bolt on OCR if a scanned paper appears; do not replace stage 1 for it.
10. **`pdf_inspector.extract_structure_elements` exists and is unused.** Tested: the two Elsevier PDFs are tagged (real `H2`/`H3` roles, `TD`/`TH` table cells, ~800 elements); the Frontiers one returns 2 elements, i.e. nothing. Deliberately not adopted — the `BOLD_HEAD` regex extracts Kropotov's 36 headings correctly and no failure has been observed. Reach for this only when heading detection actually breaks.

## Design decisions made this session

All are already written into the design doc; sections given for the reasoning.

1. **Branch on "did the authors collect the data?", not the review/experimental label** (§3). Puts meta-analysis on the primary-data side where it belongs. Detected from headings, no model call. **Verified 2026-09-07 on Rieger 2016**: `has_primary_data=True`, forest plot (Figure 2, p. 4) indexed. The rule holds — but only after trap 9 was fixed; the first run said `False`.
2. **Only two things differ between branches** (§3): the spine of *Understanding the Paper*, and the job of *What the Evidence Supports* — "results vs interpretation" for primary data, "established vs this author's position" for synthesis.
3. **Reviews carry one more layer of interpretation** (§4.3). Claims in a review get tagged (a) original result / (b) review author's position / (c) field consensus, and **(b) must never be written as (c)**.
4. **Figures are pointed at, not embedded** (§2.3). `→ Fig. 5 · p. 9` plus "what to look at". Reason: the guide must not replace the paper; the user's stated problem is not opening the PDF.
5. **Evaluation is quarantined to Part 3** and labelled. Parts 1–2 report what the paper says. From user feedback: evaluation woven through the narrative makes the reader absorb the analyst's judgment instead of forming their own — the exact failure mode the whole project exists to avoid.
6. **An experimental paper's Introduction gets the review treatment** (§3). It is a mini-review and it is where the user most needs to learn. Do not compress it to background — this was violated once and had to be fixed.
7. **Output is Markdown.** An HTML version exists (`sorsa-2026-reading-guide.html`, published at https://claude.ai/code/artifact/32f8a360-b650-44bf-af25-b62584a7fc14) and looks better, but MD is the format. Markdown cannot set fonts or sizes; the seven levers that do work are code spans for statistics, blockquotes for the two marked voices, tables for comparisons, heading density (~1 per 130 words), the `→ Fig. n · p. n` convention, 3–4 sentence paragraphs, and bolded standalone instruction sentences.
8. **Writing section splits by branch** (§2.2): synthesis papers teach Introduction/Discussion moves, primary-data papers teach Methods/Results moves. The user is weakest on Introduction and Discussion, so reviews are the *main* source, not the secondary one.

9. **The reader's own notes go in the guide, and stage 3 must not clobber them** (decided 2026-09-07, in response to the user asking where their thinking goes). This is not an accessory — the project's whole thesis is that the user's judgment is the product, so the note slot is where the value gets created.
   - **Editor: Obsidian, with `output/reading-guides/` opened as a vault.** No conversion, files stay plain Markdown, git still works. Buys `==highlight==`, `> [!note]` callouts that render distinctly from the guide's own blockquote voices, and `[[wikilinks]]` between guides — which is the cross-paper structure the user will want at 200 papers, for free, with no knowledge-graph feature to build.
   - **Convention:** inline thoughts as `> [!note] 我` directly under the paragraph they answer; paper-level thoughts appended under a `## My Notes` heading at the end. Do **not** reuse a bare `>` — decision 7 already spends plain blockquotes on two marked voices.
   - **The protecting rule, for SKILL.md:** stage 3 never overwrites an existing guide. If the target `.md` exists, write `<name>-r2.md` and let the user merge. One sentence, no code, and it makes regeneration safe now that stage 3 costs only ~7.7k tokens and will be re-run often.
   - Explicitly **not** a sixth section and **not** a comprehension quiz (§2.5 killed that). The five-part structure is unchanged; `## My Notes` is user-created, appended after Key Takeaways.

10. **Decisions 6 and 8 contradicted each other on Part 4; resolved while writing SKILL.md (2026-09-07).** Decision 8 assigns Methods/Results moves to primary-data papers, decision 6 says a primary-data paper's Introduction is a mini-review and the place the user most needs to learn. The card-only run then produced a Part 4 that taught Introduction moves on a primary-data paper, which read fine and violated 8. **The ruling in SKILL.md: the branch sets the emphasis, it does not ban a section.** A primary-data paper may teach a gap-building move from its Introduction, but a Part 4 that is *only* Introduction phrases is wrong, because Methods and Results are what the user cannot learn from a review. This has not been checked against user reading feedback.

## Measured numbers

- **Bytes per token, measured from a real transcript** (not estimated): prose in `body.md` **2.47 B/tok**; `evidence-card.json` **2.03 B/tok**. JSON is denser than prose — braces, quotes and repeated keys all cost. Do not use the generic ~4 B/tok for either.
- Stage-3 input, per paper:

  | | body.md | card | body tok | card tok | ratio |
  |---|---|---|---|---|---|
  | Sorsa 2026 | 70.7 KB | 13.4 KB | 28.6k | 6.6k | **4.3×** |
  | Kropotov 2016 | 54.1 KB | 15.6 KB | 21.9k | 7.7k | **2.8×** |

  The earlier **8×** was arithmetic on a wrong card estimate (13 KB scored as 3.5k tokens instead of 6.6k). Superseded.
- Fixed session overhead before any paper is touched: **75.6k tokens** (harness + CLAUDE.md + skill listing). The card saves ~12k against that floor, so the honest framing of stage 3's saving is *~15% of a session*, not *8× of anything*.
- References are **29–40%** of extracted text; splitting them out is the single largest stage-1 saving.
- Stage 1 runtime: ~2 s per paper, 0 tokens.
- HTML vs MD markup overhead: **+23%** on content, plus a one-time 7.3 KB stylesheet.

## Open questions

1. ~~The 8× reduction is unverified.~~ **Closed 2026-09-07 by a clean-session run.** See *Verification of the card-only route* below. Short version: the ratio is **2.2×**, not 8×, and the card is sufficient for four of the five parts.
2. **Two copies of the design doc have diverged.** Root copy (261 lines) is current; `output/paper-learning-skill-design-for-review.md` (219 lines) is the pre-session version. Nothing was deleted — the user should decide.
3. **Two of the three paper types have never been through the current rules.** The only review sample (`horowitz-kraus-2026-reading-guide.md`) predates every decision above, so the (a)/(b)/(c) tagging rule has never been exercised on a real review. **Meta-analysis: stage 1 done 2026-09-07** (Rieger 2016, `out/15-years-of-microstate-.../`), stages 2–3 still pending. The old note read: it has never been run at all — and it is the case decision 1's branching rule was written for, so it is the rule's only real test. Both need a paper and a full pass. This is now the largest open risk in the project.
4. **§9 of the design doc still asks questions that are now answered** (figure extraction, whether to adopt pdf-inspector). Stale for anyone reading it fresh.
5. **Guide length settled around 2900–3250 words** across two papers. Not yet confirmed against user reading feedback.

## Verification of the card-only route

Run 2026-09-07, in a session whose only paper input was `evidence-card.json`. Product:
`output/reading-guides/kropotov-2016-reading-guide-cardonly.md`. Token counts below are read
out of the session transcript, not estimated.

**Verdict: the card works, the 8× does not.**

### What it cost

| | tokens |
|---|---|
| evidence card (15.6 KB) | 7.7k |
| one targeted `body.md` re-read (5.7 KB, 4 windows) | 2.3k |
| **stage-3 paper input, total** | **10.0k** |
| reading `body.md` instead | 21.9k |
| **actual reduction** | **2.2×** |

### What the card carried, and what it did not

Parts 1, 2, 3 and 5 came out of the card with **zero** access to the paper. Design logic,
figure pointers with page numbers, the results/interpretation split, all eight analyst notes,
the extraction warning — all present, all usable as written.

**Part 4 (*Learning to Write*) is structurally impossible from the card.** It requires verbatim
sentences from the paper and the card schema contains none. That single gap is what forced the
re-read and is the whole of the 2.8× → 2.2× loss.

> **Fix, and it is nearly free:** add a `writing_samples` array to the card schema. Stage 2 already
> reads `body.md` in full, so harvesting 5–6 quotable sentences there costs nothing extra and makes
> stage 3 a pure card read. Do this before writing SKILL.md — it changes the card spec.

### Card accuracy, spot-checked against the source

Four high-value claims were checked against `body.md` and all four are verbatim-accurate:
`I1`'s "unequivocally", `A1`'s 5–6 / 16 ms per decade, `A2`'s Conclusion-vs-Results contradiction,
`L3`'s descriptive-study admission.

One apparent discrepancy resolved **in the card's favour**: card `R1` gives reaction times as
385–407 ms, the paper's prose says "between 390 and 410 ms". Table 1's actual values are
385, 389, 391, 398, 407 — the card read the table, the authors rounded their own range wrongly
and excluded their own minimum. Worth adding as a ninth analyst note.

### Output comparison

| | hand-written (full paper in context) | card-only (this run) |
|---|---|---|
| words | 3,243 | 3,147 |
| headings | 20 | 23 |
| five-part structure | yes | yes |

No quality gap I can detect from structure and content coverage. **Side finding:** the hand-written
guide's Part 4 teaches Introduction/Discussion moves on a primary-data paper, which contradicts
design decision 8. Judged from its headings only — worth a proper look before it is used as the
worked example for SKILL.md.

## Next task

**Run the synthesis branch end to end, following `SKILL.md` and nothing else.** It is the largest
open risk in the project (open question 3) and the only test of the rules that were written for it:
the (a)/(b)/(c) tier tagging, the synthesis card schema — which `SKILL.md` specifies but which has
never been written even once — and the review spine for Part two.

Paper to use: `The interplay between executive function and learning disabilities.pdf`
(Horowitz-Kraus 2026, Elsevier, `has_primary_data=False`). Stage 1 already done:
`out/the-interplay-between-executive-function-and-learning-disabi/`. There is an old guide for it
(`horowitz-kraus-2026-reading-guide.md`) that predates every current rule — do not read it before
writing, and do not overwrite it; the never-clobber rule sends the new one to `-r2.md`.

Also pending, cheaper: stages 2–3 for Rieger 2016 (meta-analysis, `out/15-years-of-microstate-.../`)
— it is the case decision 1's branching rule was written for, and stage 1 flags that its references
were never split, so budget ~40% wasted tokens or fix trap 8 first.

Worked examples of the output spec, both current:

- `sorsa-2026-reading-guide.md` — primary-data branch, Elsevier
- `kropotov-2016-reading-guide.md` — primary-data branch, Frontiers, includes an extraction warning and eight analyst notes

## File map

```
SKILL.md                      the skill itself; install = copy this folder to ~/.claude/skills/paper-reading-guide/
pdf2md.py                     stage 1, ~110 lines, one dependency
test_pdf2md.py                self-check: running-head filter + caption parsing
paper-learning-skill-design-for-review.md   requirements and design (current)
out/<slug>/                   stage 1 output; only evidence-card.json is tracked
output/reading-guides/        deliverables
HANDOFF.md                    this file
```

Three PDFs are in the project root and gitignored: Sorsa 2026 (Elsevier, primary data), Horowitz-Kraus 2026 (Elsevier, review), Kropotov 2016 (Frontiers, primary data). Git history has one commit per change since the repo was created this session.
