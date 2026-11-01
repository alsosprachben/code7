#!/usr/bin/env python3
# dups.py DIR...: report glyphs with identical bitmaps across the given glyph dirs, and glyphs with no ink
# (all the same size; a file in a later dir replaces the same name in an earlier one,
# so drafts can be checked against a font: dups.py fnt/code7/6x7 drafts/code7).
# Every character must differ from every other by at least one pixel; the agreed
# exceptions below are not reported. A glyph with no pixels set is reported unless it is one of
# the BLANK characters (an empty 🛜 once slipped through). Exits 1 if anything is reported.
import collections, sys
import glyphlib

EXEMPT = [
	{0x20, 0xa0, 0x2800},   # space, no-break space, braille blank: all blank
	{0x305, 0x23ba},        # combining overline, scan line 1: full width so it joins
	{0x332, 0x23bd},        # combining low line, scan line 9
	{0x336, 0x2500},        # combining long stroke, box drawings light horizontal
]
BLANK = {0x20, 0xa0, 0x2800}  # space, no-break space, braille blank

if len(sys.argv) < 2:
	sys.exit(__doc__ or 'usage: dups.py DIR...')
glyphs = {}
for d in sys.argv[1:]:
	for name in glyphlib.files(d):
		glyphs[name] = glyphlib.read(d, name)
by = collections.defaultdict(list)
for name, bitmap in glyphs.items():
	by[bitmap].append(name)
bad = 0
for group in by.values():
	if len(group) > 1 and {glyphlib.codepoint(n) for n in group} not in EXEMPT:
		print(' = '.join(sorted(group, key=glyphlib.codepoint)))
		bad += 1
for name, bitmap in glyphs.items():
	if not any(c != '.' for r in bitmap for c in r) and glyphlib.codepoint(name) not in BLANK:
		print('blank: ' + name)
		bad += 1
sys.exit(1 if bad else 0)
