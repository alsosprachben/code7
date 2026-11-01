#!/usr/bin/env python3
# flags.py TTF FLAGDIR: add flags to code7w.ttf as ligatures, for terminals that shape text
# (kitty, WezTerm). Each file in FLAGDIR holds a 12x7 drawing in cbdt.py's palette letters
# and is named either after a country code (US, JP ...), for a regional indicator pair, or
# after the hex codepoints of any other emoji sequence joined by '-' (1F3F4-E0067-...-E007F
# for England, 1F3F3-FE0F-200D-1F308 for the rainbow flag). This adds a two-cell outline
# glyph (white parts left blank) and a GSUB ligature from the sequence to it; cbdt.py then
# gives it its colour bitmap. Codepoints in a sequence that the font lacks (tags, ZWJ,
# variation selectors) get an empty zero-width glyph, since ligatures only match glyphs the
# font has. The letter keys and 🏳 are narrowed to one cell, the width terminals give them.
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
# one cell wide: an unmatched letter pair then shows as two keys side by side
for cp in list(range(0x1F1E6, 0x1F200)) + [0x1F3F3]:
	if cp in cmap:
		hmtx[cmap[cp]] = (6 * px, 0)
def glyph_for(cp):
	"""the glyph for cp, adding an empty zero-width one if the font has none"""
	if cp not in cmap:
		name = 'u%04X' % cp
		glyf[name] = TTGlyphPen(None).glyph()
		hmtx[name] = (0, 0)
		for t in f['cmap'].tables:
			if t.isUnicode() and (cp <= 0xFFFF or t.format >= 12):
				t.cmap[cp] = name
		cmap[cp] = name
	return cmap[cp]
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
	name = 'flag_' + code.replace('-', '_')
	glyf[name] = pen.glyph()
	hmtx[name] = (len(rows[0]) * px, 0)
	if len(code) == 2:
		seq = [0x1F1E6 + ord(c) - ord('A') for c in code]
	else:
		seq = [int(h, 16) for h in code.split('-')]
	subs.append('sub %s by %s;' % (' '.join(glyph_for(cp) for cp in seq), name))
f.setGlyphOrder(glyf.glyphOrder)
rules = '\n'.join(subs)
addOpenTypeFeaturesFromString(f, 'feature ccmp {\n%s\n} ccmp;\nfeature liga {\n%s\n} liga;\n' % (rules, rules))
f.save(path + '.tmp.ttf')
os.replace(path + '.tmp.ttf', path)
