#!/usr/bin/env python3
"""Structural preflight for easy-paper v4 cards and verification logs.

Checks are intentionally mechanical; they cannot establish scientific truth.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = {'schema','source','paper','questions','methods','results',
            'interpretations','limitations','writing_samples','figure_pointers',
            'extraction_warnings'}
LISTS = REQUIRED - {'schema','source','paper'}


def validate(card_path: Path, verification_path: Path | None = None) -> list[str]:
    failures = []
    try:
        data = json.loads(card_path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return [f'Cannot read card: {exc}']
    if not isinstance(data, dict):
        return ['Evidence card must be a JSON object']
    if data.get('schema') != 'evidence-card/v4':
        failures.append('schema must equal evidence-card/v4')
    missing = REQUIRED - data.keys()
    if missing:
        failures.append('Missing keys: ' + ', '.join(sorted(missing)))
    for field in LISTS & data.keys():
        if not isinstance(data[field], list):
            failures.append(f'{field} must be an array')
    src = data.get('source')
    n_pages = src.get('n_pages') if isinstance(src, dict) else None
    if type(n_pages) is not int or n_pages < 1:
        failures.append('source.n_pages must be a positive integer')
        n_pages = None
    if not isinstance(data.get('paper'), dict) or not data['paper'].get('title'):
        failures.append('paper.title must be present')
    if not isinstance(src, dict) or not src.get('pdf_sha256') or not src.get('extractor_sha256'):
        failures.append('source must preserve pdf_sha256 and extractor_sha256')
    for field in LISTS & data.keys():
        if not isinstance(data[field], list):
            continue
        for index, item in enumerate(data[field]):
            if not isinstance(item, dict):
                failures.append(f'{field}[{index}] must be an object')
                continue
            locations = item.get('locations', [])
            if not isinstance(locations, list):
                failures.append(f'{field}[{index}].locations must be an array')
                continue
            for j, loc in enumerate(locations):
                page = loc.get('page') if isinstance(loc, dict) else None
                if type(page) is not int or page < 1 or (n_pages and page > n_pages):
                    failures.append(f'{field}[{index}].locations[{j}].page is not a valid PDF page')
            if field == 'writing_samples' and not item.get('quote'):
                failures.append(f'writing_samples[{index}] missing verbatim quote')
    if verification_path:
        try:
            log = json.loads(verification_path.read_text('utf-8'))
            if not isinstance(log, dict) or not log:
                failures.append('verification.json must be a nonempty object')
        except (OSError, ValueError) as exc:
            failures.append(f'verification.json missing or invalid: {exc}')
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('evidence_card', type=Path)
    ap.add_argument('--verification', type=Path)
    args = ap.parse_args()
    errors = validate(args.evidence_card, args.verification)
    if errors:
        for error in errors:
            print('FAIL', error)
        return 1
    print('PASS: v4 structural checks (NOT scientific/source verification)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())