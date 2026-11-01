#!/usr/bin/env python3
# genders.py COLORDIR OUTDIR: add ligature sources for gendered sequences to OUTDIR (for flags.py,
# cbdt.py and then skintones.py). For each base below, BASE-200D-2642-FE0F (🏃‍♂️) and
# BASE-200D-2640-FE0F (🏃‍♀️) are the base's colour drawing with its clothes recoloured: blue for ♂
# and red for ♀, as in 👨 and 👩. The drawing comes from COLORDIR (U+BASE), or for a text-style
# base from OUTDIR (BASE-FE0F, whose sequences keep that FE0F: 26F9-FE0F-200D-2640-FE0F).
# Generated at build time, not stored in fnt/.
import os, sys

MALE, FEMALE = '2642', '2640'
ALL = range(7)
# base: (clothing letter, rows it is recoloured in), or a dict of {gender: rows} for a drawing
# that doesn't follow the rule; None leaves the base unchanged for that gender
SPEC = {
	0x1F3C3: ('b', ALL),         # 🏃 runner
	0x1F3C4: ('b', range(4)),    # 🏄 surfer, not the sea
	0x1F3CA: None,               # 🏊 swimmer: see CAPS
	0x26F9: ('b', ALL),          # ⛹ ball
	0x1F3CB: ('b', ALL),         # 🏋 weights
	0x1F3CC: ('b', ALL),         # 🏌 golf
	0x1F46E: ('b', ALL),         # 👮 police
	0x1F46F: ('p', ALL),         # 👯 bunny ears
	0x1F471: ('b', [5]),         # 👱 blond
	0x1F473: ('b', [5]),         # 👳 turban
	0x1F477: ('o', [5]),         # 👷 construction
	0x1F481: ('g', ALL),         # 💁
	0x1F482: ('r', [5]),         # 💂 guard's coat, not the chin strap
	0x1F486: ('g', ALL),         # 💆
	0x1F487: ('g', ALL),         # 💇
	0x1F575: ('n', [4, 5]),      # 🕵 detective's coat
	0x1F645: ('g', ALL),         # 🙅
	0x1F646: ('g', ALL),         # 🙆
	0x1F647: ('g', ALL),         # 🙇
	0x1F64B: ('g', ALL),         # 🙋
	0x1F64D: ('g', ALL),         # 🙍
	0x1F64E: ('g', ALL),         # 🙎
	0x1F6A3: ('b', [1, 2]),      # 🚣 rower, not the water
	0x1F6B4: ('b', ALL),         # 🚴
	0x1F6B5: ('b', ALL),         # 🚵
	0x1F6B6: ('b', ALL),         # 🚶
	0x1F926: ('g', ALL),         # 🤦
	0x1F935: ('k', [5]),         # 🤵 tuxedo (KEEP)
	0x1F470: ('w', [5]),         # 👰 veil: the dress (KEEP)
	0x1F937: ('g', ALL),         # 🤷
	0x1F938: ('b', ALL),         # 🤸
	0x1F939: ('b', range(2, 7)), # 🤹 juggler, not the balls
	0x1F93C: None,               # 🤼 wrestlers: see PAIRS
	0x1F93D: ('b', [2]),         # 🤽 water polo, not the water
	0x1F93E: ('b', ALL),         # 🤾 handball
	0x1F9B8: ('b', [5]),         # 🦸 superhero's suit
	0x1F9B9: ('k', [5]),         # 🦹 supervillain's suit, not the mask
	0x1F9CD: ('b', ALL),         # 🧍
	0x1F9CE: ('b', ALL),         # 🧎
	0x1F9CF: ('g', ALL),         # 🧏
	0x1F9D4: None,               # 🧔 beard: see SHIRTS
	0x1F9D6: ('g', ALL),         # 🧖 sauna
	0x1F9D7: ('b', ALL),         # 🧗 climber
	0x1F9D8: ('b', ALL),         # 🧘
	0x1F9D9: ('v', ALL),         # 🧙 mage
	0x1F9DA: ('g', ALL),         # 🧚 fairy
	0x1F9DB: ('k', [5]),         # 🧛 vampire's cape
	0x1F9DC: ('g', ALL),         # 🧜 merperson
	0x1F9DD: ('g', ALL),         # 🧝 elf
	0x1F9DE: ('b', ALL),         # 🧞 genie
	0x1F9DF: ('n', [5]),         # 🧟 zombie's clothes, not its skin
}
COLOUR = {MALE: 'b', FEMALE: 'r'}
CAPS = {0x1F3CA: (0, [6, 7])}                # 🏊: a swim cap above the head (row, columns)
PAIRS = {0x1F93C: {MALE: {'r': 'c'}, FEMALE: {'b': 'p'}}}  # 🤼: two blues, or two reds
KEEP = {0x1F935: MALE, 0x1F470: FEMALE}  # 🤵‍♂️ and 👰‍♀️ are drawn like the base
SHIRTS = {0x1F9D4: (6, range(2, 9))}         # 🧔: the beard has no clothes; add a shirt (row, columns)

colordir, outdir = sys.argv[1:3]
n = 0
for base, spec in SPEC.items():
	path, prefix = os.path.join(colordir, 'U+%05X' % base), '%04X' % base
	if not os.path.exists(path):
		path, prefix = os.path.join(outdir, '%04X-FE0F' % base), '%04X-FE0F' % base
	rows = [list(r) for r in open(path).read().split()]
	for g, c in COLOUR.items():
		out = [r[:] for r in rows]
		if spec and KEEP.get(base) != g:
			letter, rs = spec
			for y in rs:
				out[y] = [c if ch == letter else ch for ch in out[y]]
		if base in CAPS:
			y, xs = CAPS[base]
			for x in xs:
				out[y][x] = c
		if base in PAIRS:
			out = [[PAIRS[base][g].get(ch, ch) for ch in r] for r in out]
		if base in SHIRTS:
			y, xs = SHIRTS[base]
			for x in xs:
				out[y][x] = c
		open(os.path.join(outdir, '%s-200D-%s-FE0F' % (prefix, g)), 'w').write('\n'.join(''.join(r) for r in out) + '\n')
		n += 1
print('genders.py: %d sequences' % n, file=sys.stderr)
