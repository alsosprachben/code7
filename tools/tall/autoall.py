# autoall.py [NotoSansDevanagari.ttf]: drafts every Thai and Devanagari character on the 6x9 grid from Noto
# (OFL) renderings at a fixed scale, into auto9.json -- a STARTING POINT, corrected by hand in assemble9.py.
import sys, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autodraft.py')).read())
import json
TH='/usr/share/fonts/truetype/noto/NotoLoopedThai-Regular.ttf'
DV=sys.argv[1] if len(sys.argv) > 1 else 'NotoSansDevanagari.ttf'   # (Noto Sans Devanagari, OFL: google/fonts ofl/notosansdevanagari)
thai=[chr(c) for c in list(range(0xE01,0xE3B))+list(range(0xE3F,0xE5C))]
deva=[chr(c) for c in list(range(0x900,0x951))+list(range(0x958,0x971))]
TMARK={0xE31,*range(0xE34,0xE3B),*range(0xE47,0xE4F)}
DMARK={0x900,0x901,0x902,0x93A,0x93C,*range(0x941,0x949),0x94D,0x951,0x952,0x953,0x954,0x955,0x956,0x957,0x962,0x963}
MARKS.update(chr(c) for c in TMARK|DMARK)
g={}
g.update(draft(TH,thai,0,7,143,0.3))
g.update(draft(DV,deva,0,7,153,0.3))
g.update({'LIG%d'%i: v for i, v in enumerate(draft(DV,['क्ष','ज्ञ','त्र','श्र'],0,7,153,0.3).values())})
def clean(ch,rows):
    cp=ord(ch) if len(ch)==1 else 0x915; r=[list(x) for x in rows]
    if 0x900<=cp<0x980 and cp not in DMARK:
        # headline: over the whole cell where the letter has one, so letters join
        if 'x' in rows[1]:
            gap = [i for i in range(1,5) if r[1][i]=='.' and r[1][i-1]=='x' and 'x' in rows[1][i+1:]]
            for i in range(6): r[1][i]='x'
            for i in gap: r[1][i]='.'
    if cp not in DMARK and cp not in TMARK:
        # keep column 6 blank under the headline: shift left when there is room
        for _ in range(2):
            if any(r[k][5]=='x' for k in range(2,9)) and all(r[k][0]=='.' for k in range(2,9)):
                for k in range(2,9): r[k]=r[k][1:]+['.']
        # double stems to one: a pixel whose right neighbour is ink and that has no ink above/below except stem
        for c in range(4):
            col=[r[k][c]=='x' and r[k][c+1]=='x' for k in range(2,7)]
            if sum(col)>=4 and all(r[k][c+1]=='x' for k in range(2,7)):
                for k in range(2,7):
                    if c==0 or r[k][c-1]=='.': r[k][c]='.'
    return [''.join(x) for x in r]
for ch in g: g[ch]=clean(ch,g[ch])
json.dump({('%04X'%ord(k) if len(k)==1 else k):v for k,v in g.items()},open('auto9.json','w'),indent=0)
print(len(g))
