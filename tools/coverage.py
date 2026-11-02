#!/usr/bin/env python3
# coverage.py [UNICODEDIR]: check the font sources against Unicode's emoji lists (emoji-sequences.txt
# and emoji-zwj-sequences.txt, from https://unicode.org/Public/emoji/latest/; a copy is kept in
# tools/unicode). It builds the ligature sources the way ttf.sh does (fnt/code7w-flags plus
# genders.py, directions.py, emojiforms.py and skintones.py, in a temporary directory) and reports:
#   - an emoji with no code7w glyph (fnt/code7w/12x7);
#   - a text-style emoji (listed with FE0F) missing from any of the 6x7 fonts, or with no colour
#     emoji form (a CP-FE0F source, or a code7w glyph);
#   - a keycap, flag, skin-tone or ZWJ sequence with no ligature source;
#   - a ligature source with no ink.
# flags.py turns each source into one ligature, so this matches what the build produces.
# Exits 1 if anything is missing.
import collections, os, shutil, subprocess, sys, tempfile
import glyphlib

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
FNT = os.path.join(REPO, 'fnt')
unicode_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TOOLS, 'unicode')


def inked(d):
	"""Codepoints in glyph dir d that have at least one pixel set."""
	return {glyphlib.codepoint(n) for n in glyphlib.files(d) if any(c != '.' for r in glyphlib.read(d, n) for c in r)}


def source_name(cps):
	"""The ligature source name flags.py expects: a country code for a regional-indicator pair, else hex."""
	if len(cps) == 2 and all(0x1F1E6 <= c <= 0x1F1FF for c in cps):
		return ''.join(chr(c - 0x1F1E6 + ord('A')) for c in cps)
	return '-'.join('%04X' % c for c in cps)


wide = inked(os.path.join(FNT, 'code7w/12x7'))
narrow = [inked(os.path.join(FNT, f, '6x7')) for f in ('code7', 'code7sc', 'code7it')]
tmp = tempfile.mkdtemp()
try:
	seq = os.path.join(tmp, 'seq')
	shutil.copytree(os.path.join(FNT, 'code7w-flags/12x7'), seq)
	for script, src in (('genders.py', 'code7w-color/12x7'), ('directions.py', 'code7w-color/12x7'),
			('emojiforms.py', 'code7/6x7'), ('skintones.py', 'code7w-color/12x7')):
		subprocess.run([sys.executable, os.path.join(REPO, script), os.path.join(FNT, src), seq],
			check=True, stderr=subprocess.DEVNULL)
	sources = {}
	for n in os.listdir(seq):
		sources[n] = any(c not in '.\n' for c in open(os.path.join(seq, n)).read())
finally:
	shutil.rmtree(tmp)

missing = collections.defaultdict(list)
total = collections.Counter()
for fn in ('emoji-sequences.txt', 'emoji-zwj-sequences.txt'):
	for line in open(os.path.join(unicode_dir, fn), encoding='utf-8'):
		line = line.split('#')[0].strip()
		if not line:
			continue
		cps, kind = [f.strip() for f in line.split(';')[:2]]
		if '..' in cps:
			a, b = cps.split('..')
			seqs = [[c] for c in range(int(a, 16), int(b, 16) + 1)]
		else:
			seqs = [[int(c, 16) for c in cps.split()]]
		for s in seqs:
			text = ''.join(map(chr, s))
			if kind == 'Basic_Emoji' and len(s) == 1:
				total['emoji'] += 1
				if s[0] not in wide:
					missing['emoji with no code7w glyph'].append(text)
			elif kind == 'Basic_Emoji':
				total['text-style emoji'] += 1
				cp = s[0]
				if cp not in wide and not all(cp in n for n in narrow):
					missing['text-style emoji missing from a 6x7 font'].append(text)
				if cp not in wide and source_name(s) not in sources:
					missing['text-style emoji with no colour form'].append(text)
			else:
				total['sequence'] += 1
				if source_name(s) not in sources:
					missing['sequence with no ligature source'].append(text)
for n, ink in sorted(sources.items()):
	if not ink:
		missing['ligature source with no ink'].append(n)

print('coverage.py: %s' % ', '.join('%d %s' % (v, k) for k, v in total.items()))
for k, v in missing.items():
	print('%s (%d): %s' % (k, len(v), ' '.join(v[:60]) + (' ...' if len(v) > 60 else '')))
sys.exit(1 if missing else 0)
