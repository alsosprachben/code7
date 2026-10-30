.PHONY: all check

all: code7.ttf code7sc.ttf code7it.ttf code7w.ttf

# every character must differ from every other by at least one pixel
check:
	./tools/dups.py ./fnt/code7/6x7
	./tools/dups.py ./fnt/code7sc/6x7
	./tools/dups.py ./fnt/code7it/6x7
	./tools/dups.py ./fnt/code7w/12x7

%.ttf: %.bdf fontforge Dockerfile.ttf ttffix.py
	docker image rm ttf || true
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.ttf --build-arg font=${*} --target ttf -t ttf .
	DOCKER_BUILDKIT=1 docker build -f Dockerfile     --build-arg font=${*} --target export --output type=local,dest=. .

code7_glyphs   := $(wildcard ./fnt/code7/6x7/*)
code7sc_glyphs := $(wildcard ./fnt/code7sc//6x7/*)
code7it_glyphs := $(wildcard ./fnt/code7it//6x7/*)
code7w_glyphs  := $(wildcard ./fnt/code7w/12x7/*)

code7.bdf: ${code7_glyphs}
	./fnt/src/2bdf.sh "${<D}" > "${@}"

code7sc.bdf: ${code7sc_glyphs}
	./fnt/src/2bdf.sh "${<D}" > "${@}"

code7it.bdf: ${code7it_glyphs}
	./fnt/src/2bdf.sh "${<D}" > "${@}"

# double-width glyphs for xterm's wideFont / faceNameDoublesize, plus pixel-doubled
# Latin-1 so xterm accepts the TTF as a font (see latin2x.py)
code7w.bdf: ${code7w_glyphs} ${code7_glyphs} latin2x.py
	d="$$(mktemp -d)" && cp -r ./fnt/code7w/12x7 "$$d/" \
		&& ./latin2x.py ./fnt/code7/6x7 "$$d/12x7" \
		&& ./fnt/src/2bdf.sh "$$d/12x7" > "${@}"; s=$$?; rm -rf "$$d"; exit $$s

fontforge:
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.fontforge --build-arg font=${*} --target fontforge -t fontforge .
	touch fontforge
