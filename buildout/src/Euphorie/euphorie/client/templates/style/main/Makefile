PACK		= yuicompressor --charset utf-8 --nomunge

TARGETS		= screen.min.css \
		  screen-ie6.min.css \
		  screen-ie7.min.css \
		  screen-ie8.min.css

all: ${TARGETS}

clean:
	-rm ${TARGETS}

%.min.css: %.css
	set -e ; $(PACK) $< > $@~ ; mv $@~ $@

.PHONY: all clean
