# Pooling seven small studies

**Rieger K, Diaz Hernandez L, Baenninger A, Koenig T (2016). 15 Years of Microstate Research in
Schizophrenia — Where Are We? A Meta-Analysis. *Frontiers in Psychiatry* 7:22.
doi:10.3389/fpsyt.2016.00022**

| | |
|---|---|
| **What it asks** | "To obtain an overall estimate of the effect size of these microstate abnormalities … over all studies available to date relating EEG microstates to schizophrenia." |
| **What it found** | Two of four microstate classes differ between patients and controls with medium effect sizes: class C is more frequent and covers more time, class D covers less time and is shorter. Class A shows nothing. |
| **What is new** | Fifteen years of separate small studies get one pooled number each, and that number is placed against the published effect sizes for spectral EEG and for ERP markers of schizophrenia. |

---

## Part 1 — Before You Read

### What a microstate is

Resting EEG does not drift continuously. The scalp voltage map holds one spatial configuration for a
few tens of milliseconds, then switches abruptly to another, and across subjects the same small set
of configurations recurs — which is what makes them countable. The paper calls them "subsecond global
states of stable connectivity patterns directly related to the recruitment of different types of
information processing modes."

Four prototypical maps, labelled A to D, are fitted to everyone's data. Each class is then quantified
three ways, and the paper defines all three in one sentence: **coverage** ("percent total analysis
time covered by each microstate class"), **occurrence** ("number of microstates observed per second
for each microstate class"), and **mean duration** ("average duration of microstates of a given
class"). Three features times four classes is the `12` cells this meta-analysis fills.

### Why the disorder licenses a task-free measure

The Introduction argues in two steps: breadth of deficit implies a task-free measure, and the
disconnection hypothesis implies a whole-brain rather than a local one. Microstates satisfy both,
which is why they are the measure. The sentences that do this are quoted in Part 4, *Building the
gap*.

---

## Part 2 — Understanding the Paper

### What the authors expected, and what the design can deliver

Individual studies had reported microstate abnormalities since Koenig et al. in 1999, so the
expectation is not that an effect exists but that the scattered effects converge on a size: the paper
asks *how large*, not *whether*. A meta-analysis has no participants of its own, and its design
decisions are which studies to admit, what to extract, and how to weight them. Read those the way
you would read a montage and a filter setting.

### How the studies were found, selected and pooled

**This is the sub-section to read twice, because it is the part of the paper you can reuse.**

**Finding the literature.** "To identify the relevant literature, we conducted a PubMed search with
the terms 'schizophrenia' and 'microstate.'" One database, two terms. No date range, no date of
search, no language restriction, no second database, and no screening procedure or second rater are
stated. One further study entered outside the search: "we were aware of, and included one more study
that met the above criteria and had been accepted for publication, but was not yet registered in
PubMed (28)."

**The four inclusion criteria**, all required: `(1)` the paper reported original findings; `(2)` the
electrode array covered at least the area of the standard 10-20 system; `(3)` four microstate classes
were fitted to the data, "being the most frequently used number of microstate classes across
studies"; `(4)` subjects were recorded in a task-free resting-state condition. "Care was taken to
exclude the duplicate reporting of data in different papers." Seven studies survive, from 1999 to the
in-press Tomescu et al.

Criterion `(3)` is the one that shapes everything downstream: the four-class solution is an entry
condition, not a finding. Return to that in Part 3.

**One documented deviation.** Criterion `(2)` was bent once, in the Methods, at the point the
criterion is set: "the multicenter-study by Lehmann et al. (21) included a small (six patients and
six controls) subset of subjects where the midline electrodes were interpolated. Since the data were
only presented across all study centers and since there were many more subjects from other centers,
we decided to include this study despite this fact."

**Who is in the pooled sample.** → **TABLE 1 · p. 3.** Seven rows. Read down the channel-count
column and the mean-age column: as extracted, channel counts run `16` to `204` and mean ages run
`16.5` to `34.5`, and the medication column reads No for four studies and Yes for three. One included
sample is an at-risk group (22q11.2 deletion syndrome) rather than a diagnosed one. The pooled number
of patients and the pooled number of controls are stated nowhere in the paper.

> ⚠ **READ THIS TABLE OFF THE PDF.** Table 1 came out of the extraction as two disconnected fragments
> with scrambled columns — the header reads `R eference | | n | ender C hannels | R ecruitment area`
> and the last study's row is out of order. The spread quoted above is reliable; any individual cell
> is not.

**What was extracted.** "From all of these studies, mean and standard deviation (SD) of patient and
control data were available for most of the typical microstate parameters and thus collected for the
meta-analysis. Where data before and after medication were available, the data obtained before
medication were used." The input to the pooling is therefore group-level means and SDs, one per
study, per group, per feature, per class — never individual data.

Class identity across sixteen years rests on topography: all seven studies used classes "labeled
from A to D according to the similarity of the obtained microstate classes with the microstate
prototype maps reported in the first study of this kind (23)." No similarity measure or threshold is
given.

**The statistical model.** Hedges' `g` and its SD as the within-study effect size, computed "using
the package 'compute.es' (34) of the R-software (35)"; no version numbers. Within-study effect sizes
"were then weighted by their inverse variance to obtain a weighted mean effect size across studies,"
with the standard error extracted. Significance by `Z`-test, with upper and lower confidence
intervals computed. That is `12` tests, one per feature per class.

**The correction, and the argument for it.** "In order to correct for potential false positives due
to multiple testing, a Bonferroni correction was applied with a factor of 8." The factor is argued
from the dependency structure rather than the count: all studies reported four classes and two
independent features per class, and "the sometimes additionally reported coverage can be computed
from occurrence and mean duration and was thus not considered as an additional independent test."

**The planned sensitivity analysis.** "Significant overall mean effects were tested for potential
confounding effects of medication by excluding studies that had investigated patients under
medication."

**What could not be done, stated in Methods:** "Since the single-subject data were not available, it
was not possible to extend the analysis to a multifactorial level that would assess the overall
significance of group by microstate class interactions."

### What was observed

→ **FIGURE 2 · p. 4** carries five forest plots. Look at the spread of the seven study estimates
inside each panel and compare panel A against panel B; the prose reports only the pooled value. The
caption states that panel A and panel E did not survive Bonferroni correction.

Class C occurs more often — `g = 0.760`, `uncorrected p = 0.0003`, `corrected p = 0.0024` — and
covers more time — `g = 0.569`, `uncorrected p = 0.011`, `corrected p = 0.088` — "whereas no
significant effect was found for mean duration (`g = 0.176` and `uncorrected p = 0.39`)." Class D
runs the other way: less coverage, `g = -0.759`, `corrected p = 0.0064`, and shorter duration,
`g = -0.712`, `corrected p = 0.0056`, with "no consistent change in occurrence" at `g = -0.351`,
`p = 0.090`.

Class C is more frequent but not longer; class D is shorter but not rarer. Class B shows a shortening
at `g = -0.435`, `p = 0.037` that does not survive correction, and "the meta-analyses did not identify
any consistent effects in microstate class A."

Removing the medicated samples: "these effects were preserved and mostly showed increased effect
sizes (contribution class C: `g = 0.393`, occurrence class C: `g = 0.800`, contribution class D:
`g = -0.821`, and duration class D: `g = -0.970`)." Three of the four grow; coverage of class C falls
from `0.569` to `0.393`, which is what "mostly" carries. No p values are given for these four.

### How the authors explain it

The explanation is imported rather than derived. Class D "ha[s] been attributed to flexible aspects
of attention, such as switching and reorientation of attention," on the strength of its association
with the frontoparietal attention network in fMRI (19). Class D is also reduced in hypnosis, sleep
and acute hallucination — states the authors call reality remote — and from that: "This leads to the
assumption that microstates of class D might be related to the updating of mental content based on
internal and external information that is close to reality."

Class C maps to the salience network in the same fMRI study, and its increase "dovetails with the
view that schizophrenia is a state of aberrant assignment of salience 'at a mind level' (46)." The
two halves then combine: "We may thus interpret the overall picture of our findings as an imbalance
between attentional and saliency-related processes in schizophrenia patients."

---

## Part 3 — What the Evidence Supports

### Well supported

**Class D covers less time and lasts shorter in schizophrenia.** Both estimates clear Bonferroni
correction (`corrected p = 0.0064` and `0.0056`), both grow when medicated samples are dropped, and
the per-study estimates are visible in `→ FIGURE 2 · p. 4`, panels C and D.

**Class C occurs more frequently.** `corrected p = 0.0024`, rising to `g = 0.800` without medicated
samples.

**The medication confound is addressed rather than asserted.** The sensitivity analysis was specified
in Methods and its four effect sizes are reported — though without p values, confidence intervals, or
a statement of how many studies remained in it.

### Supported, but reaching past the design

**"Coverage of class C is increased."** `corrected p = 0.088`. It appears in the Abstract's "medium
size effects for two classes of microstates" alongside effects that did survive.

**The C-versus-D imbalance.** Assembled from two separate one-cell tests, because the group by
microstate class interaction could not be run — as the Methods state.

**Effect sizes lie between spectral EEG and ERP markers.** The comparison runs across separate
meta-analyses with different samples and paradigms — spectral delta `0.46` and theta `0.42`; P50 from
`-0.93` to `-1.56`; mismatch negativity `0.99`; P300 `-0.83`; N400 latency `0.82` — and no statistical
comparison is performed. The authors hedge accordingly: the result "may indicate that … microstate
analysis succeeds better in distinguishing between brain processes that are, or are not relevant for
schizophrenia, but not to the same degree as some of the averaged evoked potentials do."

### Interpretation, not result

**Class D indexes updating of mental content close to reality.** Rests on the fMRI attention-network
association (19) plus reduced D in hypnosis, sleep and hallucination — all outside the pooled set.
Marked twice in the grammar: "leads to the assumption," "might be related."

**Resting-state abnormalities are causally upstream of task-state abnormalities.** Offered as "may
thus be," with "up-stream" in scare quotes, from cross-sectional group differences.

**Microstate analysis has potential clinical value.** Rests on the single at-risk 22q11.2 study
inside the pooled set, which "showed the same microstate abnormalities in these individuals as in
schizophrenia patients."

### Four things the paper does not report

No heterogeneity statistic appears anywhere — not `Q`, not `I²`, not `τ²` — in the Methods, the
Results, or the caption of Figure 2, while Table 1 shows electrode counts from `16` to `204` and mean
ages from `16.5` to `34.5`. Inverse-variance weighting with no between-study variance component is a
fixed-effect model, which the paper never names. No publication-bias assessment is reported: no
funnel plot, no Egger test, no statement that bias was considered. And the screening numbers exist
only inside `→ FIGURE 1 · p. 2` and Table S1 of the Supplementary Material, so a reader of the prose
never learns how many records the search returned.

One arithmetic point: the Methods count `12` tests and correct with a factor of `8`, excluding
coverage on the grounds that it is derivable from occurrence and duration — and the Results then
report a corrected p for coverage itself, in both class C and class D.

Most of these sentences sit in the paper's closing paragraph, at the foot of p. 6, under no heading
of its own — the paper has no Conclusion section, so the limitations are easy to walk past.

> **BOUNDARIES THE AUTHORS STATE**
> "Given the small number of studies that has been done so far, an enlargement of the sample size in
> future studies is essential." · "Furthermore, the heterogeneity of the included subjects in terms
> of medication and diagnosis gives reason to a cautious interpretation of the presented results." ·
> "Note that the justification of the choice of these criteria was purely pragmatic … We do not imply
> that these criteria are the optimal choice to investigate microstates in general." · On class B:
> "the fact that the findings in microstate where not significant after correcting for multiple
> testing casts further doubt on the relevance of this effect." · And the ceiling they set on their
> own conclusion: the results justify "further investigation of microstate classes C and D as state
> markers of acute schizophrenia and the attempt to modulate them … as a possible add-on treatment."

---

## Part 4 — Learning to Write

### Building the gap — §Introduction, p. 1

> **THE AUTHORS' SENTENCE** — §Introduction, p. 1
> "Schizophrenia patients show abnormalities in a broad range of task demands. Therefore, an
> explanation common to all these abnormalities has to be sought independently of any particular
> task, ideally in the brain dynamics before a task takes place or during resting state."

The move is to derive the method from the shape of the problem. Breadth of the deficit is stated as
a fact about the disorder, and the task-free measure follows as a consequence rather than as a
preference. Use it when the generality of a phenomenon is itself the reason your measure has to be
general; it does not work when the method was chosen for convenience.

### Stating a design choice — §Materials and Methods, p. 2

> **THE AUTHORS' SENTENCE** — §Materials and Methods, p. 2
> "Note that the justification of the choice of these criteria was purely pragmatic; it identified
> the broadest common ground to compare studies on microstates in schizophrenia at the time of this
> paper being written. We do not imply that these criteria are the optimal choice to investigate
> microstates in general."

State the basis of a choice, then fence what the choice does not claim — in the Methods, where the
choice is made, not in a limitations paragraph at the end. The fence costs nothing, because admitting
the criteria are pragmatic weakens no result that follows, and the reader carries the qualification
through the Results instead of meeting it afterwards. The second sentence, naming what is *not*
claimed, is the half most drafts leave out.

### Reporting a result — §Results, p. 3

> **THE AUTHORS' SENTENCE** — §Results, p. 3
> "Namely, microstates of class C were found to occur more frequently in schizophrenia (`g = 0.760`,
> uncorrected `p = 0.0003`, and corrected `p = 0.0024`) and to cover more percent of time
> (`g = 0.569`, uncorrected `p = 0.011`, and corrected `p = 0.088`), whereas no significant effect was
> found for mean duration (`g = 0.176` and uncorrected `p = 0.39`)."

**The format to copy: a pooled effect size, then both p values in the same parenthesis, then the null
in the same sentence under "whereas."** Direction is carried by a verb — "occur more frequently,"
"cover more percent of time" — not by the sign alone.

Carrying uncorrected and corrected p side by side lets the reader see what the correction cost
without the paper commenting on it. Putting the null in the same sentence means the shape of the
finding — more frequent but not longer — arrives whole, instead of in a paragraph the reader can
skip. What this convention omits: confidence intervals never appear in the prose, only in the forest
plots.

### From result to interpretation — §Discussion, p. 4

> **THE AUTHORS' SENTENCE** — §Discussion, p. 4
> "These effects could not reasonably be explained as side effects of medication upon the EEG,
> because they persisted when studies with medicated patients were excluded."

The confound the reader is already thinking about is raised by the authors first, and closed in the
same sentence by an analysis that was planned in the Methods. The crossing costs them nothing here
precisely because the answer was budgeted for in advance — the move is a Methods decision that pays
out in the Discussion, and it is unavailable if the sensitivity analysis was never run.

### A move to avoid — §Discussion, p. 4

> **THE AUTHORS' SENTENCE** — §Discussion, p. 4
> "The fact that the meta-analysis across those studies yielded evidence for consistent effects
> suggests that using four microstate classes has empirical justification and that these should be
> considered in future studies."

Criterion `(3)` admitted only studies that had already fitted four classes, so no included study
could have come out otherwise; the comparison that would support the claim was removed by the
inclusion rule. The sentence is well built, which is what makes it worth studying — it reads as an
ordinary inference.

**Before you write a sentence of this shape, ask what result would have counted against it, then
check whether your sampling or inclusion rule made that result impossible to observe.**

---

## Part 5 — Key Takeaways

**Two of four microstate classes carry the entire finding.** Class C is more frequent and covers more
time; class D covers less time and is shorter. Class A shows nothing consistent and class B does not
survive correction. Effects are medium, `|g|` between `0.57` and `0.76`.

**The inclusion criteria are the design, and one of them decides a later conclusion.** Requiring four
fitted classes made the pooling possible and simultaneously removed every case that could have
contradicted the four-class claim in the Discussion. In a meta-analysis, read the criteria before the
forest plots.

**The paper's central reading was assembled from separate tests, and it says so.** The C-versus-D
imbalance rests on two one-cell results, because individual-participant data were unavailable and the
interaction test could not be run. The Methods state this; the Discussion does not repeat it.

**Heterogeneity is visible in Table 1 and quantified nowhere.** Electrode counts from `16` to `204`,
mean ages from `16.5` to `34.5`, medicated and unmedicated samples, one at-risk group — pooled under
inverse-variance weighting with no between-study variance term and no `I²`.

**An effect size means something once it has neighbours.** Placing `g ≈ 0.76` between spectral EEG at
`0.42`–`0.46` and ERP markers at `0.82`–`1.56` tells the reader what the measure buys, which the word
"medium" does not.

---

## About this guide

Statistics sit in code spans so they stay findable in prose. Figures and tables are pointed at and
never reproduced — `→ FIGURE 2 · p. 4` means the fourth PDF page, and all page numbers are PDF pages.
Evaluation is confined to Part 3, where the job is to map each claim onto its evidence rather than to
judge it; Parts 1 and 2 report what the paper says.

Two smaller extraction faults affected nothing quoted above: five section headings are shredded by
the PDF font encoding (`MA D ME TH ODS`, `UL TS`), and references 1–14 remain interleaved in the body
text on p. 6. The prose itself is intact.
