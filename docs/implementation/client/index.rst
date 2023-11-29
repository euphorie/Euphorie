Online client
=============

:mod:`euphorie.client` contains the *client* for the Euphorie surveys. The
client is the web interface normal users interact with. It uses the content
types from the :mod:`euphorie.content` package, combined with a SQL database
to store session data.

This packages also contains the logic to copy a survey from the content
management section of the Plone site to a special client area. This action
is called *publication of a survey*.

.. toctree::
   :maxdepth: 2

   cookies
   flow
   localisation
   session
   url
   users
   registry

