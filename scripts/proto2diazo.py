#!/usr/bin/env python
# coding=utf-8
import os
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(sys.argv[0])

THEME_DIR = os.path.join("src", "euphorie", "client", "resources")


def fix_urls(filepath):
    """ Fix the urls in filepath
    """
    logger.info("Rewriting resource URLs in %s", filepath)
    content = None
    try:
        with open(filepath) as f:
            content = f.read()
    except:
        logger.exception("Problem reading %s", filepath)
        return

    content = content.replace("url(/media/", "url(++resource++euphorie.media/")
    open(filepath, "w").write(content)


def run():
    ## Recursively walk the theme directory and replace in all CSS files.
    ## https://stackoverflow.com/a/3964691/1337474
    # for root, dirs, files in os.walk(THEME_DIR):
    #    for file in files:
    #        if file.endswith(".css"):
    #            fix_urls(os.path.join(root, file))

    fix_urls(os.path.join(THEME_DIR, "daimler", "style", "all.css"))
    fix_urls(os.path.join(THEME_DIR, "oira", "style", "all.css"))


if __name__ == "__main__":
    run()
