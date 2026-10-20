#!/usr/bin/env python3
"""Render an offline, single-file HTML guide to A4 PDF with Playwright Chromium."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def render(html_path: Path, pdf_path: Path, browser_path: str | None = None) -> Path:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError('Install PDF renderer: python -m pip install playwright && python -m playwright install chromium') from exc

    source = html_path.resolve()
    if not source.is_file():
        raise FileNotFoundError(f'HTML input not found: {source}')
    content = source.read_text('utf-8')
    if '<html' not in content.lower() or '</html>' not in content.lower():
        raise ValueError('Input must be a complete HTML document')
    target = pdf_path.resolve()
    if target.exists():
        raise FileExistsError(f'Output already exists; preserve previous guide: {target}')
    target.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        launch = {'headless': True}
        if browser_path:
            browser = Path(browser_path).expanduser().resolve()
            if not browser.is_file():
                raise FileNotFoundError(f'Chromium not found: {browser}')
            launch['executable_path'] = str(browser)
        chromium = pw.chromium.launch(**launch)
        try:
            page = chromium.new_page(viewport={'width': 1120, 'height': 900})
            # The exported page must be portable: all CSS, JS and images embedded.
            page.route('**/*', lambda route: route.abort() if route.request.url.startswith(('http:', 'https:', 'file:')) else route.continue_())
            page.set_content(content, wait_until='load', timeout=30000)
            page.emulate_media(media='print')
            status = page.evaluate('''async () => {
              const imgs=[...document.querySelectorAll('img')].filter(i => !i.closest('#lightbox'));
              for (const i of imgs) i.loading='eager';
              await Promise.all(imgs.map(i => i.decode().catch(() => null)));
              return imgs.map(i => ({src: i.getAttribute('src')||'', width:i.naturalWidth}));
            }''')
            if any(not x['src'].startswith('data:image/') or not x['width'] for x in status):
                raise ValueError('All printed images must be valid embedded data:image resources')
            page.pdf(path=str(target), format='A4', prefer_css_page_size=True,
                     print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        finally:
            chromium.close()
    if not target.exists() or target.stat().st_size < 1024:
        raise RuntimeError('PDF export failed')
    return target


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html', type=Path)
    ap.add_argument('--out', type=Path, help='Defaults to same stem, PDF extension')
    ap.add_argument('--browser-path')
    a = ap.parse_args()
    try:
        output = render(a.html, a.out or a.html.with_suffix('.pdf'), a.browser_path)
        print(f'PDF: {output}')
        return 0
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())