============
Installation
============

Euphorie is implemented as a set of add-on products for `Plone`_. To install
Euphorie you will first need to `download`_ and install Plone. Euphorie
requires Plone 3.3 or later. Plone 4 is supported, but currently not yet
recommended.

After installing Plone you can install Euphorie. To do this you will need
to edit the ``buildout.cfg`` file of your Plone installation. This file
is normally located in the ``zinstance`` directory if your Plone install.
Look for an *eggs* line and add Euphorie there::

  [buildout]
  ...
  eggs =
      Euphorie

This will instruct Plone to install the Euphorie software. Next you will
need to add some *zcml* entries to load the necessary configuration as well::

  [instance]
  ...
  zcml =
      euphorie.deployment-meta
      euphorie.deployment
      euphorie.deployment-overrides

After making these two changes you must (re)run buildout and restart your Zope
instance. Navigate to your ``zinstance`` directory and type::

    $ bin/buildout
    $ bin/plonectl restart

A new *Euphorie website* option should now appear in the list of add-on products
in your Plone control panel. Installing this will setup Euphorie in your site.

For more information on installing add-on products in your Plone site please
see the article `installing an add-on product`_ in the Plone knowledge base.

.. _Plone: http://plone.org/
.. _download: http://plone.org/download
.. _installing an add-on product: http://plone.org/documentation/kb/third-party-products/installing
