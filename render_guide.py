#!/usr/bin/env python3
"""Render a complete easy-paper Markdown guide as offline HTML, optionally A4 PDF.

Canonical content is the verified Markdown. The renderer changes *presentation only*:
no rewriting, summarization, remote CSS, or AI calls. Python: pip install mistune>=3.
Optional PDF: pip install playwright && python -m playwright install chromium.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import sys
from pathlib import Path

try:
    import mistune
except ImportError as exc:
    raise SystemExit('Missing rendering dependency: python -m pip install "mistune>=3,<4"') from exc

HERE = Path(__file__).resolve().parent
H2 = re.compile(r'<h2>(.*?)</h2>', re.I | re.S)
H3 = re.compile(r'<h3>(.*?)</h3>', re.I | re.S)
P = re.compile(r'(<p>.*?</p>)', re.I | re.S)
FIG = re.compile(r'\bfig(?:ure)?\.?\s*(\d+[a-z]?)\b', re.I)
ALLOWED = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}


def plain(fragment: str) -> str:
    return html.unescape(re.sub(r'<[^>]+>', '', fragment)).strip()


def slug(text: str) -> str:
    name = re.sub(r'[^a-z0-9]+', '-', text.casefold()).strip('-')[:60]
    return name or 'section'


def load_figures(path: Path | None) -> dict[str, dict]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema') != 'easy-paper-figures/v1' or not isinstance(data.get('figures'), list):
        raise ValueError('Figure manifest requires schema easy-paper-figures/v1 and figures[]')
    output = {}
    for fig in data['figures']:
        name = str(fig.get('id', ''))
        match = FIG.search(name)
        if not match or not fig.get('inspected'):
            raise ValueError(f'Figure must have an id and inspected=true: {name!r}')
        page = fig.get('page')
        if type(page) is not int or page < 1:
            raise ValueError(f'Figure {name} needs a positive one-based PDF page integer')
        image_path = (path.parent / fig['path']).resolve()
        if not image_path.is_file() or image_path.suffix.lower() not in ALLOWED:
            raise ValueError(f'Figure {name} image missing or unsupported: {image_path}')
        contents = image_path.read_bytes()
        signatures = {'.png': contents.startswith(b'\x89PNG\r\n\x1a\n'), '.jpg': contents.startswith(b'\xff\xd8\xff'), '.jpeg': contents.startswith(b'\xff\xd8\xff'), '.webp': contents.startswith(b'RIFF') and contents[8:12] == b'WEBP'}
        if not signatures[image_path.suffix.lower()]:
            raise ValueError(f'Figure is not a valid {image_path.suffix} image: {image_path}')
        identifier = match.group(1).lower()
        if identifier in output:
            raise ValueError(f'Duplicate figure {name}')
        output[identifier] = {
            'id': name, 'page': page, 'key': str(fig.get('key') or ''), 'mime': ALLOWED[image_path.suffix.lower()],
            'data': base64.b64encode(contents).decode('ascii'),
            'alt': str(fig.get('alt') or f'Original {name}, PDF page {page}'),
            'caption': str(fig.get('caption') or ''),
        }
    return output


def embed_figures(markup: str, figures: dict[str, dict]) -> str:
    """Attach a source-checked original figure at its first prose pointer.

    No figure asset means the existing page pointer remains unchanged. Figure crops
    are supplied only after visual inspection; never guess pixels from captions.
    """
    used = set()
    explicit = re.compile(r'<p>\s*\[\[FIG:([a-zA-Z0-9_-]+)\]\]\s*</p>', re.I)
    by_key = {v['key']: (number, v) for number, v in figures.items() if v['key']}
    def figure_tag(fig: dict) -> str:
        caption = html.escape(fig['caption'])
        alt = html.escape(fig['alt'], quote=True)
        ident = html.escape(fig['id'])
        return (f'<figure class="paper-figure"><div class="figure-head">'
                f'<strong>{ident}</strong><span>Original PDF · p. {fig["page"]}</span></div>'
                f'<img class="figure-image" loading="lazy" alt="{alt}" '
                f'src="data:{fig["mime"]};base64,{fig["data"]}">'
                f'<figcaption>{caption}</figcaption></figure>')
    def from_marker(match: re.Match) -> str:
        key = match.group(1)
        if key not in by_key:
            return f'<p class="missing-figure">Original figure not embedded: {html.escape(key)}. Refer to the original PDF.</p>'
        number, fig = by_key[key]
        if number in used:
            return ''
        used.add(number)
        return figure_tag(fig)
    markup = explicit.sub(from_marker, markup)

    def after_paragraph(found: re.Match) -> str:
        para = found.group(1)
        embedded = []
        for fig_ref in FIG.finditer(plain(para)):
            key = fig_ref.group(1).lower()
            if key in used or key not in figures:
                continue
            used.add(key)
            fig = figures[key]
            embedded.append(figure_tag(fig))
        return para + '\n' + '\n'.join(embedded)

    return P.sub(after_paragraph, markup)


def generate(markdown: str, figures: dict[str, dict] | None = None) -> str:
    if not markdown.strip():
        raise ValueError('Empty Markdown guide: no HTML generated')
    md = mistune.create_markdown(escape=True, plugins=['table', 'strikethrough'])
    body = md(markdown)
    if not body.lstrip().lower().startswith('<h1>'):
        raise ValueError('Guide must start with an H1 title; do not invent paper identity')
    title_match = re.search(r'<h1>(.*?)</h1>', body, re.I | re.S)
    title = plain(title_match.group(1))
    if not title:
        raise ValueError('Empty heading')
    sections = []
    seen = set()

    def heading_repl(match: re.Match) -> str:
        raw = match.group(1)
        label = plain(raw)
        base = slug(label)
        uid = base
        n = 2
        while uid in seen:
            uid, n = f'{base}-{n}', n + 1
        seen.add(uid)
        sections.append((uid, label))
        return f'<h2 id="{uid}">{raw}</h2>'

    body = H2.sub(heading_repl, body)
    body = H3.sub(lambda m: f'<h3>{m.group(1)}</h3>', body)
    body = embed_figures(body, figures or {})
    toc = '\n'.join(f'<a class="toc-link" href="#{html.escape(uid, quote=True)}">'
                    f'{html.escape(label)}</a>' for uid, label in sections)
    style = (HERE / 'templates' / 'reader.css').read_text(encoding='utf-8')
    script = (HERE / 'templates' / 'reader.js').read_text(encoding='utf-8')
    escaped_title = html.escape(title)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escaped_title} · easy-paper</title><style>{style}</style></head>
<body><div class="read-progress" id="progress"></div>
<div class="layout"><aside class="sidebar"><div class="brand">easy-paper / close reading</div>
<div class="sidebar-title">{escaped_title}</div><div class="sidebar-meta">Complete guide · source-grounded</div>
<div class="nav-rule"></div><div class="toc-header">On this page</div><nav>{toc}</nav>
<div class="sidebar-bottom">PDF-page pointers refer to the original source. Click embedded figures to zoom. The HTML and PDF contain the same reading text.</div></aside>
<main class="main"><div class="inner"><div class="kicker">Research reading / verified source</div>
<article id="paper">{body}</article>
<div class="note-bottom"><strong>About this guide.</strong> Page references are to the source PDF, not this exported guide. The original article remains authoritative. The HTML is a presentation of the complete Markdown, not an abbreviated summary.</div>
</div></main></div>
<div id="lightbox" role="dialog" aria-label="Enlarged original figure" aria-modal="true" aria-hidden="true">
<button id="close" aria-label="Close enlarged figure">×</button><img alt="Enlarged original figure"></div>
<script>{script}</script></body></html>'''


def unique_target(path: Path, want_pdf: bool) -> Path:
    """Never overwrite an existing HTML/PDF or the reader's annotated revisions."""
    base = path.with_suffix('')
    n = 1
    while True:
        suffix = '' if n == 1 else f'-r{n}'
        candidate = base.with_name(base.name + suffix).with_suffix('.html')
        if not candidate.exists() and (not want_pdf or not candidate.with_suffix('.pdf').exists()):
            return candidate
        n += 1


def run(guide: Path, output: Path | None = None, figures: Path | None = None,
        pdf: bool = False, browser_path: str | None = None) -> tuple[Path, Path | None]:
    guide = guide.resolve()
    text = guide.read_text(encoding='utf-8')
    result = generate(text, load_figures(figures.resolve() if figures else None))
    dest = unique_target(output or guide.with_suffix('.html'), pdf)
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive create preserves annotated versions and guards accidental overwrites.
    with dest.open('x', encoding='utf-8') as out:
        out.write(result)
    exported_pdf = None
    if pdf:
        from render_html_pdf import render
        exported_pdf = render(dest, dest.with_suffix('.pdf'), browser_path)
    return dest, exported_pdf


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('guide', type=Path, help='Full verified English guide in Markdown')
    parser.add_argument('--out', type=Path, help='Desired HTML name (existing output gets -r2)')
    parser.add_argument('--figures', type=Path, help='Optional inspected original-figure manifest JSON')
    parser.add_argument('--pdf', action='store_true', help='Also export A4 PDF via Playwright Chromium')
    parser.add_argument('--browser-path', help='Optional Chromium executable path')
    args = parser.parse_args()
    try:
        html_path, pdf_path = run(args.guide, args.out, args.figures, args.pdf, args.browser_path)
        print(f'HTML: {html_path}')
        if pdf_path:
            print(f'PDF:  {pdf_path}')
        return 0
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())