.PHONY: all check

all: code7.ttf code7sc.ttf code7it.ttf code7w.ttf code7t.bdf kitty-code7.conf

# every character must differ from every other by at least one pixel, and every emoji in
# Unicode's lists (tools/unicode) must have a glyph or ligature source
check:
	./tools/coverage.py
	./tools/dups.py ./fnt/code7/6x7
	./tools/dups.py ./fnt/code7sc/6x7
	./tools/dups.py ./fnt/code7it/6x7
	./tools/dups.py ./fnt/code7w/12x7
	./tools/dups.py ./fnt/code7w-color/12x7
	./tools/dups.py ./fnt/code7t/6x9

# run ttf.sh in the fontforge image with the repo mounted: nothing is copied, and no image layers are left behind
%.ttf: %.bdf fontforge ttf.sh ttffix.py
	docker run --rm --user "$$(id -u):$$(id -g)" -e HOME=/tmp -v "$$PWD:/code7" -w /code7 fontforge ./ttf.sh ${*}

code7_glyphs   := $(wildcard ./fnt/code7/6x7/*)
code7sc_glyphs := $(wildcard ./fnt/code7sc//6x7/*)
code7it_glyphs := $(wildcard ./fnt/code7it//6x7/*)
code7w_glyphs  := $(wildcard ./fnt/code7w/12x7/*)
code7w_color   := $(wildcard ./fnt/code7w-color/12x7/*)
code7w_flags   := $(wildcard ./fnt/code7w-flags/12x7/*)

# colour versions of code7w glyphs, added to the TTF only (see cbdt.py)
code7w.ttf: cbdt.py flags.py genders.py directions.py emojiforms.py skintones.py tools/glyphlib.py ${code7w_color} ${code7w_flags} ${code7_glyphs}

code7.bdf: ${code7_glyphs}
	./fnt/src/2bdf.sh "${<D}" > "${@}"

code7sc.bdf: ${code7sc_glyphs}
	./fnt/src/2bdf.sh "${<D}" > "${@}"

# Thai and Devanagari in a 6x9 cell (code7's 7 rows and one above and one below, for their marks); BDF only
code7t_glyphs  := $(wildcard ./fnt/code7t/6x9/*)
code7t.bdf: ${code7t_glyphs}
	./fnt/src/2bdf.sh "${<D}" > "${@}"

code7it.bdf: ${code7it_glyphs}
	./fnt/src/2bdf.sh "${<D}" > "${@}"

# double-width glyphs for xterm's wideFont / faceNameDoublesize, plus pixel-doubled
# Latin-1 so xterm accepts the TTF as a font (see latin2x.py)
code7w.bdf: ${code7w_glyphs} ${code7_glyphs} latin2x.py
	d="$$(mktemp -d)" && cp -r ./fnt/code7w/12x7 "$$d/" \
		&& ./latin2x.py ./fnt/code7/6x7 "$$d/12x7" \
		&& ./fnt/src/2bdf.sh "$$d/12x7" > "${@}"; s=$$?; rm -rf "$$d"; exit $$s

# kitty routes characters to fonts itself; send every code7w glyph to code7w
kitty-code7.conf: tools/kitty-conf.py tools/glyphlib.py ${code7w_glyphs}
	./tools/kitty-conf.py > "${@}"

fontforge: Dockerfile.fontforge
	DOCKER_BUILDKIT=1 docker build -t fontforge - < Dockerfile.fontforge
	touch fontforge
