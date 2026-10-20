#!/usr/bin/env python3
"""Crop a visually inspected figure from one source PDF page (coordinates 0..1).

Use screenshot/visual inspection before choosing the rectangle. This helper does
not identify figures and cannot validate semantic content.
"""
import argparse
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pdf', type=Path)
    ap.add_argument('--page', type=int, required=True, help='1-based source PDF page')
    ap.add_argument('--rect', type=float, nargs=4, required=True, metavar=('LEFT','TOP','RIGHT','BOTTOM'),
                    help='Normalized [0,1] rectangle chosen after viewing the original page')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--scale', type=float, default=2.0)
    a = ap.parse_args()
    try:
        import fitz
        if not (0 <= a.rect[0] < a.rect[2] <= 1 and 0 <= a.rect[1] < a.rect[3] <= 1):
            raise ValueError('Rectangle must lie within [0,1] with nonzero area')
        if a.out.exists():
            raise FileExistsError(f'Crop already exists; preserving notes: {a.out}')
        if a.scale <= 0:
            raise ValueError('--scale must be positive')
        doc = fitz.open(a.pdf)
        if a.page < 1 or a.page > doc.page_count:
            raise ValueError(f'Page must lie in 1..{doc.page_count}')
        page = doc[a.page - 1]
        r = page.rect
        clip = fitz.Rect(r.x0 + a.rect[0]*r.width, r.y0 + a.rect[1]*r.height,
                         r.x0 + a.rect[2]*r.width, r.y0 + a.rect[3]*r.height)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        page.get_pixmap(matrix=fitz.Matrix(a.scale,a.scale),clip=clip,alpha=False).save(a.out)
        print(f'Saved {a.out}; visually inspect the resulting crop before marking inspected=true')
        return 0
    except (OSError, ValueError, ImportError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())