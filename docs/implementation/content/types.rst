.. _content_types:

Content types
=============

Sector
------

A sector is a sector of industry in a specific country. Sector objects act
both as a container for all content for a sector organisation and as a
Plone user account object. 


Survey group
------------

A survey group is a container which can contain multiple versions of a
survey. It only defines fields which have to be the same for all versions
of a survey.

The title of a survey group is shown to users in the client. The title
of surveys themselves are only used internally as a version name.

Each survey group is associated with a country specific classification code,
which uniquely identifies the type of industry the survey is targeted to. This
code is based on the revision 2 of the `NACE code`_, possibly extended with
extra digits.

.. _NACE code: http://ec.europa.eu/competition/mergers/cases/index/nace_all.html


Fields
~~~~~~

+----------------------+---------------------------------------------------+
| Field name           | Description                                       |
+======================+===================================================+
| title                | Survey group title, shown to users in the client. |
+----------------------+---------------------------------------------------+
| classification_code  | NACE-based classification code.                   |
+----------------------+---------------------------------------------------+
| language             | Language used in the survey.                      |
+----------------------+---------------------------------------------------+


Survey
------

The survey object is the root of a survey.

All content inside a sector has a unique id. This id is unique within the
sector, not globally.

Content in a survey can only be deleted if the survey has not been published
yet. This is managed via the :ref:`survey <workflow-survey>` workflow, which
controls the Zope2 ``Delete objects`` permission. There is an exception
for site managers (users with the ``Manager`` role): they are always
allowed to delete objects.


Module
------

Questions in a survey can be grouped in *modules*. A module is normally used
for grouping. A module can be marked as being optional.

.. attention:: Optional modules are a new feature in Euphorie. In the RIE
   system this was implemented by a special question type.
   

Fields
~~~~~~

+--------------------+-----------------------------------------------+
| Field name         | Description                                   |
+====================+===============================================+
| title              | Module title, shown in the navigation tree.   |
+--------------------+-----------------------------------------------+
| description        | Description, shown in identication and        |
|                    | evaluation phases.                            |
+--------------------+-----------------------------------------------+
| solution_direction | Description text for solution directions for  |
|                    | risks in this module. Shown during the action |
|                    | plan phase.                                   |
+--------------------+-----------------------------------------------+
| optional           | Indicates whether this module is optional.    |
+--------------------+-----------------------------------------------+

Risk
--------

The question content type is used for all questions asked (except profile
questions). There are two major question types: filter questons and risks.
A filter question can be used to make (part of) a module optional: if the
user answers *yes* to a filter question all further elements in the same
module will be skipped.


Fields
~~~~~~

+----------------------+-------------------------------------------------+
| Field name           | Description                                     |
+======================+=================================================+
| title                | Risk statement, shown in inventorisation phase. |
|                      | Also shown during evaluation and action plan    |
|                      | phases if no *problem_description* is provided. |
+----------------------+-------------------------------------------------+
| description          | Description, shown identification phase. Also   | 
|                      | shown during evaluation and action plan phases  |
|                      | if no *problem_description* is provided.        |
+----------------------+-------------------------------------------------+
| risk_type            | The risk type (risk, policy or top5).           |
+----------------------+-------------------------------------------------+
| show_notapplicable   | Indicate if a ''not applicable'' option should  |
|                      | given in addition to the standard ''yes'' and   |
|                      | ''no'' answers.                                 |
+----------------------+-------------------------------------------------+
| evaluation_method    | The evaluation method used for a risk.          |
+----------------------+-------------------------------------------------+
| default_probability  | Default probability for calculated evaluation.  |
+----------------------+-------------------------------------------------+
| default_frequency    | Default frequency for calculated evaluation.    |
+----------------------+-------------------------------------------------+
| default_effect       | Default effect for calculated evaluation.       |
+----------------------+-------------------------------------------------+
| image                | An image to show with this question.            |
+----------------------+-------------------------------------------------+
| links                | A list of URLs pointing to sites with more      |
|                      | information. Every link has both a URL and a    |
|                      | title.                                          |
+----------------------+-------------------------------------------------+
| legal_reference      | Text explaining related law and policies.       |
+----------------------+-------------------------------------------------+
| skip_condition       | An expression which determins if this question  |
|                      | should be skipped.                              |
+----------------------+-------------------------------------------------+

.. attention:: In the RIE system two fields are used for legal reference: a
   reference code for an article of law, and explanatory text. 

A risk can have standard solutions. These are managed as children of the
risk object.


Question types
~~~~~~~~~~~~~~

There are three different question types:

risk
  A possible risk.

top5
  A top-5 risk. These risks do not have to be evaluated and are always considered
  to be present.

policy
  A question related to health & safety policies.

.. attention:: The RIE system has a fourth type: *filter*. This has been
   replaced by the *optional* flag in a module.


Evaluation methods
~~~~~~~~~~~~~~~~~~
A risk can be evaluated using several different mechanisms:

direct
  Direct evaluation asks the user for the evaluation.

calculated
  Users are asked for the probability, frequency and effect. The answers are
  multiplied to determine the evaluation.

none
  No evaluation is necessary.



Solution
--------

A risk can have standard solutions associated with it. These solutions can
be used as a base for a new action plan measure.

Fields
~~~~~~

+----------------------+-------------------------------------------------+
| Field name           | Description                                     |
+======================+=================================================+
| title                | Title for the solution.                         |
+----------------------+-------------------------------------------------+
| solution             | The solution text. This will be copied to the   |
|                      | *measure* field of a new action plan measure.   |
+----------------------+-------------------------------------------------+
| links                | A list of links to pages with extra information.|
+----------------------+-------------------------------------------------+

