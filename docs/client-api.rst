Introduction
============

This document describes the client API for the Euphorie. This API allows
interface with the client component of an Euphorie system and can be used
to implement a custom frontend. It exposes client users, surveys, surveys
sessions and all interactions with them. It does not allow for management of
sectors or surveys: this must be done through the standard Euphorie CMS
system.


Concepts
========

Country
-------

A country is the top level grouping item for survey content. There are
different country types to indicate the EU membership status. A country
contains zero or more sectors. 

Sector
------

A sector is a national organisation for a single sector of industry. A sector
can have zero or more surveys.

Survey
------

A survey is a hierarchical questionnaire used identify risks in an environment
and build a plan to tackle them.

Session
-------

A session is an instance of a survey as created by a user and contains all
information provided by the user.


API operations
==============

Error responses
---------------

An error can occur for several reasons: bad data being passed to an API
call, Euphorie encountering an internal error, a disk running out of space,
etc. If this happens an error-response will be returned. These can be
recognized by the ``type`` key being set to ``error``.

::

    {
            "type": "error",
            "message": "Required data missing",
    }



Users
-----

Create new user
~~~~~~~~~~~~~~~

+------+---------------------------+------------------------------+
| Verb | URI                       | Description                  |
+======+===========================+==============================+
| POST | /users                    | Create a new user.           |
+------+---------------------------+------------------------------+

Using this call you can create a new user. The user information must be
supplied in a JSON dictionary::

   {
        "login": "jane@example.com",
        "password": "john",
   }

The ``login`` key is required.  Specifying the password is optional: if a
password is given the user can login with that password on the Euphorie client
directly.  If no password is given access is only possible with the
authentication token returned by this call.

The response is a JSON dictionary with details for the newly created account::

   {
        "token": "e1490672-4015-4572-a036-ba53c45e9509",
        "id": 17,
        "login": "jane@example.com",
        "email": "jane@example.com",
   }

If the login is not a valid email address or another account with the same
email address already exists an error is returned.


User authentication
~~~~~~~~~~~~~~~~~~~

+------+---------------------+------------------------------+
| Verb | URI                 | Description                  |
+======+=====================+==============================+
| POST | /users/authenticate | Authenticate a user.         |
+------+---------------------+------------------------------+

In order to authenticate you must submit a JSON object with two keys:

* ``login``: the users login (this should be an email address)
* ``password``: the users password

If authentication failed an error response is returned with status code 403.
If authentication is succesful a JSON response is returned with an
authentication token and a list of existing sessions::

   {
       "token": "e1490672-4015-4572-a036-ba53c45e9509",
       "id": 17,
       "login": "jane@example.com",
       "email": "jane@example.com",
       "sessions": [
           {
                   "id": 1926,
                   "title": "Hoveniers en Groenvoorzieners",
                   "created": "2010-09-27T11:35:00Z",
                   "modified": "2012-04-23T10:29:13Z",
           },
           {
                   "id": 23945,
                   "title": "Vlakglas",
                   "created": "2010-09-27T11:35:00Z",
                   "modified": "2012-04-23T10:29:13Z",
           },
       ],
   }

The token should be supplied in an ``X-Euphorie-Token`` HTTP header for all
requests that require authentication.

User details
~~~~~~~~~~~~

+------+---------------------+------------------------------+
| Verb | URI                 | Description                  |
+======+=====================+==============================+
| GET  | /users/<userid>     | Return user information.     |
+------+---------------------+------------------------------+

This will return information about the user, including all known sessions. A
user can only request information for his own account: any attempt to request
information on another user will result in a HTTP 403 error response.

::

   {
       "id": 17,
       "login": "jane@example.com",
       "email": "jane@example.com",
       "sessions": [
           {
                   "id": 1926,
                   "title": "Hoveniers en Groenvoorzieners",
                   "created": "2010-09-27T11:35:00Z",
                   "modified": "2012-04-23T10:29:13Z",
           },
           {
                   "id": 23945,
                   "title": "Vlakglas",
                   "modified": "2011-12-06T15:15:24Z",
           },
       ],
   

This token should be supplied in an ``X-Euphorie-Token`` HTTP header for all
requests that require authentication.


Update user
~~~~~~~~~~~

+------+---------------------+------------------------------+
| Verb | URI                 | Description                  |
+======+=====================+==============================+
| PUT  | /users/<userid>     | Update user information.     |
+------+---------------------+------------------------------+

This call allows updating the user information. The only key that can
be updated is ``login``. Currently the login name and email address
are defined to be the same, so updating the login will also update the
users email address.

::

   {
       "login": "jane@example.com",
       "password": "bruce",
   }

The response is identical to the :ref:`user details query <User details>`.


Survey catalog
--------------

List countries
~~~~~~~~~~~~~~

+------+----------+------------------------------+
| Verb | URI      | Description                  |
+======+==========+==============================+
| GET  | /surveys | List all defined countries   |
+------+----------+------------------------------+

Example response::

   {
       "countries": [
           {
                   "id": "nl",
                   "title": "The Netherlands",
                   "type": "eu-member",
           },
           {
                   "id": "be",
                   "title": "Belgium",
                   "type": "eu-member",
           },
   }

The possible country types are:

* ``eu-member``: country is a full EU member state
* ``candidate-eu``: candidate member of the EU
* ``potential-candidate-eu``: potentital candidate member of the EU
* ``efta``: member of the European Free Trade Association
* ``region``: generic region, not an individual country

Note that even though a country has a title frontends are encouraged to use
use locale-specific name for the country. This can be based on the id, which
is guaranteed to be a valid country code. 



List sectors
~~~~~~~~~~~~

+------+--------------------------------------------+-----------------------------------+
| Verb | URI                                        | Description                       |
+======+============================================+===================================+
| GET  | /surveys/<country>                         | List all sectors in a country.    |
+------+--------------------------------------------+-----------------------------------+
| GET  | /surveys/<country>?details                 | List all sectors in a country     |
|      |                                            | including its surveys.            |
+------+--------------------------------------------+-----------------------------------+
| GET  | /surveys/<country>?details&language=<lang> | List all sectors in a country     |
|      |                                            | including all surveys in the given|
|      |                                            | language.                         |
+------+--------------------------------------------+-----------------------------------+

Example response::

   {
       "id": "nl",
       "title": "The Netherlands",
       "type": "eu-member",
       "sectors": [
           {
                   "id": "bovag",
                   "title": "BOVAG",
           },
           {
                   "id": "bovag",
                   "title": "BOVAG",
           },
   }

Example detail response::

   {
       "id": "nl",
       "title": "The Netherlands",
       "type": "eu-member",
       "sectors": [
           {
                   "id": "stigas",
                   "title": "STIGAS",
                   "surveys": [
                       {
                               "id": "akkerbouw-en-vollegrondsgroenteteelt",
                               "title": "Akkerbouw en vollegrondsgroenteteelt",
                               "language": "nl",
                       },
                       {
                               "id": "bos-en-natuur",
                               "title": "Bos en natuur",
                               "language": "nl",
                       }
                       ,
                   ],
           },
           {
                   "id": "dierenartsen",
                   "title": "Dierenartsen",
                   "surveys": [
                       {
                               "id": "dierenartsen",
                               "title": "Dierenartsen",
                               "language": "nl",
                       },
                   ],
           },
   }


List sector details
~~~~~~~~~~~~~~~~~~~

+------+------------------------------------------------+-----------------------------------+
| Verb | URI                                            | Description                       |
+======+================================================+===================================+
| GET  | /surveys/<country>/<sectorid>                  | List details of the given sector. |
+------+------------------------------------------------+-----------------------------------+
| GET  | /surveys/<country>/<sectorid>?language=<lang>  | List details of the given sector, |
|      |                                                | only including surveys in the     |
|      |                                                | given language.                   |
+------+------------------------------------------------+-----------------------------------+


Example response::

   {
           "id": "stigas",
           "title": "STIGAS",
           "surveys": [
                   {
                           "id": "nl/akkerbouw-en-vollegrondsgroenteteelt",
                           "title": "Akkerbouw en vollegrondsgroenteteelt",
                           "language": "nl",
                   },
                   {
                            "id": "nl/bos-en-natuur",
                            "title": "Bos en natuur",
                            "language": "nl",
                    },
           ],
   }


Survey interaction
------------------

The general structure for interacting with a survey is as follows:

1. Authenticate the user
2. Start a new survey session
3. Start identification phase and walk through all identification steps
4. Start evaluation phase and walk through all evaluation steps
5. Start action plan phase and walk through all action plan steps


Standard response components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All responses to API calls involving a survey session follow a standard
structure. They include the following keys:

* ``phase``: the current survey phase. This will be one of ``identification``,
* ``type``: an indicator of the response type. This will be one of ``survey``,
  ``profile``, ``module``, ``risk``, ``update`` or ``error``.
* ``title``: the title for the current context. Depending on the context this
  will be the title of the survey, module or the risk.
* ``previous-step``: a URL pointing to the API location of the previous logical
  step.  If the end start of the survey is reached this key will not be
  present.
* ``next-step``: a URL pointing to the API location of the next logical step.
  If the end of the survey is reached this key will not be present.

If a survey was updated since the last interaction of the user with the survey
and the structure of the survey has changed a *survey-update* response is
generated. The response type can be identified by ``type`` set to ``update``.

::

   {
           "type": "update",
           "confirm-profile": true,
           "next-step": "http://api.instrumenten.rie.nl/users/13/sessions/193714/update",
   }


Context menu
~~~~~~~~~~~~

When looking at a module or risk you can ask for a context menu information to
be included in the response by adding a ``menu`` parameter to the query
string. The parameter does not need to have a value.

The menu information is provided in a ``menu`` key and formatted as a
nested dictionary reflecting the elements of a navigation tree. Each
element in the tree is an object with the following keys:

* ``type``: node type (one of ``risk`` or ``module``).
* ``number``: human presentable numbering for the node.
* ``title``: title of the risk or module.
* ``current``: boolean indicating if this is the current node.
  parent.
* ``active``: boolean indicating if this is a parent node of the current node.
* ``children``: list of child nodes (in the right order).
* ``url``: URL for the API interface to this node..
* ``status``: only present for risks and specifies the risk status. The value
  is one of ``postponed``, ``present``, ``not-present`` or *null* if the
  user has not seen the risk yet.

.. note::

   The content of the context menu depends on the currently active phase.
   Requesting the menu without specifying the phase will not return any
   menu data.


Start a new survey session
~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+---------------------------+------------------------------+
| Verb | URI                       | Description                  |
+======+===========================+==============================+
| POST | /users/<userid>/sessions  | Start a new survey session.  |
+------+---------------------------+------------------------------+

To start a new survey session a POST request must be send. This must include a
JSON body with the following keys:

* ``survey``: path of the survey. This is a combination of the id of the sector
  id and survey id, separated by a slash.
* ``title``: title of the new session. This should default to the title of
  the survey itself.

This requires that the user already authenticated and a suitable authentication
token is set in the ``X-Euphorie-Token`` header.

Here is an example request::

   {
           "survey": "nl/stigas/bos-en-natuur",
           "title": "Beheer stadspark oost",
   }

The response will be a JSON block::


   {
           "id": "193714",
           "survey": "nl/stigas/bos-en-natuur",
           "type": "session",
           "title": "Beheer stadspark oost",
           "introduction": "Introduction text from the survey.",
           "next-step: "http://api.instrumenten.rie.nl/users/13/sessions/193714/profile",
   }

If the survey has a configurable profile ``next-step`` will either to the
profile update API. For surveys without profile questions ``next-step`` will
point directly to the start of the identification phase.


Survey session information
~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+--------------------------------------+------------------------------+
| Verb | URI                                  | Description                  |
+======+======================================+==============================+
| GET  | /users/<userid>/sessions/<survey id> | Get information on survey.   |
+------+--------------------------------------+------------------------------+

.. note::

   This is also the API interface to use when resuming an existing survey
   session.

This function returns almost exactly the same response as the survey session
creation method. The only difference is the addition of a ``modified`` entry.

::

   {
           "id": "193714",
           "survey": "nl/stigas/bos-en-natuur",
           "type": "session",
           "created": "2011-12-06T15:15:24Z",
           "modified": "2012-04-23T10:29:13Z",
           "title": "The title of the survey",
           "introduction": "Introduction text from the survey.",
           "next-step: "http://api.instrumenten.rie.nl/users/13/sessions/193714/profile",
   }


Remove survey session
~~~~~~~~~~~~~~~~~~~~~

+--------+---------------------------------------+------------------------------+
| Verb   | URI                                   | Description                  |
+========+=======================================+==============================+
| DELETE | /users/<userid>/sessions/<session id> | Delete a survey session.     |
+--------+---------------------------------------+------------------------------+

This will delete an existing survey session.


View profile information
~~~~~~~~~~~~~~~~~~~~~~~~

+------+-----------------------------------------------+------------------------------+
| Verb | URI                                           | Description                  |
+======+===============================================+==============================+
| GET  | /users/<userid>/sessions/<session id>/profile | Get survey profile.          |
+------+-----------------------------------------------+------------------------------+


The response will be a JSON block::

   {
      "id": 15,
      "type": "profile",
      "title": "The title of the survey",
      "profile": [
          {
               "id": "1",
               "type": "optional",
               "question": "Do you have a storeroom?",
               "value": false,
          },
          {
               "id": "3",
               "type": "repetable",
               "question": "Enter your shop locations",
               "value": [
                   "New York",
                   "Paris",
               ],
          },
      ],
   }

.. note::

   As you can see in the example the response does not have ``previous-step``
   or ``next-step`` information.

The ``id`` is set to the survey id. Please note that not all surveys have a
profile, so the ``profile`` list might be empty.


Update profile
~~~~~~~~~~~~~~

+------+-----------------------------------------------+------------------------------+
| Verb | URI                                           | Description                  |
+======+===============================================+==============================+
| PUT  | /users/<userid>/sessions/<session id>/profile | Update survey profile.       |
+------+-----------------------------------------------+------------------------------+

The request body must be a JSON block specifying the new profile::

   {
           "1": false,
           "3": [
                   "New York",
                   "Paris",
           ],
   }

It is mandatory that all profile questions are included in the request data. If
data for a question is missing or invalid an error will be returned.

The response to a profile update returns the same information as the profile
information view. **The id of the survey may change as a result of a profile
update**.

::

   {
           "id": 15,
           "type": "profile",
           "title": "The title of the survey",
   }


Acknowledge survey update
~~~~~~~~~~~~~~~~~~~~~~~~~

+------+-----------------------------------------------+------------------------------+
| Verb | URI                                           | Description                  |
+======+===============================================+==============================+
| GET  | /users/<userid>/sessions/<session id>/update  | Get update information.      |
+------+-----------------------------------------------+------------------------------+
| PUT  | /users/<userid>/sessions/<session id>/update  | Confirm survey update.       |
+------+-----------------------------------------------+------------------------------+

If a survey was updated since the last user interaction and the survey
structure was changed (for example a new risk has been added) the user must
acknowledge the change and request that his survey session is updated
accordingly. 

These calls return the same information as the `profile information<View
profile information>`_ and `update profile <Update profile>`_ calls. The only
difference is that the ``type`` got a GET query will be set to ``update``.



Start identification phase
~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+-------------------------------------------------------+------------------------------+
| Verb | URI                                                   | Description                  |
+======+=======================================================+==============================+
| GET  | /users/<userid>/sessions/<session id>/identification  | Request idenfication info.   |
+------+-------------------------------------------------------+------------------------------+

This call will return information that is needed to start the identification
phase in a survey. A frontend may not need to display any of this information
but only use it to find locate the first unanswered question in the survey
session, which is given in the ``next-step`` key.

::

    {
            "type": "session",
            "phase": "identification",
            "title": "The title of the survey",
            "next-step": "http://api.instrumenten.rie.nl/users/13/sessions/1931714/1",
            "menu": [ ... ],
    }


Start evaluation phase
~~~~~~~~~~~~~~~~~~~~~~

+------+---------------------------------------------------+------------------------------+
| Verb | URI                                               | Description                  |
+======+===================================================+==============================+
| GET  | /users/<userid>/sessions/<session id>/evaluation  | Request evaluation info.     |
+------+---------------------------------------------------+------------------------------+

This call will return information that is needed to start the evaluation phase
in a survey. A frontend may not need to display any of this information but
only use it to find locate the first unanswered evaluation question in the
survey session, which is given in the ``next-step`` key.

::

    {
            "type": "session",
            "phase": "evaluation",
            "title": "The title of the survey",
            "next-step": "http://api.instrumenten.rie.nl/users/13/sessions/1931714/2/5/13",
            "menu": [ ... ],
    }


Start action plan phase
~~~~~~~~~~~~~~~~~~~~~~~

+------+--------------------------------------------------+------------------------------+
| Verb | URI                                              | Description                  |
+======+==================================================+==============================+
| GET  | /users/<userid>/sessions/<session id>/actionplan | Request evaluation info.     |
+------+--------------------------------------------------+------------------------------+

This call will return information that is needed to start the action plan phase
in a survey.  A frontend may not need to display any of this information but
only use it to find locate the first unanswered action plan question in the
survey session, which is given in the ``next-step`` key.

::

    {
            "type": "session",
            "phase": "actionplan",
            "title": "The title of the survey",
            "next-step": "http://api.instrumenten.rie.nl/users/13/sessions/1931714/2/5/13",
            "menu": [ ... ],
    }


Module information
~~~~~~~~~~~~~~~~~~

+------+------------------------------------------------------+------------------------------+
| Verb | URI                                                  | Description                  |
+======+======================================================+==============================+
| GET  | /users/<userid>/sessions/<session id>/<path>         | Request module information   |
+------+------------------------------------------------------+------------------------------+
| GET  | /users/<userid>/sessions/<session id>/<path>/<phase> | Request module information   |
|      |                                                      | for the given phase.         |
+------+------------------------------------------------------+------------------------------+

.. note::

   The URL does not indicate if the data at that location is a module or a
   risk. That means a client must check the returned ``type`` information to
   determine the resource type and act accordingly.

``previous-step`` and ``next-step`` can only be returned if the phase is
provided. The phase must be one of ``identification``, ``evaluation`` or
``actionplan``.

Beyond the standard fields a module will return these extra fields:

+------------------------+---------------+----------+--------------------------------+
| Field                  | Type          | Required |                                |
+========================+===============+==========+================================+
| ``image``              | object        | No       | An image related to the module.|
|                        |               |          | This has three keys:           |
|                        |               |          | ``original``, ``thumbnail``    |
|                        |               |          | and ``caption``.               |
+------------------------+---------------+----------+--------------------------------+
| ``solution-direction`` | string (HTML) | No       | Explanation of how to handle   |
|                        |               |          | risks in this module.          |
+------------------------+---------------+----------+--------------------------------+
| ``optional``           | boolean       | Yes      | Flag indicating if this module |
|                        |               |          | is optional.                   |
+------------------------+---------------+----------+--------------------------------+
| ``question``           | string        | No       | For optional modules this is   |
|                        |               |          | the question to ask users to   |
|                        |               |          | determine if children of this  |
|                        |               |          | module should be included or   |
|                        |               |          | skipped.                       |
+------------------------+---------------+----------+--------------------------------+
| ``skip-children``      | boolean       | No       | The users answer to the        |
|                        |               |          | question. If the question has  |
|                        |               |          | not been answered yet this is  |
|                        |               |          | set to ``null``.               |
+------------------------+---------------+----------+--------------------------------+


Update module identification data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+-------------------------------------------------------------+-----------------------+
| Verb | URI                                                         | Description           |
+======+=============================================================+=======================+
| PUT  | /users/<userid>/sessions/<session id>/<path>/identification | Update module status  |
+------+-------------------------------------------------------------+-----------------------+

This call is only useful for optional modules. For normal (ie mandatory) modules
it is an error to use this call.

The request must be a JSON block with an answer for the ``skip-children``
flag:

::

    {
            "skip-children": false,
    }


Risk information
~~~~~~~~~~~~~~~~

+------+------------------------------------------------------+----------------------------+
| Verb | URI                                                  | Description                |
+======+======================================================+============================+
| GET  | /users/<userid>/sessions/<session id>/<path>         | Request risk information   |
+------+------------------------------------------------------+----------------------------+
| GET  | /users/<userid>/sessions/<session id>/<path>/<phase> | Request risk information   |
|      |                                                      | for the given phase.       |
+------+------------------------------------------------------+----------------------------+

.. note::

   The URL does not indicate if the data at that location is a module or a
   risk. That means a client must check the returned ``type`` information to
   determine the resource type and act accordingly.

``previous-step`` and ``next-step`` can only be returned if the phase is
provided. The phase must be one of ``identification``, ``evaluation`` or
``actionplan``.

Beyond the standard fields a risk will return these extra fields:

+-------------------------+---------------+----------+--------------------------------+
| Field                   | Type          | Required |                                |
+=========================+===============+==========+================================+
| ``module-title``        | string        | Yes      | The title of the parent        |
|                         |               |          | module.                        |
+-------------------------+---------------+----------+--------------------------------+
| ``problem-description`` | string        | Yes      | The inverse of the risk title. |
|                         |               |          | This should be used instead of |
|                         |               |          | the title if risk is known to  |
|                         |               |          | be present.                    |
+-------------------------+---------------+----------+--------------------------------+
| ``evaluation-method``   | string        | Yes      | The evaluation method to use.  |
|                         |               |          | Will be either ``direct`` or   |
|                         |               |          | ``calcualated``.               |
+-------------------------+---------------+----------+--------------------------------+
| ``images``              | list of       | No       | An list of image related to the|
|                         | objects       |          | risk. Each entry is an object  |
|                         |               |          | with three keys: ``original``, |
|                         |               |          | ``thumbnail`` and ``caption``. |
+-------------------------+---------------+----------+--------------------------------+
| ``standard-solutions``  | list of       | No       | A list of standard solutions   |
|                         | objects       |          | for this risk. Each entry is   |
|                         |               |          | with four keys:                |
|                         |               |          | ``description``,               |
|                         |               |          | ``action-plan``,               |
|                         |               |          | ``prevention-plan`` and        |
|                         |               |          | ``requirements``.              |
+-------------------------+---------------+----------+--------------------------------+
| ``legal-reference``     | string (HTML) | No       | A reference to related legal   |
|                         |               |          | and policy references.         |
+-------------------------+---------------+----------+--------------------------------+
| ``show-not-applicable`` | boolean       | Yes      | Indicates of a *not            |
|                         |               |          | applicable* option should be   |
|                         |               |          | offered in the identification  |
|                         |               |          | phase.                         |
+-------------------------+---------------+----------+--------------------------------+
| ``present``             | string        | Yes      | Indicates if the risk is       |
|                         |               |          | present. One of ``yes``,       |
|                         |               |          | ``no``, ``n/a`` (only if       |
|                         |               |          | ``show-not-applicable`` is set)|
|                         |               |          | or null of not yet known.      |
+-------------------------+---------------+----------+--------------------------------+
| ``priority``            | string        | Yes      | The priority of the risk. One  |
|                         |               |          | ``low``, ``medium``, ``high``  |
|                         |               |          | or *null* if not known yet.    |
+-------------------------+---------------+----------+--------------------------------+
| ``comment``             | string        | No       | A comment added by the user.   |
+-------------------------+---------------+----------+--------------------------------+


For risks with an evalution option of ``calculated`` these extra fields are included:


+-------------------------+---------------+----------+--------------------------------+
| Field                   | Type          | Required |                                |
+=========================+===============+==========+================================+
| ``frequency-options``   | list of       | Yes      | A list of allowed frequency    |
|                         | objects       |          | answers. Each entry is an      |
|                         |               |          | object with two string keys:   |
|                         |               |          | ``value`` and ``title``.       |
+-------------------------+---------------+----------+--------------------------------+
| ``frequency``           | integer       | Yes      | Users answer to the frequency  |
|                         |               |          | question.                      |
+-------------------------+---------------+----------+--------------------------------+
| ``effect-options``      | list of       | Yes      | A list of allowed effect       |
|                         | objects       |          | answers. Each entry is an      |
|                         |               |          | object with two string keys:   |
|                         |               |          | ``value`` and ``title``.       |
+-------------------------+---------------+----------+--------------------------------+
| ``effect``              | integer       | Yes      | Users answer to the effect     |
|                         |               |          | question.                      |
+-------------------------+---------------+----------+--------------------------------+
| ``probability-options`` | list of       | Yes      | A list of allowed probability  |
|                         | objects       |          | answers. Each entry is an      |
|                         |               |          | object with two string keys:   |
|                         |               |          | ``value`` and ``title``.       |
+-------------------------+---------------+----------+--------------------------------+
| ``probability``         | integer       | Yes      | Users answer to the probability|
|                         |               |          | question.                      |
+-------------------------+---------------+----------+--------------------------------+


Update risk identification data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+-------------------------------------------------------------+---------------------+
| Verb | URI                                                         | Description         |
+======+=============================================================+=====================+
| PUT  | /users/<userid>/sessions/<session id>/<path>/identification | Update risk status  |
+------+-------------------------------------------------------------+---------------------+


The request must be a JSON block with a (new) answer for the ``present`` flag. The comment
can also be updated by including the ``comment`` field.

::

    {
            "present": "no",
            "comment": "Verify with John at the shipping department!",
    }


Update risk evaluation data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+-------------------------------------------------------------+---------------------+
| Verb | URI                                                         | Description         |
+======+=============================================================+=====================+
| PUT  | /users/<userid>/sessions/<session id>/<path>/evaluation     | Update risk status  |
+------+-------------------------------------------------------------+---------------------+
                    
The possbile values depend on the evaluation method used for the risk. For
risks that use a direct evaluation the priority field can be set directly. For
risks using a calculated evaluation method the frequency, effect and
probability information must be provided.

The comment can also be updated by including the ``comment`` field.

::

    {
            "frequency": 10,
            "effect": 3,
            "probability": 7,
    }


Update risk action plan data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+-------------------------------------------------------------+---------------------+
| Verb | URI                                                         | Description         |
+======+=============================================================+=====================+
| PUT  | /users/<userid>/sessions/<session id>/<path>/actionplan     | Update risk status  |
+------+-------------------------------------------------------------+---------------------+
                    
This method updates the action plan-specific information for a risk. For top-5
and policy risks only the commend field may be updated. For other risks the
priority can be set directly as well (but it may be reset of the user
re-evaluates the risk).

The possible values for priority are ``low``, ``medium`` and ``high``.

::

    {
            "comment": "We need to take another look at this",
            "priority": "medium",
    }


Action plans can be added, updated or deleted through the ``actionplans``
container (see below).


List action plans
~~~~~~~~~~~~~~~~~

+------+----------------------------------------------------------+-------------------+
| Verb | URI                                                      | Description       |
+======+==========================================================+===================+
| GET  | /users/<userid>/sessions/<session id>/<path>/actionplans | List action plans |
+------+----------------------------------------------------------+-------------------+

During the action plan phase a user is asked to indicate how he wants to tackle
a risk by defining specific actions to be taken. This API call will return a
list of all action plans provided by the user.

The response is returned in the form of a JSON object with a ``action-plans`` key
containing a list of plans.

::

     {
             "action-plans": [
                     {
                             "id": 15,
                             "plan": "Clean the workplace",
                             "prevention": "Educate workers to clean daily.",
                             "requirements": "Soap, vacuumcleaner",
                             "responsible": "John Doe",
                             "budget": 1500,
                             "planning-start": "2012-04-15",
                             "planning-end": null,
                             "reference": "2012a16.5",
                     },
             ],
     }

See the :ref:`view action plan <View action plan>` call for details on the
returned information.


View action plan
~~~~~~~~~~~~~~~~

+------+---------------------------------------------------------------+----------------------------+
| Verb | URI                                                           | Description                |
+======+===============================================================+============================+
| GET  | /users/<userid>/sessions/<session id>/<path>/actionplans/<id> | View action plan details.  |
+------+---------------------------------------------------------------+----------------------------+

The response is returned in the form of a JSON object containing all known
information about an action plan.

::

     {
             "type": "actionplan",
             "id": 15,
             "plan": "Clean the workplace",
             "prevention": "Educate workers to clean daily.",
             "requirements": "Soap, vacuumcleaner",
             "responsible": "John Doe",
             "budget": 1500,
             "planning-start": "2012-04-15",
             "planning-end": null,
             "reference": "2012a16.5",
     }

The ``reference`` key is not part of the standard Euphorie user interface, but
can be used by consumers of this API to link a measure to an external system.


Create new action plan
~~~~~~~~~~~~~~~~~~~~~~

+------+----------------------------------------------------------+----------------------+
| Verb | URI                                                      | Description          |
+======+==========================================================+======================+
| POST | /users/<userid>/sessions/<session id>/<path>/actionplans | Add new action plan. |
+------+----------------------------------------------------------+----------------------+

The request must be a JSON object with data for the action plan to be added. The
only required field is ``plan``; all either items are optional.

+-------------------------+---------------+----------+--------------------------------+
| Field                   | Type          | Required |                                |
+=========================+===============+==========+================================+
| ``plan``                | string        | Yes      | Description of actions needed  |
|                         | string        |          | to remove the current risk.    |
+-------------------------+---------------+----------+--------------------------------+
| ``prevention``          | string        | No       | Description of what should be  |
|                         |               |          | done to remove this risk.      |
+-------------------------+---------------+----------+--------------------------------+
| ``requirements``        | string        | No       | A description of the           |
|                         |               |          | requirements for this plan.    |
+-------------------------+---------------+----------+--------------------------------+
| ``responsible``         | string        | No       | The name of the person or group|
|                         |               |          | who is available for this task.|
+-------------------------+---------------+----------+--------------------------------+
| ``budget``              | integer       | No       | The budget that is available   |
|                         |               |          | for this task.                 |
+-------------------------+---------------+----------+--------------------------------+
| ``planning-start``      | string (ISO   | No       | Start date for the plan.       |
|                         | date)         |          |                                |
+-------------------------+---------------+----------+--------------------------------+
| ``planning-end``        | string (ISO   | No       | Completion date for the plan.  |
|                         | date)         |          |                                |
+-------------------------+---------------+----------+--------------------------------+
| ``reference``           | string        | No       | Reference to external system.  |
|                         |               |          |                                |
+-------------------------+---------------+----------+--------------------------------+

The ``reference`` key is not part of the standard Euphorie user interface, but
can be used by consumers of this API to link a measure to an external system.

The response is a JSON object with complete information on the newly created action
plan. See the :ref:`view action plan <View action plan>` call for details.


Update action plan
~~~~~~~~~~~~~~~~~~

+------+---------------------------------------------------------------+------------------------+
| Verb | URI                                                           | Description            |
+======+===============================================================+========================+
| PUT  | /users/<userid>/sessions/<session id>/<path>/actionplans/<id> | Update an action plan. |
+------+---------------------------------------------------------------+------------------------+

The request must be a JSON object with all items that must be updated. Items
not included in the request will not be changed.


Delete action plan
~~~~~~~~~~~~~~~~~~

+--------+---------------------------------------------------------------+------------------------+
| Verb   | URI                                                           | Description            |
+========+===============================================================+========================+
| DELETE | /users/<userid>/sessions/<session id>/<path>/actionplans/<id> | Remove an action plan. |
+--------+---------------------------------------------------------------+------------------------+

This call will remove an action plan for a risk.


View company details
~~~~~~~~~~~~~~~~~~~~

+------+-----------------------------------------------+------------------------------+
| Verb | URI                                           | Description                  |
+======+===============================================+==============================+
| GET  | /users/<userid>/sessions/<session id>/company | Request company information  |
+------+-----------------------------------------------+------------------------------+

This interface will return information about the company to which this survey
session applies. The response is returned in the form of a JSON object
containing all known information about the company. The possible fields are:

+------------------------+---------------+----------+--------------------------------+
| Field                  | Type          | Required |                                |
+========================+===============+==========+================================+
| ``country``            | string        | No       | ISO country code.             .|
+------------------------+---------------+----------+--------------------------------+
| ``employees``          | string        | No       | Indicator of company size in   |
|                        |               |          | terms of number of employees.  |
|                        |               |          | One of ``1-9``, ``10-49``,     |
|                        |               |          | ``50-249`` or ``250+``.        |
+------------------------+---------------+----------+--------------------------------+
| ``conductor``          | string        | No       | Role of person who conducted   |
|                        |               |          | the survey. Must be one of     |
|                        |               |          | ``staff``, ``third-party`` or  |
|                        |               |          | ``both``.                      |
+------------------------+---------------+----------+--------------------------------+
| ``referer``            | string        | No       | How the user learned about the |
|                        |               |          | tool. Must be one of           |
|                        |               |          | ``employers-organisation``,    |
|                        |               |          | ``trade-union``,               |
|                        |               |          | ``national-public-institution``|
|                        |               |          | ``eu-institution``             |
|                        |               |          | ``health-safety-experts``      |
|                        |               |          | or ``other``.                  |
+------------------------+---------------+----------+--------------------------------+

Update company details
~~~~~~~~~~~~~~~~~~~~~~

+------+-----------------------------------------------+------------------------------+
| Verb | URI                                           | Description                  |
+======+===============================================+==============================+
| PUT  | /users/<userid>/sessions/<session id>/company | Update company details.      |
+------+-----------------------------------------------+------------------------------+

This interface will update the company information for a survey session.
See the :ref:`View company details` section for the supported fields.


Identifcation report
~~~~~~~~~~~~~~~~~~~~

+------+------------------------------------------------------------+--------------------------------+
| Verb | URI                                                        | Description                    |
+======+============================================================+================================+
| GET  | /users/<userid>/sessions/<survey id>/report-identification | Download identifcation report. |
+------+------------------------------------------------------------+--------------------------------+

This API call will return the identification report. This is returned as
a downloadable RTF file.


Action plan report
~~~~~~~~~~~~~~~~~~

+------+--------------------------------------------------------+------------------------------+
| Verb | URI                                                    | Description                  |
+======+========================================================+==============================+
| GET  | /users/<userid>/sessions/<survey id>/report-actionplan | Download action plan report. |
+------+--------------------------------------------------------+------------------------------+

This API call will return the action plan report. This is returned as a
downloadable RTF file.


Action plan timeline report
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+------------------------------------------------------+--------------------------------+
| Verb | URI                                                  | Description                    |
+======+======================================================+================================+
| GET  | /users/<userid>/sessions/<survey id>/report-timeline | Download action plan timeline. |
+------+------------------------------------------------------+--------------------------------+

This API call will return the action plan timeline. This is returned as
a downloadable OpenXML (xlsx) file.


API reference
-------------

+--------+-----------------------------------------------------------------+-----------------------------------+
| Verb   | URI                                                             | Description                       |
+========+=================================================================+===================================+
| POST   | /users                                                          | Create a new user.                |
+--------+-----------------------------------------------------------------+-----------------------------------+
| POST   | /users/authenticate                                             | Authenticate a user.              |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>                                                 | Return user information.          |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>                                                 | Update user information.          |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /surveys                                                        | List all defined countries        |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /surveys/<country>                                              | List all sectors in a country.    |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /surveys/<country>?details                                      | List all sectors in a country     |
|        |                                                                 | including its surveys.            |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /surveys/<country>?details&language=<lang>                      | List all sectors in a country     |
|        |                                                                 | including all surveys in the      |
|        |                                                                 | given language.                   |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /surveys/<country>/<sectorid>                                   | List details of the given sector. |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /surveys/<country>/<sectorid>?language=<lang>                   | List details of the given sector, |
|        |                                                                 | only including surveys in the     |
|        |                                                                 | given language.                   |
+--------+-----------------------------------------------------------------+-----------------------------------+
| POST   | /users/<userid>/sessions                                        | Start a new survey session.       |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<survey id>                            | Get information on survey.        |
+--------+-----------------------------------------------------------------+-----------------------------------+
| DELETE | /users/<userid>/sessions/<session id>                           | Delete a survey session.          |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/profile                   | Get survey profile.               |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>/sessions/<session id>/profile                   | Update survey profile.            |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/update                    | Get update information.           |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>/sessions/<session id>/update                    | Confirm survey update.            |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/identification            | Request idenfication info.        |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/evaluation                | Request evaluation info.          |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/actionplan                | Request evaluation info.          |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/<path>                    | Request module information        |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/<path>/<phase>            | Request module information        |
|        |                                                                 | for the given phase.              |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>/sessions/<session id>/<path>/identification     | Update module status              |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/<path>                    | Request risk information          |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/<path>/<phase>            | Request risk information          |
|        |                                                                 | for the given phase.              |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>/sessions/<session id>/<path>/identification     | Update risk status                |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>/sessions/<session id>/<path>/evaluation         | Update risk status                |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>/sessions/<session id>/<path>/actionplan         | Update risk status                |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/<path>/actionplans        | List action plans                 |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/<path>/actionplans/<id>   | View action plan details.         |
+--------+-----------------------------------------------------------------+-----------------------------------+
| POST   | /users/<userid>/sessions/<session id>/<path>/actionplans        | Add new action plan.              |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>/sessions/<session id>/<path>/actionplans/<id>   | Update an action plan.            |
+--------+-----------------------------------------------------------------+-----------------------------------+
| DELETE | /users/<userid>/sessions/<session id>/<path>/actionplans/<id>   | Remove an action plan.            |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<session id>/company                   | Request company information       |
+--------+-----------------------------------------------------------------+-----------------------------------+
| PUT    | /users/<userid>/sessions/<session id>/company                   | Update company details.           |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<survey id>/report-identification      | Download identifcation report.    |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<survey id>/report-actionplan          | Download action plan report.      |
+--------+-----------------------------------------------------------------+-----------------------------------+
| GET    | /users/<userid>/sessions/<survey id>/report-timeline            | Download action plan timeline.    |
+--------+-----------------------------------------------------------------+-----------------------------------+
