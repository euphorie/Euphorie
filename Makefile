YUICOMPRESS	?= yui-compressor
PYTHON		?= python

CSS_PACK	= $(YUICOMPRESS) --charset utf-8 --nomunge
CSS_DIR		= Prototype/style/main
CSS_TARGETS	= $(CSS_DIR)/screen.min.css \
		  $(CSS_DIR)/screen-ie7.min.css \
		  $(CSS_DIR)/screen-ie8.min.css \
		  $(CSS_DIR)/screen-osha.min.css

JS_PACK		= $(YUICOMPRESS) --charset utf-8
JS_DIR		= Prototype
JS_TARGETS	= $(JS_DIR)/behaviour/common.min.js

JQUERY 		= $(JS_DIR)/libraries/jquery-1.3.2.js \
		  $(JS_DIR)/libraries/jquery-ui-1.7.2.min.js
JQUERY_UI	= $(JS_DIR)/libraries/ui-1.7.2/ui.core.js \
		  $(JS_DIR)/libraries/ui-1.7.2/effects.core.js \
		  $(JS_DIR)/libraries/ui-1.7.2/ui.accordion.js
EXTRAS		= $(JS_DIR)/libraries/jquery.hoverIntent.js \
		  $(JS_DIR)/libraries/jquery.bt.js  \
		  $(JS_DIR)/libraries/jcarousellite_1.0.1.js \
		  $(JS_DIR)/libraries/css_browser_selector.js \
		  $(JS_DIR)/libraries/jquery.numeric.js \
		  $(JS_DIR)/libraries/jquery.scrollTo.js \
		  $(JS_DIR)/libraries/jquery.localscroll.js \
		  $(JS_DIR)/libraries/fancybox/jquery.fancybox-1.3.1.pack.js \
		  $(JS_DIR)/libraries/fancybox/jquery.mousewheel-3.0.2.pack.js 

EUPHORIE_PO_FILES	= $(wildcard buildout/src/Euphorie/euphorie/deployment/locales/*/LC_MESSAGES/euphorie.po)
PLONE_PO_FILES	= $(wildcard buildout/src/Euphorie/euphorie/deployment/locales/*/LC_MESSAGES/plone.po)
MO_FILES	= $(EUPHORIE_PO_FILES:.po=.mo) $(PLONE_PO_FILES:.po=.mo)

TARGETS		= $(CSS_TARGETS) $(JS_TARGETS) $(MO_FILES)

all: ${TARGETS}

clean:
	-rm ${TARGETS}

buildout/bin/buildout: buildout/bootstrap.py
	cd buildout ; $(PYTHON) bootstrap.py

buildout/bin/test buildout/bin/sphinx-build: buildout/bin/buildout buildout/buildout.cfg buildout/versions.cfg buildout/devel.cfg
	cd buildout ; bin/buildout -c devel.cfg

check:: buildout/bin/test
	cd buildout ; bin/test

check:: buildout/bin/sphinx-build
	$(MAKE) -C buildout/src/Euphorie/docs linkcheck

$(JS_DIR)/behaviour/common.min.js: ${JQUERY} ${JQUERY_UI} ${EXTRAS} $(JS_DIR)/behaviour/markup.js
	set -e ; (for i in $^ ; do $(JS_PACK) $$i ; done ) > $@~ ; mv $@~ $@

$(EUPHORIE_PO_FILES): buildout/src/Euphorie/euphorie/deployment/locales/euphorie.pot
	msgmerge --update $@ $<

$(PLONE_PO_FILES): buildout/src/Euphorie/euphorie/deployment/locales/plone.pot
	msgmerge --update $@ $<

%.min.css: %.css
	set -e ; $(CSS_PACK) $< > $@~ ; mv $@~ $@

.po.mo:
	msgfmt -c --statistics -o $@~ $< && mv $@~ $@

.PHONY: all clean
.SUFFIXES:
.SUFFIXES: .po .mo .css .min.css
