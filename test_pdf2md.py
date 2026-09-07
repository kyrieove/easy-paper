"""Self-checks for the two non-trivial bits: running head/foot filter, figure index."""
from pdf2md import index_figures, strip_running

pages = [f"Dev Cogn Neurosci 79 (2026)\nbody line {i}\n101722" for i in range(10)]
pages[3] += "\nrare line"
pages[7] += "\nrare line"

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
print("ok")
