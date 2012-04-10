Introduction
============

This document describes the client API for the Euphorie. This API allows
interface with the client component of an Euphorie system and can be used
to implement a custom frontend. It exposes client users, surveys, surveys
sessions and all interactions with them. It does allow for management of
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
| POST | /users/authenticate |  Authenticate a user.        |
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
                   "modified": "2010-09-27T11:35:00Z",
           },
           {
                   "id": 23945,
                   "title": "Vlakglas",
                   "modified": "2011-12-06T15:15:24Z",
           },
       ],
   }

This token should be supplied in an ``X-Euphorie-Token`` HTTP header for all
requests that require authentication.

.. note::

   Note that this is only possible for accounts that were created in an
   Euphorie system directly, or for accounts that were created via this API
   and have performed a password reset to set a password for the account.

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
                   "modified": "2010-09-27T11:35:00Z",
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
| POST | /users/<userid>     | Return user information.     |
+------+---------------------+------------------------------+

This call allows updating the user information. Keys that can be updated
are ``email`` and ``password``.

::

   {
       "email": "jane@example.com",
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
| GET  | /surveys |  List all defined countries  |
+------+-----------+-----------------------------+

Example response::

   {
       "countries": [
           {
                   "id": "nl",
                   "type": "eu-member",
                   "languages": ["nl"],
           },
           {
                   "id": "be",
                   "type": "eu-member",
                   "languages": ["nl", "fr"],
           },
   }

The possible country types are:

* ``eu-member``: country is a full EU member state
* ``candidate-eu``: candidate member of the EU
* ``potential-candidate-eu``: potentital candidate member of the EU
* ``efta``: member of the European Free Trade Association
* ``region``: generic region, not an individual country


List sectors
~~~~~~~~~~~~

+------+--------------------------------------------+-----------------------------------+
| Verb | URI                                        | Description                       |
+======+============================================+===================================+
| GET  | /surveys/<country>                         | List all surveys in a country.    |
+------+--------------------------------------------+-----------------------------------+
| GET  | /surveys/<country>/details                 | List all surveys in a country     |
|      |                                            | including its surveys.            |
+------+--------------------------------------------+-----------------------------------+
| GET  | /surveys/<country>/details?language=<lang> | List all surveys in a country     |
|      |                                            | including all surveys in the given|
|      |                                            | language.                         |
+------+--------------------------------------------+-----------------------------------+

Example response::

   {
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

+------+--------------------------------+-----------------------------------+
| Verb | URI                            | Description                       |
+======+================================+===================================+
| GET  | /surveys/<country>/<sectorid>  | List details of the given sector. |
+------+--------------------------------+-----------------------------------+


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

Standard response components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All responses to API calls involving a survey session follow a standard
structure. They include the following keys:

* ``phase``: the current survey phase. This will be one of ``identification``,
* ``type``: an indicator of the response type. This will be one of ``survey``,
  ``profile``, ``module``, ``risk`` or ``update``.
* ``title``: the title for the current context. Depending on the context this
  will be the title of the survey, module or the risk.
  ``evaluation`` or ``actionplan``.
* ``previous-step``: a URL pointing to the API location of the previous logical
  step.  If the end start of the survey is reached this key will not be
  present.
* ``next-step``: a URL pointing to the API location of the next logical step.
  If the end of the survey is reached this key will not be present.

If a survey was updated since the last interaction of the user with the survey
and the structure of the survey has changed a *survey-update* response is
generated. The response type can be identified by ``type`` set to ``update``
and ``next-step`` pointing to the API interface for the profile step.

XXX:
- add survey version to update notice
- add different update types: simple confirm or reconfirm propfile

.. note::

   Need to define menu structure here as well. See euphorie.client.navigation.getTreeData

.. note::

   Need to specify error responses.


Start a new survey
~~~~~~~~~~~~~~~~~~

+------+---------------------------+------------------------------+
| Verb | URI                       | Description                  |
+======+===========================+==============================+
| POST | /users/<userid>/surveys   | Start a new survey session.  |
+------+---------------------------+------------------------------+

To start a new survey a POST request must be send. This must include a JSON
body with the following keys:

* ``id``: id of the survey.
* ``title``: title of the new session. This should default to the title of
  the survey itself.

This requires that the user already authenticated and a suitable authentication
token is set in the ``X-Euphorie-Token`` header.

The response will be a JSON block::


   {
           "id": "193714",
           "type": "survey",
           "title": "The title of the survey",
           "introduction": "Introduction text from the survey.",
           "next-step: "http://instrumenten.rie.nl/users/13/surveys/193714/profile",
   }

If the survey has a configurable profile ``next-step`` will either to the
profile update API. For surveys without profile questions ``next-step`` will
point directly to the start of the identification phase.


Survey information
~~~~~~~~~~~~~~~~~~

+------+-------------------------------------+------------------------------+
| Verb | URI                                 | Description                  |
+======+=====================================+==============================+
| GET  | /users/<userid>/surveys/<survey id> | Get information on survey.   |
+------+-------------------------------------+------------------------------+

.. note::

   This is also the API interface to use when resuming an existing survey.

This will return the same information as the previous API call.


View profile information
~~~~~~~~~~~~~~~~~~~~~~~~

+------+---------------------------------------------+------------------------------+
| Verb | URI                                         | Description                  |
+======+=============================================+==============================+
| GET  | /users/<userid>/surveys/<survey id>/profile | Get survey profile.          |
+------+---------------------------------------------+------------------------------+


The response will be a JSON block::

   {
      "type": "profile",
      "title": "The title of the survey",
      "profile": [
          {
               "id": "1",
               "type": "optional",
               "title": "Do you have a storeroom?",
               "value": false,
          },
          {
               "id": "3",
               "type": "repetable",
               "title": "Enter your shop locations",
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


Update profile
~~~~~~~~~~~~~~

+------+---------------------------------------------+------------------------------+
| Verb | URI                                         | Description                  |
+======+=============================================+==============================+
| PUT  | /users/<userid>/surveys/<survey id>/profile | Update survey profile.       |
+------+---------------------------------------------+------------------------------+

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

The response for a profile update is a standard response with ``next-step``
pointing to the start of the identification phase::

   {
           "next-step: "http://instrumenten.rie.nl/users/13/surveys/193714/identification",
   }


Acknowledge survey update
~~~~~~~~~~~~~~~~~~~~~~~~~

+------+---------------------------------------------+------------------------------+
| Verb | URI                                         | Description                  |
+======+=============================================+==============================+
| POST | /users/<userid>/surveys/<survey id>/update  | Confirm survey update.       |
+------+---------------------------------------------+------------------------------+

If a survey was updated since the last user interaction and the survey
structure was changed (for example a new risk has been added) the user must
acknowledge the change and request that his survey session is updated
accordingly. 

For surveys without profile questions the request does not require any data to be
specified. For surveys with a profile the (updated) profile must be provided. This
uses the same format as a normal :ref:`profile update <Update profile>`.

The response is a standard response with ``next-step`` pointing to the start of
the identification phase::

   {
           "next-step: "http://instrumenten.rie.nl/users/13/surveys/193714/identification",
   }
