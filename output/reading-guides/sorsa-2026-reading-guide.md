# Reading Guide

**Sorsa, A., Tretow, A., Xu, W., Gerike, G., Lohvansuu, K., Hämäläinen, J. A., & Leppänen, P. H. T. (2026).** Development of brain responses to speech sounds and associations with reading and reading related skills in adults with childhood dyslexia. *International Journal of Psychophysiology, 222*, 113339.

Page numbers below are **PDF pages**. The PDF opens with a repository cover sheet, so the article itself starts on PDF page 2. Open the paper alongside this guide — the figures are not reproduced here on purpose.

---

## Before You Read

This paper asks whether a brain difference that showed up in children with dyslexia is still there when those same children are 26–28 years old.

Three things are worth knowing before the argument will land.

**The sample is unusual and it is the reason the paper exists.** The Jyväskylä Longitudinal Study of Dyslexia (JLD) has followed the same Finnish participants from birth into adulthood. Because of that, this paper is not comparing adults with dyslexia to strangers; it is comparing adults to *their own younger selves* as measured in earlier JLD papers. Groups are therefore defined by **childhood** reading status, not adult status — a point that quietly shapes everything else.

**The measurement is an ERP, recorded in a passive oddball task.** Participants watched a silent film and ignored a stream of speech sounds. One sound repeated 80% of the time (the *standard*); two rarer sounds (the *deviants*) broke the pattern. Averaging the EEG time-locked to each sound type yields an event-related potential — a waveform whose bumps (N1, P2, MMN, P3a, LDN) index successive stages of auditory processing. The key one is the **mismatch negativity (MMN)**: a response the brain produces automatically when a repeated pattern is violated, without the listener attending. A group difference in the MMN is usually read as a difference in how sharply the brain encodes that speech contrast.

**Two deviants, two different phonetic features.** The standard was the Finnish pseudoword /at:a/. One deviant, /ata/, differed in **phonemic length** (a shorter silent gap before the consonant). The other, /ap:a/, differed in **place of articulation** (/p/ instead of /t/). Finnish uses phonemic length to distinguish word meanings, which is why the length contrast matters here more than it would in English. Keep the two deviants apart in your head: the paper's central finding is that the groups differ on *one* of them and not the other, and that this has flipped since childhood.

One more expectation to set. **Most of what this paper reports is an absence.** Two of its three headline claims are null results. That is not a flaw in itself, but it changes how you should read the Discussion, and it is where the guide will slow down.

---

## Understanding the Paper

### The question, and why it is not obvious

Earlier JLD work found that at 9.5 years, children with dyslexia produced *enhanced* ERP responses to the length deviant /ata/ compared to typical readers (Lohvansuu et al., 2014). Note the direction: enhanced, not reduced. Most of the dyslexia literature reports attenuated MMN — a blunter response to speech contrasts. The JLD sample has consistently gone the other way, and the authors have previously explained this as compensation: more neurons recruited, working harder, to encode the same contrast.

So the question in this paper (§1.4, p. 5) splits in two:

- **RQ1** — Do those childhood group differences in ERPs persist into adulthood?
- **RQ2** — In adulthood, do these brain responses still track reading ability, as they did in childhood?

Both questions only make sense against the longitudinal backdrop. A single-timepoint study could ask neither.

### How the design answers it

**Grouping (§2.1 and Table 1, p. 5).** Adults were split by their *childhood* status into RDFR (childhood reading difficulty plus familial risk, **N = 17**), TRFR (typical readers with familial risk, N = 37), and TRC (typical readers, no risk, N = 37). This retrospective grouping is deliberate: it reproduces the grouping used in the 9.5-year paper so the two ages can be compared. It also means the dyslexia cell is small — hold on to that number, it becomes decisive later.

The two research questions ran on slightly different samples: RQ1 on EEG from 91 participants, RQ2 on combined M/EEG from 84, after seven were dropped for MEG data quality.

**Task and stimuli (§2.3, Fig. 2 on p. 7 and Fig. 3 on p. 8).** Open Fig. 2 now — it shows the oddball structure in one picture, and nothing downstream makes sense without it. Then look at Fig. 3 and find the silent gap in the middle of each waveform: that gap (95 ms vs 255 ms) *is* the length contrast. Notice also that the deviant feature sits in the **middle** of the pseudoword, not at its onset. Most comparable adult studies put the contrast at the onset. The authors return to this in the Limitations, and you should file it as a reason that comparisons with other studies are indirect.

**Statistics (§2.4.3, p. 9).** Group differences were tested with threshold-free cluster enhancement plus permutation testing — a data-driven method that finds clusters of effect across time and sensors without the researcher choosing a time window in advance. This is a real strength: it removes one common route to a false positive. Nine comparisons were run (three group pairs × three stimuli), and twelve correlations for RQ2 (three stimuli × four behavioural measures). **No correction was applied across either family.**

### What was observed

Read the results in three layers.

**Layer 1 — behaviour is still different.** In adulthood, the childhood-dyslexia group still scored lower on reading fluency (F(2, 88) = 24.87, p < .001, η² = 0.36), reading accuracy (F(2, 88) = 9.67, p < .001, η² = 0.18), and rapid naming (F(2, 86) = 7.70, p < .001, η² = 0.15). Those are large effects. Whatever else changed, the reading difficulty did not go away.

**Fig. 1 (p. 6)** plots fluency and accuracy from 9.5 years to adulthood for all three groups. Look at whether the three lines stay *parallel* rather than fanning out. That parallelism is the entire basis of the paper's claim about the Matthew effect — the idea that early reading gaps widen over time. Here they did not widen; the time × group interaction was non-significant for both measures (p = .743 and p = .236).

**Layer 2 — the brain difference is still there, but it has moved.** For the place-of-articulation deviant /ap:a/, the childhood-dyslexia group showed **stronger** responses than both other groups: versus TRFR from 152 ms to 800 ms across midline and both hemispheres, and versus TRC in the left hemisphere around 300 ms and 600 ms. The two typical-reading groups did not differ from each other, so familial risk alone did not produce the effect.

**Fig. 5 (p. 9)** is the result figure. The masked colour boxes mark significant clusters and the yellow stars in panels C and D mark which channels. The thing to verify with your own eyes: the effect appears only in the /ap:a/ row. **Fig. 7 (p. 11)** regroups the same data by speech sound — go to panel B, the length deviant /ata/, and see that the three group curves now sit on top of one another. In the 9.5-year paper, that panel was where the group difference lived.

**Layer 3 — the brain–behaviour link is gone.** No significant correlations were found between source-level M/EEG activity and any of the four behavioural measures, across all twelve combinations.

This is where the paper does something worth imitating. A null correlation is easy to dismiss as a failure to measure well. So the authors went further (§3.1.3, p. 10; **Fig. 9 on p. 13**): they plotted the full distribution of point-wise correlations for each of the twelve tests. The distributions were roughly normal and centred near zero (mean r between −0.05 and +0.09), and the proportion of correlations passing the uncorrected threshold ran from 1.4% to 11.8% — around what chance alone would produce. That converts "we found nothing" into "the thing we were looking for is not there in a form this method could see." When you look at Fig. 9, check the red dashed lines at ±0.215 and the inset statistics; those are what carry the argument.

### How the authors explain it

The interpretation is developmental (§4.1, pp. 12–13): the *feature* that separates the groups shifts with age. Length separated them at 9.5 years; place of articulation separates them at 27. The authors attribute this to maturation plus continued exposure to speech, which makes different linguistic features salient at different stages.

For RQ2 they argue (§4.2, p. 13) that adult reading is shaped by so many other things — reading exposure, learned strategies — that a childhood link between speech encoding and reading would be expected to wash out.

And they name a genuine conflict rather than smoothing it over, which is the most interesting paragraph in the paper. In the wider literature, *enhanced* responses to native speech deviancy are taken to reflect **better** speech processing and better reading. In the JLD sample, enhancement is what the dyslexia group shows. The same directional finding therefore carries opposite meanings in the two literatures. The authors have themselves given it two different mechanistic readings at different ages — maturational (larger, less specific neuronal populations) at 6.5 years, compensatory (more neurons working harder) at 9.5 years — and neither is tested here.

---

## What the Evidence Supports

Separating what was measured from what it was taken to mean.

**Well supported.** The behavioural group differences in adulthood (large effects, three converging measures). The presence of a group difference for /ap:a/ in the direction of enhancement. The absence of detectable brain–behaviour correlations *within the sensitivity of this method and sample* — the Fig. 9 histograms make this a positive demonstration rather than a bare null.

**Supported but with the direction assumed.** That the group difference has "moved" from length to place of articulation. This compares a significant result here against a significant result in a different paper, and a null here against a significant result there. No age × feature interaction was tested, even though 79 participants have EEG at both ages. The claim is a reasonable reading of two studies; it is not a tested effect.

**Interpretation, not result.** The maturation-plus-exposure account, and the compensation account of why the dyslexia group's responses are enhanced. Both are stories fitted to a direction of effect. Nothing in this design distinguishes "more neurons recruited to compensate" from "less sharply tuned populations responding more broadly" — the authors have used both, at different ages, for the same observation.

**Boundaries the authors state (§4.3, pp. 13–14).** The stimulus setup changed between the infant/6.5-year measurements and the later ones. Nine comparisons inflate Type I error, and no correction was applied — the authors say choosing one is not straightforward given longitudinal priors and non-independent effects. The mid-word placement of the deviant feature may cause masking and makes comparison with other adult studies indirect. Difference waves could not be computed because the stimuli differ in physical length; the authors argue that since the standard showed no group difference, the deviant effect is likely stimulus-specific.

**Concerns I would add as a reader — these are mine, not the authors'.**

1. **The nulls rest on 17 people.** Both central developmental claims — no /ata/ difference, no brain–behaviour correlation — depend on the RDFR cell. No power analysis or equivalence test is reported, so "the childhood difference is gone" and "we could not detect it with N = 17" are not distinguished. The Fig. 9 histograms partly answer this for RQ2; nothing answers it for RQ1.
2. **The uncorrected comparisons cut one way only.** Type I inflation threatens the single positive finding (/ap:a/), not the nulls. The authors raise it as a general caveat, but it applies asymmetrically to their own results.
3. **The two questions ran on different samples** (N = 91 vs N = 84). Reading the group difference and the correlation null as one developmental story is slightly looser than it appears.
4. **The Matthew-effect contrast is low-powered too.** "No widening" comes from a non-significant interaction across three groups totalling 82, one group holding 17. Non-significance is the expected outcome here whether or not widening occurred.
5. **The joint analysis seems available and was not run.** With 79 participants measured at both ages, a within-subject test of the age × feature shift appears possible from what the Methods describe.

None of these make the paper wrong. They mark where its confidence should sit lower than a fast reading would put it.

---

## Learning to Write

Four moves from this paper that transfer to your own Methods and Results sections. The originals are pointed to rather than reproduced; open the page and read the sentence in place.

**1. Turning a null into a demonstration.** §3.1.3 (p. 10), the sentences after the correlation result. The authors do not stop at "no significant correlations were found." They report the shape of the whole correlation distribution and compare the observed rate of threshold-crossing against chance. The move is: *when your result is an absence, characterise the absence quantitatively instead of asserting it.*

Transferable pattern (my example, not the authors'):

> No significant association was found between X and Y. Across all N tests, the coefficient distributions were centred near zero (mean r = …, SD = …), and the proportion exceeding the uncorrected threshold (…) was …%, consistent with chance expectation.

Use it whenever a null is load-bearing for your argument. Do not use it to dress up a null you did not predict and do not need.

**2. Justifying a design choice by naming what it protects against.** §2.4.3 (p. 9), where TFCE is introduced. The method is not just named; the sentence says what it buys — clusters found across time and sensors *without a predefined threshold*, with permutation testing controlling multiple comparisons.

Transferable pattern (my example):

> We used [method], which [does X] without requiring [the researcher choice that would otherwise bias the result], while [second method] provides control for [specific threat].

The habit worth copying is the subordinate clause. A method sentence that only names the method leaves the reader to guess why; one clause converts it into an argument.

**3. Stating a limitation and then bounding it.** §4.3 (p. 14), the passage on difference waves. The authors explain why difference waves could not be computed, and then immediately argue that the standard stimulus showed no group difference, so the deviant effect is likely stimulus-specific. The limitation is admitted and then fenced.

Transferable pattern (my example):

> [Constraint] meant that [analysis] could not be performed, because [reason]. However, [independent observation from the same data], and therefore [the specific inference that survives].

This is the difference between a limitations section that erodes the paper and one that delimits it. Note what makes it work: the fence is built from evidence already reported, not from reassurance.

**4. Reporting a contrast with the literature without overclaiming.** §4.1 (pp. 12–13), where the authors set their enhanced responses against the field's attenuated ones. They do not argue the field is wrong, and they do not fold their result into it. They mark the conflict and leave it open — the paper describes it as an interesting conflict in interpreting the results.

Transferable pattern (my example):

> In [other samples], [finding] has been interpreted as reflecting [meaning A]. This is partly in contrast to [our result], where [same direction] appears in [opposite population]. [One sentence on what would resolve it.]

Reach for this when your result points the same way as prior work but cannot mean the same thing. Naming the tension is more publishable, and more honest, than a hedge that hopes the reviewer will not notice.

**One thing not to copy.** The Discussion opens by restating the two research questions and then re-narrating the results before interpreting them (§4, p. 11). By that point the reader has just finished the Results. A Discussion that begins with the *interpretation* and pulls in results as evidence is shorter and does more work.

---

## Key Takeaways

- **The finding is a shift, not a disappearance.** A brain difference remains in adults with childhood dyslexia, but it now attaches to place of articulation rather than phonemic length. The strength of that claim depends on comparing across two papers, not on a tested interaction.
- **Direction matters as much as significance.** This sample shows *enhanced* responses in the dyslexia group where most of the field reports attenuation. Whether enhancement means compensation or blunter tuning is unresolved, and the same authors have argued both.
- **Behaviour and brain came apart.** Reading difficulty persisted with large effects while the brain–behaviour correlation vanished — the paper's most consequential result, and a null.
- **A null can be argued for.** Fig. 9 (p. 13) is the technique: characterise the distribution of your non-effect against chance rather than asserting absence. This is the single most reusable thing in the paper.
- **Read N = 17 into every conclusion.** Small-cell nulls and non-significant interactions carry less information than they appear to, and the uncorrected comparisons threaten the one positive finding rather than the nulls.

---

*Sources are given as PDF page numbers in this file. Statistical values are quoted from the paper as reported. Where this guide adds an evaluation that the authors did not make, it is marked as such.*
