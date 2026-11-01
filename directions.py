#!/usr/bin/env python3
# directions.py COLORDIR OUTDIR: add ligature sources for the facing-right sequences (🚶‍➡️) to OUTDIR,
# for flags.py and cbdt.py. Each is the left-facing drawing mirrored, saved as SOURCE-200D-27A1-FE0F.
# The drawing comes from COLORDIR (U+BASE) for a single emoji, or from OUTDIR for a sequence, so this
# runs after genders.py and before skintones.py, which then tones them (🏃🏽‍♀️‍➡️).
# Generated at build time, not stored in fnt/.
import os, sys

PEOPLE = ['1F6B6', '1F3C3', '1F9CE']  # 🚶 🏃 🧎, and their ♀ and ♂ forms
SOURCES = PEOPLE + ['%s-200D-%s-FE0F' % (p, g) for p in PEOPLE for g in ('2640', '2642')] \
	+ ['%s-200D-%s' % (p, o) for p in ('1F9D1', '1F468', '1F469') for o in ('1F9AF', '1F9BC', '1F9BD')]  # 🦯 🦼 🦽

colordir, outdir = sys.argv[1:3]
n = 0
for src in SOURCES:
	path = os.path.join(colordir, 'U+%05X' % int(src, 16)) if '-' not in src else os.path.join(outdir, src)
	rows = open(path).read().split()
	w = len(rows[0]) - 1  # the last column stays blank
	open(os.path.join(outdir, src + '-200D-27A1-FE0F'), 'w').write('\n'.join(r[w - 1::-1] + r[w:] for r in rows) + '\n')
	n += 1
print('directions.py: %d sequences' % n, file=sys.stderr)
