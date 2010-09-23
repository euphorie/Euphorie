#!/bin/sh

i18ndude rebuild-pot --pot locales/euphorie.pot \
	--create euphorie \
	--merge locales/euphorie-manual.pot \
	.

for lang in bg ca cy da de el en es eu fr ga gd gl hr hu it kw lt lv mt \
		nl pl pt ro se sk sl sv tr ; do
	[ -d locales/$lang/LC_MESSAGES ] || mkdir -p locales/$lang/LC_MESSAGES
	[ -f locales/$lang/LC_MESSAGES/euphorie.po ] || touch locales/$lang/LC_MESSAGES/euphorie.po
	i18ndude sync --pot locales/euphorie.pot locales/$lang/LC_MESSAGES/euphorie.po
done


