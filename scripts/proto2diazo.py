#!/usr/bin/env python
# coding=utf-8
import os
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(sys.argv[0])

THEME_DIR = os.path.join("src", "euphorie", "client", "resources")
HELP_DIR = os.path.join("src", "euphorie", "client",
                        "resources", "oira", "help")


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

    delta = len(filepath.split("/")) - 6
    shim = "../" * delta
    content = content.replace("url(/media/", "url(++resource++euphorie.media/")
    content = content.replace("=\"/assets/oira/", "=\"" + shim)
    content = content.replace("=\"//assets/oira/", "=\"" + shim)
    content = content.replace("=\"/media/", "=\"" + shim + "media/")

    open(filepath, "w").write(content)


def run():
    # Recursively walk the help directory and replace in all html files.
    # https://stackoverflow.com/a/3964691/1337474
    for root, dirs, files in os.walk(HELP_DIR):
        for file in files:
            if file.endswith(".html"):
                fix_urls(os.path.join(root, file))

    fix_urls(os.path.join(THEME_DIR, "daimler", "style", "all.css"))
    fix_urls(os.path.join(THEME_DIR, "oira", "style", "all.css"))


if __name__ == "__main__":
    run()
