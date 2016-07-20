Session handling
================

The state of a survey needs to be remembered. The state consists of a lot of
data: the profile, evaluation, inventory, action plan answers and
company details. This is too much information to manage via form variables
or HTTP cookies so we need to use a server-side storage mechanism. The Zope
session mechanism is known to quickly generate a lot of conflicts, which
makes it unsuitable (the faster_ product improves things a lot though). An
extra requirement to consider is that we expect to need to handle persistent
sessions in the future. In light of these considerations the session system
is based on a SQL database.

.. _faster: http://agendaless.com/Members/tseaver/software/faster/


.. _survey_tree:

Survey tree
-----------

A survey starts with all profile questions. Once these have been answered a tree
is generated for all items (modules and risks) that are exposed to the user via
the survey user interface. This also takes care of profile questions: modules
are skipped or repeated as necessary based on the profile question answers.

This tree is stored in a mixed path enumeration (also called materialized tree)
and adjancency list model. This combination of models allows for fast location
of tree nodes during traversal as well as an efficient way to walk up the tree
to find parent nodes.

As path a simple numbering scheme is used, which makes it possible to convert
the path into a dotted numbering scheme in the user interface. For example this
survey::

   1. Do you have a mobile shop?
   1.1 Is it serviced annually?
   1.2 Is the tire pressured checked every week?
   2. Are you open nights?
   ..
   ..

will have ''001'', ''001001'', ''001002'' and ''002'' as paths in the
database.

Each survey has a session record in the database which holds data for the
session ans is located using a HTTP cookie. Each session has its own tree with
module and question information.


.. _schema_structure:

Schema structure
----------------

Session information is stored in a series of SQL tables.


+----------------+---------------------------------------------+
| Table          | Description                                 |
+================+=============================================+
| account        | Registered users.                           |
+----------------+---------------------------------------------+
| tree           | Tree node data.                             |
+----------------+---------------------------------------------+
| session        | User sessions. Each session is a tree root. |
+----------------+---------------------------------------------+
| profile_answer | An answer to a profile question.            |
+----------------+---------------------------------------------+
| module         | A module.                                   |
+----------------+---------------------------------------------+
| risk           | Answers for a risk (for all phases).        |
+----------------+---------------------------------------------+
| action_plan    | Action plan items for questions.            |
+----------------+---------------------------------------------+

The session table has a modification timestamp which is used to remove stale
sessions. This timestamp is also updated when the session is resumed. This
guarantees that a session does not expire if a user looks at an earlier
session but does not make any changes.

For performance reasons every row in the tree table lists the title for the
item and a pointer to the root session. This makes it possible to build a
tree without having to load any objects from the ZODB.

Because the tree consists of modules and risks, each record in the *tree* table
can be either a module or a risk. The *type* column is set to *module* or *risk*
accordingly.
The *path* column holds the path as explained in :ref:`survey_tree` while
*zodb_path* is a reference to the corresponding Plone object (see
:ref:`content_types`).

Modules and risks each have additional attributes which are stored
in the *module* and *risk* tables respectively.

The *action_plan* table stores information entered in the action plan phase.

.. graphviz:: relationships.real.large.dot
