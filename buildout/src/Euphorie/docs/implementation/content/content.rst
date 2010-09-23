
Content types
=============

A survey is a hierarchical questionnaire. This maps very well on the
hierarchical structure used for Plone content, which allows us to reuse the
standard Plone interface for content editing.

Technology
-----------

Standard Plone content types are based on Archetypes. These are very flexible
and well supported, but have some downsides that make them undesirable for
Euphorie:

- Archetypes objects are large, which makes them slow to load from the ZODB,
  and reduces cache efficiency.
- Archetypes does not handle unicode text very well; while it stores data
  in unicode its API always uses encoded strings.
- Archetypes has lots of unneeded complexity and few tests, which can make
  debugging problems or extending it very hard.

For these reasons the implementation is based on Dexterity_ instead. Dexterity
offers light weight objects, a clean design and has excellent test coverage,
making it an excellent basis.

.. _Dexterity: http://svn.plone.org/svn/plone/plone.dexterity/trunk/README.txt

