#!/usr/bin/env python
# coding=utf-8
import os
import re
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(sys.argv[0])

THEME_DIR = os.path.join("src", "euphorie", "client", "resources")
HELP_DIR = os.path.join("src", "euphorie", "client",
                        "resources", "oira", "help")

patt_webpack = re.compile("__webpack_require__.p[ ]*=[ ]*\"(.*)?\";")


def strip_help(filepath):
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
    delta = len(filepath.split("/")) - 7
    shim = "../" * delta
    content = content.replace(
        '="/assets/oira/help/', '="' + shim)

    for folder in ('style', 'script', 'favicon'):
        content = content.replace(
            '="/assets/oira/' + folder + '/', '="../' + shim + folder + '/')

    # remove the top navigation for the main pages
    if filepath.split("/")[-2] != "illustrations":
        p = re.compile('<header id="toolbar">.*</header>',
                       re.I | re.S | re.L | re.M)
        content = p.sub('', content)
        p = re.compile('<div id="browser">.*?</div>',
                       re.I | re.S | re.L | re.M)
        content = p.sub('', content)

    content = content.replace(
        '="/depts/index', '="++resource++euphorie.resources/oira/depts.html')

    # replace paths to images, which can be src=, href= or url()
    patt = re.compile('(href=\"|src=\"|url\()(/media)')

    def repl(match):
        return match.group().replace(match.group(2), "../../../media")
    content = patt.sub(repl, content)

    open(filepath, "w").write(content)


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

    content = content.replace(
        "url(/media/", "url(++resource++euphorie.resources/media/"
    )

    open(filepath, "w").write(content)


def run():
    # Recursively walk the help directory and replace in all html files.
    # https://stackoverflow.com/a/3964691/1337474
    for root, dirs, files in os.walk(HELP_DIR):
        for file in files:
            if file.endswith(".html"):
                strip_help(os.path.join(root, file))

    fix_urls(os.path.join(THEME_DIR, "daimler", "style", "all.css"))
    fix_urls(os.path.join(THEME_DIR, "oira", "style", "all.css"))


if __name__ == "__main__":
    run()
