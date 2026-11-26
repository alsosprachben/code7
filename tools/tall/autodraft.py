# render letters from a real font onto the 6x9 grid at a fixed scale: a starting draft to correct by hand
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
SS = 16                                   # (supersampling: one grid pixel = SS rendered pixels)
def draft(font, chars, top_row_y, base_row, size, thr=0.28, dx=0):
    """top_row_y: the font's y (at render size) that falls on the top of grid row 1; base_row: grid row whose
    bottom is the baseline. size: font size so that the script's body spans the rows meant for it."""
    f = ImageFont.truetype(font, size)
    out = {}
    for ch in chars:
        im = Image.new('L', (SS * 12, SS * 12), 0)
        d = ImageDraw.Draw(im)
        asc = f.getmetrics()[0]
        # (baseline of the text at y = base_row * SS)
        txt = ('◌' + ch) if ch in MARKS else ch
        d.text((SS * 2, base_row * SS - asc), txt, font=f, fill=255)
        a = np.asarray(im, dtype=float) / 255
        cols = np.where(a.sum(0) > 0)[0]
        if not len(cols):
            out[ch] = ['......'] * 9; continue
        x0 = cols[0]
        if ch in MARKS:      # (a mark: keep it where it falls over the circle)
            x0 = SS * 2
        w = (cols[-1] - x0 + 1) / SS
        off = int(round((5 - w) / 2 * SS)) + dx * SS
        g = []
        for r in range(9):
            row = ''
            for c in range(6):
                xa = x0 - off + c * SS
                cell = a[r * SS:(r + 1) * SS, max(0, xa):max(0, xa + SS)]
                row += 'x' if cell.size and cell.mean() > thr else '.'
            g.append(row)
        out[ch] = g
    return out
MARKS = set()
