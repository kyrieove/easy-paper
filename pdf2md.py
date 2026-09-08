"""PDF -> body.md / refs.md / figures.json / meta.json.

Stage 1 of the easy-paper pipeline: deterministic local preprocessing.
No model calls, no network, no API key. Text extraction via pdf-inspector.

Writes to output/extracted/<slug>/ by default.
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


def load_extractor():
    try:
        import pdf_inspector
        return pdf_inspector
    except ImportError as error:
        raise SystemExit(
            "pdf-inspector is not installed for this interpreter.\n\n"
            f"  interpreter: {sys.executable}\n"
            f"  fix:         \"{sys.executable}\" -m pip install pdf-inspector\n\n"
            "If you believe it is installed, you are running a different Python than you "
            "think. LibreOffice, Anaconda and the Windows Store stub all shadow the one on "
            "PATH -- use the full path to the interpreter you installed it into."
        ) from error


PIPELINE_VERSION = 2

# pdf-inspector emits section headings as bold runs (**3. Results**), not ATX headings.
REF_HEAD = re.compile(r"(?:^|(?<=\s))(?:#{1,4}\s*|\*\*)(references|bibliography|literature cited)\**\b", re.I)
# A caption is "Fig. 1." (Elsevier) or "FIGURE 1 |" (Frontiers). The delimiter after the
# number is what separates it from an in-text mention ("as shown in Fig. 1, ..."), which is
# followed by a comma or a word. Add delimiters here as new publishers turn up.
CAPTION = re.compile(r"^(fig(ure)?\.?|table)\s*\.?\s*\d+[a-z]?\s*[.:|]", re.I)
FIG_ID = re.compile(r"^(fig(?:ure)?\.?\s*\d+[a-z]?|table\s*\d+)", re.I)
PRIMARY = re.compile(r"^(?:\d+\.)*\s*(methods?|participants|materials|results)\b", re.I)
# Some PDFs render section headings in small caps and emit them shredded:
# "MA D ME TH ODS", "FIG URE 1", "UL TS". Body prose is unaffected. Matching
# against the de-spaced form recovers the heading without touching any text.
PRIMARY_FLAT = re.compile(r"(methods|participants|results)", re.I)
# Bibliography-entry shape, for when the References heading is shredded or absent.
YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
NUMBERED = re.compile(r"^\s*[\[(]?\d{1,3}[\].)]\s+[A-Z]")
# "Smith, J. A." (APA) and "Blasi G," (Vancouver/PLoS) are the two common author forms.
INITIALS = re.compile(r"[A-Z][a-z]+,\s*(?:[A-Z]\.\s*){1,3}|[A-Z][a-z]{2,}\s+[A-Z]{1,3}\s*[,;]")
# A page range closes a citation; "a sample of 40-60 children" is prose. The trailing
# lookahead is what separates them.
PAGE_RANGE = re.compile(r"\b\d{1,4}\s*[–—-]\s*\d{1,4}\b(?!\s+[a-z])")
DOI = re.compile(r"\b10\.\d{4,}/", re.I)
SHRED = re.compile(r"\b\w{1,2}\b(?:\s+\w{1,2}\b)+")
HEADING = re.compile(r"^#{1,4}\s+(.+?)\s*$")
BOLD_HEAD = re.compile(r"^\*\*((?:\d+\.)*\s*[A-Z][^*\n]{0,80}?)\*\*")


def slugify(stem):
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")[:60]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_running(pages, thresh=0.6):
    """Remove repeated edge lines, retaining short documents and interior prose."""
    n = len(pages)
    if n < 3:
        return list(pages), set()
    seen = Counter()
    for md in pages:
        lines = [l.strip() for l in md.splitlines() if l.strip()]
        for line in set(lines[:1] + lines[-1:]):
            seen[line] += 1
    junk = {l for l, c in seen.items() if c > thresh * n and len(l) < 200}
    cleaned = []
    for md in pages:
        lines = md.splitlines()
        occupied = [i for i, line in enumerate(lines) if line.strip()]
        edges = set(occupied[:1] + occupied[-1:])
        cleaned.append("\n".join(line for i, line in enumerate(lines)
                                 if not (i in edges and line.strip() in junk)))
    return cleaned, junk


def cite_count(line):
    """How many bibliography entries this line appears to hold. Usually 0 or 1.

    Needs a year plus one other citation marker: the year alone matches in-text
    citations all through the body, and the pair is what makes it specific.

    It returns a count rather than a flag because two-column extraction sometimes
    merges an entire reference list into one 4,000-character line. Counting those
    as a single entry is what made 19 papers look like they had too few references
    to be a reference list.
    """
    if len(line) < 30:
        return 0
    years = len(YEAR.findall(line))
    if not years:
        return 0
    if not (NUMBERED.match(line) or INITIALS.search(line)
            or DOI.search(line) or PAGE_RANGE.search(line)):
        return 0
    return years


def cite_like(line):
    return cite_count(line) > 0


def refs_by_shape(pages):
    """Find where the reference list starts, by content rather than by heading.

    The heading approach fails whenever the PDF font encoding shreds it -- and
    `REFERENCES` is small-caps often enough that this hit 35% of one real library.
    A reference list has a shape no heading can hide: a long run of citation-shaped
    lines at the end of the paper. Returns (page_index, line_index) or None.
    """
    flat = [(pi, li, line.strip())
            for pi, md in enumerate(pages)
            for li, line in enumerate(md.splitlines())]
    if not flat:
        return None
    marks = [cite_like(l) for _, _, l in flat]

    k = len(flat) - 1
    while k >= 0 and not marks[k]:   # skip running feet and trailing sections
        k -= 1
    if k < 0:
        return None

    end, start, hits, gap = k, k, 0, 0
    while k >= 0:
        if marks[k]:
            start, hits, gap = k, hits + 1, 0
        else:
            gap += 1
            if gap > 3:              # a real list tolerates a stray wrapped line, not a paragraph
                break
        k -= 1

    span = end - start + 1
    # Thresholds measured over 221 papers, not guessed.
    #   hits >= 8   -- one citation-shaped LINE per entry. Counting citations *within* a
    #                  line instead was tried and eats body text: a Discussion paragraph
    #                  citing five papers scores five, and 23 papers lost real prose.
    #   density     -- real reference lists here bottom out at 0.39, because wrapped
    #                  continuation lines carry no year. 0.60 rejected 19 genuine lists.
    #   position    -- a reference list is never in the front half.
    if hits < 8 or hits < 0.35 * span or start < 0.5 * len(flat):
        return None
    return flat[start][0], flat[start][1]


def split_refs(pages):
    """Return (body_pages, refs_text).

    Two passes. The heading split is tried first and is exact when it works, but it
    can be partial: when the list restarts after a page break or a column-order
    glitch, the heading matches once and the tail stays in the body. The shape pass
    then picks up what was left. Two papers in 221 needed exactly this.
    """
    body, refs = split_at_heading(pages)
    tail_body, tail_refs = split_at_shape(body)
    if tail_refs:
        # The shape-detected block sits before the heading-detected one in the paper.
        return tail_body, (tail_refs + "\n" + refs).strip()
    return body, refs


def split_at_heading(pages):
    for i, md in enumerate(pages):
        lines = md.splitlines()
        for j, line in enumerate(lines):
            m = REF_HEAD.search(line)
            if m:
                return partition_references(pages, i, j, m.start())
    return pages, ""


def split_at_shape(pages):
    found = refs_by_shape(pages)
    if found:
        i, j = found
        return partition_references(pages, i, j)
    return pages, ""


def partition_references(pages, start_page, start_line, start_col=0):
    """Keep original page positions and restore recognizable post-reference content.

    Unrecognized trailing content remains recoverable from raw.md; this heuristic
    is not proof that everything assigned to refs.md is a bibliography.
    """
    body = list(pages)
    refs = []
    ended = False
    for pno in range(start_page, len(pages)):
        kept, removed = [], []
        for lno, line in enumerate(pages[pno].splitlines()):
            if pno == start_page and lno < start_line:
                kept.append(line)
                continue
            first = pno == start_page and lno == start_line
            plain = line.replace("*", "").lstrip("# ").strip()
            if not first and (CAPTION.match(plain) or re.match(
                r"^(appendix|appendices|supplement(?:ary|al)?(?:\s|$)|"
                r"supporting information|figure legends?|table legends?|tables?\s*$|figures?\s*$)",
                plain, re.I,
            )):
                ended = True
            if ended:
                kept.append(line)
            elif first:
                kept.append(line[:start_col])
                removed.append(line[start_col:])
            else:
                removed.append(line)
        body[pno] = "\n".join(kept)
        if removed:
            refs.append(f"<!-- Page {pno + 1} -->\n" + "\n".join(removed))
    return body, "\n\n".join(refs)


def page_markdown(pages):
    return "\n\n".join(f"<!-- Page {i} -->\n{md}" for i, md in enumerate(pages, 1))


def index_figures(body_pages):
    """Locate figures and tables by caption -- no image is extracted.

    The guide points at the original ("Fig. 3, PDF p. 8") and the reader opens
    the PDF. Pages are PDF page numbers, which is what a viewer jumps to.
    """
    out, seen = [], set()
    for pno, md in enumerate(body_pages, 1):
        lines = [" ".join(l.replace("*", "").lstrip("# ").split()) for l in md.splitlines()]
        for i, line in enumerate(lines):
            # The delimiter after the number still guards against in-text
            # mentions, so probing the de-spaced line adds no false positives.
            probe = line if CAPTION.match(line) else line.replace(" ", "")
            if not CAPTION.match(probe):
                continue
            m = FIG_ID.match(probe)
            fid = m.group(1).rstrip(".") if m else probe[:12]
            if fid.lower() in seen:
                continue
            seen.add(fid.lower())
            caption = line
            if len(caption) < 20:  # "Fig. 1." alone -- caption text is the next line
                nxt = next((l for l in lines[i + 1:i + 3] if l), "")
                caption = f"{caption} {nxt}".strip()
            out.append({"id": fid, "page": pno, "caption": caption[:400]})
    return out


def run(pdf_path, outroot, force=False):
    pdf_path = Path(pdf_path)
    digest = sha256(pdf_path)
    # The slug alone collides: two papers whose titles agree for 60 characters land in
    # the same folder and the second silently overwrites the first. That is not a corner
    # case -- it cost 10 of 221 papers in one real library, with no error reported.
    # The hash suffix also makes re-extraction of an edited PDF a new folder, not a
    # half-overwritten one.
    dest = Path(outroot) / f"{slugify(pdf_path.stem)[:52]}-{digest[:6]}"
    meta_f = dest / "meta.json"
    extractor_hash = sha256(Path(__file__))
    required = ("raw.md", "body.md", "refs.md", "figures.json")
    if meta_f.exists() and not force:
        cached = json.loads(meta_f.read_text("utf-8"))
        if (cached.get("pdf_sha256") == digest
                and cached.get("extractor_sha256") == extractor_hash
                and cached.get("pipeline_version") == PIPELINE_VERSION
                and all((dest / name).is_file() for name in required)):
            print("cached", dest)
            for warning in cached.get("warnings", []):
                print(f"  !! {warning}")
            return dest
    pi = load_extractor()
    dest.mkdir(parents=True, exist_ok=True)

    cls = pi.classify_pdf(str(pdf_path))
    res = pi.extract_pages_markdown(str(pdf_path))
    raw_pages = [p.markdown for p in res.pages]
    (dest / "raw.md").write_text(page_markdown(raw_pages), "utf-8")
    pages, junk = strip_running(raw_pages)
    body_pages, refs = split_refs(pages)

    body = page_markdown(body_pages)
    (dest / "body.md").write_text(body, "utf-8")
    (dest / "refs.md").write_text(refs, "utf-8")

    figures = index_figures(raw_pages)
    (dest / "figures.json").write_text(json.dumps(figures, ensure_ascii=False, indent=1), "utf-8")

    headings = []
    for md in pages:
        for line in md.splitlines():
            m = HEADING.match(line) or BOLD_HEAD.match(line)
            if m and not CAPTION.match(m.group(1)):
                headings.append(m.group(1).strip())
    shredded = [h for h in headings if SHRED.search(h)]
    primary = any(PRIMARY.match(h) for h in headings)
    if not primary and shredded:
        # Only when the clean path already failed, so normal papers keep the
        # stricter anchored test.
        primary = any(PRIMARY_FLAT.search(h.replace(" ", "")) for h in headings)

    warnings = []
    if cls.pages_needing_ocr:
        warnings.append("pages need OCR; inspect meta.json and the PDF before making claims of missing content")
    if not any(page.strip() for page in body_pages):
        warnings.append("body text is empty; do not build an evidence card until extraction is repaired")
    if refs.strip():
        warnings.append("reference split is heuristic; inspect the boundary and raw.md tail for tables, figures and appendices")
    if not refs.strip():
        warnings.append("references were not split; refs.md is empty and body.md "
                        "still carries them (~30-40% more tokens in stage 2)")
    if not figures:
        warnings.append("no figures or tables indexed")
    if not primary:
        warnings.append("no empirical headings detected; classify the paper from its content, not this flag")
    # A stray one or two is normal noise; a real font problem hits a quarter of them.
    if len(shredded) >= 3 and len(shredded) > 0.15 * len(headings):
        warnings.append(f"{len(shredded)} of {len(headings)} headings look shredded by the "
                        "PDF font encoding; every heading-derived field is unreliable")

    meta = {
        "pipeline_version": PIPELINE_VERSION, "extractor_sha256": extractor_hash,
        "pdf_path": str(pdf_path), "pdf_sha256": digest,
        "n_pages": cls.page_count, "pdf_kind": cls.pdf_type,
        "confidence": round(cls.confidence, 3),
        "pages_needing_ocr": list(cls.pages_needing_ocr),
        "pages_with_columns": list(res.pages_with_columns),
        "pages_with_tables": list(res.pages_with_tables),
        "has_primary_data": primary,
        "warnings": warnings,
        "headings": headings,
        "dropped_running_lines": sorted(junk),
        "figures": len(figures),
    }
    meta_f.write_text(json.dumps(meta, ensure_ascii=False, indent=1), "utf-8")
    print(f"{dest}: {cls.page_count}p kind={cls.pdf_type} figs_indexed={len(figures)} "
          f"primary={meta['has_primary_data']}")
    for w in warnings:
        print(f"  !! {w}")
    return dest


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", default="output/extracted")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    run(a.pdf, a.out, a.force)
