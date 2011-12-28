YUICOMPRESS	?= yui-compressor
PYTHON		?= python2.6

CSS_PACK	= $(YUICOMPRESS) --charset utf-8 --nomunge
CSS_DIR		= src/euphorie/client/templates/style/main
CSS_TARGETS	= $(CSS_DIR)/screen.min.css \
		  $(CSS_DIR)/screen-ie7.min.css \
		  $(CSS_DIR)/screen-ie8.min.css \
		  $(CSS_DIR)/screen-osha.min.css

JS_PACK		= $(YUICOMPRESS) --charset utf-8
JS_DIR		= src/euphorie/client/templates
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

EUPHORIE_POT	= src/euphorie/deployment/locales/euphorie.pot
EUPHORIE_PO_FILES	= $(wildcard src/euphorie/deployment/locales/*/LC_MESSAGES/euphorie.po)
PLONE_PO_FILES	= $(wildcard src/euphorie/deployment/locales/*/LC_MESSAGES/plone.po)
MO_FILES	= $(EUPHORIE_PO_FILES:.po=.mo) $(PLONE_PO_FILES:.po=.mo)

TARGETS		= $(CSS_TARGETS) $(JS_TARGETS) $(MO_FILES)

all: ${TARGETS}

clean:
	-rm ${TARGETS}

bin/buildout: bootstrap.py
	$(PYTHON) bootstrap.py

bin/test bin/sphinx-build: bin/buildout buildout.cfg versions.cfg devel.cfg setup.py
	bin/buildout -c devel.cfg
	touch bin/test
	touch bin/sphinx-build

check:: bin/test ${MO_FILES}
	bin/test

check:: bin/sphinx-build
	$(MAKE) -C docs linkcheck

jenkins: bin/test bin/sphinx-build ${MO_FILES}
	bin/test --xml -s euphorie

$(JS_DIR)/behaviour/common.min.js: ${JQUERY} ${JQUERY_UI} ${EXTRAS} $(JS_DIR)/behaviour/markup.js
	set -e ; (for i in $^ ; do $(JS_PACK) $$i ; done ) > $@~ ; mv $@~ $@

pot: bin/buildout
	bin/pybabel extract -F babel.cfg \
		--copyright-holder='Simplon B.V., SYSLAB.COM GmbH' \
		--msgid-bugs-address='euphorie@lists.wiggy.net' \
		--charset=utf-8 \
		src/euphorie > $(EUPHORIE_POT)~
	mv $(EUPHORIE_POT)~ $(EUPHORIE_POT)	

$(EUPHORIE_PO_FILES): src/euphorie/deployment/locales/euphorie.pot
	msgmerge --update $@ $<

$(PLONE_PO_FILES): src/euphorie/deployment/locales/plone.pot
	msgmerge --update $@ $<

%.min.css: %.css
	set -e ; $(CSS_PACK) $< > $@~ ; mv $@~ $@

.po.mo:
	msgfmt -c --statistics -o $@~ $< && mv $@~ $@

.PHONY: all clean jenkins pot
.SUFFIXES:
.SUFFIXES: .po .mo .css .min.css
