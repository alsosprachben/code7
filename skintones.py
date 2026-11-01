#!/usr/bin/env python3
# skintones.py COLORDIR OUTDIR: add ligature sources for skin-tone sequences to OUTDIR,
# for flags.py and cbdt.py. For each emoji modifier base with a colour glyph in COLORDIR,
# and each modifier U+1F3FB-1F3FF, the base's drawing is copied with its skin (palette 'y')
# recoloured to the modifier's tone and saved as BASE-MODIFIER (e.g. 1F44D-1F3FD), so a
# shaping terminal draws 👍🏽 in that tone. Generated at build time, not stored in fnt/.
import os, sys

# Emoji_Modifier_Base, Unicode 15.0 (emoji-data.txt)
BASES = [0x261D, 0x26F9] + list(range(0x270A, 0x270E)) + [0x1F385, 0x1F3C2, 0x1F3C3, 0x1F3C4, 0x1F3C7, 0x1F3CA, 0x1F3CB, 0x1F3CC,
	0x1F442, 0x1F443] + list(range(0x1F446, 0x1F451)) + list(range(0x1F466, 0x1F479)) + [0x1F47C, 0x1F481, 0x1F482, 0x1F483,
	0x1F485, 0x1F486, 0x1F487, 0x1F48F, 0x1F491, 0x1F4AA, 0x1F574, 0x1F575, 0x1F57A, 0x1F590, 0x1F595, 0x1F596, 0x1F645, 0x1F646,
	0x1F647] + list(range(0x1F64B, 0x1F650)) + [0x1F6A3, 0x1F6B4, 0x1F6B5, 0x1F6B6, 0x1F6C0, 0x1F6CC, 0x1F90C, 0x1F90F] \
	+ list(range(0x1F918, 0x1F920)) + [0x1F926] + list(range(0x1F930, 0x1F93A)) + [0x1F93C, 0x1F93D, 0x1F93E, 0x1F977, 0x1F9B5,
	0x1F9B6, 0x1F9B8, 0x1F9B9, 0x1F9BB, 0x1F9CD, 0x1F9CE, 0x1F9CF] + list(range(0x1F9D1, 0x1F9DE)) + [0x1FAC3, 0x1FAC4, 0x1FAC5] \
	+ list(range(0x1FAF0, 0x1FAF9))
TONES = dict(zip(range(0x1F3FB, 0x1F400), 'aeijl'))  # palette letters in cbdt.py, light to dark

colordir, outdir = sys.argv[1:3]
os.makedirs(outdir, exist_ok=True)
n = 0
for base in BASES:
	path = os.path.join(colordir, 'U+%05X' % base)
	if not os.path.exists(path):
		continue
	rows = open(path).read().split()  # a base with no yellow skin (💅, 🧛) is copied unchanged, so it still draws
	for mod, tone in TONES.items():
		open(os.path.join(outdir, '%04X-%04X' % (base, mod)), 'w').write('\n'.join(r.replace('y', tone) for r in rows) + '\n')
		n += 1
print('skintones.py: %d sequences' % n, file=sys.stderr)
