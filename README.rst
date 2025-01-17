About
=====

.. image:: https://github.com/euphorie/Euphorie/workflows/tests/badge.svg
    :target: https://github.com/euphorie/Euphorie/actions?query=workflow%3Atests

Euphorie is a tool for risk assessment.  It was developed by `SYSLAB`_ and `TNO`_
in cooperation with `Simplon B.V.`_ and `Cornelis Kolbach`_ in commission of
`The European Agency for Safety and Health at Work`_ as part of the
`Healthy Workplaces`_ campaign.

.. _syslab: http://syslab.com/
.. _TNO: http://www.tno.nl/index.cfm?Taal=2
.. _Simplon B.V.: http://www.simplon.biz/
.. _Cornelis Kolbach: http://cornae.org/
.. _The European Agency for Safety and Health at Work: http://osha.europa.eu/en/
.. _Healthy Workplaces: http://osha.europa.eu/en/campaigns/hw2008


Introduction
============

The Euphorie risk assessment tool is based on hierarchical questionnaires. A
questionnaire (or survey) covers all possible risks for a specific sector of
industry.

Each sector organisation can have one or more surveys published simultaneously.
In order to facilitate development and testing of surveys the system supports
multiple versions for a survey. Only a single version of a survey can be public
at any point in time.


Compatibility
=============

Euphorie 17 is meant to be used with `Plone 6` and `Python >= 3.11`.

In Euphorie 15 the "publication feature" was changed in the more generic "locking feature".
That makes the registry record ``euphorie.use_publication_feature`` obsolete.

Euphorie 12 is meant to be used with Plone 5.2.
Since Euphorie 12, NuPlone 2 is needed.

NuPlone 2 no longer uses the ``z3c.appconfig``.
The configuration is now stored in the registry.

- instead of ``appconfig["euphorie"]["allow_guest_accounts"]``, please use the registry record ``euphorie.allow_guest_accounts``.
- instead of ``appconfig["euphorie"]["allow_social_sharing"]``, please use the registry record ``euphorie.allow_social_sharing``.
- instead of ``appconfig["euphorie"]["allow_user_defined_risks"]``, please use the registry record ``euphorie.allow_user_defined_risks``.
- instead of ``appconfig["euphorie"]["client"]``, please use the registry record ``euphorie.client_url``.
- instead of ``appconfig["euphorie"]["default_country"]``, please use the registry record ``euphorie.default_country``.
- instead of ``appconfig["euphorie"]["extra_text_identification"]``, please use the registry record ``euphorie.extra_text_identification``.
- instead of ``appconfig["euphorie"]["library"]``, please use the registry record ``euphorie.library``.
- instead of ``appconfig["euphorie"]["max_login_attempts"]``, please use the registry record ``euphorie.max_login_attempts``.
- instead of ``appconfig["euphorie"]["terms-and-conditions"]``, please use the registry record ``euphorie.terms-and-conditions``.
- instead of ``appconfig["euphorie"]["use_archive_feature"]``, please use the registry record ``euphorie.use_archive_feature``.
- instead of ``appconfig["euphorie"]["use_clone_feature"]``, please use the registry record ``euphorie.use_clone_feature``.
- instead of ``appconfig["euphorie"]["use_existing_measures"]``, please use the registry record ``euphorie.use_existing_measures``.
- instead of ``appconfig["euphorie"]["use_integrated_action_plan"]``, please use the registry record ``euphorie.use_integrated_action_plan``.
- instead of ``appconfig["euphorie"]["use_involve_phase"]``, please use the registry record ``euphorie.use_involve_phase``.
- instead of ``appconfig["euphorie"]["use_publication_feature"]``, please use the registry record ``euphorie.use_publication_feature``.
- instead of ``appconfig["euphorie"]["use_training_module"]``, please use the registry record ``euphorie.use_training_module``.

More informations can be found in NuPlone 2 README file.

Euphorie 12 uses ``weasyprint`` to render PDF files.
That means that the ``appconfig["euphorie"]["smartprintng_url"]`` is now obsolete.


More information
================

For more information please see the `online documentation
<http://euphorie.readthedocs.org>`_.
