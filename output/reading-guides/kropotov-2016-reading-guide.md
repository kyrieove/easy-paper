# Splitting the Ageing ERP

**Kropotov, J., Ponomarev, V., Tereshchenko, E. P., Müller, A., & Jäncke, L. (2016).**
Effect of aging on ERP components of cognitive control.
*Frontiers in Aging Neuroscience, 8*, 69.

| | |
|---|---|
| **What it asks** | Does cognitive ageing show up in the brain as general slowing, or as one region taking over for another? |
| **What it found** | Both. Everything slows, and the slowing scales with how late the process is. Separately, posterior responses shrink with age while frontal ones grow. |
| **What is new** | The scalp waves are pulled apart into latent components first. Inside a single wave, one component collapses with age and another rises — a split invisible at the scalp. |

**Two conventions used throughout.** `→ FIGURE 4 · p. 9` marks a place to stop and open the PDF — figures are not reproduced here on purpose. Statistics appear as `F[4, 449]` so they stay findable in the prose. Page numbers are **PDF pages**.

Evaluation is confined to Part three and labelled there. Parts one and two report what the paper says.

> ⚠ **EXTRACTION WARNING** — Tables 2, 3, 6 and 7 lose their p-value exponents when the PDF is converted to text: a cell reading `4.85, 10` with a stray `3` below it means `p < 10⁻³`. Read numeric p values off the PDF pages, never from the extracted text.

---

## Part one · Before You Read

*Background you need that the paper assumes you already have.*

### The task, in one paragraph

Every trial is a **pair** of pictures, one second apart. The first picture (`s1`) is either an animal — meaning *get ready, a response may be needed* — or a plant, meaning *nothing will happen this trial*. The second picture (`s2`) decides it: animal after animal means press the button; plant after animal means withhold.

That structure buys two independent contrasts from one task:

- **`s1`: Cue vs NonCue** — isolates **proactive control**, the preparing you do before anything happens.
- **`s2`: NOGO vs GO** — isolates **reactive control**, the stopping you do once the situation turns out to require it.

Keep this pair in mind. Almost every result in the paper is reported twice, once for each contrast.

### The waves

Averaging EEG time-locked to a stimulus gives an **event-related potential** (ERP) — a waveform whose peaks are named by polarity and rough latency. Four matter here:

| Wave | Where | What it is taken to index |
|---|---|---|
| **N2Cue** | frontal-central | orienting to the cue |
| **P3Cue** | posterior | extracting the relevant information from the cue |
| **CNV** | central | anticipation and motor preparation, a slow drift while you wait for `s2` |
| **N2d / P3d NOGO** | frontal | conflict detection and inhibition, measured as NOGO minus GO |

### The move that makes this paper different

A scalp wave is not one process. It is the sum of everything active at that moment, projected onto the scalp and blurred by the skull. Two sources rising and falling in opposite directions can cancel into a wave that looks flat.

So the authors decompose the ERPs into **latent components** by blind source separation — a statistical model that assumes each subject's ERP is a mixture of a small set of underlying signals sharing one mixing matrix across subjects. The number of components is chosen by BIC, and each is checked for split-half reliability.

**This is the whole point of the paper.** If the components behave differently with age *inside* one wave, then the wave was hiding the effect. That is what they report.

### The two hypotheses on trial

- **Processing speed** (Salthouse, 1996) — older cognition is degraded because everything runs slower, so operations cannot complete in time. Predicts latency shifts.
- **Compensation** (Cabeza, 2002) — deteriorating functions are taken over by better-preserved ones, notably prefrontal cortex. Predicts amplitude going down in one place and up in another, with behaviour holding steady.

The paper is framed as adjudicating between them. Notice as you read that they are not mutually exclusive, and that the paper ends up endorsing both.

---

## Part two · Understanding the Paper

*What the paper argues, and how each step is supported.*

### The literature the paper is arguing with

The Introduction (§Introduction, p. 2) opens on a consensus: episodic memory, working memory and executive function decline nearly linearly from early adulthood (Salthouse, 2010), and this is generally tied to the prefrontal cortex. Four theories are laid side by side:

| Theory | Claim |
|---|---|
| **Frontal aging** | decline is primarily deterioration of the frontal lobes |
| **Inhibitory deficit** | more specific — decline is deterioration of *inhibitory* processes |
| **Processing speed** | performance degrades because processing is slower |
| **Posterior-anterior shift** | frontal increases accompany posterior decreases, and this is compensatory |

Then comes the move that creates the gap. On **latencies**, the authors report that almost all studies find age-related delay, confirming the processing speed account. On **amplitudes**, the evidence is a mess: CNV amplitude has been found increased in older participants, reduced, reduced only frontally, and unchanged, across four separate literatures. N2d and P3d NOGO are usually reported smaller in older adults — with one study finding the opposite.

**That contrast is the argument for the method.** If latencies replicate and amplitudes do not, one explanation is that the amplitude of a scalp wave is not a stable quantity to begin with, because it sums sources that may be moving in opposite directions. Watch how the review is arranged to make decomposition look necessary rather than merely available.

### How the design answers it

**Sample** (§Subjects, pp. 2–3). `N = 454` healthy adults across five bands: 18–23 `(114)`, 24–33 `(70)`, 34–50 `(125)`, 51–60 `(70)`, 61–89 `(75)`. Recruited in Switzerland and St Petersburg. Neurological and psychiatric problems excluded, older participants checked for mild cognitive impairment and dementia, all required to show at least average cognitive skills.

This is large for an ERP study, and the size is the paper's main claim to authority. It is also **cross-sectional**: every age effect is a comparison between different people.

**Recording** (§Data Recording, p. 3). 19-channel EEG, `0.3–50 Hz`, `250 Hz` sampling. Blinks removed by zeroing the corresponding ICA components; noisy epochs excluded automatically.

**Decomposition** (§Decomposition, p. 3). Blind source separation on second-order statistics, with the mixing matrix assumed identical across subjects. Component count set by BIC — see `→ FIGURE 2 · p. 6`, where the minimum of the curve *is* the justification for choosing seven components for `s1` and six for `s2`. Split-half reliability was estimated by repeating the whole procedure 1000 times on random halves.

**Localisation** (§Imaging, p. 3). sLORETA on those 19 electrodes. The authors state plainly that they wanted rough localisation, not a precise inverse solution.

### What was observed

#### First, behaviour did not differ

Errors stayed below `2.5%` in every band and mean reaction time moved only between `385` and `407 ms` with no systematic trend (`→ TABLE 1 · p. 4`).

**This finding is load-bearing.** It is what licenses reading every later ERP difference as a difference in *process* rather than in accuracy or effort. Check it first.

#### Second, the scalp waves behave inconsistently — as the literature said

For `s1` (`→ FIGURE 1 · p. 5` panel A, `→ TABLE 2 · p. 6`): N2Cue and CNV amplitudes rise with age while parietal P3Cue falls. Latencies of both N2Cue and P3Cue rise about `4 ms` per decade.

For `s2` (panel C, `→ TABLE 3 · p. 6`): parietal P3Go falls with age, frontal N2d NOGO falls, P3d NOGO goes the other way. Positive-wave latencies rise about `6 ms` per decade while N2d NOGO latency at Fz stays put.

#### Third, decomposition splits the waves apart

Seven components for `s1`, six for `s2`, most with split-half topography similarity above `0.90` (`→ TABLE 5 · p. 8` gives the region for each). Together they explain over 90% of the signal variance.

Now the result that only the decomposition can show. **Three components load onto the single P3Cue wave, and they diverge** (`→ FIGURE 4 · p. 9`, panel C):

- the **temporal** component drops sharply with age
- the **parietal** component does not change
- the **frontal** component *increases*

The same splitting appears for reactive control (`→ FIGURE 5 · p. 10`). P3Go divides into a parietal component that falls and a frontal one that rises. Of the three components loading on N2d/P3d NOGO, all decrease in their N2 portion, while their P3 portions diverge by location: central increases, frontal flat, parietal falls sharply.

#### Fourth, slowing scales with latency

Latency increase is not uniform. Sensory components shift about `4–5 ms` per decade; P3Cue-related components about `20 ms` per decade. The later the process, the more age costs it.

### How the authors explain it

**Processing speed** (§Processing Speed Hypothesis, p. 11) is called unequivocally supported: latency increase is independent of amplitude change, and it scales with a component's own peak latency. They speculate this reflects myelin damage and reduced fibre count — a mechanism imported from structural work, not measured here.

**Compensation** (§Compensation Hypothesis, p. 11) is supported by the anticorrelated pattern: reduced P3Cue in the superior temporal component alongside increased P3 in the medial frontal one; reduced fusiform C2.2 alongside increased cingulate C2.5. With behaviour flat, the reading is that frontal recruitment is holding performance up.

**Posterior-anterior shift** (§Posterior-Anterior Shift, p. 12) puts numbers on it: parietal P3Cue falls about `0.2 µV` per decade, centro-frontal N2 rises about `0.4 µV` per decade, offered as the ERP counterpart of a pattern established in fMRI.

Each component is also given a psychological job — C2.2 comparison with working memory, C2.6 conflict detection, C2.4 overriding a prepotent response, whose decline is read as supporting the inhibitory deficit theory.

---

## Part three · What the Evidence Supports

*Separating what was measured from what it was taken to mean. All evaluation in this guide lives here.*

### Well supported

Latency increase with age, and its scaling with a component's own peak latency. With `N = 454` this gradient is about as solid as cross-sectional ERP data gets. The reliability of the decomposition itself — split-half similarity above `0.90` for most components is a real number, not an assertion. And the central observation that components loading on one scalp wave move in opposite directions with age.

### Supported, but reaching past the design

The compensation account. What is measured is an anticorrelated pattern plus flat behaviour. Compensation additionally requires that the frontal increase be *doing work*, and nothing here tests that.

The posterior-anterior shift as a cross-method convergence. Directions match a well-known fMRI pattern; no joint measurement was made.

### Interpretation, not result

The psychological labels on components — working-memory comparison, conflict detection, response override. These are carried in from earlier papers by association, and the authors say so themselves.

The myelin explanation for slowing. Imported wholesale from structural ageing work.

> **BOUNDARIES THE AUTHORS STATE** — §Limitations, p. 12
>
> Blind source separation is one of several such methods, each with its own assumptions about ERP signals. sLORETA adds no information beyond the component's topography, because the image is a linear transformation of it — it is used only as a rough approximation. And the study is descriptive: little is known about what the components mean functionally, so interpretation is speculation based on loose association with earlier wave studies.

> **READER'S NOTES — MINE, NOT THE AUTHORS'**
>
> **1. Three different numbers for the headline result.** The abstract and conclusion both say `8 ms` per decade for early components and `20` for late. The Results give about `4 ms` per decade for sensory components and `20` for P3Cue-related ones. The Discussion says `5–6 ms` per decade at 100–200 ms and about `16` at 400–500 ms. The `8` that appears in the abstract appears nowhere in the Results.
>
> **2. The conclusion contradicts the results on behaviour.** Abstract and Results state that omissions and reaction times were similar across age groups — the premise the entire interpretation rests on. The Conclusion instead describes age differences in omissions (the older the fewer) and reaction times (the older the slower). Both cannot be true, and the argument only works if the Results version is.
>
> **3. The N2Cue direction is stated three ways.** The Grand Average section says N2Cue amplitude increases with age. The component section says C1.5 and C1.6 decrease with age and calls that *the same pattern as observed for the N2Cue wave*. The Discussion says both components increase with age. Sign conventions for a negative wave may explain part of this, but the text as written cannot all be right.
>
> **4. Cross-sectional data, developmental language.** Every age effect compares different people. Cohort differences in education, test familiarity and screen exposure go unaddressed, and phrases like *latencies increase with age* describe a gradient across people, not a change in anyone.
>
> **5. Healthy-survivor selection favours the compensation story.** Older participants were screened for MCI and dementia and required to show at least average cognitive skills. Flat behaviour across age is partly manufactured by that screening — and flat behaviour is the premise compensation is inferred from.
>
> **6. Compensation is never linked to performance.** No correlation between component amplitude and reaction time or errors is reported, in the older group or anywhere. Anticorrelated posterior and frontal trajectories are equally consistent with dedifferentiation, or with non-specific frontal activity that accomplishes nothing.
>
> **7. Windows were chosen from the observed curves,** and no correction is reported across the dozens of ANOVAs in Tables 2, 3, 6 and 7. With `N = 454` the main gradients would survive; individual component-level claims are less secure than their p values suggest.
>
> **8. The stated age range is inconsistent** — 18–84 in abstract and conclusion, 18–89 in Methods, a top band labelled 61–89 in Table 1 and 61–84 in the figure legends.
>
> Items 1, 2, 3 and 8 are copy-editing failures rather than design flaws, but there are four of them in one paper, and two touch the headline numbers. That is worth knowing before citing a specific figure from it.

---

## Part four · Learning to Write

*Four moves from this paper, for your own Introduction and Methods. Originals are pointed to, not reproduced — open the page and read the sentence in place.*

### 1 · Building the gap out of an inconsistency in prior work

§Introduction, p. 2, the paragraph beginning with age-related delays in the main ERP waves. The authors set up a contrast: on latency the literature agrees, on amplitude it contradicts itself four ways. They do not call anyone wrong. The disagreement itself becomes the reason a new method is needed.

> **PATTERN — my example, not the authors'**
>
> Almost all studies have found [robust effect], confirming [established account]. With respect to [the other measure], however, the findings are less consistent. [Increase] was found in some studies (…). Other studies report [decrease] (…), with [a qualified version] (…). Some studies have reported no group differences (…).

This is the strongest gap-building move available when your field has a replication problem rather than a blank space. The list of contradictions *is* the argument. Note the order: agreement first, so the disagreement lands as a contrast.

### 2 · Making an assumption visible instead of burying it

§Decomposition, p. 3. The mixing matrix is stated to be assumed the same for all subjects, in the sentence that introduces it, not in the limitations.

> **PATTERN — my example, not the authors'**
>
> [Quantity] is modelled as [structure], where [term] is assumed to be [property] and independent of [other term]. The main assumption underlying [the method] is that [assumption stated plainly].

Stating a load-bearing assumption in the Methods, in plain language, costs one sentence and removes a reviewer's best objection — that you did not notice it. Burying it in Limitations reads as a concession; putting it here reads as control.

### 3 · Conceding a method's limits while keeping its result

§Imaging of Latent Components, p. 3. The authors concede that sLORETA validity depends on electrode count and that 19 is few — then explain the trade (non-intrusiveness), state that they only wanted rough localisation, and cite work showing 19-channel estimates can be valid on clean data.

> **PATTERN — my example, not the authors'**
>
> We are aware that [method] depends strongly on [factor], with [more of it] providing better estimates. However, we used [our setting] in order to [the trade you chose]. In addition, we were not interested in [the stronger claim]; rather, we were interested in [the weaker claim we actually need].

The load-bearing phrase is *we were not interested in X; rather, in Y*. It shrinks the claim to what the method can carry. Use it when a reviewer's objection is correct but does not reach your actual conclusion.

### 4 · Marking speculation as speculation, in the verb

Throughout the Discussion — *we can speculate that*, *we may speculate*, *this suggestion fits with*. The hedge sits in the verb, so the sentence can then be fully specific about the mechanism without overclaiming it.

> **PATTERN — my example, not the authors'**
>
> If we consider that [interpretive premise], we may speculate that [mechanism], which fits with [independent evidence].

Cheap and effective, but rationed: this paper uses it often enough that a reader starts discounting the Discussion. One or two per section keeps the signal; a dozen turns into noise.

**One thing not to copy.** The abstract, results and conclusion of this paper disagree with each other on two numbers and one direction (see Part three). Whatever else you take from it, take the habit of reading your own abstract against your own Results table before submitting.

---

## Part five · Key Takeaways

**A scalp wave is a sum, not a process.**
Three components load onto one P3Cue wave: one collapses with age, one is flat, one grows. At the scalp you would see a single moderate decline and conclude something simpler and wrong.

**Slowing scales with lateness.**
Early sensory components lose `4–5 ms` per decade, late cognitive ones about `20`. Age does not slow everything by the same fraction — it costs most where the process is already long.

**Posterior down, frontal up.**
The compensation pattern is real as a pattern. Whether the frontal increase is compensating, or just dedifferentiating, this design cannot say — nothing here links component size to performance.

**Flat behaviour can be manufactured.**
Screening older participants for MCI and requiring at least average cognition helps produce the flat performance that compensation is then inferred from. Read the inclusion criteria before believing a null behavioural difference.

**Check the abstract against the results table.**
This paper reports `8 ms` per decade in its abstract and `4–6` in its results. Take the number from the Results, and take the habit with you.

---

*Sources are given as PDF page numbers. Statistics are reproduced as reported in the paper; p-value exponents were verified against the PDF, not the extracted text. Blockquotes labelled READER'S NOTES are this guide's own evaluation and are not claims the authors made; the block labelled BOUNDARIES THE AUTHORS STATE is theirs.*
