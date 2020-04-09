#!/usr/bin/env python
# coding=utf-8
from os.path import join

import os
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(sys.argv[0])

PROTO_STYLE_DIR = join('prototype', '_site', 'style')
THEME_DIR = join('src', 'euphorie', 'client', 'resources')


def fix_urls(filename):
    ''' Fix the urls in filename
    '''
    logger.info("Rewriting resource URLs in %s", filename)
    path = join(PROTO_STYLE_DIR, filename)
    target = join(THEME_DIR, filename)
    try:
        with open(path) as f:
            content = f.read()
    except:
        logger.exception('Problem reading %s', filename)
        return

    content = (
        content
        .replace(
            'url(/media/',
            'url(++resource++euphorie.media/'
        )
    )
    try:
        os.makedirs(os.path.dirname(target))
    except OSError:
        if not os.path.isdir(os.path.dirname(target)):
            raise
    open(target, 'w').write(content)


def run():
    fix_urls('screen.css')


if __name__ == '__main__':
    run()
