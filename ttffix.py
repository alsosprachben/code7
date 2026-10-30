#!/usr/bin/env python3
# ttffix.py FONT TTF: fix the names bdf2ttf gives a TTF so fontconfig can tell the fonts apart.
# code7it is marked italic (bdf2ttf leaves it as a second "code7 medium"), and code7w gets a
# family of its own so xterm's faceNameDoublesize can select it. Other fonts are left alone.
import os, sys
import fontforge

font, path = sys.argv[1:3]
if font not in ('code7it', 'code7w'):
	sys.exit(0)

f = fontforge.open(path)
if font == 'code7it':
	f.fontname = 'code7-MediumItalic'
	f.fullname = 'code7 Medium Italic'
	f.italicangle = -10.0
	f.os2_stylemap = (f.os2_stylemap & ~0x40) | 0x01   # fsSelection: ITALIC, not REGULAR
	f.macstyle |= 0x02
	f.sfnt_names = tuple(n for n in f.sfnt_names if n[1] != 'SubFamily') + (('English (US)', 'SubFamily', 'Medium Italic'),)
else:
	f.familyname = 'code7w'
	f.fontname = 'code7w-Medium'
	f.fullname = 'code7w Medium'
	f.sfnt_names = tuple(n for n in f.sfnt_names if n[1] not in ('Family', 'Preferred Family')) + (('English (US)', 'Family', 'code7w'),)
f.generate(path + '.tmp.ttf')
os.replace(path + '.tmp.ttf', path)
