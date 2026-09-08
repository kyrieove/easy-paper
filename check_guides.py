"""Gate a batch run before you trust it. Usage: python check_guides.py <run-dir>

<run-dir> holds extracted/<slug>/{body.md,refs.md,evidence-card.json} and
reading_guides/*.md. Exits 1 if anything fails, so it can front a batch script.

The checks exist because a run fails in ways a per-file success line hides: a
subagent that skimmed the source produces a guide that is fluent, correctly
structured, in the right language, and thin. Only the ratio to the source sees it.
"""
import sys, os, re, glob, io, json, hashlib, collections

CJK = re.compile(r'[一-鿿]')
DEC = re.compile(r'(?<![\w.])\d{1,4}\.\d{2,3}(?![\w.])')

# A subagent that did not open SKILL.md still writes a card -- it reconstructs a
# plausible schema from the skill's name and calls it v3. The key set is the only
# thing that separates that from a real extraction; prose and length do not.
COMMON = {'schema', 'paper', 'questions', 'unstated_by_the_paper',
          'extraction_warnings', 'writing_samples', 'figure_pointers'}
REQUIRED = {
    'evidence-card/primary-data/v3': COMMON | {
        'methods', 'results', 'results_reporting', 'author_interpretations',
        'limitations_author_acknowledged'},
    'evidence-card/synthesis/v3': COMMON | {'claims', 'disagreements'},
}


def variants(x):
    """.05 and 0.050 are the same number; the paper and the guide need not agree."""
    v = {x, x.rstrip('0').rstrip('.')}
    return v | {s[1:] for s in list(v) if s.startswith('0.')}


def main(run):
    cards, fails = collections.defaultdict(list), []

    for d in sorted(glob.glob(os.path.join(run, 'extracted', '*', ''))):
        slug = os.path.basename(os.path.normpath(d))
        card = os.path.join(d, 'evidence-card.json')
        if not os.path.exists(card):
            fails.append(slug + ': no evidence-card.json')
            continue
        cards[hashlib.sha256(io.open(card, 'rb').read()).hexdigest()].append(slug)
        try:
            c = json.load(io.open(card, encoding='utf-8'))
        except ValueError as e:
            fails.append('%s: card is not valid JSON (%s)' % (slug, e))
            continue
        want = REQUIRED.get(c.get('schema'))
        if want is None:
            fails.append('%s: schema is %r, not one of the two in SKILL.md -- stage 2 '
                         'invented its own format, redo it' % (slug, c.get('schema', c.get('$schema'))))
        elif want - set(c):
            fails.append('%s: card missing %s' % (slug, ', '.join(sorted(want - set(c)))))

    for slugs in cards.values():
        if len(slugs) > 1:
            fails.append('identical card in %d dirs (copied, not extracted): %s'
                         % (len(slugs), ', '.join(slugs)))

    for g in sorted(glob.glob(os.path.join(run, 'reading_guides', '*.md'))):
        name = os.path.basename(g)
        text = io.open(g, encoding='utf-8').read()
        if CJK.search(text):
            fails.append('%s: %d Chinese characters' % (name, len(CJK.findall(text))))
        missing = [p for p, n in (('one', '1'), ('two', '2'), ('three', '3'),
                                  ('four', '4'), ('five', '5'))
                   if not re.search(r'(?im)^#{1,3}\s*part\s+(' + p + '|' + n + r')\b', text)]
        if missing:
            fails.append('%s: missing Part %s' % (name, ', '.join(missing)))

        src = ''
        for d in glob.glob(os.path.join(run, 'extracted', name[:3] + '*', '')):
            for f in ('body.md', 'refs.md'):
                p = os.path.join(d, f)
                if os.path.exists(p):
                    src += io.open(p, encoding='utf-8').read()
        if src:
            # DOIs and years look like statistics and are not.
            nums = set(n for n in DEC.findall(text) if not n.startswith(('10.', '20')))
            bad = [n for n in nums if not any(v in src for v in variants(n))]
            if len(bad) > len(nums) * 0.05:
                fails.append('%s: %d/%d statistics absent from the source: %s'
                             % (name, len(bad), len(nums), sorted(bad)[:6]))

    for f in fails:
        print('FAIL', f)
    print('\n%d failures' % len(fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
