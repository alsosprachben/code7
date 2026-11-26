#!/usr/bin/env python3
# arabic.py [--force] [--sheet PNG]: drafts code7's Arabic from skeletons and dots, into fnt/code7{,sc,it}/6x7.
#
# Arabic letters are a few skeletons told apart by their dots (ب ت ث ن ي پ one tooth; ج ح خ چ one bowl), each
# in up to four joining forms. This writes every letter's forms (the presentation forms, U+FB50.. and U+FE70..,
# which a shaping program -- the Clavitone app's nui/shape.h, mlterm -- puts in the text), the base letters as
# their isolated forms, the harakat as marks, the digits and the punctuation.
#
# The cursive exception to "column 6 blank": a form that joins the letter after it (initial, medial) has ink in
# column 1 of row 6, the baseline; one that joins the letter before it (final, medial) in column 6. Read right to
# left, the letters' baselines meet across the cells. Isolated and initial forms keep column 6 blank.
#
# Existing files are left alone (they may have been redrawn by hand) unless --force. --sheet draws every form and
# some words beside a reference font, to check by eye (needs Pillow).
import os, sys

TOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = [os.path.join(TOP, 'fnt', f, '6x7') for f in ('code7', 'code7sc', 'code7it')]
E = '......'

def G(*rows):
    rows = list(rows)
    assert len(rows) == 7 and all(len(r) == 6 for r in rows), rows
    return rows

# ---- THE SKELETONS: forms I (isolated), F (final), N (initial), M (medial); and per form where the dots go:
#      (row, col) of the middle dot above and below, 1-based
S = {}
A = {}   # (anchors: skeleton -> form -> (above, below))
def sk(name, forms, anchors):
    S[name], A[name] = forms, anchors

sk('alef', {
    'I': G('...x..', '..x...', '..x...', '..x...', '..x...', '..x...', E),
    'F': G('.....x', '....x.', '....x.', '....x.', '....x.', '....xx', E)},
   {'I': ((1, 3), (7, 3)), 'F': ((1, 5), (7, 5))})
sk('beh', {
    'I': G(E, E, E, E, 'x...x.', 'xxxxx.', E),
    'F': G(E, E, E, E, 'x.....', 'xxxxxx', E),
    'N': G(E, E, E, E, '...x..', 'xxxx..', E),
    'M': G(E, E, E, E, '...x..', 'xxxxxx', E)},
   {'I': ((3, 3), (7, 3)), 'F': ((3, 3), (7, 3)), 'N': ((3, 4), (7, 4)), 'M': ((3, 4), (7, 4))})
sk('noon', {
    'I': G(E, E, E, 'x...x.', 'x...x.', '.xxx..', E),
    'F': G(E, E, E, 'x.....', 'x...x.', '.xxxxx', E)},
   {'I': ((2, 3), (7, 3)), 'F': ((2, 3), (7, 3))})
sk('yeh', {   # (alef maksura's and yeh's isolated and final: the returning tail)
    'I': G(E, E, E, '...xx.', 'x..x..', '.xx...', E),
    'F': G(E, E, E, E, 'x...xx', '.xxx..', E)},
   {'I': ((2, 4), (7, 2)), 'F': ((3, 3), (7, 3))})
sk('hah', {
    'I': G(E, E, 'xxxx..', '..x...', '.x....', 'x.....', '.xxxx.'),
    'F': G(E, E, E, 'xxx...', '..x...', '.x.xxx', 'x.xx..'),
    'N': G(E, E, E, 'xxx...', '..x...', 'xxx...', E),
    'M': G(E, E, E, 'xxx...', '..x...', 'xxxxxx', E)},
   {'I': ((1, 2), (5, 4)), 'F': ((2, 2), (5, 5)), 'N': ((2, 2), (7, 2)), 'M': ((2, 2), (7, 3))})
sk('dal', {
    'I': G(E, E, E, '..x...', '...x..', 'xxxx..', E),
    'F': G(E, E, E, '..x...', '...x..', 'xxxxxx', E)},
   {'I': ((2, 3), (7, 3)), 'F': ((2, 3), (7, 3))})
sk('reh', {
    'I': G(E, E, E, '....x.', '....x.', '...x..', 'xxx...'),
    'F': G(E, E, E, E, '....x.', '....xx', '..xx..')},
   {'I': ((2, 5), (7, 5)), 'F': ((3, 5), (7, 5))})
sk('seen', {
    'I': G(E, E, E, E, '..x.x.', 'x.xxx.', '.x....'),
    'F': G(E, E, E, E, '..x.x.', 'x.xxxx', '.x....'),
    'N': G(E, E, E, E, 'x.x.x.', 'xxxxx.', E),
    'M': G(E, E, E, E, 'x.x.x.', 'xxxxxx', E)},
   {'I': ((3, 4), (7, 4)), 'F': ((3, 4), (7, 4)), 'N': ((3, 3), (7, 3)), 'M': ((3, 3), (7, 3))})
sk('sad', {
    'I': G(E, E, E, '..xxx.', 'x.x..x', '.xxxx.', E)[:4] + ['x.x.x.', '.xxxx.', E],
    'F': G(E, E, E, '..xxx.', 'x.x.x.', '.xxxxx', E),
    'N': G(E, E, E, '..xxx.', '.x..x.', 'xxxxx.', E),
    'M': G(E, E, E, '..xxx.', '.x..x.', 'xxxxxx', E)},
   {'I': ((2, 4), (7, 4)), 'F': ((2, 4), (7, 4)), 'N': ((2, 4), (7, 4)), 'M': ((2, 4), (7, 4))})
sk('tah', {
    # (the base runs on left of the upright in every form, as Naskh's does: isolated as initial, final as medial)
    'I': G('..x...', '..x...', '..x...', '..xxx.', '.x..x.', 'xxxxx.', E),
    'F': G('..x...', '..x...', '..x...', '..xxx.', '.x..x.', 'xxxxxx', E),
    'N': G('..x...', '..x...', '..x...', '..xxx.', '.x..x.', 'xxxxx.', E),
    'M': G('..x...', '..x...', '..x...', '..xxx.', '.x..x.', 'xxxxxx', E)},
   {f: ((2, 5), (7, 4)) for f in 'IFNM'})
sk('ain', {
    'I': G(E, '.xx...', 'x.....', '.xxx..', 'x.....', 'x.....', '.xxx..'),
    'F': G(E, E, E, '.x.x..', '..x...', '.x.xxx', 'x.....'),
    'N': G(E, E, '.xxx..', 'x.....', '.xx...', 'xxxxx.', E),
    'M': G(E, E, E, '.xxx..', '.x.x..', 'xxxxxx', E)},
   {'I': ((1, 2), (7, 3)), 'F': ((2, 3), (7, 3)), 'N': ((1, 3), (7, 3)), 'M': ((2, 3), (7, 3))})
sk('feh', {
    'I': G(E, E, E, '...xx.', 'x..xx.', '.xxxx.', E),
    'F': G(E, E, E, '...xx.', 'x..xx.', '.xxxxx', E),
    'N': G(E, E, E, '..xxx.', '..x.x.', 'xxxxx.', E),
    'M': G(E, E, E, '..xxx.', '..x.x.', 'xxxxxx', E)},
   {'I': ((2, 4), (7, 3)), 'F': ((2, 4), (7, 3)), 'N': ((2, 4), (7, 4)), 'M': ((2, 4), (7, 4))})
sk('qaf', {
    'I': G(E, E, E, '...xx.', '...xx.', 'x...x.', '.xxx..'),
    'F': G(E, E, E, '...xx.', '...xx.', 'x...xx', '.xxx..')},
   {'I': ((2, 4), (7, 3)), 'F': ((2, 4), (7, 3))})
sk('kaf', {
    'I': G('....x.', '....x.', '..x.x.', '.x..x.', '..x.x.', 'xxxxx.', E),
    'F': G('....x.', '....x.', '..x.x.', '.x..x.', '..x.x.', 'xxxxxx', E),
    'N': G(E, '.xxxx.', '....x.', '...x..', '....x.', 'xxxxx.', E),
    'M': G(E, '.xxxx.', '....x.', '...x..', '....x.', 'xxxxxx', E)},
   {f: ((1, 2), (7, 3)) for f in 'IFNM'})
sk('keheh', {
    'I': G('..xxx.', '....x.', '....x.', '....x.', 'x...x.', 'xxxxx.', E),
    'F': G('..xxx.', '....x.', '....x.', '....x.', 'x...x.', 'xxxxxx', E),
    'N': G(E, 'xxxxx.', '....x.', '...x..', '....x.', 'xxxxx.', E),
    'M': G(E, 'xxxxx.', '....x.', '...x..', '....x.', 'xxxxxx', E)},
   {f: ((1, 2), (7, 3)) for f in 'IFNM'})
sk('gaf', {
    'I': G('.xxx..', '..xxx.', '....x.', '....x.', 'x...x.', 'xxxxx.', E),
    'F': G('.xxx..', '..xxx.', '....x.', '....x.', 'x...x.', 'xxxxxx', E),
    'N': G('.xxx..', '..xxx.', '....x.', '...x..', '....x.', 'xxxxx.', E),
    'M': G('.xxx..', '..xxx.', '....x.', '...x..', '....x.', 'xxxxxx', E)},
   {f: ((1, 2), (7, 3)) for f in 'IFNM'})
sk('lam', {
    'I': G('....x.', '....x.', '....x.', '....x.', '....x.', 'x...x.', '.xxx..'),
    'F': G('....x.', '....x.', '....x.', '....x.', '....x.', 'x...xx', '.xxx..'),
    'N': G('...x..', '...x..', '...x..', '...x..', '...x..', 'xxxx..', E),
    'M': G('....x.', '....x.', '....x.', '....x.', '....x.', 'xxxxxx', E)},
   {f: ((1, 2), (7, 3)) for f in 'IFNM'})
sk('meem', {
    'I': G(E, E, E, '..xx..', '.x..x.', 'xxxx..', 'x.....'),
    'F': G(E, E, E, '..xx..', '.x..x.', 'x.xxxx', 'x.....'),
    'N': G(E, E, E, '..xx..', '.x..x.', 'xxxx..', E),
    'M': G(E, E, E, E, '..xx..', 'xx..xx', '..xx..')},
   {f: ((2, 3), (7, 4)) for f in 'IFNM'})
sk('heh', {
    'I': G(E, E, E, '..xx..', '.x..x.', '..xx..', E),
    'F': G(E, E, E, '..xx..', '.x..x.', '..xxxx', E),
    'N': G(E, E, '..x...', '.x.x..', 'x.xx..', 'xxxx..', E),
    'M': G(E, E, E, '..x...', '.x.x..', 'xxxxxx', '..x...')},
   {f: ((2, 3), (7, 3)) for f in 'IFNM'})
sk('hehdo', {   # (heh doachashmee, ھ: two eyes)
    'I': G(E, E, '..xx..', '.x.xx.', 'x.x.x.', '.xxx..', E),
    'F': G(E, E, '..xx..', '.x.xx.', 'x.x.x.', '.xxxxx', E),
    'N': G(E, E, '..xx..', '.x.xx.', 'x.x.x.', 'xxxx..', E),
    'M': G(E, E, '..xx..', '.x.xx.', 'x.x.x.', 'xxxxxx', E)},
   {f: ((1, 3), (7, 3)) for f in 'IFNM'})
sk('hehgoal', {   # (heh goal, ہ: a hook)
    'I': G(E, E, E, '...x..', '....x.', '.xxx..', E),
    'F': G(E, E, E, E, '...xx.', 'xxx..x', '...xx.')[:5] + ['xxx.xx', E],
    'N': G(E, E, E, '...x..', '....x.', 'xxxx..', E),
    'M': G(E, E, E, '...x..', '....x.', 'xxxxxx', '...x..')},
   {f: ((2, 3), (7, 3)) for f in 'IFNM'})
sk('waw', {
    'I': G(E, E, E, '..xx..', '..x.x.', '...x..', '.xx...'),
    'F': G(E, E, E, '...xx.', '...x.x', '....xx', '..xx..')},
   {'I': ((2, 3), (7, 3)), 'F': ((2, 4), (7, 4))})
sk('tehm', {   # (teh marbuta: heh's isolated and final; R)
    'I': G(E, E, E, '..xx..', '.x..x.', '..xx..', E),
    'F': G(E, E, E, '..xx..', '.x..x.', '..xxxx', E)},
   {f: ((2, 3), (7, 3)) for f in 'IF'})
sk('yehb', {   # (yeh barree, ے)
    'I': G(E, E, E, E, '...xx.', 'x.x...', 'xx....'),
    'F': G(E, E, E, E, E, 'x...xx', 'xxxx..')},
   {f: ((3, 3), (7, 3)) for f in 'IF'})
sk('hamza', {'I': G(E, E, E, '.xx...', 'x.....', '.xxx..', 'xx....')}, {'I': ((2, 2), (7, 2))})

# ---- THE DOTS (and small signs) over a form: a list of (row, col) from its anchor
def dots(kind, n, anchor):
    (ar, ac), (br, bc) = anchor
    if kind == 'above':
        r, c = ar, ac
        return {1: [(r, c)], 2: [(r, c - 1), (r, c + 1)], 3: [(r, c - 1), (r, c + 1), (r - 1, c)]}[n]
    r, c = br, bc
    # (three below: in a row under the baseline, a triangle inside a bowl that has no row there)
    return {1: [(r, c)], 2: [(r, c - 1), (r, c + 1)],
            3: [(r, c - 2), (r, c), (r, c + 2)] if r == 7 else [(r, c - 1), (r, c + 1), (r + 1, c)]}[n]

HAMZA_ABOVE = [(1, 0), (1, 1), (2, 0)]          # (a small ء: offsets from its top-left)
TAH_ABOVE = [(1, 0), (2, 0), (2, 1)]            # (the small ط of ٹ ڈ ڑ)
MADDA = [(1, 0), (1, 2), (2, 1)]

# ---- THE LETTERS: code point, skeleton, its marks; (presentation form code points: isolated, final, initial, medial)
L = [
    # (cp, skeleton, [(kind, n)] or a special, forms...)
    (0x0621, 'hamza', [], (0xFE80, 0, 0, 0)),
    (0x0622, 'alef', ['madda'], (0xFE81, 0xFE82, 0, 0)),
    (0x0623, 'alef', ['hamza_above'], (0xFE83, 0xFE84, 0, 0)),
    (0x0624, 'waw', ['hamza_above'], (0xFE85, 0xFE86, 0, 0)),
    (0x0625, 'alef', ['hamza_below'], (0xFE87, 0xFE88, 0, 0)),
    (0x0626, ('yeh', 'beh'), ['hamza_above'], (0xFE89, 0xFE8A, 0xFE8B, 0xFE8C)),
    (0x0627, 'alef', [], (0xFE8D, 0xFE8E, 0, 0)),
    (0x0628, 'beh', [('below', 1)], (0xFE8F, 0xFE90, 0xFE91, 0xFE92)),
    (0x0629, 'tehm', [('above', 2)], (0xFE93, 0xFE94, 0, 0)),
    (0x062A, 'beh', [('above', 2)], (0xFE95, 0xFE96, 0xFE97, 0xFE98)),
    (0x062B, 'beh', [('above', 3)], (0xFE99, 0xFE9A, 0xFE9B, 0xFE9C)),
    (0x062C, 'hah', [('below', 1)], (0xFE9D, 0xFE9E, 0xFE9F, 0xFEA0)),
    (0x062D, 'hah', [], (0xFEA1, 0xFEA2, 0xFEA3, 0xFEA4)),
    (0x062E, 'hah', [('above', 1)], (0xFEA5, 0xFEA6, 0xFEA7, 0xFEA8)),
    (0x062F, 'dal', [], (0xFEA9, 0xFEAA, 0, 0)),
    (0x0630, 'dal', [('above', 1)], (0xFEAB, 0xFEAC, 0, 0)),
    (0x0631, 'reh', [], (0xFEAD, 0xFEAE, 0, 0)),
    (0x0632, 'reh', [('above', 1)], (0xFEAF, 0xFEB0, 0, 0)),
    (0x0633, 'seen', [], (0xFEB1, 0xFEB2, 0xFEB3, 0xFEB4)),
    (0x0634, 'seen', [('above', 3)], (0xFEB5, 0xFEB6, 0xFEB7, 0xFEB8)),
    (0x0635, 'sad', [], (0xFEB9, 0xFEBA, 0xFEBB, 0xFEBC)),
    (0x0636, 'sad', [('above', 1)], (0xFEBD, 0xFEBE, 0xFEBF, 0xFEC0)),
    (0x0637, 'tah', [], (0xFEC1, 0xFEC2, 0xFEC3, 0xFEC4)),
    (0x0638, 'tah', [('above', 1)], (0xFEC5, 0xFEC6, 0xFEC7, 0xFEC8)),
    (0x0639, 'ain', [], (0xFEC9, 0xFECA, 0xFECB, 0xFECC)),
    (0x063A, 'ain', [('above', 1)], (0xFECD, 0xFECE, 0xFECF, 0xFED0)),
    (0x0641, 'feh', [('above', 1)], (0xFED1, 0xFED2, 0xFED3, 0xFED4)),
    (0x0642, ('qaf', 'feh'), [('above', 2)], (0xFED5, 0xFED6, 0xFED7, 0xFED8)),
    (0x0643, 'kaf', [], (0xFED9, 0xFEDA, 0xFEDB, 0xFEDC)),
    (0x0644, 'lam', [], (0xFEDD, 0xFEDE, 0xFEDF, 0xFEE0)),
    (0x0645, 'meem', [], (0xFEE1, 0xFEE2, 0xFEE3, 0xFEE4)),
    (0x0646, ('noon', 'beh'), [('above', 1)], (0xFEE5, 0xFEE6, 0xFEE7, 0xFEE8)),
    (0x0647, 'heh', [], (0xFEE9, 0xFEEA, 0xFEEB, 0xFEEC)),
    (0x0648, 'waw', [], (0xFEED, 0xFEEE, 0, 0)),
    (0x0649, ('yeh', 'beh'), [], (0xFEEF, 0xFEF0, 0xFBE8, 0xFBE9)),
    (0x064A, ('yeh', 'beh'), [('below', 2)], (0xFEF1, 0xFEF2, 0xFEF3, 0xFEF4)),
    # Persian and Urdu (Presentation Forms-A)
    (0x0671, 'alef', ['wasla'], (0xFB50, 0xFB51, 0, 0)),
    (0x0679, 'beh', ['tah_above'], (0xFB66, 0xFB67, 0xFB68, 0xFB69)),
    (0x067E, 'beh', [('below', 3)], (0xFB56, 0xFB57, 0xFB58, 0xFB59)),
    (0x0686, 'hah', [('below', 3)], (0xFB7A, 0xFB7B, 0xFB7C, 0xFB7D)),
    (0x0688, 'dal', ['tah_above'], (0xFB88, 0xFB89, 0, 0)),
    (0x0691, 'reh', ['tah_above'], (0xFB8C, 0xFB8D, 0, 0)),
    (0x0698, 'reh', [('above', 3)], (0xFB8A, 0xFB8B, 0, 0)),
    (0x06A9, 'keheh', [], (0xFB8E, 0xFB8F, 0xFB90, 0xFB91)),
    (0x06AF, 'gaf', [], (0xFB92, 0xFB93, 0xFB94, 0xFB95)),
    (0x06BA, 'noon', [], (0xFB9E, 0xFB9F, 0, 0)),
    (0x06BE, 'hehdo', [], (0xFBAA, 0xFBAB, 0xFBAC, 0xFBAD)),
    (0x06C1, 'hehgoal', [], (0xFBA6, 0xFBA7, 0xFBA8, 0xFBA9)),
    (0x06CC, ('yeh', 'beh'), ['farsi'], (0xFBFC, 0xFBFD, 0xFBFE, 0xFBFF)),
    (0x06D2, 'yehb', [], (0xFBAE, 0xFBAF, 0, 0)),
]

def put(g, pts, r0=0, c0=0):
    g = [list(r) for r in g]
    for r, c in pts:
        rr, cc = r + r0, c + c0
        if 1 <= rr <= 7 and 1 <= cc <= 6:
            g[rr - 1][cc - 1] = 'x'
    return [''.join(r) for r in g]

def form(cp, skel, marks, f):
    """One form (I F N M) of a letter: its skeleton's form with its dots and signs."""
    name = skel if isinstance(skel, str) else (skel[0] if f in 'IF' else skel[1])
    g = S[name][f]
    anc = A[name][f]
    for m in marks:
        if isinstance(m, tuple):
            g = put(g, dots(m[0], m[1], anc))
        elif m in ('hamza_above', 'madda', 'wasla'):
            # (over an alef: the letter shortened to make room; over the rest, at the dots' place)
            if name == 'alef':
                c = 3 if f == 'I' else 5
                g = [E, E] + g[2:]
                pat = {'hamza_above': HAMZA_ABOVE, 'madda': MADDA, 'wasla': [(1, 0), (1, 1)]}[m]
                g = put(g, pat, 0, c - 1)
            else:
                (ar, ac), _ = anc
                g = put(g, HAMZA_ABOVE, ar - 2, ac - 1)
        elif m == 'hamza_below':
            g = put(g, [(7, 0), (7, 1)], 0, 2 if f == 'I' else 4)
        elif m == 'tah_above':
            (ar, ac), _ = anc
            g = put(g, TAH_ABOVE, ar - 2, ac - 1)
        elif m == 'farsi':
            # (farsi yeh: no dots isolated and final; two below initial and medial)
            if f in 'NM':
                g = put(g, dots('below', 2, anc))
    return g

def glyphs():
    out = {}
    for cp, skel, marks, fs in L:
        for f, pcp in zip('IFNM', fs):
            if pcp:
                out[pcp] = form(cp, skel, marks, f)
        out[cp] = form(cp, skel, marks, 'I')
    # lam-alef: isolated, final; for alef with madda, hamza above, hamza below, plain
    la = {'I': G('x...x.', 'x...x.', '.x..x.', '..x.x.', '..xxx.', '.xxx..', E),
          'F': G('x...x.', 'x...x.', '.x..x.', '..x.x.', '..xxx.', '.xx.xx', E)}
    for (first, extra) in ((0xFEF5, 'madda'), (0xFEF7, 'hamza_above'), (0xFEF9, 'hamza_below'), (0xFEFB, None)):
        for k, f in enumerate('IF'):
            g = la[f]
            if extra in ('madda', 'hamza_above'):
                g = put([E, E] + g[2:], {'madda': MADDA, 'hamza_above': HAMZA_ABOVE}[extra], 0, 0)
                g = put(g, [(3, 1)])
            elif extra == 'hamza_below':
                g = put(g, [(7, 1), (7, 2)])
            out[first + k] = g
    out[0x0640] = G(E, E, E, E, E, 'xxxxxx', E)                       # tatweel
    # punctuation
    out[0x060C] = G(E, E, E, E, '...x..', '..xx..', E)                 # ، (comma, turned)
    out[0x061B] = G(E, E, '...x..', E, '...x..', '..xx..', E)          # ؛
    out[0x061F] = G('.xxx..', '....x.', '...x..', '..x...', E, '..x...', E)   # ؟ (mirrored)
    # digits: Arabic-Indic, and the Eastern (Persian, Urdu) ones that differ
    D = {0: G(E, E, E, '..x...', '.x.x..', '..x...', E),
         1: G(E, '.x....', '..x...', '..x...', '..x...', '..x...', E),
         2: G(E, 'x..x..', '.xx...', 'x.....', 'x.....', 'x.....', E),
         3: G(E, 'x.x.x.', '.x.x..', 'x.....', 'x.....', 'x.....', E),
         4: G(E, '..xx..', '.x....', '..x...', '.x....', '..xx..', E),
         5: G(E, E, '..x...', '.x.x..', 'x...x.', '.xxx..', E),
         6: G(E, 'xxxx..', '...x..', '...x..', '...x..', '...x..', E),
         7: G(E, 'x...x.', 'x...x.', '.x.x..', '..x...', '..x...', E),
         8: G(E, '.xx...', '.x.x..', '.x.x..', 'x...x.', 'x...x.', E),
         9: G(E, '.xx...', 'x..x..', '.xxx..', '...x..', '...x..', E)}
    for d, g in D.items():
        out[0x0660 + d] = g
        out[0x06F0 + d] = g
    out[0x06F4] = G(E, 'x.xx..', 'xx....', 'x.....', '.xx...', '...x..', E)
    out[0x06F5] = G(E, E, '..x...', '.x.x..', 'x...x.', 'x.x.x.', E)
    out[0x06F6] = G(E, '.xx...', 'x.....', '.xx...', '...x..', '..x...', E)
    # harakat (marks: drawn over the letter before them, in its cell)
    out[0x064B] = G('..x..x', '.x..x.', E, E, E, E, E)       # fathatan
    out[0x064C] = G('.xx.x.', '..x.x.', E, E, E, E, E)       # dammatan
    out[0x064D] = G(E, E, E, E, E, E, '.xx.xx')              # kasratan
    out[0x064E] = G('...x..', '.xx...', E, E, E, E, E)       # fatha
    out[0x064F] = G('...xx.', '....x.', E, E, E, E, E)       # damma
    out[0x0650] = G(E, E, E, E, E, E, '..xx..')              # kasra
    out[0x0651] = G('x.x.x.', '.xxx..', E, E, E, E, E)       # shadda
    out[0x0652] = G('..xx..', '..xx..', E, E, E, E, E)       # sukun
    out[0x0653] = G('.xx.x.', E, E, E, E, E, E)              # madda above
    out[0x0654] = G('...xx.', '...x..', E, E, E, E, E)       # hamza above
    out[0x0655] = G(E, E, E, E, E, E, '..xxx.')              # hamza below
    out[0x0670] = G('...x..', '...x..', E, E, E, E, E)       # superscript alef
    return out

def main():
    force = '--force' in sys.argv
    out = glyphs()
    wrote = 0
    for d in DIRS:
        for cp, g in sorted(out.items()):
            p = os.path.join(d, 'U+%04X' % cp)
            if os.path.exists(p) and not force:
                continue
            with open(p, 'w') as f:
                f.write('\n'.join(g) + '\n')
            wrote += 1
    print('%d glyphs, %d files written' % (len(out), wrote))
    if '--sheet' in sys.argv:
        sheet(out, sys.argv[sys.argv.index('--sheet') + 1])

def sheet(out, path):
    from PIL import Image, ImageDraw, ImageFont
    S_, cw = 6, 6
    ref = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf', 30)
    rows = [(cp, fs) for cp, _, _, fs in L]
    img = Image.new('RGB', (1400, 60 + len(rows) * 50), 'white')
    d = ImageDraw.Draw(img)
    for i, (cp, fs) in enumerate(rows):
        y = 10 + i * 50
        for k, pcp in enumerate(fs):
            if not pcp:
                continue
            g = out[pcp]
            x0 = 10 + k * 70
            for r, row in enumerate(g):
                for c, v in enumerate(row):
                    if v == 'x':
                        d.rectangle([x0 + c * S_, y + r * S_, x0 + c * S_ + S_ - 1, y + r * S_ + S_ - 1], fill=0)
            d.rectangle([x0 - 1, y - 1, x0 + 6 * S_, y + 7 * S_], outline=(200, 200, 200))
            joiner = {0: '', 1: '‍', 2: '', 3: '‍'}[k]
            txt = {0: chr(cp), 1: '‍' + chr(cp), 2: chr(cp) + '‍', 3: '‍' + chr(cp) + '‍'}[k]
            d.text((x0 + 300, y), txt, font=ref, fill='red')
        d.text((620, y + 10), 'U+%04X' % cp, fill='black')
    img.save(path)

if __name__ == '__main__':
    main()
