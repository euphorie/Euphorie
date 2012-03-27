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

Authenticate user
~~~~~~~~~~~~~~~~~

+------+---------------------+------------------------------+
| Verb | URI                 | Description                  |
+======+=====================+==============================+
| POST | /users/authenticate |  List all defined countries. |
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


Surveys
-------

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
                   "languages": ["nl"],
           },
           {
                   "id": "be",
                   "languages": ["nl", "fr"],
           },
   }


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
   }
