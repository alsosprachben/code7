#!/usr/bin/env python3
# cbdt.py TTF COLORDIR BDF: give code7w.ttf a 14px colour bitmap strike (CBDT/CBLC tables),
# for xterm's TrueType mode at faceNameDoublesize code7w:pixelsize=14.
#
# Glyphs in COLORDIR (12x7, palette letters below, '.' transparent) are drawn in colour.
# Every other glyph in BDF goes into the strike too, in the foreground colour: once Xft picks
# a font's colour strike it can no longer load that font's outlines, and xterm rejects a
# double-size font whose Latin-1 glyphs fail to load. Each design pixel becomes 2x2.
import os, struct, sys, zlib
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import E_B_L_C_ as eblc, C_B_D_T_ as cbdt
from fontTools.ttLib.tables.BitmapGlyphMetrics import SmallGlyphMetrics

# Explicit emoji colours, independent of the terminal theme (colour glyphs ignore it anyway),
# chosen to read on dark and light backgrounds alike.
PALETTE = {
	'r': (0xdd, 0x2e, 0x44),  # red
	'o': (0xf4, 0x90, 0x0c),  # orange
	'y': (0xfd, 0xcb, 0x58),  # yellow
	'g': (0x78, 0xb1, 0x59),  # green
	'b': (0x55, 0xac, 0xee),  # blue
	'v': (0xaa, 0x8e, 0xd6),  # purple
	'n': (0xc1, 0x69, 0x4f),  # brown
	'p': (0xea, 0x59, 0x6e),  # pink
	'w': (0xe6, 0xe7, 0xe8),  # white
	'k': (0x66, 0x75, 0x7f),  # grey
	'd': (0x31, 0x37, 0x3d),  # dark
	'a': (0xf7, 0xde, 0xce),  # skin tones, light to dark
	'e': (0xf3, 0xd2, 0xa2),
	'i': (0xd5, 0xab, 0x88),
	'j': (0xaf, 0x7e, 0x57),
	'l': (0x7c, 0x53, 0x3e),
	'x': (0x93, 0x93, 0x93),  # neutral grey: glyphs with no colour version
}
SCALE = 2           # screen pixels per design pixel at 14px
ASCENT, DESCENT = 6, 1  # design rows above and below the baseline


def png(rows):
	"""An RGBA PNG of rows of palette letters, each cell SCALE x SCALE pixels."""
	w, h = len(rows[0]) * SCALE, len(rows) * SCALE
	raw = b''
	for r in rows:
		line = b''.join((bytes(PALETTE[c]) + b'\xff' if c != '.' else b'\0\0\0\0') * SCALE for c in r)
		raw += (b'\0' + line) * SCALE
	def chunk(tag, data):
		return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data))
	return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
		+ chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def bdf_glyphs(path):
	"""{codepoint: rows of 'x'/'.'} from a BDF."""
	glyphs, enc, width, rows = {}, None, 0, None
	for line in open(path):
		if line.startswith('ENCODING'):
			enc = int(line.split()[1])
		elif line.startswith('BBX'):
			width = int(line.split()[1])
		elif line.startswith('BITMAP'):
			rows = []
		elif line.startswith('ENDCHAR'):
			glyphs[enc] = [''.join('x' if int(h, 16) >> (len(h) * 4 - 1 - i) & 1 else '.' for i in range(width)) for h in rows]
			rows = None
		elif rows is not None:
			rows.append(line.strip())
	return glyphs


def line_metrics():
	m = eblc.SbitLineMetrics()
	for a in ('caretSlopeDenominator', 'caretOffset', 'minOriginSB', 'minAdvanceSB',
			'maxBeforeBL', 'minAfterBL', 'pad1', 'pad2'):
		setattr(m, a, 0)
	m.ascender, m.descender, m.widthMax, m.caretSlopeNumerator = ASCENT * SCALE, -DESCENT * SCALE, 12 * SCALE, 1
	return m


path, colordir, bdf = sys.argv[1:4]
f = TTFont(path)
cmap = f.getBestCmap()
glyphs = {cmap[cp]: rows for cp, rows in bdf_glyphs(bdf).items() if cp in cmap}
for n in os.listdir(colordir):
	glyphs[cmap[int(n[2:], 16)]] = open(os.path.join(colordir, n)).read().split()
names = sorted(glyphs, key=f.getGlyphID)

data, subtables = {}, []
for name in names:
	rows = glyphs[name]
	m = SmallGlyphMetrics()
	m.width, m.height = len(rows[0]) * SCALE, len(rows) * SCALE
	m.BearingX, m.BearingY, m.Advance = 0, ASCENT * SCALE, m.width
	g = cbdt.cbdt_bitmap_format_17(b'', f)
	g.metrics, g.imageData = m, png(rows)
	data[name] = g
	sub = eblc.eblc_index_sub_table_1(b'', f)
	sub.indexFormat, sub.imageFormat, sub.names = 1, 17, [name]
	sub.firstGlyphIndex = sub.lastGlyphIndex = f.getGlyphID(name)
	subtables.append(sub)

size = eblc.BitmapSizeTable()
size.hori, size.vert = line_metrics(), line_metrics()
size.colorRef, size.ppemX, size.ppemY, size.bitDepth, size.flags = 0, 7 * SCALE, 7 * SCALE, 32, 1
size.startGlyphIndex, size.endGlyphIndex = f.getGlyphID(names[0]), f.getGlyphID(names[-1])
strike = eblc.Strike()
strike.bitmapSizeTable, strike.indexSubTables = size, subtables

f['CBLC'] = newTable('CBLC')
f['CBLC'].version, f['CBLC'].strikes = 3.0, [strike]
f['CBDT'] = newTable('CBDT')
f['CBDT'].version, f['CBDT'].strikeData = 3.0, [data]
f.save(path + '.tmp.ttf')
os.replace(path + '.tmp.ttf', path)
