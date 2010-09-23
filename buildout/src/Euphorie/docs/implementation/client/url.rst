URL handling
============

It is important to have sensible URLs for every item in a survey. This means
it is not possible to use the ZODB structure for URLs since: the ZODB structure
does not map directly to the users unique survey tree due to profile questions
influencing the tree contents, and every item must have separate URLs for the
identification, evaluation and action plan phase.

To solve this a special *publish traverser* for the ZODB Survey object is used.
This traverser is only triggered when using the IClientSkinLayer so as not to
influence the normal content editing activities.

A second trigger for the traverser is one of the terms ''identification'',
''evaluation'' and ''actionplan''. If one of these is the first path component
the request is decorated with an extra skin layer indicating the current phase.

Next the traverse will look for numeric path elements that could reflect nodes
in the survey tree as stored in the SQL database. It will look for the longest
traversal path that can be found in the database, remove that from the traversal
stack and build an acquisition chain that reflects the path with the SQLAlchemy
model instance as tail node. This allows Zope2 to use SQL objects as normal
data objects on which you can call absolute_url(), getPhysicalPath() and from
where further traversal to find views or other objects can happen.

