EUPHORIE_POT   = src/euphorie/deployment/locales/euphorie.pot
EUPHORIE_PO_FILES      = $(wildcard src/euphorie/deployment/locales/*/LC_MESSAGES/euphorie.po)
PLONE_PO_FILES = $(wildcard src/euphorie/deployment/locales/*/LC_MESSAGES/plone.po)
MO_FILES       = $(EUPHORIE_PO_FILES:.po=.mo) $(PLONE_PO_FILES:.po=.mo)

TARGETS        = $(MO_FILES)
SHELL=/bin/bash

all: ${TARGETS}

clean::
	-rm ${TARGETS}

bin/buildout:
	virtualenv -p python2.7 --clear --no-site-packages .
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

pot: bin/i18ndude
	i18ndude rebuild-pot --exclude="generated prototype examples" --pot $(EUPHORIE_POT) --merge src/euphorie/deployment/locales/plone.pot src/euphorie --create euphorie
	$(MAKE) $(MFLAGS) $(EUPHORIE_PO_FILES)

$(EUPHORIE_PO_FILES): src/euphorie/deployment/locales/euphorie.pot
	msgmerge --update -N --lang `echo $@ | awk -F"/" '{print ""$$5}'` $@ $<

########################################################################
## Setup
## You don't run these rules unless you're a prototype dev

clean-proto:
	cd prototype && make clean

prototype:: ## Get the latest version of the prototype
	@if [ ! -d "prototype" ]; then \
		git clone git@github.com:syslabcom/oira.prototype.git prototype; \
	else \
		cd prototype && git pull; \
	fi;

bundle: prototype
	cd prototype && make bundle-osha

jekyll: prototype
	@echo 'DO: rm prototype/stamp-bundler to force Jekyll re-install'
	@cd prototype && make jekyll

## resources-install: bundle jekyll
resources-install:
	cp prototype/bundles/bundle* src/euphorie/client/resources
	cp -R prototype/bundles/chunks/* src/euphorie/client/resources/bundles/chunks/
	cp -R prototype/_site/style/* src/euphorie/client/resources
	@./scripts/proto2diazo.py
	@echo "Make sure to go to ../NuPlone, make bundle there, and copy oira.cms* to src/euphorie/client/resources"

.po.mo:
	msgfmt -c --statistics -o $@ $<

.PHONY: all clean docs jenkins pot
.SUFFIXES:
.SUFFIXES: .po .mo .css .min.css
