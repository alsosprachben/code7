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
	{0x336, 0x2500, 0x23AF},  # combining long stroke, box drawings light horizontal, horizontal line extension
	# bracket and line extension pieces: they sit in column 2 to join the pieces above and below
	{0x2502, 0x239C, 0x239F, 0x23A2, 0x23A5, 0x23AA, 0x23AE, 0x23D0},
	# musical symbols that share a bitmap with a symbol they won't be confused with (agreed 2026-11-01)
	{0x23B8, 0x1D100},  # ⎸ 𝄀
	{0x2847, 0x1D104},  # ⡇ 𝄄
	{0x2806, 0x1D108},  # ⠆ 𝄈
	{0x30C, 0x1D127},  # ̌ 𝄧
	{0x2722, 0x1D144},  # ✢ 𝅄
	{0x25E6, 0x1D146},  # ◦ 𝅆
	{0x25C2, 0x1D14B},  # ◂ 𝅋
	{0x25B8, 0x1D14D},  # ▸ 𝅍
	{0x25FB, 0x1D15A},  # ◻ 𝅚
	{0x2BC0, 0x1D15B},  # ⯀ 𝅛
	{0x307, 0x1D17C},  # ̇ 𝅼
	{0x304, 0x1D17D},  # ̄ 𝅽
	{0x302, 0x1D17F},  # ̂ 𝅿
	{0x2506, 0x1D18B},  # ┆ 𝆋
	{0x22C4, 0x1D1B9},  # ⋄ 𝆹
	{0x2759, 0x1D1C1, 0x1CE4C},  # ❙ 𝇁 𜹌
	{0x1F797, 0x1D1C2},  # 🞗 𝇂
	{0x2316, 0x1D1CF},  # ⌖ 𝇏
	{0x23FD, 0x1D1FF, 0x1CE4B},  # ⏽ 𝇿 𜹋
	# legacy computing pieces that share a bitmap with a box drawing or symbol they join or stand in for (agreed 2026-11-01)
	{0x1FB97, 0x1CC45}, {0x2309, 0x1CE18}, {0x230B, 0x1CE19}, {0x2578, 0x1CE1E}, {0x2501, 0x1CE1F}, {0x2533, 0x1CE20},
	{0x257A, 0x1CE25}, {0x2523, 0x1CE28}, {0x2503, 0x1CE29}, {0x2769, 0x1CE2E}, {0x252B, 0x1CE36}, {0x254B, 0x1CE3A},
	{0x253B, 0x1CE40}, {0x22C5, 0x1CE4D}, {0x1D19C, 0x1CE58}, {0xAD, 0x1CE5C},
	{0x26AD, 0x1CC88},  # ⚭ 𜲈: the marriage symbol is two rings
	{0x1CE52, 0x1CE92}, {0x1CE70, 0x1CE9E},  # separated sextant cells that coincide with sixteenth blocks
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
