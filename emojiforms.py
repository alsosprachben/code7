#!/usr/bin/env python3
# emojiforms.py NARROWDIR OUTDIR: add colour emoji forms (CP-FE0F, as in ✂️) of text-style characters to
# OUTDIR, for flags.py and cbdt.py. Each is the character's 6x7 glyph from NARROWDIR, centred in two
# cells and drawn in the palette letter below; a tile (arrows, media controls, religious symbols)
# is the glyph in white on a square of that colour, as in the hand-drawn ↔️. A form already in OUTDIR
# (stored in fnt/code7w-flags, such as ❤️) is left alone. Generated at build time, not stored in fnt/.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
import glyphlib

T = 'tile'
FORMS = {  # codepoint: palette letter (see cbdt.py), or (T, letter)
	0xA9: 'x', 0xAE: 'x', 0x203C: 'r', 0x2049: 'r', 0x2122: 'x', 0x2139: (T, 'b'),
	0x2196: (T, 'b'), 0x2197: (T, 'b'), 0x2198: (T, 'b'), 0x2199: (T, 'b'), 0x21A9: (T, 'b'), 0x21AA: (T, 'b'),
	0x2328: 'x', 0x23CF: (T, 'b'), 0x23ED: (T, 'b'), 0x23EE: (T, 'b'), 0x23EF: (T, 'b'), 0x23F1: 'x', 0x23F2: 'x',
	0x23F8: (T, 'b'), 0x23F9: (T, 'b'), 0x23FA: (T, 'b'), 0x24C2: 'b', 0x25AA: 'x', 0x25AB: 'w', 0x25B6: (T, 'b'),
	0x25C0: (T, 'b'), 0x25FB: 'w', 0x25FC: 'x',
	0x2600: 'y', 0x2601: 'w', 0x2602: 'v', 0x2603: 'w', 0x2604: 'o', 0x260E: 'r', 0x2611: 'x', 0x2618: 'g',
	0x2622: 'y', 0x2623: 'o', 0x2626: (T, 'v'), 0x262A: (T, 'v'), 0x262E: (T, 'v'), 0x262F: (T, 'v'),
	0x2638: (T, 'v'), 0x2639: 'y', 0x263A: 'y', 0x265F: 'x', 0x2660: 'x', 0x2663: 'x', 0x2665: 'r', 0x2666: 'r',
	0x2668: 'r', 0x267B: 'g', 0x267E: 'b', 0x2692: 'x', 0x2694: 'x', 0x2697: 'c', 0x2699: 'x', 0x269B: (T, 'v'),
	0x269C: 'o', 0x26A0: 'y', 0x26B0: 'n', 0x26B1: 'n', 0x26C8: 'w', 0x26CF: 'x', 0x26D1: 'r', 0x26E9: 'r',
	0x26F0: 'n', 0x26F1: 'p', 0x26F4: 'w', 0x26F7: 'b', 0x26F8: 'c',
	0x2702: 'x', 0x2709: 'w', 0x270F: 'o', 0x2712: 'x', 0x2714: 'x', 0x2716: 'x', 0x271D: (T, 'v'),
	0x2721: (T, 'v'), 0x2733: 'g', 0x2734: 'o', 0x2747: 'g', 0x2763: 'r', 0x2934: (T, 'b'), 0x2935: (T, 'b'),
	0x2B05: (T, 'b'), 0x2B06: (T, 'b'), 0x2B07: (T, 'b'),
	0x1F170: 'r', 0x1F171: 'r', 0x1F17E: 'r', 0x1F17F: 'b',  # already solid buttons with the letter cut out
	0x1F321: 'r', 0x1F324: 'y', 0x1F325: 'w', 0x1F326: 'w', 0x1F327: 'c', 0x1F328: 'w', 0x1F329: 'y',
	0x1F32A: 'x', 0x1F32C: 'c', 0x1F336: 'r', 0x1F37D: 'x', 0x1F396: 'o', 0x1F397: 'o', 0x1F399: 'x',
	0x1F39A: 'x', 0x1F39B: 'x', 0x1F39E: 'x', 0x1F39F: 'r', 0x1F3CD: 'x', 0x1F3CE: 'r', 0x1F3D4: 'w',
	0x1F3D5: 'g', 0x1F3F3: 'w', 0x1F3D6: 'y', 0x1F3D7: 'o', 0x1F3D8: 'n', 0x1F3D9: 'b', 0x1F3DA: 'n', 0x1F3DB: 'w',
	0x1F3DC: 'o', 0x1F3DD: 'g', 0x1F3DE: 'g', 0x1F3DF: 'x', 0x1F3F5: 'o', 0x1F3F7: 'o', 0x1F43F: 'n',
	0x1F4FD: 'x', 0x1F549: (T, 'v'), 0x1F54A: 'w', 0x1F56F: 'w', 0x1F570: 'n', 0x1F573: 'k', 0x1F576: 'k',
	0x1F577: 'k', 0x1F578: 'w', 0x1F579: 'r', 0x1F587: 'x', 0x1F58A: 'b', 0x1F58B: 'x', 0x1F58C: 'o',
	0x1F58D: 'r', 0x1F5A5: 'x', 0x1F5A8: 'x', 0x1F5B1: 'x', 0x1F5B2: 'x', 0x1F5BC: 'n', 0x1F5C2: 'o',
	0x1F5C3: 'n', 0x1F5C4: 'x', 0x1F5D1: 'x', 0x1F5D2: 'w', 0x1F5D3: 'w', 0x1F5DC: 'x', 0x1F5DD: 'o',
	0x1F5DE: 'w', 0x1F5E1: 'x', 0x1F5E3: 'x', 0x1F5EF: 'w', 0x1F5F3: 'w', 0x1F5FA: 'g', 0x1F6CB: 'n',
	0x1F6CD: 'p', 0x1F6CE: 'o', 0x1F6CF: 'n', 0x1F6E0: 'x', 0x1F6E1: 'b', 0x1F6E2: 'b', 0x1F6E3: 'x',
	0x1F6E4: 'n', 0x1F6E5: 'w', 0x1F6E9: 'x', 0x1F6F0: 'x', 0x1F6F3: 'w',
}

narrow, outdir = sys.argv[1:3]
n = 0
for cp, colour in FORMS.items():
	out = os.path.join(outdir, '%04X-FE0F' % cp)
	if os.path.exists(out):
		continue
	glyph = glyphlib.read(narrow, glyphlib.find(narrow, cp))
	if isinstance(colour, tuple):  # white on a 9x7 tile in columns 1-9
		colour = colour[1]
		rows = ['.' + ''.join('w' if c == 'x' else colour for c in ('..' + r + '.')[:9]) + '..' for r in glyph]
	else:
		rows = ['...' + r.replace('x', colour) + '...' for r in glyph]
	open(out, 'w').write('\n'.join(rows) + '\n')
	n += 1
print('emojiforms.py: %d forms' % n, file=sys.stderr)
