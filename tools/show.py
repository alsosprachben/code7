#!/usr/bin/env python3
# show.py DIR HEX...: print the glyphs for the given codepoints side by side,
# whatever entity name their files use, e.g. show.py fnt/code7sc/6x7 41 3b1 2500
import sys
import glyphlib

d, cps = sys.argv[1], [int(x, 16) for x in sys.argv[2:]]
w, h = glyphlib.size(d)
found = [(cp, glyphlib.find(d, cp)) for cp in cps]
missing = [cp for cp, name in found if not name]
if missing:
	print('absent:', ' '.join('%04X' % cp for cp in missing))
found = [(cp, name) for cp, name in found if name]
per = max(1, 80 // (w + 2))
for i in range(0, len(found), per):
	row = found[i:i + per]
	print('  '.join(('%04X' % cp).ljust(w) for cp, _ in row))
	bitmaps = [glyphlib.read(d, name) for _, name in row]
	for y in range(h):
		print('  '.join(b[y] for b in bitmaps))
	print()
