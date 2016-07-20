Plone modifications
===================

Reducing Plone behaviour
------------------------

Plone_ is a very rich Content Management System. Euphorie only requires a
small subset of Plone's features; all the extra features Plone offers
add extra complexity to the user interface or have a possible performance
impact.

This :mod:`euphorie.deployment` package disables various parts of Plone
to make it better fit the Euphorie requirements:

* content rules are disabled
* automatic creation of redirects for moved content are disabled
* the *sharing* page is disabled

.. _Plone: http://plone.org


Login behaviour
---------------

Euphorie modifies the login behaviour of Plone a little bit: if a user has a
home folder in the site he will be redirected to that folder after logging in.
This is used for sectors accounts: the home folder location in the
`portal_membership` tool is set to the `sectors` object in the site root, which
is where all sectors live. This means that if a sector account logs in he
will automatically be redirected to his own *home*.


