"""Self-checks for the non-trivial bits: running head/foot filter, figure index,
shape-based reference detection."""
from pdf2md import index_figures, is_primary, split_refs, strip_running

pages = [f"Dev Cogn Neurosci 79 (2026)\nbody line {i}\n101722" for i in range(10)]
pages[3] = pages[3].replace("\n101722", "\nrare line\n101722")
pages[7] = pages[7].replace("\n101722", "\nrare line\n101722")

out, junk = strip_running(pages)

assert "Dev Cogn Neurosci 79 (2026)" in junk, "running header on 10/10 pages must be dropped"
assert "101722" in junk, "running footer on 10/10 pages must be dropped"
assert "rare line" not in junk, "line on 2/10 pages must be kept"
assert "rare line" in out[3]
assert "body line 5" in out[5], "unique body text must survive"
assert all("101722" not in p for p in out)

figs = index_figures([
    "some prose\n**Fig. 1.**\nDevelopment of reading fluency by group.",
    "Fig. 1, childhood grouping still appears relevant here\n**Table 2.** Group demographics.",
    "## FIGURE 3 | Grand average ERPs broken down by age group.",
])
ids = [f["id"] for f in figs]
assert ids == ["Fig. 1", "Table 2", "FIGURE 3"], ids
assert figs[0]["page"] == 1 and figs[1]["page"] == 2
assert "Grand average" in figs[2]["caption"], "Frontiers pipe captions must parse"
assert "reading fluency" in figs[0]["caption"], "split caption must pull the next line"
assert not any("childhood grouping" in f["caption"] for f in figs), \
    "in-text mention ('Fig. 1, ...') must not be taken as the caption"

# --- reference splitting -----------------------------------------------------
# Prose that cites heavily is the thing the shape detector must never eat. Real
# Discussion paragraphs like these cost 23 papers their body text during tuning.
prose = "\n".join(
    f"Previous work (Smith et al., 2014; Jones, 2016) reported effects of {t} on "
    f"control, though Lee (2018) found the opposite in a sample of 40-60 children."
    for t in ["age", "load", "practice", "arousal", "sleep", "training"]
)
body, refs = split_refs([prose, prose])
assert refs == "", "body prose with in-text citations must not be taken for a bibliography"

# A numbered list with no heading at all -- the case that broke on 35% of a real corpus.
entries = "\n".join(
    f"{i}. Author A{i}, Boffin B, Carr C (20{10 + i % 9}) A study of something. "
    f"Journal of Things {i}: {100 + i}-{120 + i}."
    for i in range(1, 15)
)
body, refs = split_refs([prose] * 4 + [entries])
assert "Journal of Things 14" in refs, "numbered bibliography must be split without a heading"
assert "arousal" in "\n".join(body), "body must survive the split"
assert "Author A1" not in "\n".join(body), "references must leave the body"

# Same list, but only four entries: too short to be a bibliography, so leave it alone.
short = "\n".join(entries.splitlines()[:4])
body, refs = split_refs([prose] * 4 + [short])
assert refs == "", "four citation-shaped lines are not a reference list"

# A reference list in the front half is not a reference list.
body, refs = split_refs([entries] + [prose] * 6)
assert refs == "", "a citation run before halfway must be rejected"

# A heading split that stops early still leaves a tail; the second pass takes it.
body, refs = split_refs([prose] * 3 + [entries, "**References**\nAaron, A. (2001). Later list."])
assert "Later list" in refs and "Author A1" in refs, "both blocks must end up in refs"
assert "Author A1" not in "\n".join(body)

# --- which branch the paper goes down --------------------------------------------
clean = ["1. Introduction", "2. Methods", "3. Results"]
assert is_primary(clean, [], "") == (True, True), "a methods heading decides it alone"

# Brain and Cognition: the real headings never reached `headings`, only table cells did.
junk = ["Brain and Cognition", "article info abstract", "Controls vs. ADHD", "F Value"]
study = "Forty children took part. All parents gave written consent before testing."
assert is_primary(junk, [], study) == (True, False), \
    "consent prose must rescue the branch when the headings are junk, and say so"

review = "This review summarises twenty years of microstate research in schizophrenia."
assert is_primary(junk, [], review) == (False, False), \
    "a review with no methods heading and no consent stays synthesis"

# Shredded small caps: "MA D ME TH ODS". The de-spaced probe still runs first.
assert is_primary(["MA D ME TH ODS"], ["MA D ME TH ODS"], "") == (True, True)

print("ok")
