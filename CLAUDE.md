# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`code7` is a 7px-tall bitmap font (the upper 7 rows of a 9px design) for xterm, in four fonts:
- `code7` — regular
- `code7sc` — small caps, **registered as the "bold" weight** so xterm's bold maps to small caps instead of a heavier stroke
- `code7it` — italic (slanted capitals; lowercase is the same as regular)
- `code7w` — 12x7 double-width companion: glyphs for East-Asian-wide characters (emoji), used as xterm's `wideFont` / `faceNameDoublesize`

Each is built as a BDF (X11 bitmap) and a TTF. Source glyphs live in the `fnt` git submodule: `fnt/<font>/6x7/*`, and `fnt/code7w/12x7/*`.

## Build

```sh
git submodule update --init    # required — fnt/ is empty without this
make all                       # builds the four TTFs (and their BDFs)
make code7sc.ttf               # build a single font
make check                     # duplicate-bitmap check on all four fonts
```

The build pipeline per font:
1. `fnt/src/2bdf.sh fnt/<font>/<W>x<H>` → `<font>.bdf` (rows are padded to whole bytes, so widths over 8 work)
2. `Dockerfile.fontforge` builds an Ubuntu image with `python3-fontforge` + `bdf2ttf`
3. `Dockerfile.ttf` runs `bdf2ttf`, then `ttffix.py`, which marks `code7it.ttf` italic and gives `code7w.ttf` its own family (bdf2ttf would register both as a second "code7 medium")
4. `Dockerfile` exports the TTF back to the host via BuildKit `--output type=local`

For `code7w.ttf`, `Dockerfile.ttf` then runs `cbdt.py`, which adds a 14px colour bitmap strike (CBDT/CBLC tables). Glyphs in `fnt/code7w-color/12x7` are drawn in colour; every other code7w glyph goes into the strike in a neutral grey. This is required: once Xft uses a font's colour strike it can't load that font's outlines, and xterm then rejects the font for failing its Latin-1 check. So in TrueType mode, wide glyphs don't follow the terminal's text colour. The BDF and bitmap mode stay monochrome.

Before that, `flags.py` adds country flags to `code7w.ttf` as ligatures, for terminals that shape text (kitty, WezTerm): each file in `fnt/code7w-flags/12x7` is named after a country code (`US`, `JP` ...) and drawn in the colour palette; `flags.py` adds a two-cell glyph `flag_XX` and a GSUB ligature from the two regional indicator letters to it, and narrows the letter keys to one cell, and `cbdt.py` gives the flag its colour bitmap. xterm and gnome-terminal don't shape, so they keep showing the letter keys from code7.

`code7w.bdf` also gets pixel-doubled ASCII and Latin-1 from `latin2x.py` at build time: xterm rejects a `faceNameDoublesize` font without ISO-8859-1 glyphs. They are generated, not stored in `fnt/`.

The `fontforge` Make target writes a sentinel file of the same name. The image rebuilds when `Dockerfile.fontforge` changes; delete the sentinel to force a rebuild otherwise. A rebuilt image restamps the build date in every TTF; restore the unchanged ones with `git checkout` before committing. Built BDFs and TTFs are committed.

## Glyph files

Each glyph is a text file of H rows of W cells, `x` for ink and `.` for blank. It is named after its HTML entity in `fnt/src/entities.csv` if it has one (`Aacute`, `boxh`), otherwise `U+XXXXX`.

Conventions:
- In 6x7, column 6 is normally blank (the gap between characters). Capitals use rows 1-6, lowercase bodies rows 2-6, with accents above and descenders in row 7.
- In 12x7 (`code7w`), draw in columns 1-11 and leave column 12 blank. Pictograms are about 7-9 wide and centred, so they look square.
- `fnt/code7w-color/12x7` holds optional colour versions of code7w glyphs, with the same file names. Their cells are palette letters instead of `x`: `r o y g b v n p c` for red, orange, yellow, green, blue, purple, brown, pink and light blue, `w` white, `k` grey, `d` dark, `a e i j l` for the five skin tones, and `x` for a neutral grey. The palette is defined in `cbdt.py`. A colour glyph must also exist in `fnt/code7w/12x7` as the monochrome fallback.
- Symbols are the same in all three 6x7 variants. Letters differ: code7sc lowercase is small caps, and code7it has hand-slanted capitals.
- **Every character must differ from every other by at least one pixel**, within each font. Prefer an added mark over reshaping a letter. `tools/dups.py` lists the only agreed exceptions: the blanks (space, no-break space, braille blank) and three full-width combining marks.
- Greek and Cyrillic letters that would match an existing glyph carry a 1-pixel script mark in row 7: Cyrillic at the bottom right, Greek at the bottom left.
- Any character that is East-Asian-wide (`unicodedata.east_asian_width` W or F) and is in code7 must also have a 12x7 version in `fnt/code7w/12x7`. xterm draws a wide character missing from the wide font as blank (bitmap) or a box (TrueType).

Tools (run from anywhere):
- `tools/dups.py DIR...` reports identical bitmaps. A later dir overrides an earlier one, so a draft can be checked against a font.
- `tools/show.py DIR HEX...` prints the given codepoints.
- `tools/sheet.py DIR` prints a whole glyph dir with character headers.
- `tools/kitty-conf.py` prints the kitty config (`make all` writes it to `kitty-code7.conf`).

## Installing into an X session

- `setup.sh` — adds this directory to the X font path (`xset fp+`), runs `fc-cache`, and merges `Xresources.code7` (bitmap fonts at 1x) plus `Xresources.dark` (solarized dark colours).
- `setup-double.sh` — the same with `Xresources.code7-2x`: the bitmap fonts at 14px, scaled 2x by the X server.
- `setup-ttf.sh` — copies the four TTFs to `~/.local/share/fonts`, installs `fontconfig-code7.conf` as `~/.config/fontconfig/conf.d/50-code7.conf` (code7w becomes the first fallback for code7, for terminals such as gnome-terminal that find missing glyphs through fontconfig), installs `kitty-code7.conf` as `~/.config/kitty/code7.conf` and includes it from `kitty.conf` (kitty routes characters to fonts itself; the config's `symbol_map` sends every code7w glyph to code7w and is regenerated by `make all` from `tools/kitty-conf.py`), and merges `Xresources.code7-2x` then `Xresources.code7-ttf`, which turns on `renderFont` (Xft) with `faceName: code7:pixelsize=14` and `faceNameDoublesize: code7w:pixelsize=14`. Only this mode reaches characters above U+FFFF: X11 core (bitmap) fonts are limited to the BMP.
- `term.sh` — sources `setup.sh` then execs `xterm`.

The XLFD names in `fonts.dir` are what the Xresources files reference. They are spelled out in full (e.g. `-bwoolley-code7-medium-r-normal--7-70-75-75-m-60-iso10646-1`), because a wildcard such as `-bwoolley-code7-medium-r-*` also matches code7w (spacing `c`, width 120). At 2x the names become `--14-140-...-m-120` and `--14-140-...-c-240`. If you rename a BDF or change its FOUNDRY/FAMILY, update `fonts.dir` to match, or xterm will fail to find the font.
