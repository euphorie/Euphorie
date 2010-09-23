PACK		= yuicompressor --charset utf-8

JQUERY 		= ../libraries/jquery-1.3.2.js ../libraries/jquery-ui-1.7.2.min.js
JQUERY_UI	= ../libraries/ui-1.7.2/ui.core.js \
		  ../libraries/ui-1.7.2/effects.core.js \
		  ../libraries/ui-1.7.2/ui.accordion.js
EXTRAS		= ../libraries/jquery.hoverIntent.js \
		  ../libraries/jquery.bt.js  \
		  ../libraries/jcarousellite_1.0.1.js \
		  ../libraries/css_browser_selector.js

TARGETS		= common.min.js

all: ${TARGETS}

clean:
	-rm ${TARGETS}

common.min.js: ${JQUERY} ${JQUERY_UI} ${EXTRAS} markup.js
	set -e ; (for i in $^ ; do $(PACK) $$i ; done ) > $@~ ; mv $@~ $@

.PHONY: all clean
