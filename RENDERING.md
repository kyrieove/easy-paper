# HTML / PDF delivery for easy-paper

The canonical reading material is the **complete, source-verified Markdown guide** generated under `SKILL.md` v4. Rendering is a deterministic **presentation step**, not a second summarization or a new AI writing pass. A short, beautiful PDF is not acceptable if it omits source-grounded material.

## Install (once, in the same Python environment)

```powershell
python -m pip install pdf-inspector "mistune>=3,<4"
python -m pip install playwright pymupdf
python -m playwright install chromium
```

`pdf-inspector` handles the existing local PDF extraction. `mistune` powers HTML generation. Playwright/Chromium is needed only for PDF export. PyMuPDF (`pymupdf`) is optional and is used only for manually selected original-figure crops. No account/API key is required. Chrome can instead be supplied with `--browser-path` if Playwright's bundled Chromium is unavailable.

## Exact agent-agnostic workflow

1. Follow `SKILL.md` v4 on the paper: extract and inspect original PDF, create/review `evidence-card.json`, write full English `reading-guide.md`, verify central claims/quotations/pages against the source, and record `verification.json` with unresolved checks. **Do not write a condensed HTML-specific guide.**
2. Validate card structure (this is not a substitute for checking the source):

   ```powershell
   python validate_v4.py output/extracted/<paper>/evidence-card.json --verification output/extracted/<paper>/verification.json
   ```

3. Produce offline HTML from the full guide (HTML images are optional):

   ```powershell
   python render_guide.py output/reading-guides/paper-reading-guide.md
   ```

4. For the **same content plus a print-ready A4 PDF**:

   ```powershell
   python render_guide.py output/reading-guides/paper-reading-guide.md --pdf
   ```

   Or render an existing HTML without regenerating it: `python render_html_pdf.py path/to/guide.html`.

5. Open **both** HTML and PDF; check all headings and source pointers, first and last pages, tables, important figures, truncated/overlapping material, and missing fonts. Fix the **source Markdown** if the content is wrong; fix the **template** if formatting is wrong. Regenerate without overwriting annotated versions; the renderer automatically creates `-r2`, `-r3`, etc.

The template `templates/reader.css` provides a responsive fixed sidebar, legible serif headings, constrained measure, subdued tables/callouts, and A4 print CSS. `templates/reader.js` adds reading progress, section highlighting, and figure zoom. Styles/scripts are embedded in the output: HTML works offline in Codex, Antigravity, DSH and a normal browser, assuming the same inputs and dependency versions.

## Original figures (optional; never hallucinate)

The `figures.json` created by `pdf2md.py` indexes **captions** only. It cannot identify or crop pixels. To embed a figure, **inspect the original PDF** and make a separate manifest:

```json
{
  "schema": "easy-paper-figures/v1",
  "figures": [
    {
      "id": "Fig. 5",
      "page": 9,
      "path": "assets/fig5.png",
      "key": "sorsa_fig5",
      "caption": "Original Figure 5 (caption verified against PDF)",
      "alt": "Original EEG comparison plots, figure 5",
      "inspected": true
    }
  ]
}
```

`page` is the one-based **PDF viewer page**, not the journal's printed page. Assets are resolved relative to the manifest. Generate and inspect crops using any image editor; the optional helper takes **normalized** page coordinates and must be used only *after* locating the figure visually:

```powershell
python crop_pdf_figure.py paper.pdf --page 9 --rect 0.06 0.22 0.94 0.84 --out assets/fig5.png
python render_guide.py guide.md --figures my-figures.json --pdf
```

The rectangle above is **illustrative only**, not a measured crop for any paper. Inspect and adjust. A `key` is optional: if the guide contains a standalone `[[FIG:sorsa_fig5]]` marker, the figure is inserted **exactly there**. Otherwise an image is placed after its **first prose mention** of `Fig. N` / `Figure N`. References not associated with supplied visual assets remain as text pointing at the source; the script does not invent images. All figure images are embedded as data URIs so the HTML and PDF never depend on external paths or services.

## Reproducibility and boundaries

- **Same content:** model writes/verifies the Markdown; scripts only format it. Check the final HTML/PDF; machine tests do not check scientific reasoning.
- **Same appearance:** the repository's CSS/JS is shared; every agent runs the same code and fonts available on the user's OS. System font differences and installed Chromium versions can change pagination slightly.
- **One owner for the text:** no second AI HTML-writing stage, no arbitrary length restriction, no new conclusions in print layout, no fixed number of parts.
- **Safe reruns:** source files and annotated outputs are not overwritten. Do not publish PDFs without checking figure crops and page citations.
- **Historical checks:** `check_guides.py` belongs to the old v3 format. Use `validate_v4.py` for basic v4 structure; actual claims still require the `SKILL.md` source audit.