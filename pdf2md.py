"""PDF -> body.md / refs.md / figs/ / figs.json / meta.json.

Deterministic local preprocessing for the paper-reading pipeline.
No model calls, no network. Text via pdf-inspector, figures via PyMuPDF.

Run with the interpreter that has both deps:  D:\\2\\software\\python.exe
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import pdf_inspector as pi

# pdf-inspector emits section headings as bold runs (**3. Results**), not ATX headings.
REF_HEAD = re.compile(r"^(?:#{1,4}\s*|\*\*)(references|bibliography|literature cited)\**\s*$", re.I)
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
    """Drop short lines that appear on more than `thresh` of pages (running heads/feet)."""
    n = len(pages)
    seen = Counter()
    for md in pages:
        for line in {l.strip() for l in md.splitlines() if l.strip()}:
            seen[line] += 1
    junk = {l for l, c in seen.items() if c > thresh * n and len(l) < 200}
    return [
        "\n".join(l for l in md.splitlines() if l.strip() not in junk) for md in pages
    ], junk


def split_refs(pages):
    """Return (body_pages, refs_text). Splits at the first References heading."""
    for i, md in enumerate(pages):
        lines = md.splitlines()
        for j, line in enumerate(lines):
            if REF_HEAD.match(line.strip()):
                body = pages[:i] + ["\n".join(lines[:j])]
                refs = "\n".join(lines[j:]) + "\n" + "\n".join(pages[i + 1:])
                return body, refs
    return pages, ""


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
    dest = Path(outroot) / slugify(pdf_path.stem)
    meta_f = dest / "meta.json"
    digest = sha256(pdf_path)
    if meta_f.exists() and not force:
        if json.loads(meta_f.read_text("utf-8")).get("pdf_sha256") == digest:
            print("cached", dest)
            return dest
    dest.mkdir(parents=True, exist_ok=True)

    cls = pi.classify_pdf(str(pdf_path))
    res = pi.extract_pages_markdown(str(pdf_path))
    raw_pages = [p.markdown for p in res.pages]
    pages, junk = strip_running(raw_pages)
    body_pages, refs = split_refs(pages)

    body = "\n\n".join(f"<!-- Page {i} -->\n{md}" for i, md in enumerate(body_pages, 1))
    (dest / "body.md").write_text(body, "utf-8")
    (dest / "refs.md").write_text(refs, "utf-8")

    figures = index_figures(body_pages)
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
    if not refs.strip():
        warnings.append("references were not split; refs.md is empty and body.md "
                        "still carries them (~30-40% more tokens in stage 2)")
    if not figures:
        warnings.append("no figures or tables indexed")
    if not primary:
        warnings.append("has_primary_data is False; confirm by hand before trusting the branch")
    # A stray one or two is normal noise; a real font problem hits a quarter of them.
    if len(shredded) >= 3 and len(shredded) > 0.15 * len(headings):
        warnings.append(f"{len(shredded)} of {len(headings)} headings look shredded by the "
                        "PDF font encoding; every heading-derived field is unreliable")

    meta = {
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
    ap.add_argument("--out", default="out")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    run(a.pdf, a.out, a.force)
