Euphorie buildout
=================

This buildout supports both Plone 3 and Plone 4. In order to prevent accidental
switches between Plone versions there is no buildout.cfg file, requiring you
to always specify the desired version.

To create a Plone 3 buildout run these commands::

  $ python2.4 bootstrap.py -c plone3.cfg
  $ bin/buildout -c plone3.cfg

To create a Plone 4 buildout run these commands::

  $ python2.6 bootstrap.py -c plone4.cfg
  $ bin/buildout -c plone4.cfg

Note that Python 2.6 is required for Plone 4.
