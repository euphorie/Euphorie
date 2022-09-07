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

pot: bin/i18ndude
	i18ndude rebuild-pot --exclude="generated prototype examples illustrations help" --pot $(EUPHORIE_POT) src/euphorie --create euphorie
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

jekyll:
	@echo 'DO: rm prototype/stamp-bundler to force Jekyll re-install'
	@cd prototype && make jekyll


.PHONY: bundle
bundle: resources-install
resources-install:   # bundle
	cp -R prototype/_site/assets/* src/euphorie/client/resources/
	## For the script directory, always start with a clean slate
	rm -rf src/euphorie/client/resources/oira/script
	## Copy the bundle directly from assets, not from _site
	cp -R prototype/assets/oira/script src/euphorie/client/resources/oira/
	cp -R prototype/_site/media src/euphorie/client/resources/
	cp prototype/_site/depts/index.html src/euphorie/client/resources/oira/depts.html
	@./scripts/proto2diazo.py
	@echo "To update the oira.cms bundle, go to ../NuPlone and run ``make bundle`` there."


.po.mo:
	msgfmt -c --statistics -o $@ $<

theme: jekyll resources-install


# DEV

# Create symbolic links from prototype's script directory to this packages resource directory.
# You can then do a ``yarn watch`` in oira.prototype, devlop Patternslib and get your changes updated here.
.PHONY: devln
devln:
	@cd src/euphorie/client/resources/oira &&\
		rm -Rf script/ &&\
		ln -s ../../../../../prototype/assets/oira/script ./script &&\
		echo "Created symbolic link to prototype's bundles for developing in:" &&\
		ls -la .

# Undo devln
.PHONY: undevln
undevln:
	@cd src/euphorie/client/resources/oira &&\
		unlink script &&\
		git checkout . &&\
		echo "Restored generated bundles"


.PHONY: all clean docs jenkins pot
.SUFFIXES:
.SUFFIXES: .po .mo .css .min.css
