# Shared helpers for the glyph tools: name <-> codepoint mapping and glyph loading.
# A glyph file is named after its HTML entity (fnt/src/entities.csv) or U+XXXX[X],
# and holds H rows of W 'x'/'.' cells, W and H coming from its directory (e.g. 6x7).
import os

FNT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fnt')

names = {}   # codepoint -> every entity name it has
codes = {}   # entity name -> codepoint
for line in open(os.path.join(FNT, 'src', 'entities.csv')):
	name, code = line.strip().split(',')
	names.setdefault(int(code, 16), []).append(name)
	codes.setdefault(name, int(code, 16))


def size(d):
	"""(W, H) of a glyph directory such as fnt/code7/6x7."""
	w, h = os.path.basename(os.path.normpath(d)).split('x')
	return int(w), int(h)


def codepoint(name):
	return int(name[2:], 16) if name.startswith('U+') else codes.get(name)


def files(d):
	"""Glyph file names in d (skipping Settings and unknown names), in codepoint order."""
	return sorted((n for n in os.listdir(d) if n != 'Settings' and codepoint(n) is not None), key=codepoint)


def read(d, name):
	"""A glyph as a tuple of H rows, each padded or cut to W cells."""
	w, h = size(d)
	rows = [r.ljust(w, '.')[:w] for r in open(os.path.join(d, name)).read().split('\n')[:h]]
	return tuple(rows + ['.' * w] * (h - len(rows)))


def find(d, cp):
	"""The file in d that holds codepoint cp, or None."""
	for name in names.get(cp, []) + ['U+%05X' % cp, 'U+%04X' % cp]:
		if os.path.exists(os.path.join(d, name)):
			return name
	return None
