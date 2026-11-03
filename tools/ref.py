#!/usr/bin/env python3
# ref.py [-f FONTDIR] HEX...: each character rendered from an installed reference font, beside the font's glyph,
# to draw from real letterforms instead of guessing. The reference is found with fontconfig (Noto Serif first,
# then any font that has the character); combining marks are shown on a dotted circle. Needs Pillow.
# FONTDIR defaults to fnt/code7/6x7; give fnt/code7w/12x7 for wide glyphs.
import os, subprocess, sys, unicodedata
from PIL import Image, ImageDraw, ImageFont
import glyphlib

TOOLS = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
fontdir = os.path.join(os.path.dirname(TOOLS), 'fnt/code7/6x7')
if args[:1] == ['-f']: fontdir, args = args[1], args[2:]
cps = [int(a, 16) for a in args]
PREFER = ('NotoSerif-Regular', 'NotoSerif', 'NotoSans-Regular', 'NotoSans', 'FreeSerif', 'DejaVuSans')
W, H, STEP = 36, 52, 2


def font_for(c):
	out = subprocess.run(['fc-list', ':charset=%x' % c, 'file'], capture_output=True, text=True).stdout
	files = [l.split(':')[0] for l in out.splitlines() if l and 'code7' not in l]
	for p in PREFER:
		for f in files:
			if os.path.basename(f).startswith(p): return f
	return files[0] if files else None


def reference(c):
	fp = font_for(c)
	if not fp: return ['(no font)'.ljust(W // STEP)] + ['.' * (W // STEP)] * (H // STEP - 1), '-'
	text = ('◌' if unicodedata.category(chr(c)).startswith('M') else '') + chr(c)
	im = Image.new('L', (W, H), 0)
	ImageDraw.Draw(im).text((2, 0), text, font=ImageFont.truetype(fp, 34), fill=255)
	px = im.load()
	return [''.join('o' if px[x, y] > 100 else '.' for x in range(0, W, STEP)) for y in range(0, H, STEP)], os.path.basename(fp)


def ours(c):
	n = glyphlib.find(fontdir, c)
	return list(glyphlib.read(fontdir, n)) if n else ['?' * 6] * 7


for i in range(0, len(cps), 5):
	grp = cps[i:i + 5]
	refs = [reference(c) for c in grp]
	mine = [ours(c) for c in grp]
	w = max(len(g[0]) for g in mine)
	print('   '.join(('%04X %s %s' % (c, chr(c), r[1][:10])).ljust(W // STEP + 1 + w) for c, r in zip(grp, refs)))
	for y in range(H // STEP):
		line = '   '.join(r[0][y] + ' ' + (g[y] if y < len(g) else ' ' * w) for r, g in zip(refs, mine))
		if line.replace('.', '').replace(' ', ''): print(line)
	print()
