#!/usr/bin/env python3
# flags.py TTF FLAGDIR: add country flags to code7w.ttf as ligatures of regional indicator
# pairs, for terminals that shape text (kitty, WezTerm). Each file in FLAGDIR is named after
# its country code (US, JP ...) and holds a 12x7 drawing in cbdt.py's palette letters; this
# adds a two-cell outline glyph flag_XX (white parts left blank) and a GSUB ligature from
# the two letters to it. cbdt.py then gives flag_XX its colour bitmap. The letter keys
# themselves are narrowed to one cell, the width terminals give them.
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

path, flagdir = sys.argv[1:3]
f = TTFont(path, lazy=False)
glyf, hmtx, cmap = f['glyf'], f['hmtx'], f.getBestCmap()
px = f['head'].unitsPerEm // 7
ascent = f['hhea'].ascent
subs = []
# the letters are one cell wide: an unmatched pair then shows as two keys side by side
for cp in range(0x1F1E6, 0x1F200):
	hmtx[cmap[cp]] = (6 * px, 0)
for code in sorted(os.listdir(flagdir)):
	rows = open(os.path.join(flagdir, code)).read().split()
	pen = TTGlyphPen(None)
	for r, row in enumerate(rows):
		x = 0
		while x < len(row):
			if row[x] in '.w':
				x += 1
				continue
			x2 = x
			while x2 < len(row) and row[x2] not in '.w':
				x2 += 1
			top, bottom = ascent - px * r, ascent - px * (r + 1)
			pen.moveTo((x * px, bottom)); pen.lineTo((x * px, top)); pen.lineTo((x2 * px, top)); pen.lineTo((x2 * px, bottom)); pen.closePath()
			x = x2
	name = 'flag_' + code
	glyf[name] = pen.glyph()
	hmtx[name] = (len(rows[0]) * px, 0)
	a, b = (cmap[0x1F1E6 + ord(c) - ord('A')] for c in code)
	subs.append('sub %s %s by %s;' % (a, b, name))
f.setGlyphOrder(glyf.glyphOrder)
rules = '\n'.join(subs)
addOpenTypeFeaturesFromString(f, 'feature ccmp {\n%s\n} ccmp;\nfeature liga {\n%s\n} liga;\n' % (rules, rules))
f.save(path + '.tmp.ttf')
os.replace(path + '.tmp.ttf', path)
