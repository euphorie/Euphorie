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


.PHONY: resources-install
resources-install:
	@echo "🧪 Copy resources from prototype."

	@cp -R prototype/_site/assets/* src/euphorie/client/resources/
	@cp -R prototype/_site/media src/euphorie/client/resources/
	@cp prototype/_site/depts/index.html src/euphorie/client/resources/oira/depts.html

	@echo "🧪 Fix resource paths."

	@./scripts/proto2diazo.py &> /dev/null

	@echo "🧪 Git add and commit."

	@# Prototype and Euphorie handle Patternslib bundle inclusion differently.
	@# Let's update the bundle in a different step.
	@rm -Rf src/euphorie/client/resources/oira/script/
	@git checkout src/euphorie/client/resources/oira/script
	@# Store the prototype commit id for better reproducibility.
	@$(eval PROTOTYPE_COMMIT_ID := $(shell cd prototype && git rev-parse --verify HEAD))
	@echo $(PROTOTYPE_COMMIT_ID) > LATEST-PROTOTYPE
	@# Add and commit.
	@git add src/euphorie/client/resources LATEST-PROTOTYPE
	@# commit, but ignore if nothing is to commit.
	-@git commit -m"Update prototype from commit $(PROTOTYPE_COMMIT_ID)" > /dev/null

	@# Spit out info.
	@echo ""
	@echo "📦 Resource dir size is: "
	@cd src/euphorie/client/resources/ && du -sh
	@echo ""
	@echo "⚡ To update Patternslib:"
	@echo "  - run ``make update-patterns``,"
	@echo "  - or for a speficic version other than the latest non-pre release:"
	@echo "    ``PATTERNSLIB_VERSION=9.7.0-alpha.5 make update-patterns``"
	@echo ""
	@echo "🗿 To update the oira.cms bundle, go to ../NuPlone and run ``make bundle`` there."
	@echo ""
	@echo "✅ Updated prototype from commit $(PROTOTYPE_COMMIT_ID)"
	@echo ""


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


# From: oira.prototype
# Download the latest Patternslib universal bundle from GitHub releases and
# replace the existing one.
# Also see: https://stackoverflow.com/a/42040905/1337474
# You can use the `PATTERNSLIB_VERSION` environment variable to download a
# specific version, e.g. a pre-release version which would not be picked up
# automatically.
# This can be used like so:
# `PATTERNSLIB_VERSION=9.7.0-alpha.5 make update-patterns`
.PHONY: update-patterns
update-patterns:
ifndef PATTERNSLIB_VERSION
	@echo "🧪 Get the latest Patternslib version from GitHub (no pre-release)."

	@# If no PATTERNSLIB_VERSION environment variable is defined,
	@# Get the latest version from the GitHub API.
	$(eval PATTERNSLIB_VERSION := $(shell curl https://api.github.com/repos/patternslib/Patterns/releases/latest -s | jq .tag_name -r))
	@echo "🏷️  Patternslib version is: $(PATTERNSLIB_VERSION)"

endif
	@echo "🧪 Copy bundle from GitHub."

	@# Download the Patternslib bundle.
	wget https://github.com/Patternslib/Patterns/releases/download/$(PATTERNSLIB_VERSION)/patternslib-bundle-$(PATTERNSLIB_VERSION).zip 1> /dev/null 2> /dev/null
	@unzip patternslib-bundle-$(PATTERNSLIB_VERSION).zip > /dev/null
	@# Replace the old Patternslib with the new one.
	@rm -Rf src/euphorie/client/resources/oira/script
	@mv patternslib-bundle-$(PATTERNSLIB_VERSION) src/euphorie/client/resources/oira/script
	@# Cleanup.
	@rm patternslib-bundle-$(PATTERNSLIB_VERSION).zip

	@echo "🧪 Git add and commit."

	@# Add and commit.
	@echo $(PATTERNSLIB_VERSION) > LATEST-PATTERNSLIB
	@git add src/euphorie/client/resources/oira/script LATEST-PATTERNSLIB
	@# commit, but ignore if nothing is to commit.
	-@git commit -m"Update Patternslib to $(PATTERNSLIB_VERSION)." > /dev/null

	@# Spit out info.
	@echo ""
	@echo "📦 Script dir size is: "
	@cd src/euphorie/client/resources/oira/script && du -sh
	@echo ""
	@echo "🚀 Updated Patternslib to $(PATTERNSLIB_VERSION)."
	@echo ""


.PHONY: all clean docs jenkins pot
.SUFFIXES:
.SUFFIXES: .po .mo .css .min.css
