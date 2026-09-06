# HANDOFF — easy-paper

Written 2026-09-07 at the end of the design/prototyping session. **Read this first in a new session.**

## What this project is

Build a reusable skill that turns local academic PDFs into readable English study guides, so the user (writing a paper in developmental cognitive neuroscience, ~200 local PDFs, low domain confidence) builds their own judgment and learns academic English writing. Token-light. Evidence traceable. Does not connect papers to the user's own research and does not recommend what to read next.

Full requirements: [paper-learning-skill-design-for-review.md](paper-learning-skill-design-for-review.md) — 261 lines, kept current through this session.

## Where things stand

| | Status |
|---|---|
| Stage 1 — local preprocessing | **Done**, run on 3 papers, self-checked |
| Stage 2 — evidence card | **Done by hand** (model pass), 2 papers, no automation |
| Stage 3 — English guide | **Done by hand**, 2 papers |
| SKILL.md | **Not started — this is the next task** |
| End-to-end token cost | **Not measured in a clean session** (see Open questions) |

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

Model reads `body.md` in full, writes `out/<slug>/evidence-card.json`. Layers: design / results / author interpretations / author-acknowledged limitations / analyst-raised limitations / extraction warnings / figure pointers with "what to look at".

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

## Design decisions made this session

All are already written into the design doc; sections given for the reasoning.

1. **Branch on "did the authors collect the data?", not the review/experimental label** (§3). Puts meta-analysis on the primary-data side where it belongs. Detected from headings, no model call.
2. **Only two things differ between branches** (§3): the spine of *Understanding the Paper*, and the job of *What the Evidence Supports* — "results vs interpretation" for primary data, "established vs this author's position" for synthesis.
3. **Reviews carry one more layer of interpretation** (§4.3). Claims in a review get tagged (a) original result / (b) review author's position / (c) field consensus, and **(b) must never be written as (c)**.
4. **Figures are pointed at, not embedded** (§2.3). `→ Fig. 5 · p. 9` plus "what to look at". Reason: the guide must not replace the paper; the user's stated problem is not opening the PDF.
5. **Evaluation is quarantined to Part 3** and labelled. Parts 1–2 report what the paper says. From user feedback: evaluation woven through the narrative makes the reader absorb the analyst's judgment instead of forming their own — the exact failure mode the whole project exists to avoid.
6. **An experimental paper's Introduction gets the review treatment** (§3). It is a mini-review and it is where the user most needs to learn. Do not compress it to background — this was violated once and had to be fixed.
7. **Output is Markdown.** An HTML version exists (`sorsa-2026-reading-guide.html`, published at https://claude.ai/code/artifact/32f8a360-b650-44bf-af25-b62584a7fc14) and looks better, but MD is the format. Markdown cannot set fonts or sizes; the seven levers that do work are code spans for statistics, blockquotes for the two marked voices, tables for comparisons, heading density (~1 per 130 words), the `→ Fig. n · p. n` convention, 3–4 sentence paragraphs, and bolded standalone instruction sentences.
8. **Writing section splits by branch** (§2.2): synthesis papers teach Introduction/Discussion moves, primary-data papers teach Methods/Results moves. The user is weakest on Introduction and Discussion, so reviews are the *main* source, not the secondary one.

## Measured numbers

- `body.md` 69 KB ≈ **29k input tokens**. Real ratio ≈ 2.4 bytes/token, not the usual 4 — citations and markup are dense.
- Evidence card 13 KB ≈ **3.5k tokens**. Design target for stage 3 is reading the card instead of the body: **8× smaller**.
- References are **29–40%** of extracted text; splitting them out is the single largest stage-1 saving.
- Stage 1 runtime: ~2 s per paper, 0 tokens.
- HTML vs MD markup overhead: **+23%** on content, plus a one-time 7.3 KB stylesheet.

## Open questions

1. **The 8× reduction is unverified.** Stages 2 and 3 both ran in a session that already had the full paper in context. A clean-session run reading only `evidence-card.json` would confirm or kill it. Worth doing first.
2. **Two copies of the design doc have diverged.** Root copy (261 lines) is current; `output/paper-learning-skill-design-for-review.md` (219 lines) is the pre-session version. Nothing was deleted — the user should decide.
3. **The review branch has no guide produced under the current rules.** The only review sample (`horowitz-kraus-2026-reading-guide.md`) predates every decision above. The (a)/(b)/(c) tagging rule has therefore never been exercised on a real review.
4. **§9 of the design doc still asks questions that are now answered** (figure extraction, whether to adopt pdf-inspector). Stale for anyone reading it fresh.
5. **Guide length settled around 2900–3250 words** across two papers. Not yet confirmed against user reading feedback.

## Next task

Write `SKILL.md`. Roughly half of it is the output spec, and the two guides in `output/reading-guides/` are the worked examples of that spec:

- `sorsa-2026-reading-guide.md` — primary-data branch, Elsevier
- `kropotov-2016-reading-guide.md` — primary-data branch, Frontiers, includes an extraction warning and eight analyst notes

Both are current. `horowitz-kraus-2026-reading-guide.md` is **not** — do not use it as a model.

## File map

```
pdf2md.py                     stage 1, ~110 lines, one dependency
test_pdf2md.py                self-check: running-head filter + caption parsing
paper-learning-skill-design-for-review.md   requirements and design (current)
out/<slug>/                   stage 1 output; only evidence-card.json is tracked
output/reading-guides/        deliverables
HANDOFF.md                    this file
```

Three PDFs are in the project root and gitignored: Sorsa 2026 (Elsevier, primary data), Horowitz-Kraus 2026 (Elsevier, review), Kropotov 2016 (Frontiers, primary data). Git history has one commit per change since the repo was created this session.
