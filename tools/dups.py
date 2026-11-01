#!/usr/bin/env python3
# dups.py DIR...: report glyphs with identical bitmaps across the given glyph dirs, and glyphs with no ink
# (all the same size; a file in a later dir replaces the same name in an earlier one,
# so drafts can be checked against a font: dups.py fnt/code7/6x7 drafts/code7).
# Every character must differ from every other by at least one pixel; the agreed
# exceptions below are not reported. A glyph with no pixels set is reported unless it is one of
# the BLANK characters (an empty 🛜 once slipped through). Two files for one character (Tau and U+03A4,
# U+27A1 and U+027A1) are reported too: the build would put both in the font. Exits 1 if anything is reported.
import collections, sys
import glyphlib

EXEMPT = [
	{0x20, 0xa0, 0x2800, *range(0x2000, 0x200B), 0x202F, 0x205F},   # the spaces and the braille blank: all blank
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
	{0x2722, 0x1D144, 0x2B29},  # ✢ 𝅄 ⬩
	{0x25E6, 0x1D146, 0x2B1E},  # ◦ 𝅆 ⬞
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
	{0x4DD3, 0x1CE03},  # ䷓ 𜸃
	# glyphs drawn their natural way although they match an unrelated or same-meaning glyph (agreed 2026-11-01)
	{0x27A1, 0x2B95},  # ➡ ⮕
	{0x27F5, 0x1F800}, {0x27F6, 0x1F802}, {0x27A7, 0x1F81A}, {0x279C, 0x1F82E}, {0x2799, 0x1F846},  # same-direction arrows
	{0x1F590, 0x1F591},  # 🖐 🖑: the hand is symmetric, so mirroring it changes nothing
	{0x2B1B, 0x4DC0},  # ⬛ ䷀: six solid lines with no room for gaps
	{0xE0B1, 0x1FBDF}, {0xE0B3, 0x1FBDD},  # Powerline thin arrows, legacy computing diagonals
	{0x2371, 0x2661},  # ⍱ ♡
	{0x3A9, 0x2126}, {0x4B, 0x212A}, {0xC5, 0x212B},  # Ω Ω, K K, Å Å: the ohm, Kelvin and ångström signs are canonically the letters
	# one-letter Roman numerals are their letters
	{0x49, 0x2160}, {0x56, 0x2164}, {0x58, 0x2169}, {0x4C, 0x216C}, {0x43, 0x216D}, {0x44, 0x216E}, {0x4D, 0x216F},
	{0x69, 0x2170}, {0x76, 0x2174}, {0x78, 0x2179}, {0x6C, 0x217C}, {0x63, 0x217D}, {0x64, 0x217E}, {0x6D, 0x217F},
	{0x1D1B8, 0x2043}, {0x23E6, 0x2053}, {0x273E, 0x2055}, {0x250A, 0x205E},  # 𝆸 ⁃, ⏦ ⁓, ✾ ⁕, ┊ ⁞
]
BLANK = {0x20, 0xa0, 0x2800, *range(0x2000, 0x200B), 0x202F, 0x205F}  # the spaces and the braille blank

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
files = collections.defaultdict(list)
for name in glyphs:
	files[glyphlib.codepoint(name)].append(name)
for cp, names in files.items():
	if len(names) > 1:
		print('two files for U+%04X: %s' % (cp, ' '.join(names)))
		bad += 1
for name, bitmap in glyphs.items():
	if not any(c != '.' for r in bitmap for c in r) and glyphlib.codepoint(name) not in BLANK:
		print('blank: ' + name)
		bad += 1
sys.exit(1 if bad else 0)
