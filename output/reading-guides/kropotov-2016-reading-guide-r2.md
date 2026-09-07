# Splitting the Ageing ERP

**Kropotov, J., Ponomarev, V., Tereshchenko, E. P., Müller, A., & Jäncke, L. (2016).**
Effect of aging on ERP components of cognitive control.
*Frontiers in Aging Neuroscience, 8*, 69.

| | |
|---|---|
| **What it asks** | Does cognitive ageing show up in the brain as general slowing, or as one region taking over for another? |
| **What it found** | Both. Latency grows with age and the growth scales with how late the process already is. Separately, posterior responses shrink with age while frontal ones grow. |
| **What is new** | The scalp waves are decomposed into latent components first. Inside a single wave, one component collapses with age and another rises — a split that is invisible at the scalp, where the three sum into one moderate decline. |

**Conventions.** `→ FIGURE 4 · p. 9` marks a place to stop and open the PDF; figures are not reproduced here. Statistics appear as `F[4, 449]`. Page numbers are **PDF pages**.

Parts one and two report what the paper says. Part three maps its claims onto the evidence for them and stops there; the conclusions are yours to draw.

> ⚠ **EXTRACTION WARNINGS — TWO KINDS OF NUMBER ARE CORRUPTED**
>
> **p-value exponents.** In Tables 2, 3, 6 and 7 the superscripts detach onto their own rows: a cell reading `4.85, 10` with a stray `3` beneath it means `p < 10⁻³`. Read numeric p values off the PDF.
>
> **Micro signs.** The artifact-rejection thresholds read `100 mV`, `50 mV`, `35 mV` in the extracted text. The units are microvolts. Check any unit against the PDF before you copy it.

---

## Part one · Before You Read

### The task

Every trial is a **pair** of pictures. The first (`s1`) is an animal — *get ready, a response may be needed* — or a plant, meaning nothing will happen. The second (`s2`) decides it: animal after animal means press; plant after animal means withhold.

That buys two independent contrasts from one task. **Cue minus NonCue** isolates *proactive* control — preparing. **NOGO minus GO** isolates *reactive* control — stopping. The paper analyses the two separately throughout, and the section headings track them as `s1` and `s2`.

### The waves

Four names carry the whole paper. **N2Cue**, frontal-central, orienting to the cue. **P3Cue**, posterior, extracting what the cue means. **CNV**, the slow negative drift while waiting for `s2`. **N2d/P3d NOGO**, frontal, appearing when a prepared response has to be withheld.

### The move the paper is built on

A scalp wave is a sum. Several generators fire at once and the electrode records their mixture. **Blind source separation** works backwards from the mixture to a set of latent components, each with its own topography and time course. The paper's claim is that components loading on one wave can move in *opposite* directions with age, which the wave itself hides.

### The two hypotheses on trial

**Processing speed** (Salthouse, 1996): cognition degrades because processing is slower and operations cannot complete in time. Predicts latency effects.

**Compensation** (Cabeza, 2002): older brains recruit frontal regions to hold performance steady, producing the posterior-anterior shift seen in fMRI. Predicts an amplitude trade — posterior down, frontal up — alongside flat behaviour.

---

## Part two · Understanding the Paper

### The literature the paper is arguing with

The Introduction sets up an asymmetry. On **latency**, the literature agrees: almost all studies find age-related delays in the main ERP waves of cognitive control. On **amplitude**, it contradicts itself. CNV amplitude was found increased in older participants in some studies, reduced in others, reduced only frontally in others again, and unchanged in others. N2d and P3d NOGO are reported smaller in the elderly, with one study reporting the opposite.

The gap is built out of that inconsistency: if the same wave gives four answers, the wave may not be the right unit of analysis.

### The question

Which of the two accounts do ERP components of cognitive control support? The framing is a contest, but the two are not mutually exclusive, and the paper ends up supporting both.

### How the design answers it

Three choices do the work. A large sample across a wide age range, so that a gradient can be seen rather than a young-versus-old difference. One task yielding both control contrasts, so proactive and reactive control are measured in the same people. And decomposition before analysis, so that an amplitude effect can be located to a generator instead of a scalp site.

### How the data were collected and processed

**Participants.** `N = 454` healthy adults, recruited in Chur, Switzerland, from a database project, and in St Petersburg from university students and institute staff. Five age bands: 18–23 (`N = 114`), 24–33 (`N = 70`), 34–50 (`N = 125`), 51–60 (`N = 70`), 61–89 (`N = 75`).

Inclusion required freedom from obvious neurological and psychiatric problems, no vision or hearing problems, **at least average cognitive skills**, and a symptom-checklist score below clinical significance. Systemic medical disease excluded. Older participants were additionally screened for mild cognitive impairment and dementia with a standard cognitive test. Handedness by self-report: 17 left-handed, 10 ambidextrous, the rest right-handed. Ethics approval EK 20/07, canton Graubünden.

**Stimuli.** Images of animals, plants and humans, drawn from children's textbooks and matched so that overall luminance and image size were approximately equal across animals and plants. Twenty images per category, recombined randomly to avoid habituation. Novel sounds occasionally accompanied the human images on ignore trials, to hold alertness.

**Procedure.** Stimulus duration `100 ms`, inter-stimulus interval `1000 ms`, inter-trial interval `3000 ms`. Four trial types: a–a (GO, press), a–p (NOGO, withhold), p–p, and p–h with a novel sound (ignore). Speed and accuracy equally emphasised, with practice beforehand and a few minutes' rest every 200 trials. Seated upright at a 17-inch CRT at `1.5 m`, stimuli subtending `3.8°`. Presentation by *Psytask*, written by one of the authors.

**Recording.** 19 scalp sites, 10–20 system, on a Mitsar-201 with Electro-Cap tin recessed electrodes and ECI gel. Online bandpass `0.3–50 Hz`, digitised at `250 Hz` per channel, referenced to linked ears. Button presses made with the right hand and recorded on a separate channel. Quantification in WinEEG.

**Processing.** Re-referenced computationally to common average before decomposition. Blinks corrected by running ICA on raw fragments and zeroing the activation curves of the blink components. Epochs rejected automatically at `100 µV` for unfiltered EEG, `50 µV` for slow waves in `0–1 Hz`, and `35 µV` for fast waves in `20–35 Hz`.

**Analysis.** Each ERP is modelled as a linear mixture of `K` latent signals plus additive noise, with a mixing matrix **assumed to be the same for every subject**. Separation by blind source separation on second-order statistics, adapted for transient responses. The number of components is set by the minimum of BIC, computed separately for `s1` and `s2` → `FIGURE 2 · p. 6` — the minimum of that curve is the entire argument for seven components and six.

Component locations come from sLORETA over 19 electrodes, 2394 voxels at `7 mm`. Measurement windows were chosen per component from local peaks of the difference curves. Statistics are one-way ANOVA over age bands for behaviour, and two-way repeated-measures ANOVA (Age × Location, `F[4, 449]` for age) for wave and component amplitudes.

**Three things the paper does not specify.** No epoch window or baseline-correction interval is given anywhere, and no count of trials surviving rejection, overall or per age band. Trial totals contradict themselves inside one paragraph: four blocks of one hundred trials each, then each block consisting of 400 trials with 100 per category. And no multiple-comparison correction is reported, either for the dozens of ANOVAs or for the data-driven window selection.

### What was observed

#### Behaviour did not differ

Omission and commission errors stayed below `2.5%` in every band. Mean reaction time ran between `385` and `407 ms` with no systematic age trend.
→ `TABLE 1 · p. 4` — check that errors stay under 2.5% and that RT does not trend. This table licenses every later reading of an ERP difference as a difference in process rather than in effort.

#### The scalp waves behave inconsistently — as the literature said

For `s1`: central N2Cue and CNV amplitudes **increase** with age while parietal P3Cue **decreases**; both N2Cue and P3Cue peak latencies grow about `4 ms` per decade. For `s2`: parietal P3Go decreases, frontal N2d NOGO decreases, P3d NOGO moves the other way. Positive-wave latencies grow about `6 ms` per decade while N2d NOGO latency at Fz stays flat.
→ `FIGURE 1 · p. 5` — panel A is `s1` (Cue−NonCue), panel C is `s2` (NOGO−GO). Follow one colour across panels; the five colours are the five age bands.

#### Decomposition splits the waves apart

Seven components for `s1`, six for `s2`, with split-half topography similarity mostly above `0.90`. Locations span cuneus and fusiform, superior temporal and paracentral, medial and superior frontal gyri.
→ `TABLE 5 · p. 8` — every anatomical claim in the Discussion is read off this table.

Three components load on P3Cue and they diverge by location: the temporal one drops sharply with age, the parietal one does not change, the frontal one rises. On the `s2` side, P3Go splits into a parietal component that falls and a frontal one that rises; of the three components loading on N2d/P3d NOGO, all decrease in their N2 part while their P3 parts diverge — central up, frontal flat, parietal sharply down.
→ `FIGURE 4 · p. 9`, panel C — the confidence intervals per age band are where the divergence by location becomes visible. Then `FIGURE 5 · p. 10`, panels F and G, for the NOGO−GO difference.

#### Slowing scales with lateness

Latency increase is not uniform. Sensory components slow by roughly `4–5 ms` per decade, P3Cue-related components by roughly `20`.

### How the authors explain it

Latency is read as **processing speed**: the increase is independent of amplitude change and scales with a component's own peak latency, and is attributed, speculatively, to myelin damage and fibre loss.

The opposed amplitude trajectories are read as **compensation**: posterior falls, frontal rises, behaviour holds. Parietal P3Cue falls about `0.2 µV` per decade while centro-frontal N2 rises about `0.4`, which is presented as the ERP counterpart of the fMRI posterior-anterior shift.

Individual components are assigned psychological operations — comparison with working memory, conflict detection, overriding a prepotent response — and the decline of the override component is read as support for the inhibitory deficit theory of ageing.

---

## Part three · What the Evidence Supports

*Each claim, what it rests on, and where the paper says it stops.*

| Claim | Rests on | Where it stops |
|---|---|---|
| Latency rises with age and scales with a component's own latency | `N = 454`, the gradient across five bands, `F[4, 449]` | Cross-sectional: every effect compares different people, not the same person over time |
| Myelin damage explains the slowing | Nothing measured here | Imported from structural ageing work; no structural measure was taken |
| Components loading on one wave move in opposite directions | Split-half topography similarity above `0.90`; Tables 6 and 7 | Depends on one mixing matrix fitting all 454 subjects across 66 years, an assumption stated but not tested |
| The pattern is compensation | Anticorrelated posterior/frontal trajectories plus flat behaviour | Compensation requires the frontal rise to be doing work. No correlation between component amplitude and reaction time or errors is reported, and no mediation |
| Convergence with the fMRI posterior-anterior shift | Matching directions | No joint measurement; direction agreement only |
| The psychological labels on components | Association with earlier wave studies | The authors state the study is descriptive and the labels rest on loose association — see below |

Four numbers in the paper disagree with other numbers in the paper. The headline slowing rate is given three ways: `8` and `20 ms` per decade in the abstract and conclusion, about `4` and `20` in the Results, `5–6` and about `16` in the Discussion. The stated age range is 18–84 in the abstract and conclusion, 18–89 in Methods, 61–89 in Table 1 and 61–84 in the figure legends. The Conclusion says omissions and reaction times *differed* by age; the Results and abstract say they did not, and the interpretation only works on the Results version. Trial totals contradict themselves as described above.

> **BOUNDARIES THE AUTHORS STATE** — §Limitations, p. 12
>
> Blind source separation is one of several such methods, each resting on its own assumptions about ERP signals. sLORETA adds no information beyond the component's topography, since the image is a linear transformation of it; it is used only as a rough approximation. And the study is descriptive — little is known about the functional meaning of the components, so interpretation is speculation based on loose association with earlier wave studies.

---

## Part four · Learning to Write

*Moves from this paper's Methods, Results and Discussion. Open the page and read each sentence in place.*

### 1 · Reporting a null as a licence, not as an absence

`§Results/Behavioral Data, p. 4`.

> **THE AUTHORS' SENTENCE** — §Results, p. 4
>
> "Thus, although the behavioral data are roughly similar the ERP differences reported below cannot be attributed to different behavioral performances."

A flat behavioural result could be written as a disappointment. Here it is what permits everything that follows, and the sentence spends no words apologising — it names what the null buys.

**Only when the null actually eliminates a rival explanation.** If the measure was simply insensitive, that needs a different and more honest sentence.

### 2 · Stating a data-driven analysis choice without defending it

`§Materials and Methods/Statistical Analysis, p. 4`.

> **THE AUTHORS' SENTENCE** — §Methods, p. 4
>
> "Intervals were chosen for each latent component separately on the basis of local peaks of the difference curves."

The choice was made after seeing the data, and the Methods says so in one flat sentence. Burying it would be worse.

The sentence is incomplete as written: it does not say how the resulting false-positive inflation was handled. Learn it together with the correction sentence this paper omits.

### 3 · Using a concession to force in a second mechanism

`§Discussion/Processing Speed Hypothesis, p. 11`.

> **THE AUTHORS' SENTENCE** — §Discussion, p. 11
>
> "However, although such structural damage may explain the reduction in amplitude and increase in latency for the parietally distributed P3 GO, it cannot directly explain the enhancement of the frontally distributed P3 NOGO wave."

Grant that explanation A covers part of the data. Name precisely the part it does not cover. Let that gap require explanation B. The reader arrives at the compensation account feeling it was necessary rather than added, and this one sentence is the pivot of the Discussion.

**The move is only as strong as the specificity of the finding A fails to cover.** A vague gap forces nothing.

### 4 · The adverb to avoid

`§Discussion/Processing Speed Hypothesis, opening, p. 11`.

> **THE AUTHORS' SENTENCE — AN EXAMPLE TO AVOID** — §Discussion, p. 11
>
> "Our data unequivocally support the processing speed hypothesis of aging (Salthouse, 1996)."

`Unequivocally` sits three pages from the authors' own statement that the study is descriptive and its interpretation speculative. A cross-sectional design cannot rule out cohort effects, so nothing here is unequivocal.

**Reserve absolute adverbs for claims the design could in principle have falsified.** Calibrated alternatives: *are consistent with*, *support*, *provide converging evidence for*.

---

## Part five · Key Takeaways

**A scalp wave is a sum, not a process.**
Three components load onto one P3Cue wave: one collapses with age, one is flat, one grows. At the scalp you see a single moderate decline and conclude something simpler.

**Slowing scales with lateness.**
Early sensory components lose `4–5 ms` per decade, late cognitive ones about `20`. Age does not slow everything by the same fraction.

**Flat behaviour can be built in by the inclusion criteria.**
Screening older participants for MCI and requiring at least average cognitive skills helps produce the flat performance that compensation is then inferred from. Read the inclusion criteria before accepting a null behavioural difference.

**Check the abstract against the results table.**
This paper gives its headline slowing rate three different ways and its age range four. Both are recoverable from the tables.

---

*Generated from `out/effect-of-aging-on-erp-components-of-cognitive-control/evidence-card.json` (schema v3). The 2026-09-07 guide, `kropotov-2016-reading-guide.md`, is kept unchanged.*
