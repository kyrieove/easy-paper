#!/usr/bin/env python3
"""Print a self-contained reading-guide HTML to an A4 PDF with Chromium.

Usage:
    python render_html_pdf.py guide.html --out guide.pdf
    python render_html_pdf.py guide.html --browser-path /usr/bin/chromium

Install: python -m pip install playwright && python -m playwright install chromium
For reproducibility, embed all images, fonts and styles in the HTML. The renderer
never fetches remote resources, and it refuses missing/non-embedded images.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def render(html_path: Path, pdf_path: Path, browser_path: str | None = None) -> Path:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError(
            "Playwright is missing. Run: python -m pip install playwright && "
            "python -m playwright install chromium"
        ) from e

    html_path = html_path.resolve()
    if not html_path.is_file():
        raise FileNotFoundError(f"HTML input does not exist: {html_path}")
    html = html_path.read_text(encoding="utf-8")
    if "<html" not in html.lower() or "</html>" not in html.lower():
        raise ValueError("Input must be a complete HTML document")
    pdf_path = pdf_path.resolve()
    if pdf_path == html_path:
        raise ValueError("PDF output must be different from HTML input")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        config = {"headless": True}
        if browser_path:
            chrome = Path(browser_path).expanduser().resolve()
            if not chrome.is_file():
                raise FileNotFoundError(f"Chromium executable not found: {chrome}")
            config["executable_path"] = str(chrome)
        browser = playwright.chromium.launch(**config)
        try:
            page = browser.new_page(viewport={"width": 1120, "height": 900}, device_scale_factor=1)
            # set_content avoids OS-specific file:// browser restrictions. Consequently
            # the HTML must be self-contained; remote URLs and local image paths fail.
            def reject_external(route):
                if route.request.url.startswith(("http://", "https://", "file://")):
                    return route.abort("blockedbyclient")
                return route.continue_()
            page.route("**/*", reject_external)
            page.set_content(html, wait_until="load", timeout=30000)
            images = page.locator("img").evaluate_all("""els => els.map(e => ({
                src: e.getAttribute('src') || '', complete: e.complete,
                width: e.naturalWidth
            }))""")
            if any(not item["src"].startswith("data:image/") or not item["complete"] or not item["width"] for item in images):
                raise ValueError("Every <img> must use a valid embedded data:image/ URI")
            page.pdf(path=str(pdf_path), format="A4", prefer_css_page_size=True,
                     print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        finally:
            browser.close()
    if not pdf_path.is_file() or pdf_path.stat().st_size < 1024:
        raise RuntimeError("PDF output was not produced")
    return pdf_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Self-contained UTF-8 HTML input")
    parser.add_argument("--out", type=Path, help="Output PDF, default: same stem as HTML")
    parser.add_argument("--browser-path", help="Optional local Chromium executable")
    args = parser.parse_args()
    try:
        output = render(args.html, args.out or args.html.with_suffix(".pdf"), args.browser_path)
        print(f"Wrote {output} ({output.stat().st_size:,} bytes)")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
