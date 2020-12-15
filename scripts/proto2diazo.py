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

ILLUSTRATION_JS_SNIPPET = """
    <script>window.__patternslib_public_path__ = "/++resource++euphorie.resources/oira/script/";</script>
    <script src="/++resource++euphorie.resources/oira/script/polyfills-loader.js" type="text/javascript"></script>
"""


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

    # We need to set the __patternslib_public_path__ in our screenshots
    a, b, c = content.partition('<script src="/assets')
    content = "".join((a + ILLUSTRATION_JS_SNIPPET, b, c))

    delta = len(filepath.split("/")) - 7
    shim = "../" * delta
    content = content.replace(
        '="/assets/oira/help/', '="' + shim)
    c_shim = "../" * (delta + 1)
    content = content.replace(
        '="/assets/oira/certificates/', '="' + c_shim + 'certificates/')

    for folder in ('style', 'script', 'favicon'):
        content = content.replace(
            '="/assets/oira/' + folder + '/', '="../' + shim + folder + '/')

    # Replace link for re-loading the toolbar / sidebar
    def repl_link(match):
        return match.group().replace(match.group(1), 'tal:define="webhelpers nocall:context/@@webhelpers;" href="${webhelpers/portal_url}/${webhelpers/selected_country}"')
    if filepath.split("/")[-2] != "illustrations":
        patt = re.compile('<a (href="/").*?id="inject-toolbar".*?>.*?</a>', re.I | re.S | re.L | re.M)
        content = patt.sub(repl_link, content)

    content = content.replace(
        '="/depts/index', '="++resource++euphorie.resources/oira/depts.html')

    # replace paths to images, which can be src=, href= or url()
    patt = re.compile('(href=\"|src=\"|url\()(/media)')

    def repl(match):
        return match.group().replace(match.group(2), "../../../../media")
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
