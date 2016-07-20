:mod:`euphorie.content.behaviour`
=================================

.. module:: euphorie.content.behaviour

The :py:mod:`euphorie.content.behaviour` package implements variours behaviours
of content in the site. Some of these are implemented using `plone.behavior`_
and configured using the FTI, others are implemented using more traditional
patterns.

.. _plone.behavior: http://pypi.python.org/pypi/plone.behavior


.. automodule:: euphorie.content.behaviour.richdescription

  .. autointerface: IRichDescription

.. automodule:: euphorie.content.behaviour.uniqueid

  .. autointerface:: IIdGenerationRoot

  .. autointerface:: INameFromUniqueId

  .. autoclass:: UniqueNameChooser
     :members:

 
.. automodule:: euphorie.content.behaviour.dirtytree

   .. autointerface:: IDirtyTreeRoot

   .. autofunction:: clearDirty

   .. autofunction:: isDirty

