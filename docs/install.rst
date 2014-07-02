Installation
============

Euphorie is implemented as a set of add-on products for `Plone`_. The
requirements for running an Euphorie site are:

* Plone 4.0 or later.
* a SQL database
* two separate virtual hosts

Development files required on the host operating system:

* libffi (Foreign Function Interface library development files)

e.g. on Debian/Ubuntu: ``sudo apt-get install libffi-dev``

Plone instalation
-----------------
To install Euphorie you will first need to `download`_ and install Plone.
Euphorie requires Plone 3.3 or later.  After installing Plone you can install
Euphorie. To do this you will need to edit the ``buildout.cfg`` file of your
Plone installation. This file is normally located in the ``zinstance``
directory if your Plone install.  Look for an *eggs* line and add Euphorie
there::

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
    $ bin/instance restart

A new *Euphorie website* option should now appear in the list of add-on products
in your Plone control panel. Installing this will setup Euphorie in your site.

For more information on installing add-on products in your Plone site please
see the article `installing an add-on product`_ in the Plone knowledge base.

Configuration
-------------

Euphorie uses `z3c.appconfig <http://pypi.python.org/pypi/z3c.appconfig>`_ to
handle application configuration. All values are stored in the ``euphorie``
section. For example::

  [euphorie]
  client=http://oira.example.com

The available options are:

. table:: configuration options

   +--------------------------+---------------------------------------+
   | options                  | Description                           |
   +==========================+=======================================+
   | ``client``               | URL for the client (see also          |
   |                          | :ref:`Virtual hosting`.               |
   +--------------------------+---------------------------------------+
   | ``terms-and-conditions`` | Boolean flag indicating it the client |
   |                          | must ask users to accept the terms    |
   |                          | and conditions of the site.           |
   +--------------------------+---------------------------------------+

Google analytics
----------------

Euphorie includes complete Google Analytics support. To enable this you
will need to configure the GA account, and optionally the domain name to
use. This must be done separately for the CMS and the client.

::

    [tile:footer]
    type=analytics
    account=UA-111111-1
    domain=.example.com

    [tile:client-analytics]
    type=analytics
    account=UA-111111-1
    domain=.example.com


SQL database
------------

Euphorie uses a SQL database to store information for users of the client. Any
SQL database supported by SQLALchemy_ should work. If you have selected a
database you will need to configure it in ``buildout.cfg``. For example if
you use postgres you will first need to make sure that the psycopg_ driver
is installed by adding it to the *eggs* section::

  [buildout]
  ...
  eggs =
      Euphorie
      psycopg2

next you need to configure the database connection information. This requires
a somewhat verbose statement in the *instance* section of ``buildout.cfg``::

  [instance]
  zcml-additional =
     <configure xmlns="http://namespaces.zope.org/zope"
                xmlns:db="http://namespaces.zope.org/db">
         <include package="z3c.saconfig" file="meta.zcml" />
         <db:engine name="session" url="postgres:///euphorie" />
         <db:session engine="session" />
     </configure>

Make sure The ``url`` parameter is correct for the database you want to use.
It uses the standard SQLAlchemy connection URI format.

To setup the database you must run buildout and run the database initialisation
command::

    $ bin/buildout
    $ bin/instance initdb

.. note::

   You need Zope 2.12.12 or later to be able to use the ``initdb`` command. For
   earlier Zope versions you need to specify the path for the
   :py:mod:`euphorie.deployment.commands.xmlimport` module on the command line.


Virtual hosts
-------------

Euphorie requires two separate virtual hosts: one host for the client, and one
for CMS tasks. It is common to use ``oira.example.com`` as hostname for the
client and ``admin.oira.example.com`` as hostname for the CMS. The standard
method for configuring virtual hosting for Plone sites apply here as well. The
Plone website has instructions for `configuring Plone with Apache`_ and
`configuring Plone with Enfold Proxy on Windows`_. Here is an example Apache
configuration::

  <VirtualHost *:80>
      ServerName admin.oira.example.com
      ProxyPass / http://localhost:8080/VirtualHostBase/http/admin.oira.example.com:80/Plone/VirtualHostRoot/

      # Prevent access to the client using the administrative site.
      <Location /client>
          order allow, deny
          deny form all
      </Location>
  </VirtualHost>

  <VirtualHost *:80>
      ServerName oira.example.com
      ProxyPass / http://localhost:8080/VirtualHostBase/http/admin.oira.example.com:80/Plone/client/VirtualHostRoot/
  </VirtualHost>


You will also need to configure the URL for the client in the ``euphorie.ini`` file::

  [euphorie]
  client=http://oira.example.com



.. _Plone: http://plone.org/
.. _download: http://plone.org/download
.. _installing an add-on product: http://plone.org/documentation/kb/add-ons/installing
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _psycopg: http://initd.org/psycopg/
.. _configuring Plone with Apache: http://plone.org/documentation/kb/plone-with-apache
.. _configuring Plone with Enfold Proxy on Windows: http://plone.org/documentation/kb/managing-your-plone-sites-in-windows-with-enfold-proxy

