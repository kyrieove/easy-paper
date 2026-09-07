# Childhood Dyslexia at 27

**Sorsa, A., Tretow, A., Xu, W., Gerike, G., Lohvansuu, K., Hämäläinen, J. A., & Leppänen, P. H. T. (2026).**
Development of brain responses to speech sounds and associations with reading and reading related skills in adults with childhood dyslexia.
International Journal of Psychophysiology, 222, 113339.

|                       |                                                                                                                                                                                          |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **What it asks**      | Finnish children whose brain responses to speech differed at 9.5 years are now 26–28. Are those differences still there — and do they still track how well the person reads?             |
| **What it found**     | A group difference survives, but it has moved to a different speech feature. The link between brain response and reading ability has not survived at all.                                |
| **Why it is unusual** | Two of the three headline results are absences, and the one positive result runs opposite to most of the dyslexia literature: responses in the dyslexia group are *larger*, not smaller. |

**Two conventions used throughout.** `→ Fig. 5 · p. 9` marks a place to stop and open the PDF — figures are not reproduced here on purpose. Statistics appear as `F(2, 88) = 24.87` so they stay findable in the prose. Page numbers are **PDF pages**; the file opens with a repository cover sheet, so the article starts on PDF page 2.

Evaluation is confined to Part three and labelled there. Parts one and two report what the paper says.

---

## Part one · Before You Read

*Background you need that the paper assumes you already have.*

### The sample is the reason the paper exists

The **Jyväskylä Longitudinal Study of Dyslexia** (JLD) has followed the same Finnish participants from birth into adulthood.

So this paper is not comparing adults with dyslexia against strangers. It is comparing them against *their own younger selves*, as measured in earlier JLD papers. Groups are therefore defined by **childhood** reading status, not adult status — a decision that quietly shapes everything downstream.

### The measurement

Participants watched a silent film and ignored a stream of speech sounds. One sound repeated 80% of the time (the **standard**); two rarer sounds (the **deviants**) broke the pattern. Averaging the EEG time-locked to each sound type yields an **event-related potential** (ERP): a waveform whose successive peaks — N1, P2, MMN, P3a, LDN — index stages of auditory processing.

The one to know is the **mismatch negativity** (MMN): a response the brain produces automatically when a repeated pattern is violated, whether or not the listener is paying attention. A group difference in the MMN is normally read as a difference in how sharply the brain encodes that particular speech contrast.

### Two deviants, two phonetic features

The standard was the Finnish pseudoword `/at:a/`.

- `/ata/` — differs in **phonemic length**, a shorter silent gap before the consonant.
- `/ap:a/` — differs in **place of articulation**, a `/p/` instead of a `/t/`.

Finnish uses phonemic length to distinguish word meanings, which is why the length contrast carries more weight here than it would in English.

Keep the two deviants apart in your head. The paper's central finding is that the groups differ on one of them and not the other, and that which one has changed since childhood.

---

## Part two · Understanding the Paper

*What the paper argues, and how each step is supported.*

### The literature the paper is arguing with

The paper's own Introduction (§1.1–1.3, pp. 2–4) is a compact review, and it is worth reading as one, because the result only registers as surprising against it.

The starting proposal is that speech perception deficits may *precede* and feed into phonological deficits, so that accurate phonological representations never form properly (Goswami, 2002). Behavioural work has documented these deficits extensively — trouble discriminating consonants, vowels and phonemic length, syllable stress, lexical tone, speech in noise.

The authors then make a specific criticism of that body of work: it establishes the deficit as a phenomenon but leaves the underlying **processing stages** unexamined. That criticism is what licenses an ERP study. Watch how much work one sentence of criticism does here — it converts a well-studied topic into an open question.

The ERP evidence itself splits by age, and the split matters:

| Population | What the literature reports |
|---|---|
| **Children with dyslexia** | Fairly consistent *attenuated* MMN, across length contrasts (`/ba/`–`/ba:/`) and place contrasts (`/ba/`–`/da/`, `/da/`–`/ga/`, `/ba/`–`/ga/`) |
| **Infants at familial risk** | Mostly smaller or absent mismatch responses; at least one study reports larger ones; newborn studies find no group effect at all |
| **Adults with dyslexia** | Genuinely fragmented — diminished MMN for some place contrasts, no group effect for vowel length, and *enhanced* N100m and N1 in two studies |
| **The JLD sample itself** | Has gone against the field: at 6.5 and 9.5 years these participants showed *enhanced* responses (Hämäläinen et al., 2013; Lohvansuu et al., 2014) |

The authors attribute the adult inconsistency to methodology as much as biology: differing dyslexia criteria, participant numbers, age ranges and stimuli.

A second strand (§1.3, p. 4) links brain responses to later reading. Larger mismatch responses in infancy are reasonably consistently associated with better later reading and pre-reading skills. Closer to school entry the picture loosens — both larger and smaller amplitudes have been linked to better outcomes, along with stronger left lateralisation, so the direction of the association is not settled. Evidence in adulthood is thin, which is the gap this paper occupies.

### The question

Two questions, stated in §1.4 (p. 5):

1. **RQ1** — do the childhood group differences in ERPs persist into adulthood?
2. **RQ2** — in adulthood, do these responses still track reading and reading-related skills?

Neither can be asked from a single timepoint. Both depend on the longitudinal backdrop above.

### How the design answers it

**Grouping** (§2.1 and `→ Table 1 · p. 5`). Adults were split by *childhood* status:

| Group | Who | N |
|---|---|---|
| RDFR | childhood reading difficulty + familial risk | `17` |
| TRFR | typical readers with familial risk | `37` |
| TRC | typical readers, no familial risk | `37` |

The grouping deliberately reproduces the one used in the 9.5-year paper so the two ages can be compared. RQ1 ran on EEG from 91 participants; RQ2 on combined M/EEG from 84, after seven were dropped for MEG data quality.

**Task and stimuli** (§2.3). Open `→ Fig. 2 · p. 7` now — it shows the oddball structure in one picture, and nothing downstream makes sense without it.

Then in `→ Fig. 3 · p. 8`, find the silent gap in the middle of each waveform. That gap, `95 ms` against `255 ms`, *is* the length contrast. Note also that the deviant feature sits in the **middle** of the pseudoword rather than at its onset, unlike most comparable adult studies.

**Statistics** (§2.4.3, p. 9). Group differences were tested with threshold-free cluster enhancement plus permutation testing — a data-driven method that locates clusters of effect across time and sensors without the researcher choosing a time window in advance. Nine comparisons were run (three group pairs × three stimuli), and twelve correlations for RQ2 (three stimuli × four behavioural measures). No correction was applied across either family.

### What was observed

Read the results in three layers.

#### Layer 1 — behaviour is still different

In adulthood the childhood-dyslexia group still scored lower on reading fluency `F(2, 88) = 24.87, p < .001, η² = 0.36`, reading accuracy `F(2, 88) = 9.67, p < .001, η² = 0.18`, and rapid naming `F(2, 86) = 7.70, p < .001, η² = 0.15`. The two typical-reading groups did not differ from each other.

`→ Fig. 1 · p. 6` plots fluency and accuracy from 9.5 years to adulthood for all three groups. **Look at whether the three lines stay parallel rather than fanning out.**

Statistically: a main effect of group for fluency `F(2, 79) = 29.56, p < .001` and accuracy `F(2, 79) = 16.69, p < .001`, accuracy improving with time `F(1, 79) = 5.57, p = .021`, and no time × group interaction for either (`p = .743`, `p = .236`).

#### Layer 2 — the brain difference has moved

For the place-of-articulation deviant `/ap:a/`, the childhood-dyslexia group showed **stronger** responses than both other groups: against TRFR from `152 ms` to `800 ms` across midline and both hemispheres, and against TRC in the left hemisphere around the `300 ms` and `600 ms` windows. TRFR and TRC did not differ, so familial risk alone did not produce the effect.

No group differences appeared for the length deviant `/ata/` or for the standard — although at 9.5 years, in a largely overlapping sample, `/ata/` was exactly where the difference lived.

`→ Fig. 5 · p. 9` is the result figure. Masked colour boxes mark significant clusters; yellow stars in panels C and D mark the channels. **Verify with your own eyes that the effect appears only in the `/ap:a/` row.**

Then `→ Fig. 7 · p. 11`, panel B, which shows the length deviant: the three group curves now sit on top of one another.

#### Layer 3 — the brain–behaviour link is gone

No significant correlations were found between source-level M/EEG activity and any of the four behavioural measures, across all twelve combinations. Source activity was where it should be, in left and right auditory cortices (`→ Fig. 8 · p. 12`).

The authors did not stop at the null. In §3.1.3 (p. 10) they plotted the full distribution of point-wise correlations for each of the twelve tests: distributions were roughly normal and centred near zero, mean `r` between `−0.05` and `+0.09`, with the share crossing the uncorrected threshold running `1.4%–11.8%` against a `5%` chance expectation.

In `→ Fig. 9 · p. 13`, **the red dashed lines at `±0.215` and the inset statistics are what carry that argument.**

### How the authors explain it

The account is developmental (§4.1, pp. 12–13): the *feature* that separates the groups shifts with age — length at 9.5 years, place of articulation at 27 — driven by maturation plus continued exposure to speech making different linguistic features salient at different stages.

For RQ2 (§4.2, p. 13) they argue that adult reading is shaped by so much else, exposure and learned strategies among it, that a childhood link between speech encoding and reading would be expected to wash out.

They also name a conflict rather than smoothing it. Elsewhere in the literature, *enhanced* responses to native speech deviancy are read as reflecting **better** speech processing and better reading. In the JLD sample, enhancement is what the dyslexia group shows. The same direction of effect therefore carries opposite meanings in the two literatures.

The authors have themselves given it two different mechanistic readings at different ages — maturational (larger, less specific neuronal populations) at 6.5 years, compensatory (more neurons working harder) at 9.5 years.

---

## Part three · What the Evidence Supports

*Separating what was measured from what it was taken to mean. All evaluation in this guide lives here.*

### Well supported

The behavioural group differences in adulthood — large effects across three converging measures. The presence of a group difference for `/ap:a/` in the direction of enhancement. The absence of detectable brain–behaviour correlations *within the sensitivity of this method and sample*; the `→ Fig. 9 · p. 13` histograms make this a positive demonstration rather than a bare null.

### Supported, but the direction is assumed

That the group difference has "moved" from length to place of articulation. This sets a significant result here against a significant result in a different paper, and a null here against a significant result there. No age × feature interaction was tested, although 79 participants have EEG at both ages.

### Interpretation, not result

The maturation-plus-exposure account, and the compensation account of the enhanced responses. Both are stories fitted to a direction of effect. Nothing in this design distinguishes "more neurons recruited to compensate" from "less sharply tuned populations responding more broadly" — the same authors have used both, at different ages, for the same observation.

> **BOUNDARIES THE AUTHORS STATE** — §4.3, pp. 13–14
>
> The stimulus setup changed between the infant and 6.5-year measurements and the later ones. Nine comparisons inflate Type I error, and no correction was applied — choosing one is said to be not straightforward given longitudinal priors and non-independent effects. The mid-word placement of the deviant feature may cause masking and makes comparison with other adult studies indirect. Difference waves could not be computed because the stimuli differ in physical length; the authors argue that since the standard showed no group difference, the deviant effect is likely stimulus-specific.

> **READER'S NOTES — MINE, NOT THE AUTHORS'**
>
> **1. The nulls rest on 17 people.** Both central developmental claims — no `/ata/` difference, no brain–behaviour correlation — depend on the RDFR cell. No power analysis or equivalence test is reported, so "the childhood difference is gone" and "we could not detect it with `N = 17`" are not distinguished. The Fig. 9 histograms partly answer this for RQ2; nothing answers it for RQ1.
>
> **2. The uncorrected comparisons cut one way only.** Type I inflation threatens the single positive finding, not the nulls. It is raised as a general caveat but applies asymmetrically to the paper's own results.
>
> **3. The two questions ran on different samples** — `N = 91` against `N = 84`. Reading the group difference and the correlation null as one developmental story is looser than it appears.
>
> **4. The Matthew-effect contrast is low-powered too.** "No widening" comes from a non-significant interaction across three groups totalling 82, one of which holds 17. Non-significance is the expected outcome here whether or not widening occurred.
>
> **5. A joint analysis seems available and was not run.** With 79 participants measured at both ages, a within-subject test of the age × feature shift appears possible from what the Methods describe.
>
> None of these make the paper wrong. They mark where its confidence should sit lower than a fast reading would put it.

---

## Part four · Learning to Write

*Four moves from this paper, for your own Methods and Results. Originals are pointed to, not reproduced — open the page and read the sentence in place.*

### 1 · Turning a null into a demonstration

§3.1.3, p. 10, the sentences after the correlation result. The authors do not stop at "no significant correlations were found": they report the shape of the whole correlation distribution and compare the observed rate of threshold-crossing against chance.

The move is — **when your result is an absence, characterise the absence quantitatively instead of asserting it.**

> **PATTERN — my example, not the authors'**
>
> No significant association was found between X and Y. Across all N tests, the coefficient distributions were centred near zero (mean r = …, SD = …), and the proportion exceeding the uncorrected threshold (…) was …%, consistent with chance expectation.

Use it when a null is load-bearing for the argument. Do not use it to dress up a null you neither predicted nor need.

### 2 · Justifying a method by naming what it protects against

§2.4.3, p. 9, where TFCE is introduced. The method is not merely named; the sentence says what it buys — clusters found across time and sensors *without a predefined threshold*, with permutation testing controlling multiple comparisons.

> **PATTERN — my example, not the authors'**
>
> We used [method], which [does X] without requiring [the researcher choice that would otherwise bias the result], while [second method] provides control for [specific threat].

The habit worth copying is the subordinate clause. A method sentence that only names the method leaves the reader to guess why; one clause turns it into an argument.

### 3 · Stating a limitation, then bounding it

§4.3, p. 14, the passage on difference waves. The authors explain why difference waves could not be computed, then immediately argue that the standard stimulus showed no group difference, so the deviant effect is likely stimulus-specific. The limitation is admitted and then fenced.

> **PATTERN — my example, not the authors'**
>
> [Constraint] meant that [analysis] could not be performed, because [reason]. However, [independent observation from the same data], and therefore [the specific inference that survives].

This is the difference between a limitations section that erodes a paper and one that delimits it. What makes it work: the fence is built from evidence already reported, not from reassurance.

### 4 · Marking a conflict with the literature instead of hedging

§4.1, pp. 12–13, where the enhanced responses are set against the field's attenuated ones. The authors neither argue the field is wrong nor fold their result into it. They mark the conflict and leave it open.

> **PATTERN — my example, not the authors'**
>
> In [other samples], [finding] has been interpreted as reflecting [meaning A]. This is partly in contrast to [our result], where [the same direction] appears in [the opposite population]. [One sentence on what would resolve it.]

Reach for this when your result points the same way as prior work but cannot mean the same thing. Naming the tension is more publishable, and more honest, than a hedge that hopes the reviewer will not notice.

---

## Part five · Key Takeaways

**The finding is a shift, not a disappearance.**
A brain difference remains in adults with childhood dyslexia, but it now attaches to place of articulation rather than phonemic length. That claim rests on comparing two papers, not on a tested interaction.

**Direction matters as much as significance.**
This sample shows enhanced responses in the dyslexia group where most of the field reports attenuation. Whether enhancement means compensation or blunter tuning is unresolved — and the same authors have argued both.

**Behaviour and brain came apart.**
Reading difficulty persisted with large effects while the brain–behaviour correlation vanished. This is the paper's most consequential result, and it is a null.

**A null can be argued for.**
Characterise the distribution of your non-effect against chance rather than asserting absence. The single most reusable technique in the paper.

**Read `N = 17` into every conclusion.**
Small-cell nulls and non-significant interactions carry less information than they appear to, and the uncorrected comparisons threaten the one positive finding rather than the nulls.

---

*Sources are given as PDF page numbers. Statistics are reproduced as reported in the paper. Blockquotes labelled READER'S NOTES are this guide's own evaluation and are not claims the authors made; the block labelled BOUNDARIES THE AUTHORS STATE is theirs.*

[^1]: claude评价式语言太多了
