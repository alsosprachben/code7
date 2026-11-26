# assemble9.py DIR: code7t's glyphs (DIR = fnt/code7t/6x9) from auto9.json (autoall.py's draft) and the
# hand-drawn letters, marks and half forms below. Run once to draft; the glyph files are the source after that.
import json, os, sys
g = json.load(open('auto9.json'))
E = '......'
def body(*b, top=(E, E), bot=(E, E)):
    assert len(b) == 5 and all(len(x) == 6 for x in b), b
    return [top[0], top[1], *b, bot[0], bot[1]]
H = 'xxxxxx'; HG = 'xx.xxx'
out = {}
# ---------------- DEVANAGARI
auto = lambda cp: g['%04X' % cp]
for cp in list(range(0x904, 0x915)) + [0x93D, 0x950, 0x960, 0x961, 0x964, 0x965] + list(range(0x966, 0x970)):
    out[cp] = auto(cp)
D = {
 0x915: body('..x...', '.xxxx.', 'x.x.x.', '.xxx..', '..x...', top=(E, H)),
 0x916: body('x...x.', 'x.x.x.', '.xx.x.', 'x.x.x.', '.x..x.', top=(E, HG)),
 0x917: body('.x..x.', '.x..x.', '.x..x.', '....x.', '....x.', top=(E, H)),
 0x918: body('x...x.', 'xxxxx.', 'x...x.', '.xxxx.', '....x.', top=(E, H)),
 0x919: body('..xx..', '.x..x.', '.xxx..', 'x...x.', '.xxx..', top=(E, H)),
 0x91A: body('....x.', 'xxx.x.', '.x..x.', '.xxxx.', '....x.', top=(E, H)),
 0x91B: body('xx.xx.', 'x.x.x.', 'xx.xx.', 'x...x.', 'xxxx..', top=(E, H)),
 0x91C: body('....x.', '..xxx.', 'x.x.x.', 'xxx.x.', '....x.', top=(E, H)),
 0x91D: body('xxx.x.', 'x...x.', 'xxxxx.', '..x.x.', 'xxx.x.', top=(E, H)),
 0x91E: body('....x.', '.xxxx.', 'x..xx.', 'xxx.x.', '....x.', top=(E, H)),
 0x91F: body('...x..', '.xxx..', 'x.....', 'xx....', '.xxxx.', top=(E, H)),
 0x920: body('..x...', '.xxx..', 'x...x.', 'x...x.', '.xxx..', top=(E, H)),
 0x921: body('..xx..', '.x....', '.xxx..', 'x...x.', '.xxx..', top=(E, H)),
 0x922: body('...x..', 'xxxx..', 'x.xx..', 'x.x.x.', '.xxx..', top=(E, H)),
 0x923: body('x.x.x.', 'x.x.x.', 'x.x.x.', 'xx..x.', '....x.', top=(E, H)),
 0x924: body('....x.', '..xxx.', '.x..x.', '.x..x.', '..x.x.', top=(E, H)),
 0x925: body('xxxxx.', 'xx..x.', 'x...x.', '.xxxx.', '....x.', top=(E, HG)),
 0x926: body('..xx..', 'xxxx..', 'x..x..', '.xxxx.', '...x..', top=(E, H)),
 0x927: body('.xx.x.', '.xx.x.', '.x..x.', '.xxxx.', '....x.', top=(E, HG)),
 0x928: body('....x.', '.xxxx.', '.xx.x.', '....x.', '....x.', top=(E, H)),
 0x92A: body('.x..x.', '.x..x.', '.xx.x.', '..xxx.', '....x.', top=(E, H)),
 0x92B: body('x..x..', 'x..xx.', 'xx.x.x', '.xxx..', '...x..', top=(E, H)),
 0x92C: body('..xxx.', '.xxxx.', '.x..x.', '..xxx.', '....x.', top=(E, H)),
 0x92D: body('xx..x.', '.x..x.', 'xxxxx.', '.x..x.', '....x.', top=(E, HG)),
 0x92E: body('.x..x.', '.x..x.', 'xxxxx.', '....x.', '....x.', top=(E, H)),
 0x92F: body('.x..x.', 'xx..x.', 'x...x.', '.xxxx.', '....x.', top=(E, H)),
 0x930: body('...x..', '.xxx..', '.xx...', '..x...', '...x..', top=(E, H)),
 0x932: body('....x.', 'xxxxx.', 'x.x.x.', 'x...x.', 'xx..x.', top=(E, H)),
 0x933: body('...xx.', 'xxxxx.', '..x.x.', '.xx.x.', 'xx..x.', top=(E, H)),
 0x935: body('..xxx.', '.xx.x.', '.x..x.', '..xxx.', '....x.', top=(E, H)),
 0x936: body('x.x.x.', '.xx.x.', 'xx..x.', 'xx..x.', '.x..x.', top=(E, H)),
 0x937: body('xx..x.', 'x.xxx.', 'xx..x.', '.xxxx.', '....x.', top=(E, H)),
 0x938: body('.x..x.', 'xx..x.', 'xxxxx.', 'xx..x.', '.x..x.', top=(E, H)),
 0x939: body('.xxx..', 'xx....', '.xxx..', 'xx.xx.', 'xx.x..', top=(E, H), bot=('.xx...', E)),
}
out.update(D)
def nukta(base):
    r = list(out[base]); r[7] = '..x...'; return r
for cp, base in ((0x929, 0x928), (0x931, 0x930), (0x934, 0x933), (0x958, 0x915), (0x959, 0x916), (0x95A, 0x917),
                 (0x95B, 0x91C), (0x95C, 0x921), (0x95D, 0x922), (0x95E, 0x92B), (0x95F, 0x92F)):
    out[cp] = nukta(base)
# (the vowel signs that take a cell: a stem under the headline, a hook above)
stem = lambda c: ['.' * (c - 1) + 'x' + '.' * (6 - c)] * 5
out[0x93E] = [E, H] + stem(2) + [E, E]                                   # ा
out[0x93F] = ['.xxxx.', H] + stem(2) + [E, E]                            # ि
out[0x940] = ['xxx...', H] + stem(3) + [E, E]                            # ी
out[0x949] = ['x.x...', H] + stem(2) + [E, E]                            # ॉ
out[0x94A] = ['x.x.x.', H] + stem(2) + [E, E]                            # ॊ
out[0x94B] = ['xx....', H] + stem(2) + [E, E]                            # ो
out[0x94C] = ['xx.xx.', H] + stem(2) + [E, E]                            # ौ
out[0x93B] = ['.x....', H] + stem(2) + [E, E]                            # ऻ
out[0x94E] = ['x.....', H] + stem(2) + [E, E]                            # ॎ
out[0x94F] = ['.xx.x.', H] + stem(2) + [E, E]                            # ॏ
out[0x903] = [E, E, E, '.x....', E, '.x....', E, E, E]                   # ः
out[0x970] = [E, E, '..x...', '.x.x..', '..x...', E, E, E, E]            # ॰
# (marks: over or under the letter before, in its cell)
M = lambda top=(E, E), bot=(E, E): [top[0], top[1], E, E, E, E, E, bot[0], bot[1]]
out.update({
 0x900: M(('xxx...', E)), 0x901: M(('x.x.x.', E)), 0x902: M(('....x.', E)), 0x93A: M(('..x...', E)),
 0x93C: M(bot=('...x..', E)), 0x941: M(bot=('..xx..', '...x..')), 0x942: M(bot=('...xx.', '..x...')),
 0x943: M(bot=('..x...', '...xx.')), 0x944: M(bot=('..x.x.', '.xxx..')), 0x945: M(('x.x...', E)),
 0x946: M(('x...x.', E)), 0x947: M(('.xx...', E)), 0x948: M(('xx.xx.', E)), 0x94D: M(bot=('....x.', '...x..')),
 0x951: M(('...x..', '...x..')), 0x952: M(bot=('.xxx..', E)), 0x953: M(('.x....', E)), 0x954: M(('....xx', E)),
 0x955: M(('xx..xx', E)), 0x956: M(bot=('..x...', '..x...')), 0x957: M(bot=('..x.x.', '..x.x.')),
 0x962: M(bot=('.x.x..', '..xx..')), 0x963: M(bot=('x.x.x.', '.xxx..')),
 0xE980: M(('...xx.', E)), 0xE981: M(bot=('...x..', '..x...')),
})
# (the independent vowels told apart by their marks: from ए and आ, each with its own)
def topmark(base, m):
    r = list(out[base]); r[0] = m; return r
out[0x910] = topmark(0x90F, '.xx...')        # ऐ
out[0x90E] = topmark(0x90F, 'x.x...')        # ऎ
out[0x90D] = topmark(0x90F, 'x...x.')        # ऍ
out[0x913] = topmark(0x906, 'xx....')        # ओ
out[0x914] = topmark(0x906, 'xx.xx.')        # औ
out[0x911] = topmark(0x906, 'x.x...')        # ऑ
out[0x912] = topmark(0x906, 'x.x.x.')        # ऒ
# ligatures, drafted from the font's own conjuncts
for i in range(4):
    out[0xE9A0 + i] = g['LIG%d' % i]
# HALF FORMS (U+E900 + offset): the consonant without its stem, its body joined on to the next letter
NOHALF = {0x919, 0x91B, 0x91F, 0x920, 0x921, 0x922, 0x926, 0x939, 0x930}
for cp in list(range(0x915, 0x93A)) + list(range(0x958, 0x960)):
    if cp in NOHALF or cp not in out or cp in (0x929, 0x931, 0x934):
        continue
    r = [list(x) for x in out[cp]]
    s = 4                                     # (the stem: column 5)
    if sum(r[k][s] == 'x' for k in range(2, 7)) < 4:
        continue
    att = [k for k in range(2, 7) if r[k][s - 1] == 'x']
    for k in range(2, 9):
        r[k][s] = '.'
    for k in (att[:1] or [4]):
        r[k][s] = 'x'; r[k][5] = 'x'
    out[0xE900 + cp - 0x900] = [''.join(x) for x in r]
# (half forms drawn by hand where the stem is not the right column: क keeps its stem and loses its hook; फ)
out[0xE915] = body('..x...', '.xxx..', 'x.xxxx', '.xxx..', '..x...', top=(E, H))
out[0xE92B] = body('x.....', 'x.....', 'xxxxxx', '.xx...', E, top=(E, H))
# (and the nukta letters' halves: the base's half and its dot)
for cp, base in ((0x929, 0x928), (0x934, 0x933), (0x958, 0x915), (0x959, 0x916), (0x95A, 0x917), (0x95B, 0x91C),
                 (0x95E, 0x92B), (0x95F, 0x92F)):
    r = list(out[0xE900 + base - 0x900]); r[7] = '..x...'
    out[0xE900 + cp - 0x900] = r
# ---------------- THAI
for cp in list(range(0xE01, 0xE31)) + [0xE32, 0xE33, 0xE3F] + list(range(0xE40, 0xE47)) + list(range(0xE4F, 0xE5C)):
    out[cp] = g['%04X' % cp]
T = {
 0xE01: body('xxxx..', '.x..x.', '.x..x.', '.x..x.', '.x..x.'),
 0xE02: body('x...x.', 'xx..x.', '.x..x.', '.x..x.', '.xxxx.'),
 0xE04: body('.xxx..', 'x...x.', 'xx..x.', 'xx..x.', 'x...x.'),
 0xE05: body('.x.x..', 'x.x.x.', 'xx..x.', 'xx..x.', 'x...x.'),
 0xE07: body('....x.', '....x.', 'xx..x.', 'xx.x..', '.xx...'),
 0xE14: body('.xxx..', 'x...x.', 'x...x.', 'x.x.x.', 'xx..x.'),
 0xE15: body('.x.x..', 'x.x.x.', 'x...x.', 'x.x.x.', 'xx..x.'),
 0xE16: body('.xxx..', 'x...x.', 'x...x.', 'xx..x.', 'xx..x.'),
 0xE17: body('xx.x..', 'xx..x.', '.x..x.', '.x..x.', '.x..x.'),
 0xE25: body('.xxx..', 'x...x.', '.x..x.', 'xx..x.', 'x...x.'),
 0xE28: body('.xxx..', 'x...x.', 'xx..x.', 'xx..x.', 'x...x.', top=(E, '....x.')),
 0xE2A: body('.xxx..', 'x...x.', '.x..x.', 'xx..x.', 'x...x.', top=(E, '....x.')),
 0xE2D: body('.xxx..', 'x...x.', 'xx..x.', 'x...x.', '.xxx..'),
 0xE2E: body('.xxx..', 'x...x.', 'xx..x.', 'x...x.', '.xxx..', top=(E, '...xx.')),
 0xE1C: body('xx..x.', 'xx..x.', '.x..x.', '.x.xx.', '.xx.x.'),
 0xE1D: body('xx..x.', 'xx..x.', '.x..x.', '.x.xx.', '.xx.x.', top=('....x.', '....x.')),
 0xE1E: body('xx..x.', 'xxx.x.', '.xx.x.', '.xx.x.', '.x.xx.'),
 0xE1F: body('xx..x.', 'xxx.x.', '.xx.x.', '.xx.x.', '.x.xx.', top=('....x.', '....x.')),
}
out.update(T)
out[0xE24] = out[0xE16][:7] + ['....x.', '....x.']           # ฤ: ถ's body, its tail down
out[0xE26] = out[0xE25][:7] + ['....x.', '....x.']           # ฦ: ล's
out.update({
 0xE31: M(('.x....', 'x.xxx.')), 0xE34: M((E, '.xxxx.')), 0xE35: M(('....x.', '.xxxx.')), 0xE36: M(('...xx.', '.xxxx.')),
 0xE37: M(('..x.x.', '.xxxx.')), 0xE38: M(bot=('...x..', '...xx.')), 0xE39: M(bot=('..x.x.', '..xxx.')),
 0xE3A: M(bot=('....x.', E)), 0xE47: M(('..xx..', '..xx..')), 0xE48: M(('...x..', E)), 0xE49: M(('..xx..', E)),
 0xE4A: M(('.x.x..', E)), 0xE4B: M(('.xxx..', E)), 0xE4C: M(('.x.x..', '..x...')), 0xE4D: M((E, '...x..')),
 0xE4E: M(('..x...', '...x..')),
})
dst = sys.argv[1]
os.makedirs(dst, exist_ok=True)
for cp, rows in out.items():
    assert len(rows) == 9 and all(len(x) == 6 for x in rows), (hex(cp), rows)
    open(os.path.join(dst, 'U+%04X' % cp), 'w').write('\n'.join(rows) + '\n')
print(len(out), 'glyphs')
