Introduction
============

This document describes the content management API for the Euphorie. This API
allows interface with the CMS component of an Euphorie system and can be
used to implement manage backend accounts.


Concepts
========

Country
-------

A country is the top level grouping item for survey content. There are
different country types to indicate the EU membership status. A country
contains zero or more sectors.

Sector
------

A sector is a national organisation for a single sector of industry.


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


Authentication
--------------

+------+---------------------+------------------------------+
| Verb | URI                 | Description                  |
+======+=====================+==============================+
| POST | /authenticate       | Authenticate a user.         |
+------+---------------------+------------------------------+

In order to authenticate you must submit a JSON object with two keys:

* ``login``: the users login name
* ``password``: the users password

If authentication failed an error response is returned with status code 403.
If authentication is successful a JSON response is returned with an
authentication token and basic information on the user::

   {
       "token": "e1490672-4015-4572-a036-ba53c45e9509",
       "login": "security",
       "title": "UK security sector",
       "url": "http://api.oira.com/countries/uk/sectors/security",
   }

The token should be supplied in an ``X-Euphorie-Token`` HTTP header for all
requests that require authentication.


Country management
------------------

List countries
~~~~~~~~~~~~~~

+------+------------+------------------------------+
| Verb | URI        | Description                  |
+======+============+==============================+
| GET  | /countries | List all defined countries.  |
+------+------------+------------------------------+

Example response::

   {
       "countries": [
           {
                   "id": "nl",
                   "title": "The Netherlands",
                   "country-type": "eu-member",
           },
           {
                   "id": "be",
                   "title": "Belgium",
                   "country-type": "eu-member",
           },
   }

This call will return information on all defined countries.


Country information
~~~~~~~~~~~~~~~~~~~

+------+-------------------------+-----------------------------------+
| Verb | URI                     | Description                       |
+======+=========================+===================================+
| GET  | /countries/<id>         | Request country information.      |
+------+-------------------------+-----------------------------------+
| GET  | /countries/<id>?details | Request country information       |
|      |                         | including all sectors and country |
|      |                         | managers.                         |
+------+-------------------------+-----------------------------------+

Example normal response::

   {
           "type": "country",
           "id": "nl",
           "title": "The Netherlands",
           "country-type": "eu-member",
   }

Example detail response::

   {
           "type": "country",
           "id": "nl",
           "title": "The Netherlands",
           "country-type": "eu-member",
           "sectors": [
             ...
           ],
           "managers": [
             ...
           ],
   }

The returned fields are:

+------------------------+---------------+----------+--------------------------------+
| Field                  | Type          | Required |                                |
+========================+===============+==========+================================+
| ``type``               | string        | Yes      | Always set to ``country``.     |
+------------------------+---------------+----------+--------------------------------+
| ``id``                 | string        | Yes      | The country code. This must be |
|                        |               |          | the offical country code       |
|                        |               |          | unless this is a generic       |
|                        |               |          | region.                        |
+------------------------+---------------+----------+--------------------------------+
| ``title``              | string        | No       | The English title of the       |
|                        |               |          | country. If not provided       |
|                        |               |          | the name will be looked up     |
|                        |               |          | based on the provided id.      |
+------------------------+---------------+----------+--------------------------------+
| ``country-type``       | string        | Yes      | The country type.              |
+------------------------+---------------+----------+--------------------------------+

The possible country types are:

* ``eu-member``: country is a full EU member state
* ``candidate-eu``: candidate member of the EU
* ``potential-candidate-eu``: potentital candidate member of the EU
* ``efta``: member of the European Free Trade Association
* ``region``: generic region, not an individual country

Note that even though a country has a title frontends are encouraged to use
use locale-specific name for the country based on the id field.


Add a new country
~~~~~~~~~~~~~~~~~

+------+------------+------------------------------+
| Verb | URI        | Description                  |
+======+============+==============================+
| POST | /countries | Add a new country.           |
+------+------------+------------------------------+

The request body must be a JSON block specifying the new profile::

   {
           "id": "nl",
           "title": "The Netherlands",
           "country-type": "eu-member",
   }

This will return the country using the same format as the GET call.


Update country information
~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+-----------------+------------------------------+
| Verb | URI             | Description                  |
+======+=================+==============================+
| PUT  | /countries/<id> | Update country information.  |
+------+-----------------+------------------------------+

The request body must be a JSON block specifying the changed fields::

   {
           "title": "The Netherlands",
           "country-type": "eu-member",
   }

Updating the ``id`` field is not allowed.


Country managers
----------------

List country managers
~~~~~~~~~~~~~~~~~~~~~

+------+---------------------------------------+-----------------------------------+
| Verb | URI                                   | Description                       |
+======+=======================================+===================================+
| GET  | /countries/<country id>/managers      | List all country managers         |
+------+---------------------------------------+-----------------------------------+

Example response::

   {
           "managers": [
               {
                   "id": "steunpunt-rie",
                   "title": "Steuntpunt RI&E",
                   "email": "steunpunt@example.com",
                   "login": "steunpunt",
                   "locked": false,
               },
           ],
   }


Country manager information
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+---------------------------------------+-----------------------------------+
| Verb | URI                                   | Description                       |
+======+=======================================+===================================+
| GET  | /countries/<country id>/managers/<id> | Request manager information.      |
+------+---------------------------------------+-----------------------------------+

Example response::

   {
           "type": "countrymanager",
           "id": "steunpunt-rie",
           "title": "Steuntpunt RI&E",
           "email": "steunpunt@example.com",
           "login": "steunpunt",
           "locked": false,
   }

The returned fields are:

+------------------------+---------------+----------+-----------------------------------+
| Field                  | Type          | Required |                                   |
+========================+===============+==========+===================================+
| ``type``               | string        | Yes      | Always set to ``countrymanager``. |
+------------------------+---------------+----------+-----------------------------------+
| ``id``                 | string        | Yes      | Identifier for the manager.       |
+------------------------+---------------+----------+-----------------------------------+
| ``title``              | string        | Yes      | The full name of the country      |
|                        |               |          | manager.                          |
+------------------------+---------------+----------+-----------------------------------+
| ``email``              | string        | Yes      | Contact email address.            |
+------------------------+---------------+----------+-----------------------------------+
| ``login``              | string        | Yes      | Login name for the account.       |
+------------------------+---------------+----------+-----------------------------------+
| ``locked``             | boolean       | No       | Indicates if the account is       |
|                        |               |          | locked.                           |
+------------------------+---------------+----------+-----------------------------------+


Add new country manager
~~~~~~~~~~~~~~~~~~~~~~~

+------+------------------------------------+------------------------------+
| Verb | URI                                | Description                  |
+======+====================================+==============================+
| POST | /countries/<country id>/managers   | Add a new country manager.   |
+------+------------------------------------+------------------------------+

The request body must be a JSON block with the necessary information::

   {
           "title": "Steuntpunt RI&E",
           "email": "steunpunt@example.com",
           "login": "steunpunt",
           "locked": false,
   }

Please note that the ``id`` field can not be set manually: it will be generated
automatically.

This will return the country manager information in the same format as returned
by the GET call.


Update country manager information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+---------------------------------------+------------------------------+
| Verb | URI                                   | Description                  |
+======+=======================================+==============================+
| PUT  | /countries/<country id>/managers/<id> | Update country manager       |
|      |                                       | information.                 |
+------+---------------------------------------+------------------------------+

The request body must be a JSON block with the data that should be updated::

   {
           "locked": true,
   }

Please note that the ``id`` and ``login`` fields can not be modified.

This will return the country manager information in the same format as returned
by the GET call.


Delete country manager
~~~~~~~~~~~~~~~~~~~~~~

+--------+---------------------------------------+---------------------------+
| Verb   | URI                                   | Description               |
+========+=======================================+===========================+
| DELETE | /countries/<country id>/managers/<id> | Delete a country manager. |
+--------+---------------------------------------+---------------------------+



Sector organisations
--------------------

List sectors
~~~~~~~~~~~~

+------+---------------------------------------+----------------------+
| Verb | URI                                   | Description          |
+======+=======================================+======================+
| GET  | /countries/<country id>/sectors       | List all sectors.    |
+------+---------------------------------------+----------------------+

Example response::

   {
           "sectors": [
               {
                       "id": "security",
                       "title": "Security",
                       "login": "security",
                       "locked": false,
               },
           ],
   }


Sector information
~~~~~~~~~~~~~~~~~~

+------+--------------------------------------+-----------------------------+
| Verb | URI                                  | Description                 |
+======+======================================+=============================+
| GET  | /countries/<country id>/sectors/<id> | Request sector information. |
+------+--------------------------------------+-----------------------------+

Example response::

   {
           "type": "sector",
           "id": "security",
           "title": "Security",
           "login": "security",
           "locked": false,
           "contact": {
                   "name": "John Smith",
                   "email": "smith@example.com",
           },
   }

The returned fields are:

+------------------------+---------------+----------+-----------------------------------+
| Field                  | Type          | Required |                                   |
+========================+===============+==========+===================================+
| ``type``               | string        | Yes      | Always set to ``sector``.         |
+------------------------+---------------+----------+-----------------------------------+
| ``id``                 | string        | Yes      | Identifier for the sector.        |
+------------------------+---------------+----------+-----------------------------------+
| ``title``              | string        | Yes      | The full name of the sector       |
+------------------------+---------------+----------+-----------------------------------+
| ``login``              | string        | Yes      | Login name for the account.       |
+------------------------+---------------+----------+-----------------------------------+
| ``locked``             | boolean       | No       | Indicates if the account is       |
|                        |               |          | locked.                           |
+------------------------+---------------+----------+-----------------------------------+
| ``contact``            | object        | Yes      | Object specifying a contact for   |
|                        |               |          | the sector organisation. This     |
|                        |               |          | must have the following keys:     |
|                        |               |          | ``name`` and ``email``.           |
+------------------------+---------------+----------+-----------------------------------+


Add new sector organisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------+------------------------------------+--------------------+
| Verb | URI                                | Description        |
+======+====================================+====================+
| POST | /countries/<country id>/sectors    | Add a new sector.  |
+------+------------------------------------+--------------------+

The request body must be a JSON block with the necessary information::

   {
           "title": "Security",
           "login": "security",
           "locked": false,
           "contact": {
                   "name": "John Smith",
                   "email": "smith@example.com",
           },
   }

Please note that the ``id`` field can not be set manually: it will be generated
automatically.

This will return the sector information in the same format as returned by the
GET call.


Update sector information
~~~~~~~~~~~~~~~~~~~~~~~~~

+------+--------------------------------------+------------------------------+
| Verb | URI                                  | Description                  |
+======+======================================+==============================+
| PUT  | /countries/<country id>/sectors/<id> | Update sector information.   |
+------+--------------------------------------+------------------------------+

The request body must be a JSON block with the data that should be updated::

   {
           "locked": true,
   }

Please note that the ``id`` and ``login`` fields can not be modified.

This will return the country manager information in the same format as returned
by the GET call.


Delete sector organisation
~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------+--------------------------------------+---------------------------+
| Verb   | URI                                  | Description               |
+========+======================================+===========================+
| DELETE | /countries/<country id>/sectors/<id> | Delete a sector.          |
+--------+--------------------------------------+---------------------------+


API reference
-------------

+--------+---------------------------------------+-----------------------------------+
| Verb   | URI                                   | Description                       |
+========+=======================================+===================================+
| POST   | /authenticate                         | Authenticate a user.              |
+--------+---------------------------------------+-----------------------------------+
| GET    | /countries                            | List all defined countries.       |
+--------+---------------------------------------+-----------------------------------+
| GET    | /countries/<id>                       | Request country information.      |
+--------+---------------------------------------+-----------------------------------+
| GET    | /countries/<id>?details               | Request country information       |
|        |                                       | including all sectors and country |
|        |                                       | managers.                         |
+--------+---------------------------------------+-----------------------------------+
| POST   | /countries                            | Add a new country.                |
+--------+---------------------------------------+-----------------------------------+
| PUT    | /countries/<id>                       | Update country information.       |
+--------+---------------------------------------+-----------------------------------+
| GET    | /countries/<country id>/managers      | List all country managers         |
+--------+---------------------------------------+-----------------------------------+
| GET    | /countries/<country id>/managers/<id> | Request manager information.      |
+--------+---------------------------------------+-----------------------------------+
| POST   | /countries/<country id>/managers      | Add a new country manager.        |
+--------+---------------------------------------+-----------------------------------+
| PUT    | /countries/<country id>/managers/<id> | Update country manager            |
|        |                                       | information.                      |
+--------+---------------------------------------+-----------------------------------+
| DELETE | /countries/<country id>/managers/<id> | Delete a country manager.         |
+--------+---------------------------------------+-----------------------------------+
| GET    | /countries/<country id>/sectors       | List all sectors.                 |
+--------+---------------------------------------+-----------------------------------+
| GET    | /countries/<country id>/sectors/<id>  | Request sector information.       |
+--------+---------------------------------------+-----------------------------------+
| POST   | /countries/<country id>/sectors       | Add a new sector.                 |
+--------+---------------------------------------+-----------------------------------+
| PUT    | /countries/<country id>/sectors/<id>  | Update sector information.        |
+--------+---------------------------------------+-----------------------------------+
| DELETE | /countries/<country id>/sectors/<id>  | Delete a sector.                  |
+--------+---------------------------------------+-----------------------------------+
