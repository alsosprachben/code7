#!/usr/bin/env python3
# latin2x.py SRC DST: write pixel-doubled copies of the ASCII and Latin-1 glyphs in
# SRC (a 6x7 glyph dir) into DST (a 12x7 glyph dir), keeping any glyph DST already has.
# xterm measures a TrueType wide font (faceNameDoublesize) by its ISO-8859-1 glyphs and
# rejects one that has none, so code7w carries these even though they are never drawn.
import os, sys

src, dst = sys.argv[1:3]
names = {}   # codepoint -> every entity name it has; a glyph file may use any of them
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fnt', 'src', 'entities.csv')):
	name, code = line.strip().split(',')
	names.setdefault(int(code, 16), []).append(name)

for cp in list(range(0x20, 0x7f)) + list(range(0xa0, 0x100)):
	out = os.path.join(dst, 'U+%05X' % cp)
	candidates = names.get(cp, []) + ['U+%05X' % cp, 'U+%04X' % cp]
	if any(os.path.exists(os.path.join(dst, name)) for name in candidates):
		continue
	for name in candidates:
		if os.path.exists(os.path.join(src, name)):
			rows = [r.ljust(6, '.')[:6] for r in open(os.path.join(src, name)).read().split('\n')[:7]]
			rows += ['......'] * (7 - len(rows))
			open(out, 'w').write('\n'.join(''.join(c * 2 for c in r) for r in rows) + '\n')
			break
