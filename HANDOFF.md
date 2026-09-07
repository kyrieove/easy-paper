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
| SKILL.md | **Written 2026-09-07**, then revised twice the same day (decisions 11–13). All three stages, plus *Prose constraints*. Never executed as an installed skill |
| Card schema | **v3** both branches. Two cards migrated; two others still on the old key — see the warning under *Next task* |
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
5. **`git add -A` swept in `output/skill-maintenance/`** (1.3 MB zip from an unrelated tool). Now gitignored. **Second occurrence, 2026-09-07:** `.gitignore` guarded `out/**` but `pdf2md.py`'s default `--out` had moved to `output/extracted/`, so the whole 221-paper extraction — **21 MB** — was one `git add -A` from the index. The rule is now mirrored for both paths, keeping `evidence-card.json` and dropping the rest. When the script's output path moves, the ignore rule does not follow it.
6. **agy delegation failed on this kind of task** — 20 minutes, 0 files, only exploration narration. It did install the deps. Do not re-delegate script-writing here without a much tighter brief; writing it directly took ~15 minutes.
7. **Some PDFs shred their small-caps headings, and it looks like success.** Rieger 2016 (Frontiers) emits `MA D ME TH ODS`, `UL TS`, `RE` + `FERENCES`, `FIG URE 1` — letters spaced and runs out of order. **Body prose is completely unaffected**; only heading-styled runs break. First run reported `figs_indexed=0 primary=False` on a *meta-analysis* and printed a normal success line. Fixed in `index_figures` and the `has_primary_data` fallback by probing the de-spaced form of the line (`line.replace(" ", "")`); the delimiter guard after the figure number still blocks in-text mentions, so this adds no false positives. **The deeper fix is that `meta.json` now carries a `warnings` list** (empty refs / zero figures / not primary / shredded headings) and `pdf2md.py` prints them with `!!`. Third time a silent stage-1 failure has cost real time — see traps 2 and 3. Check the warnings before spending stage-2 tokens.
8. ~~**Reference splitting still fails** when the `REFERENCES` heading is shredded.~~ **FIXED 2026-09-07** — and it was never an edge case. Deferred twice as "one awkward two-column paper"; on the real 221-paper library it was **74 papers, 35%, about 800k wasted stage-2 tokens**. `split_refs` now tries the heading first and falls back to a content-shaped detector: a long run of citation-shaped lines in the back half of the paper. Result across all 221 — 56 newly split, 2 partial heading splits completed, 21 still failing, 142 untouched, **0 papers lost body text**. Measured after re-extraction: refs-unsplit 74 → 21, waste 797k → 210k.

   The three thresholds are corpus-derived and the reasoning matters more than the numbers:
   - **Count citation-shaped LINES, never citations within a line.** Counting inside lines was tried first, to catch bibliographies that extraction merges into one 4,000-character line — and it ate real prose from **23 papers**, because a Discussion paragraph citing five works scores five. Those merged-line papers are most of the 21 that still fail; they still get the stage-1 warning.
   - **Density ≥ 0.35**, because real lists here bottom out at 0.39: wrapped continuation lines carry no year and dilute the run. The 0.60 first tried rejected 19 genuine lists and prevented nothing.
   - **The run must start in the back half.**

   Two papers that looked like false positives were real: the heading matched once, the list restarted after a page break, and the tail stayed in the body. `split_refs` is now two-pass for that reason.

11. **`slugify` silently overwrote 10 of 221 papers.** Found by the batch scan: 221 PDFs in, 211 folders out, every per-file call exited 0. The slug truncates the title to 60 characters, so two papers agreeing that far shared a folder and the second won. All 10 were distinct files by sha256 — not duplicate copies. **Fixed**: the folder is now `<slug[:52]>-<sha256[:6]>`, verified collision-free across 221. This is the **fourth** silent stage-1 failure (see 2, 3, 7), and the pattern never changes: a per-file success line hides a whole-corpus problem. `batch_scan.ps1` now compares folder count against PDF count and says so in red.
9. **Do not swap `pdf2md.py` for a different PDF converter without checking its engine.** Evaluated firecrawl/anydoc (2026-09-07): its text-PDF path *is* pdf-inspector, the same library `pdf2md.py` already imports. Same extraction, and switching would drop the paper-specific work on top (reference split, running-head removal, figure index, page markers, `has_primary_data`). More basic: **stage 1 costs 0 model tokens** — the PDF never enters context — so no converter can save tokens there; see the closing paragraph of §6.4 in the design doc. `body.md` has ~1.3% short-line debris, so there is nothing left to compress either. anydoc's one real use would be OCR fallback for scanned PDFs (Firecrawl Parse, API key, paid); `pdf2md.py` already flags those via `pages_needing_ocr`. Bolt on OCR if a scanned paper appears; do not replace stage 1 for it.
12. **`has_primary_data` sent 45 of 221 papers down the wrong branch.** Found 2026-09-07 by probing the corpus rather than by any failure report. `PRIMARY` only ever looked at `headings[]`, and some publishers — Brain and Cognition, Int. J. Psychophysiology — never emit section headings as bold runs at all, so `headings[]` came back holding journal names and table cells and `Methods` was never in it. "No methods heading" was then read as "this is a review".

    The flag made it invisible: `BRANCH?` fired on `has_primary_data == False`, so it fired on **all 94** synthesis papers and carried zero information. A user who ignores 94 "confirm by hand" notices also ignores the real one. **This is the fifth silent stage-1 failure and the shape has never changed** (traps 2, 3, 7, 11): a per-file success line hides a whole-corpus problem, and the warning that should catch it is tuned so loosely it is noise.

    **Fixed** with the same two-tier structure `split_refs` already uses — headings first, content shape as the fallback. Only a paper that collected data writes *informed consent* / *were recruited* / *ethics committee*, so `COLLECTED` probes `body.md` when the heading path finds nothing. New `is_primary(headings, shredded, body)` returns `(primary, from_headings)`; four asserts in `test_pdf2md.py`. `BRANCH?` now fires only when the prose decided the branch (so every heading-derived field in that paper is suspect) or when there are no headings at all.

    Measured across the 221, replayed on the extracted bodies and then confirmed by a real `-Force` re-scan:

    | | before | after |
    |---|---|---|
    | primary / synthesis | 127 / 94 | **172 / 49** |
    | `BRANCH?` flags | 94 (= every synthesis paper) | **48** |
    | zero-flag papers | 84 | **102** |

    Spot-check of the 49 that stayed synthesis: *ADHD current concepts and treatments*, *Current state of EEG/ERP microstate research*, *Executive control function*, a corrigendum. Review-shaped. The fallback is not over-firing.

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

11. **The guide was reading as a peer review, and the cause was a container in the card schema (user feedback, 2026-09-07).** The user's words: 产出包含了大量 AI 评价，有点沾边 review 而不是客观的学习材料. Measured, not asserted — superlative/verdict phrases per guide:

    | | AI verdicts | words |
    |---|---|---|
    | horowitz-kraus r2 (synthesis) | **13** | 3,553 |
    | kropotov (primary data) | **1** | 3,243 |

    Thirteen to one. The synthesis branch invites ranking because Part three's job for that branch — *established vs this author's claim* — reads as an invitation to rank the eight authors against each other. The root cause is upstream of the prose: SKILL.md made `limitations_analyst_raised[]` a first-class array, so nine opinions were produced to fill it, and stage 3 had little else to write with.

    Fixed: the array is now **`unstated_by_the_paper[]`** and every entry must pass a **pointing test** — settleable by pointing at two places that disagree, a number that does not match, a missing citation, or something the paper never states. `kind` ∈ contradiction / missing_method / number_mismatch / unsourced_claim / location. An empty array is a good outcome. Both existing cards migrated: Kropotov's 8 entries all passed unchanged (a real signal that the primary-data branch was never the problem); the synthesis card lost one entry outright — *"sections 6 and 7 are worth reading twice"* — and the other 8 were rewritten from judgments into pointings.

    Part three's job in SKILL.md changed from *evaluate it* to *map claims onto their evidence, and stop*.

12. **Prose rules borrowed from `academic-ai-pattern`; the skill itself is never invoked (decided with the user, 2026-09-07).** User's ruling: 只借用规则，而不是调用. Running the skill costs 15–20k tokens per paper (loads `quick-rules.md` + `report-schema.md`, runs a python scanner, writes a versioned report, runs a validator) and produces an audit report nobody wants — it is built for a manuscript you intend to submit.

    Of its S1–S16: **9 became write-time prohibitions** (S8 evaluative sentences, S1, S2, S3, S4, S5, S13, S15, S16); **4 are checked against the card while writing**, free because the card is already open (S10 term identity, S11 epistemic strength, S12 attribution, S9 phantom opposition); **3 need one read-back of the finished guide** (S6, S7, S14), also cheap because you just wrote it.

    ⚠ **Its keyword scanner is nearly useless here.** S8's own grep found 1 of the 13 verdicts in the synthesis guide. AI evaluation in this corpus hides in **superlatives** (`the most sceptical section`, `the strongest move`, `worth reading twice`, `in my view`), which no regex catches. The value is entirely in the judgment criteria, not the tooling.

    Its **§7 假信号** section is protective as well as restrictive, and that matters here: it forbids treating three-item lists, >35-word sentences, passive voice, nominalisation, `however`, metaphor-as-such or questions-as-such as problems. **Methods prose is passive by genre and stays passive** — which protects the methodology detail the user asked for. One unresolved conflict: ponytail mode says replace metaphor with literal action, `ai_pattern` §7 measured humans using metaphor 2.4× more than models and narrows S14 to abstractions given dramatic verbs. Currently following `ai_pattern`, because it has a corpus behind it.

13. **Card v3 — the other four user problems, all built and verified 2026-09-07.** Schema is now `evidence-card/primary-data/v3` and `evidence-card/synthesis/v3`.

    - **`design[]` → `methods[]`** with `stage` ∈ participants / materials / procedure / acquisition / processing / analysis, ordered *as the study ran*, not as the paper presents it. `what_was_done` holds the paper's own sentence; **`parameters` holds the actual numbers** — filter cutoffs, rejection thresholds, sampling rate, trial timings, viewing distance, the model and its factors. `unclear` records a step too vague to reproduce. A parameter the card drops is gone: stage 3 does not re-read the body. Part two of the guide gains a required sub-section built from this array, and it is **the last thing cut** when the guide runs long.
    - **Length: a 3,000-word ceiling with a cut order, not a target.** No lower bound — a short guide for a thin paper is correct output. Cut order: Part four to two moves → Part one background → Part three prose to a table → Part two narrative. Never cut the methods parameters, the pointers, the extraction warnings, or the authors' stated boundaries.
    - **No fixed item counts anywhere.** Writing moves and takeaways are as many as the paper offers; `writing_samples` no longer demands 5–6 or a mandatory AVOID. Padding to a number is how a guide starts inventing content.
    - **Carry the paper's wording** (new stage-2 rule 6). Where the paper states something in one sentence, the card's `text` / `what_was_done` **is that sentence**. Stage 3 quotes claims, definitions, hedges, numbers and limitation sentences; it paraphrases connective narrative only. Stage 3 cannot quote what stage 2 did not keep.

    **Verified by regenerating the Kropotov guide from the v3 card** (`kropotov-2016-reading-guide-r2.md`):

    | | words | headings | verdicts | S8 hits |
    |---|---|---|---|---|
    | old guide | 3,243 | 25 | 1 | 1 |
    | r2 | **2,758** | 24 | **0** | **0** |

    **Adding a full methods sub-section made the guide 485 words shorter.** Detail and length do not trade against each other — the verdicts were the length. That is the single most useful number from this session.

    Re-harvesting Kropotov's methods also turned up two things the old card had missed: the trial counts contradict themselves inside one paragraph (four blocks of one hundred trials, then each block consisting of 400), and the micro signs are lost in extraction, so the rejection thresholds read `100 mV` when they are microvolts.

    Cost: the card grew **15.6 KB → 27.3 KB** (~+5.8k tokens to read). Pay it. The guide has a ceiling; the card does not.

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
3. ~~**Two of the three paper types have never been through the current rules.**~~ **Closed 2026-09-07.** The synthesis branch was regenerated under v3 (commit 919689b) and the meta-analysis went end to end the same day — see *The Rieger run* below. All three paper types have now been through the current rules.
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

## Shipped, and the real corpus

**Published:** https://github.com/kyrieove/easy-paper — MIT, public, 6 files, no examples
(removed at the user's request along with everything machine-specific). Installed locally at
`~/.claude/skills/easy-paper/`; it loads without restarting the session.

**The library is real now:** `01_classified_pdfs/`, **221 papers** in 9 topic folders, gitignored.
This is the first time the project has had a corpus rather than four papers, and it immediately
falsified two "edge case" judgements (traps 8 and 11).

`batch_scan.ps1` runs stage 1 over the whole library for **0 tokens** (~10 min) and prints a triage
table plus `output/triage.csv`. Current state of the 221:

| | |
|---|---|
| usable | 220 (1 scanned, no OCR path) |
| primary / synthesis | **172 / 49** — was 127 / 94 before trap 12 was fixed |
| refs still unsplit | 21 — merged-giant-line cases, see trap 8 |
| shredded headings | 15 |
| zero-flag papers | **102** — was 84 |
| **stage 2 for everything** | **~5.37M tokens** |

That last number is the decision the project now faces. Processing the whole library is not a
sensible default; the triage exists so the user can spend on a chosen subset. The cheapest 15 ready
papers are listed at the end of every scan run.

**Batch architecture, agreed but not built.** One subagent per paper, each starting cold, doing
stage 2 and stage 3 back-to-back in the same context — the card read then costs nothing extra, and
the orchestrator's context stays flat. Do *not* batch by looping in one long session: the user's own
measurements put 74% of spend above 200k of context, so a single growing session is worse than N
cold ones. Stage 2 must not be delegated to a cheaper model; everything downstream trusts the card.

## The Rieger run — the meta-analysis, end to end

Done 2026-09-07. `output/extracted/15-years-of-microstate-research-in-schizophrenia-whe-e817e4/evidence-card.json`
and `output/reading-guides/rieger-2016-reading-guide.md`. This closes open question 3: all three paper
types have now been through the current rules.

**Decision 1's branching rule holds on the case it was written for.** `has_primary_data=True` via the
shredded-heading fallback; the card is `evidence-card/primary-data/v3`; `methods[]` came out as a
search strategy and a pooling model — 15 entries across `materials` / `procedure` / `participants` /
`processing` / `analysis` — and the stage-ordering rule (as the study ran, not as the paper presents
it) worked without modification. No schema change was needed for a paper type the schema was not
designed on.

Guide numbers, against the four Kropotov was checked on:

| | Kropotov r2 | Horowitz-Kraus r3 | **Rieger** |
|---|---|---|---|
| words | 2,758 | — | **3,368** (ceiling 3,300) |
| headings | 24 | — | **21** |
| verdicts | 0 | 0 | **0** |
| S8 hits | 0 | 0 | **0** (one `the most`, inside a verbatim quote) |

**Two findings worth acting on.**

1. **The card cost more than the paper.** `body.md` 31.0 KB = 12.9k tokens; `evidence-card.json`
   39.8 KB = **20.1k tokens**. The card is **1.56×** the body, not a fraction of it. The 2.2× *saving*
   measured on Kropotov does not generalise — it was a 54 KB body. On a short paper a detailed v3 card
   inverts the ratio, because `methods[]` is sized by how much method the paper has, not by how long
   the paper is, and a 7-page meta-analysis is almost entirely method. SKILL.md already says the card
   "exists for accuracy, not for token savings"; this is the number that proves it. **Do not sell the
   card as a token saving anywhere.**
2. **3,368 words against a 3,300 ceiling, after cut rules 1 and 4 were applied.** Going further would
   have hit the never-cut list. A meta-analysis carries a full methods sub-section *and* a
   results-reporting move (like primary data) *and* an inclusion-criteria argument that a lab study
   does not have. Either the primary-data ceiling wants ~3,500 for this sub-type, or the ceiling is
   right and 2% is inside the noise. One paper is not enough to decide; record the second before
   changing the number.

## Next task

**Read `rieger-2016-reading-guide.md` and say whether it is useful.** Every quality number in this
project is structural — words, headings, verdict counts. Not one has been checked against the user
actually reading a guide, and three of the five open questions ultimately turn on that. This costs
20 minutes and no tokens.

Then, in order:

1. **Commit the branch fix and the Rieger run.** Uncommitted as of this writing: `pdf2md.py`,
   `test_pdf2md.py`, `batch_scan.ps1`, `README.md` (recovered — see below), the Rieger card and guide,
   and this file.
2. **Spend on a first real batch.** 102 papers now carry zero flags; the cheapest is 6.3k. Ten papers
   is a defensible first spend and would give the length ceiling a real sample. Build the batch
   architecture (one subagent per paper, cold, stages 2–3 back to back) rather than looping in one
   session.
3. **The 21 REFS papers, 599k wasted tokens.** Trap 8's remaining tail: bibliographies that extraction
   merges into one giant line, which the line-counting detector cannot see by design.
4. **Two papers are byte-identical duplicates**, 70k tokens: `behavioral-inhibition-in-children-with-learning-di…`
   shares a body with `evidence-for-specificity-of-erp-abnormalities-during-d41064`, and
   `executive-functioning-profiles-and-mathematical-and-…` is filed twice under different topics.
   Checked by sha256 of `body.md` across all 221 — the 11 same-prefix slug groups are mostly *not*
   duplicates, just title-truncation collisions with genuinely different papers behind them.

**Repo hygiene, found 2026-09-07 and half-fixed.** This clone has **no git remote**, though the
HANDOFF says the skill is published at github.com/kyrieove/easy-paper — the published copy and this
repo are separate things and will drift. `README.md` existed only in `~/.claude/skills/easy-paper/`
and was untracked anywhere; it has been copied back into the repo but is still uncommitted.
`batch_scan.ps1` was never installed into the skill folder and SKILL.md never mentions it — the
installed skill could not do library-scale work. All four repo files are now synced to
`~/.claude/skills/easy-paper/`; **SKILL.md still does not document `batch_scan.ps1`.**

Worked examples of the output spec:

- `sorsa-2026-reading-guide.md` — primary-data branch, Elsevier
- `kropotov-2016-reading-guide.md` — primary-data branch, Frontiers, includes an extraction warning and eight `unstated_by_the_paper` entries
- `horowitz-kraus-2026-reading-guide-r2.md` — synthesis branch, multi-author workshop review. **Structure only.** It was written before *Prose constraints* existed and breaks them thirteen times

⚠ **Two cards outside this session's work still carry the old `limitations_analyst_raised` key** and
are uncommitted: `out/1-s2-0-s0911604424000216-main/` (v2) and
`out/development-of-brain-responses-.../` (Sorsa, still v1, also missing `writing_samples`).
Deliberately not touched — they are someone else's in-progress work. Migrate them when that work
lands. There is also an untracked `output/reading-guides/zhu-2024-reading-guide.md`.

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
