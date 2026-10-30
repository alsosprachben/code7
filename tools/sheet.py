#!/usr/bin/env python3
# sheet.py DIR [PER_ROW]: print every glyph in DIR in codepoint order, headed by the
# character and its codepoint, for reviewing a draft or a whole font.
import sys
import glyphlib

d = sys.argv[1]
w, h = glyphlib.size(d)
per = int(sys.argv[2]) if len(sys.argv) > 2 else max(1, 80 // (w + 2))
names = glyphlib.files(d)
for i in range(0, len(names), per):
	row = names[i:i + per]
	print('  '.join(('%s %04X' % (chr(glyphlib.codepoint(n)), glyphlib.codepoint(n))).ljust(w) for n in row))
	bitmaps = [glyphlib.read(d, n) for n in row]
	for y in range(h):
		print('  '.join(b[y] for b in bitmaps))
	print()
