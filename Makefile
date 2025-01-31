EUPHORIE_POT   = src/euphorie/deployment/locales/euphorie.pot
EUPHORIE_PO_FILES      = $(wildcard src/euphorie/deployment/locales/*/LC_MESSAGES/euphorie.po)
PLONE_PO_FILES = $(wildcard src/euphorie/deployment/locales/*/LC_MESSAGES/plone.po)
MO_FILES       = $(EUPHORIE_PO_FILES:.po=.mo) $(PLONE_PO_FILES:.po=.mo)

TARGETS        = $(MO_FILES)
SHELL=/usr/bin/env bash

all: ${TARGETS}

clean::
	-rm ${TARGETS}

bin/buildout:
	python3.8 -m venv .
	bin/pip install -r requirements.txt

bin/i18ndude bin/test bin/sphinx-build: bin/buildout buildout.cfg versions.cfg devel.cfg setup.py
	bin/buildout -c devel.cfg -t 10
	touch bin/i18ndude
	touch bin/sphinx-build
	touch bin/test

check:: bin/test ${MO_FILES}
	bin/test -s euphorie

jenkins: bin/test bin/sphinx-build $(MO_FILES)
	bin/test --xml -s euphorie

docs:: bin/sphinx-build
	make -C docs html

clean::
	rm -rf docs/.build

pot:
	i18ndude rebuild-pot --exclude="generated prototype examples illustrations help" --pot $(EUPHORIE_POT) src/euphorie --create euphorie
	$(MAKE) $(MFLAGS) $(EUPHORIE_PO_FILES)

$(EUPHORIE_PO_FILES): src/euphorie/deployment/locales/euphorie.pot
	msgmerge --update -N --lang `echo $@ | awk -F"/" '{print ""$$5}'` $@ $<

.po.mo:
	msgfmt -c --statistics -o $@ $<

.PHONY: all clean docs jenkins pot
.SUFFIXES:
.SUFFIXES: .po .mo .css .min.css
