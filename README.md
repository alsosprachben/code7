# code7
7px of a 9px font, with a small-caps version for bold

Run `setup.sh` to:
 1. Append this folder to your X font paths for this session.
 2. Merge Xresources.code7 into your X resources for this session.
 3. Merge Xresources.dark  into your X resources for this session.

Xresources.code7 configures xterm for using this font.
Xresources.dark changes the base color scheme to "solarized dark".

Run `term.sh` to run `setup.sh` and exec `xterm`.

`setup-double.sh` does the same at twice the size, using Xresources.code7-2x.

Run `setup-ttf.sh` to use the TrueType fonts instead, at twice the size:
 1. Copy code7.ttf, code7sc.ttf, code7it.ttf and code7w.ttf to ~/.local/share/fonts.
 2. Merge Xresources.code7-2x, then Xresources.code7-ttf, which turns on
    xterm's renderFont. Unlike the bitmap fonts, this reaches characters above
    U+FFFF.

code7w is a 12x7 font for double-width characters such as emoji. xterm uses
it as wideFont (bitmap) or faceNameDoublesize (TrueType).
