Behaviours
==========

The :mod:`euphorie.content.behaviour` package implements variours behaviours
of content in the site. Some of these are implemented using `plone.behavior`_
and configured using the FTI, others are implemented using more traditional
patterns.

.. _plone.behavior: http://pypi.python.org/pypi/plone.behavior


.. automodule:: euphorie.content.behaviour.deprecation

  .. autoclass:: IDeprecatable
     :members:

  .. autoclass:: WorkflowDeprecatable
     :members:


.. automodule:: euphorie.content.behaviour.maxdepth

  .. autoclass:: SurveyDepthConstructionFilter
     :members:


.. automodule:: euphorie.content.behaviour.publish

  .. autoclass:: IPublishRemovalProtection
     :members:

  .. autoclass:: CheckObjectRemoval
     :members:

  .. autoclass:: IObjectPublishedEvent
     :members:

  .. autoclass:: ObjectPublishedEvent
     :members:

  .. autoclass:: ObjectPublished
     :members:


.. automodule:: euphorie.content.behaviour.richdescription

  .. autoclass: IRichDescription
     :members:

.. automodule:: euphorie.content.behaviour.uniqueid

  .. autoclass:: IIdGenerationRoot
     :members:

  .. autoclass:: INameFromUniqueId
     :members:

  .. autoclass:: UniqueNameChooser
     :members:

 
