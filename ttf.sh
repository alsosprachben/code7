#!/bin/sh
# ttf.sh FONT: build FONT.ttf from FONT.bdf. Runs inside the fontforge image, with the repo mounted as the
# working directory (see the Makefile). For code7w it also adds the ligatures and the colour strike.
set -e
font=$1
t=$(mktemp -d)
trap 'rm -rf "$t"' EXIT
# bdf2ttf reads POINT_SIZE in points, not decipoints
awk '/^POINT_SIZE / { print "POINT_SIZE " int(($2 + 5) / 10); next } { print }' "$font.bdf" > "$t/$font.bdf"
bdf2ttf "$t/$font.bdf" --out "$t/$font.ttf"
python3 ttffix.py "$font" "$t/$font.ttf"
if [ "$font" = code7w ]; then
	# ligature sources: the stored ones, plus gendered, facing-right and skin-tone sequences and emoji forms of text characters
	cp -r fnt/code7w-flags/12x7 "$t/seq"
	python3 genders.py fnt/code7w-color/12x7 "$t/seq"
	python3 directions.py fnt/code7w-color/12x7 "$t/seq"
	python3 emojiforms.py fnt/code7/6x7 "$t/seq"
	python3 skintones.py fnt/code7w-color/12x7 "$t/seq"
	python3 flags.py "$t/$font.ttf" "$t/seq"
	python3 cbdt.py "$t/$font.ttf" fnt/code7w-color/12x7 "$font.bdf" "$t/seq"
fi
cp "$t/$font.ttf" "$font.ttf"
