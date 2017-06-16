Changelog
=========

9.0.16 (2017-06-16)
-------------------

- Get rid of ASCIILine, use TextLine for any field that might contain non-ASCII
- Make it possible to translate the "drag&drop help text" for sortables in the
  CMS properly, i.e. in code, not via some CSS hack (again, the problem is
  to support non-ASCII)

9.0.15 (2017-06-06)
-------------------

- Translation updates for "social sharing" and tool notification

9.0.14 (2017-05-11)
-------------------

- Translation fixes ES

9.0.13 (2017-05-11)
-------------------

- Add missing translation setup for the "share via email" text.
  Add translations in FR, ES, CA, refs MPL-399
- Slighly allow more width for the logo, fixes MOI-184

9.0.12 (2017-04-20)
-------------------

- New feature: On a tool, an editor can add an optional message
  that will be displayed to users in the client as a pop-up (re-using
  the message-of-the-day feature)


9.0.11 (2017-03-29)
-------------------

- Missing translation in CA.

9.0.10 (2017-03-29)
-------------------

- In the top-left menu inside a session (osc-header), display the user-
  defined session name, instead of the generic survey name
- Introduced "Share via Twitter / Facebook / Email".
  Must be activated via "allow_social_sharing=True" in euphorie.ini
- When a user enters a guest session, actually open the survey session
  and jump to the start of the survey
- Updated translations in NL

9.0.9 (2017-03-06)
------------------

- Bugfix for report download (print list of all risks): don't choke on user-
  defined custom risks

9.0.8 (2017-02-06)
------------------

- When it comes to generating the reports for download, be more defensive about
  fetching the custom risks (PART II)

9.0.7 (2017-02-06)
------------------

- When it comes to generating the reports for download, be more defensive about
  fetching the custom risks.

9.0.6 (2017-02-06)
------------------

- Translation changes for NL 

9.0.5 (2017-02-01)
------------------

- Add OiRA logo in colour

9.0.4 (2017-01-31)
------------------

- Translation changes for NL
- Release for "Oira 2.0" at TNO/RIE

9.0.3 (2016-12-14)
------------------

- Safeguard against a bug that was spotted repeatedly in the wild, but I
  was not yet able to reproduce: It can happen apparently that Profiles are
  added more than once to a survey. This is an attempt to prevent this.

9.0.2 (2016-11-29)
------------------

- Add translation to HR (Croatian)

9.0.1 (2016-10-31)
------------------

- Shorten text on buttons for report download #14285
- store Sector, Country and Tool names in HTML, so that Piwik code can pick it up

9.0.0 (2016-10-06)
------------------

Major re-write of the client UI


9.0.0rc1 (2016-09-29)
---------------------

- Added new option for regular risks: "Always present". Those risks will appear
  as already answered with "No" in the client. The user cannot change this.
  Syslab #13692


8.0.3 (2016-04-06)
------------------

- Merge in recent change from master:
  Better visibility for password policy and errors on sector settings
  form (Syslab #13310)

8.0.2 (2016-03-04)
------------------

- Replaced browser logos for the "outdated IE version" warning with
  their current equivalents

8.0.1 (2015-12-08)
------------------

- When logging out, make sure the session cookie is really removed
- Translation correction in SL

8.0.0 (2015-11-07)
------------------

- Final release of new major version 8

8.0.0rc3 (2015-11-05)
---------------------

- Translation fixes

8.0.0rc2 (2015-10-21)
---------------------

- Translation fixes

8.0.0rc1 (2015-10-16)
---------------------

**This is a release candidate with incomplete translations**

Feature changes
~~~~~~~~~~~~~~~

- Allow anonymous accounts for visitors who want to try out surveys without
  logging in. The feature needs to be enabled with the "allow_guest_accounts=True"
  option under the [Euphorie] section in the euphorie.ini file (OSHA #10972)
  Necessary upgrade step (16->17):

  * Indicate whether an account is a guest account, converted from one, or neither.

- Allow the users of the client to add their own risks to a survey session. This
  feature needs to be enabled with the "allow_user_defined_risks=True" option
  under the [Euphorie] section in the euphorie.ini file (OSHA #10971)
  Necessary upgrade steps (16-17):

  * Allow custom risks
  * Add new column to identify custom risks

- Use of new Patternslib version, e.g. to enable pat-clone


7.0.10 (2016-08-16)
-------------------

- Enhance survey export so that unwanted characters can be stripped

7.0.9 (2016-05-31)
------------------

- Do not escape characters of the password in the reminder email (Syslab #13579)
- Don't choke in case an image scale can't be fetched. (Syslab #13623)
- Allow Sectors, Surveys and Surveygroups to be renamed

7.0.8 - March 4, 2016
---------------------

- Revert Javascript changes for newer jquery version


7.0.7 - March 4, 2016
---------------------

Feature changes
~~~~~~~~~~~~~~~

- Expose "obsolete" flag in survey edit form. #106
- Better visibility for password policy and errors on sector settings
  form (Syslab #13310)


Bugfixes
~~~~~~~~

- Translation updates
- On logging out, make sure session cookie is really gone
- Don't choke in case of very long paths, resulting from very long survey- or
  module titles.
  Necessary upgrade step (16->17):

  * Allow longer tree item paths



7.0.6 - September 25, 2015
--------------------------

Bugfixes
~~~~~~~~

- Fix a Dutch language error.
- Fix an error in SQL migration utility logic.


7.0.5 - September 15, 2015
--------------------------

Bugfixes
~~~~~~~~

- Translation updates for IS


7.0.4 - April 1, 2015
---------------------

Feature changes
~~~~~~~~~~~~~~~

- More IS translation changes #11552

Bugfixes
~~~~~~~~

- When a survey gets imported from XML, make sure that the 'introduction' text
  gets imported too. Fixes #105
- XML export: the node for classification_code of a Survey had a typo that
  prevented correct import of that value


7.0.3 - March 19, 2015
----------------------

Bugfixes
~~~~~~~~

- More translation changes in IS #11424


7.0.2 - February 12, 2015
-------------------------

- Allow anonymous accounts for visitors who want to try out surveys without
  logging in. The feature needs to be enabled with the "allow_guest_accounts" option
  under the [Euphorie] section in the euphorie.ini file (OSHA #10972)

Bugfixes
~~~~~~~~

- Terms & Conditions: Change location, due to move of servers (OSHA #10858)
- Fix a bug in delete confirmation so that double quotes (which can come from
  translations) no longer break the Javascript (OSHA #10925)
- Translations changes in Icelandic (OSHA #11294)


7.0.1 - September 03, 2014
--------------------------

Bugfixes
~~~~~~~~

- Translation fixes in FI (OSHA #10635)


7.0.0 - August 29, 2014
-----------------------

Upgrade notes
~~~~~~~~~~~~~

This release is dependent on Plone 4.3 and higher.

This release updates the profile version. Please use the upgrade
feature in ``portal_setup`` to upgrade the ``euphorie.deployment:default``
profile.

Feature changes
~~~~~~~~~~~~~~~

- Add and enforce a password policy (OSHA #10286)
- When a sector our country manager is created, the new user receives an e-mail
  for setting the password; the admin no longer chooses the password initially
- On existing country and sector manager accounts, an admin can still manually
  set a new password.
- Lock users out after a certain amount of failed login attempts.
  Configured with the *max_login_attempts* setting in euphorie.ini.
  Set to 0 to disable completely. (OSHA #10286)



6.3.5 - July 08, 2014
---------------------

Bugfixes
~~~~~~~~

- Corrected typo in PT


6.3.4 - July 07, 2014
---------------------

Feature changes
~~~~~~~~~~~~~~~

- Differentiate between the CSS classes given to the active node in the
  navigation tree, and its parent. (OSHA #9953)
- CMS user's passwords are now hashed. (OSHA #10285)

Bugfixes
~~~~~~~~

- Translation corrections in IT (OSHA #10039 #10370)


6.3.3 - May 23, 2014
--------------------

Feature changes
~~~~~~~~~~~~~~~

- Add two more questions to the company survey (OSHA #9281)
- Customise the name of "Macedonia" to "F.Y.R. Macedonia" due to
  political sensitivities (OSHA #10100)
- Translation correntions in SL (OSHA #10059 #9589)


6.3.2 - May 2, 2014
-------------------

Feature changes
~~~~~~~~~~~~~~~

- For the left-hand navigation in the OSHA styles, make the current menu
  item white and bolder (OSHA #8472)

Bugfixes
~~~~~~~~

- Translation corrections in SL (OSHA #9584)
- Translation corrections in FI (OSHA #9806)
- Translation corrections in BG (OSHA #9790)


6.3.1 - March 2, 2014
---------------------

Bugfixes
~~~~~~~~

- Added missing i18n statement around "Official OiRA logo" in the settings
  form
- Translation corrections in IS (OSHA #9345)
- Translation corrections in LT (OSHA #9510)
- Translation corrections in BG (OSHA #9324)
- Fix logo positioning on homepage in mobile view


6.3.0 - January 14, 2014
------------------------

Feature changes
~~~~~~~~~~~~~~~

- Track clicks on externals links using an `external-link` event in Google
  Analytics.

- Track report downloads as a virtual pageview in Google Analytics.

- Add four new virtual page views for Google Analytics in the client:

  * .../login/success - used after successfull login
  * /*<country>*/register/success - used after successfully registering a new
    account.
  * /*<country>*/*<sector>*/*<survey>*/start - used when starting a new survey
    session.
  * /*<country>*/*<sector>*/*<survey>*/resume - used when resuming a survey
    session.

Bugfixes
~~~~~~~~

- Various styling improvements for the online client on mobile devices.

- Remove default Google Analytics account information.

- Remove the *Status* button on the help page if the user is not in a survey
  session.


6.2.1 - January 02, 2014
------------------------

Bugfixes
~~~~~~~~

- Fix display of not-found page when accessing acquisitioned content from outside
  the client in the client. This fixes `issue 99
  <https://github.com/euphorie/Euphorie/issues/99>`_.

- In the client, write the current language as class into the body tag, so that
  language specific CSS rules can be applied.

- The default_priority field could overwrite the fixed_priority field when saving
  a Risk from the edit form.

- Improvements for the mobile view

- Re-ran yui-compression for the CSS files, since some changes had not made it in previously


6.2 - December 19, 2013
-----------------------

Bugfixes
~~~~~~~~

- Restore add buttons for non-survey content in the content editor.

- Fix error in generation of RTF reports for sessions with a depth larger
  than 4. This fixes `TNO ticket 245
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/245`_.

- Move register link up in the frontpage to make it more noticable: too many
  people missed it in its original position, leading to support requests. This
  fixes `TNO ticket 247
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/247`_.

- New translations in Italian (IT) and Icelandic (IS). OSHA #8434

- New translations in Maltese (MT). OSHA #8435

- Translation fixes in PT. OSHA #9193


6.1.3 - November 15, 2013
-------------------------

Bugfixes
~~~~~~~~

- Added missing English text for the "outdated browser" warning. OSHA #9094

- Add missing import statement. This caused a site error when trying to
  resume an existing session in the client.


6.1.2 - October 31, 2013
------------------------

Bugfixes
~~~~~~~~

- If a survey title was modified through the survey version edit form the title
  was not updated in the index, which caused the old title to still be shown in
  the navigation tree.


6.1.1 - October 30, 2013
------------------------

Bugfixes
~~~~~~~~

- Fix a packaging error which broke the 6.1.1 release.


6.1 - October 30, 2013
----------------------

Feature changes
~~~~~~~~~~~~~~~

- Add a new *fixed* evaluation method for risks. If this is used the sector
  organisation can set the risk priority directly, and the risk will be skipped
  during evaluation.

- Modify handling of profile questions in the client: include the profile
  question in the survey tree to make the naming more intuitive for users.

- Add a new *obsolete* flag to survey groups. When a survey with this flag is
  set is published it will be put into a new group of obsolete surveys in the
  client. This addresses part of `TNO ticket 200
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/200>`_.

- Make it possible to edit the survey group title from a survey edit screen.
  This addresses part of `TNO ticket 200
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/200>`_.

- Add page number to RTF reports. This fixes
  `TNO ticket 241 <https://code.simplon.biz/tracker/tno-euphorie/ticket/241>`_.

- For OSHA, show the legend only in the identification phase.


Bugfixes
~~~~~~~~

- Security fix: modify client to always check if a survey session belongs
  to the current user.

- Fixed a typo in the client splash page. OSHA ticket #7261.

- Translation updates:

  - Add Bulgarian help headers. OSHA ticket #7317.

  - Add Portuguese translations of the splash page. OSHA ticket #7870.

  - Translate ``label_keep_logged_in`` on the client login page. OSHA ticket #7823.

  - Several minor translation fixes and updates. OSHA tickets #7830, #7766,
    #7810, #7829 and #8369.

  - Kosovo, Montenegro and Republic of Serbia are now translatable, and add
    bulgarian translations. OSHA ticket #7808.

  - Greek translation fixes. OSHA ticket #7704

  - Portugese translation fixes. OSHA ticket #7934

  - Applied new translations in 15 languages. OSHA tickets #7938, #8190, #8780

  - Added MIT Licensed script to display browser warning so that we can support
    translations. This addresses part of `OSHA ticket 7847
    <https://projects.syslab.com/issues/7847>`_ and
    `OSHA ticket 7929 <https://projects.syslab.com/issues/7929`_.

  - Added missing CA translations in the "ancient browser" warnings. This fixes
    `OSHA ticket 8418 <https://projects.syslab.com/issues/8418>`_.


6.0.1 - June 3, 2013
--------------------

- Changed tiles/AddBar to explicitly list every "Add" button with full label.
  Needed for languages where the object of "add" needs a different word form
  than the nominative case, such as Lithuanian.

- Include the top-level module in the downloadble action plan spreadsheet.

- Ensure that end date cannot be before start date in the action plan.


6.0 - May 1, 2013
-----------------

- Use scheme-less URLs for fonts so they always use the same scheme as the
  current page.

- Update Dutch translations.


6.0rc3 - April 23, 2013
-----------------------

- Update Dutch, Latvian, Lithuanian and Finnish translations.
- Use https in stylesheets (for google fonts).
- Added Hungarian translations


6.0rc2 - April 15, 2013
-----------------------

- Added Hungarian translations
- Expand OiRA acronym in header on login page (agency #7262)


6.0rc1 - April 3, 2013
----------------------

**This is a release candidate with incomplete translations.**

Bugfixes
~~~~~~~~

- Display risk information in the client evaluation page as a message so links
  are readable. This fixes `ticket 93
  <https://github.com/euphorie/Euphorie/issues/93>`_.

- Include modules without a description in the navigation tree. This fixes
  `TNO ticket 236 <https://code.simplon.biz/tracker/tno-euphorie/ticket/236>`_.

- Fix a typo in the Dutch translations. This fixes
  `TNO ticket 237 <https://code.simplon.biz/tracker/tno-euphorie/ticket/237>`_.

- Show titles for profile questions in the right order in the profile form.

- Fixed the wrong translations for the timeline xls export priorities

- Fix header styling in the client. Added a body > in sector style before the
  h1 so that it is more specific

- Exchanged translation labels for priority names to match the translations in
  the action plan view. The timeline msgids seem to be fuzzy: the translation
  for low and high is translated as "default"


6.0b4 - March 19, 2013
----------------------

**This is a beta release with incomplete translations.**

Bugfixes
~~~~~~~~

- Add translations in fr, el, lv for "Keep me logged in". Fixes #6846

- Require a newer NuPlone[r] version to fix CMS add and edit forms.

- Correct the navigation tree legend: the description for answered risks was
  not correct.

- Fixed IE9 navtree rendering bug.

- updated the text for the new login splash screen


6.0b2 - March 5, 2013
---------------------

**This is a beta release with incomplete translations.**

Bugfixes
~~~~~~~~

- Correctly initialise a newly added measure for a risk. This fixes
  `ticket 86 <https://github.com/euphorie/Euphorie/issues/86>`_.

- Prevent users from entering non-digits in number input fields. This fixes
  part of `ticket 84 <https://github.com/euphorie/Euphorie/issues/84>`_.

- Fix display of error messages in the risk action plan form. This fixes part
  of `ticket 84 <https://github.com/euphorie/Euphorie/issues/84>`_.

- Always order the measures for a risk based on moment of creation. This
  prevents unexpected ordering changes.

- Renamed a default translation in ``content/help.py```` that lead to a
  duplication in the pot file

- Fix bad translations for column headers in the action plan timeline.


6.0b1 - February 15, 2013
-------------------------

Upgrade notes
~~~~~~~~~~~~~

**This is a beta release with incomplete translations.**

Python 2.7 is now fully supported and the recommended Python version to use.
Python 2.6 is still supported.

zc.buildout has been updated to version 2. You will need to re-bootstrap your
buildout when upgrading to Euphorie 6.

This release updates the profile version to *13*. Please use the upgrade
feature in ``portal_setup`` to upgrade the ``euphorie.deployment:default``
profile to this version.

This release also updates the used Plone version to 4.2.4. You are advised to
perform the Plone migrations through the Zope Management Interface (ZMI).

The Euphorie configuration file (``etc/euphorie.ini`` in the standard buildout)
no longer needs to include the complete configuration. You now only need to
specify details that are specific to your deployment such as the Google Analytics
accounts and client URL.

Feature changes
~~~~~~~~~~~~~~~

- Add a small FAQ to the login page.
- IE 6 is no longer supported. IE 7 is only provisionally supported: it might
  work, but any bugs will no longer be fixed.
- Add a legend to the client navigation tree to explain the used icons. This
  fixes `ticket 51 <https://github.com/euphorie/Euphorie/issues/51>`_.
- Optional profile questions have been replaced with option modules. Previous
  versions supported both, and they did almost exactly the same thing which was
  a source of consution. All existing optional profile questions will
  automatically be converted to optional modules as part of the upgrade.
- Added translations for Finnish (FI) and Lithuanian (LT)
- Updated Bulgarian translations.
- Include a default application configuration file.

Bugfixes
~~~~~~~~

- Correctly show the high-priority notice for risks in the online view of
  the action plan report.

- Start using the `Patterns <http://patternslib.com/>`_ library for the
  client user interface.

- Use consistent styling of form error messages. This fixes tickets `45
  <https://github.com/euphorie/Euphorie/issues/45>`_ and
  `46 <https://github.com/euphorie/Euphorie/issues/46>`_.

- Do render bold text as white on a light background in the risk action plan
  page for the client. This fixes `ticket 75
  <https://github.com/euphorie/Euphorie/issues/75>`_.

- Use a custom icon font to display the warning-icon in client reports. This
  helps for browsers/computers that do not include the unicode warning
  symbol in their font. This fixes `ticket 61
  <https://github.com/euphorie/Euphorie/issues/61>`_.

- Change default font for page titles in the client to a font which does not
  have problems with Greek characters. This fixes `ticket 74
  <https://github.com/euphorie/Euphorie/issues/74>`_.

- Dutch Translation: Fix bad column header in timeline report.

- Correct rendering of strong text in the client to make sure it is easy to
  read. This fixes `ticket 65
  <https://github.com/euphorie/Euphorie/issues/65>`_ and
  `TNO ticket 232 <https://code.simplon.biz/tracker/tno-euphorie/ticket/232>`_.

- Fix several positioning bugs in the client user interface. This fixes
  tickets `52 <https://github.com/euphorie/Euphorie/issues/52>`_ and
  `63 <https://github.com/euphorie/Euphorie/issues/63>`_

- Make sure pasted content does not violate any internal rules. It used to
  be possible to do things like mix risks and modules in a single container
  using copy & paste.

- Upgrade to zc.buildout 2, dexterity 1.2.1 and Plone 4.2.4.

- Registering from within a country would incorrectly skip terms and conditions
  page.

- Datepicker didn't appear on newly created measures.

- Fix compatibility with plone.app.search.


5.1.1 - January 9, 2013
-----------------------

Feature changes
~~~~~~~~~~~~~~~

- Remove country headings and instead show countries alphabetically (with EU at
  the top).

Bugfixes
~~~~~~~~


5.1 - December 12, 2012
-----------------------

Upgrade notes
~~~~~~~~~~~~~

This release changes the cookie format used to authenticate users in the
client. As a result all currently logged in users will need to login again
after upgrading to this version.


Feature changes
~~~~~~~~~~~~~~~

- Sort sessions on client start screen so most recently modified sessions
  are listed first.

- Display the survey introduction text on the survey view page in the CMS.

- Add a new API to manage country manager and sector CMS accounts.

- Add option in the client login to remember a user.

- CMS: update survey display to show profile questions and modules in a single
  list. This makes the display simpler and allows better reordering.

Bugfixes
~~~~~~~~

- Remove extra space after risk severity in action plan report. This fixes
  `TNO ticket 215 <https://code.simplon.biz/tracker/tno-euphorie/ticket/215>`_.

- Fix broken translations for risk comments in identification phase. This fixes
  `TNO ticket 230 <https://code.simplon.biz/tracker/tno-euphorie/ticket/230>`_.

- Show our favicon in the client.

- IE8 fix in client. Adding a standard solution to an new/empty solution
  produces popup alerting user that they are overriding existing values.

- Fix for unicode error when providing non-ascii profile question values.



5.0 - November 22, 2012
-----------------------

Feature changes
~~~~~~~~~~~~~~~

- Update Dutch translations. This fixes
  `TNO ticket 223 <https://code.simplon.biz/tracker/tno-euphorie/ticket/223>`_.

- Add jQueryUI datepicker to the date fields in the risk action plan page [jcbrand]

- Modify all reports to always add a marker for present risks so users can more
  easily find them. This fixes
  `TNO ticket 206 <https://code.simplon.biz/tracker/tno-euphorie/ticket/206>`_.

Bugfixes
~~~~~~~~

- Several fixes for the risk action plan form (client):

  - i18n bugfix. [thomasw]

  - Do not silently ignore start and end dates for action plan measures of no
    date was provided. This fixes `TNO ticket 225
    <https://code.simplon.biz/tracker/tno-euphorie/ticket/225>`_.

  - Handle internal error for dates with large years.

- Remove stray double quote in section titles in identification report. This fixes
  `TNO ticket 222 <https://code.simplon.biz/tracker/tno-euphorie/ticket/222>`_.

- Really show the notification that a password reminder has been sent. This fixes
  `TNO ticket 229 <https://code.simplon.biz/tracker/tno-euphorie/ticket/229>`_.

- Added missing i18n statement on conditions page [thomasw]

- Fix bad link in introduction text for action plan report. This fixes
  `TNO ticket 227 <https://code.simplon.biz/tracker/tno-euphorie/ticket/227>`_.



4.1.3 - October 1, 2012
-----------------------

Bugfixes
~~~~~~~~

- Client API changes:

  - Return the update-hint as JSON data.
  - Remove invalid next-step hint which was included on the session action-plan
    response if a survey has no risks present.
  - Use image URLs within the client API so images can be accessed by users who
    are not logged in on the client site. This reverts a change from 4.1.1.


4.1.2 - September 28, 2012
--------------------------

Bugfixes
~~~~~~~~

- Client API changes:

  - return a proper JSON error message if invalid JSON data is received.
  - return a proper JSON error message if an unsupported HTTP method is used.


4.1.1 - September 27, 2012
--------------------------

Upgrade notes
~~~~~~~~~~~~~

This release upgrades Plone from version 4.1.3 to version 4.1.6. This may
require to re-bootstrap your buildout if you see an error like this::

    While:
      Installing.
      Getting section instance.
      Initializing section instance.
      Installing recipe plone.recipe.zope2instance.
    Error: There is a version conflict.
    We already have: Zope2 2.13.10


Bugfixes
~~~~~~~~

- Client API changes:

  - correct the URL for the original image size. This fixes `issue 38
    <https://github.com/euphorie/Euphorie/issues/38>`_.
  - make sure image URLs point to the client instead of the API location.



4.1 - August 29, 2012
---------------------

Upgrade notes
~~~~~~~~~~~~~

This release updates the profile version to *12*. Please use the upgrade
feature in ``portal_setup`` to upgrade the ``euphorie.deployment:default``
profile to this version.


Feature changes
~~~~~~~~~~~~~~~

- Add Flemish (nl_BE), Latvian (lv), Greek and Catalan (ca) translations.
  [thomasw]

- Client API modifications:
  - Add module title to the returned risk information.
  - Expose risk standard solutions.

- Updated privacy policy text. [jcbrand]


Bugfixes
~~~~~~~~

- Report styling improvements: correct display of comments to they are
  readable when printing a report.
  [cornae]

- Implement missing export of image data for modules and risks in the client
  API. This also changes the datastructure used for images; this should not
  break existing clients since image data was never present in earlier versions.
  [wichert]

- Fix survey XML importer to generate filenames for images if not provided.
  This solves problems with not being able to see fullsize images for
  imported images.
  [wichert]

- Show proper help URL when outside of a survey. [jcbrand]

- Correct display of standard solution titles in the CMS navigation tree.
  [jcbrand]


4.0.2 - June 21, 2012
---------------------

- Added Czech translations. [jcbrand]

- Fix access problem for survey session views in the client API.
  [wichert]


4.0.1 - June 18, 2012
---------------------

- Fix bad release.
  [wichert]


4.0 - June 18, 2012
--------------------

Upgrade notes
~~~~~~~~~~~~~

This release updates the profile version to *11*. Please use the upgrade
feature in ``portal_setup`` to upgrade the ``euphorie.deployment:default``
profile to this version. For large systems this migration spent a long
time in a SQL migration; in that situation it may be useful to run a
manual SQL migration step by hand first: connect to the database and
issue these SQL statements::

    ALTER TABLE action_plan ADD COLUMN reference TEXT;
    ALTER TABLE account ALTER COLUMN password DROP NOT NULL;


Feature changes
~~~~~~~~~~~~~~~

- Expose client functionality with via simple REST API.
  [wichert]


3.2.3 - May 16, 2012
--------------------

- SQL performance work: revise SQL query used to copy survey session data
  on a survey update to use UPDATE FROM. This means we are no longer ANSI
  SQL compliant, but makes the query run 20-50 times faster.
  [wichert]

- SQL performance work: add two extra indices to improve performance for
  looking up risk data.
  [wichert]


3.2.2 - May 14, 2012
--------------------

- 3.2.1 was a paper-brown-bag release. Try again.
  [wichert]


3.2.1 - May 14, 2012
--------------------

Bugfixes
~~~~~~~~

- Fix a bug in rendering identification reports.
  [wichert]


3.2 - May 10, 2012
------------------

Upgrade notes
~~~~~~~~~~~~~

This release updates the profile version to *10*. Please use the upgrade
feature in ``portal_setup`` to upgrade the ``euphorie.deployment:default``
profile to this version. For large systems this migration spent a long
time in a SQL migration; in that situation it may be useful to run a
manual SQL migration step by hand first: connect to the database and
issue this SQL statement::

    ALTER TABLE tree ADD has_description bool DEFAULT 'f';

Feature changes
~~~~~~~~~~~~~~~

- Remove warning-icon for risks with a problem description in the action plan
  report. Since this report only contains present risks the icon was not useful.
  This fixes `TNO ticket 219
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/219>`_.
  [wichert]

- Change default for top5 risks to not be present to work around frequent abuse
  of top5 risks by sector organisations. They will still always be included in
  reports even if not present. This fixes `TNO ticket 216
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/216>`_.
  [wichert]

- Change default for optional modules to present based on user feedback.
  This fixes `TNO ticket 197
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/197>`_.
  [wichert]

- Make description for modules optional. If a module has no description
  it is skipped in the client. This fixes `TNO ticket 213
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/213>`_.
  [wichert]

Bugfixes
~~~~~~~~

- Small grammar fix in Dutch translation for action plan introduction text.
  This fixes `TNO ticket 220
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/220>`_.
  [wichert]

- Add missing introductionary sentence in a direct survey view in the
  client which explains that a user can create a new survey. This fixes
  `TNO ticket 193
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/193>`_.
  [wichert]

- Fix case handling of email addresses when changing the email address
  in the client. Previously it was possible to change to an email address
  with capital, after which login was no longer possible.  This fixes
  a final part of `TNO ticket 194
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/194>`_.


3.1.1 - April 27, 2012
----------------------

Upgrade notes
~~~~~~~~~~~~~

No special upgrade steps are needed for this release.

Feature changes
~~~~~~~~~~~~~~~

- Add a caption field for module image captions. This fixes `TNO ticket 210
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/210>`_.
  [wichert]

- Position images for module views on the right side of the page so they
  do not break running text as badly. This should fix `TNO ticket 211
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/211>`_.
  [wichert]

- Use a slightly larger image size for the module views, and enable
  image zoom (fancybox). This fixes `TNO ticket 209
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/209>`_.
  [wichert]

Bugfixes
~~~~~~~~

- Fix case handling of email addresses when changing the email address
  in the client. Previously it was possible to change to an email address
  with capital, after which login was no longer possible.  This fixes
  a final part of `TNO ticket 194
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/194>`_.
  [wichert]

Other changes
~~~~~~~~~~~~~

- Small code restructuring to make it easier for derived sites to change
  filters for reports.
  [wichert]

3.1 - March 15, 2012
--------------------

Upgrade notes
~~~~~~~~~~~~~

No special upgrade steps are needed for this release.


Feature changes
~~~~~~~~~~~~~~~

- Do not open list of all risks (under inventorisation) in a new window or tab.
  This fixes `TNO ticket 205
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/205>`_.
  [wichert]

- Add a new column with the risk number to the Action plan xlsx rendering. This
  fixes `TNO ticket 203
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/203>`_.
  [wichert]

- Update Dutch translations.
  [wichert]

- Added Bulgarian translations
  [thomasw]

Bugfixes
~~~~~~~~

- Fix handling of text-style tags (strong/b/em/etc.) outside paragraphs
  when generating an RTF report. This fixes the second part of
  `TNO ticket 208
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/208>`_.
  [wichert]

- Fix colour of bold text in reports. This fixes
  `TNO ticket 208
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/208>`_.
  [wichert]

- The identification report wrongly showed the problem description for
  unanswered risks. This fixes
  `TNO ticket 207
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/207>`_.
  [wichert]

- Fix broken translations on risk action plan template. This fixes
  `TNO ticket 201
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/201>`_.
  [wichert]

- Use problem description instead of risk title in action timeline. This fixes
  `TNO ticket 202
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/202>`_.
  [wichert]

- No longer rotate the client navigation tree.
  [jcbrand, wichert]

- Bugfix, unpublishing a survey that's in an active session raises KeyError.
  [jcbrand]

- Bugfix. CMS-style accessors must return bytestrings.
  [jcbrand]

- Removed setuptools_git as a dependency.
  [jcbrand]

- Fixed 2 typos that caused duplicate default translations
  [thomasw]



3.0.1 - December 28, 2011
-------------------------

- Fix packaging error.
  [wichert]


3.0 - December 28, 2011
-----------------------

Upgrade notes
~~~~~~~~~~~~~

Development of Euphorie and related projecst has moved to the
`euphorie organisation <https://github.com/euphorie>`_ on github.

This release updates the profile version to *9*. Please use the upgrade
feature in ``portal_setup`` to upgrade the ``euphorie.deployment:default``
profile to this version.

Feature changes
~~~~~~~~~~~~~~~

- Add a timeline export for the action plan: this generates an xlsx file
  with all measures for all risks.
  [wichert]

- Change risk priority terminology in Dutch.
  [wichert]

- Add an *Currently unknown* option for risk identification. This can be
  used to remove an existing answer.
  [wichert]

- Ignore case when checking the email address for client logins.
  [wichert]

- Use a better standard solution selector in the client. This fixes
  `github ticket 5 <https://github.com/euphorie/Euphorie/issues/5>`_.
  [cornae, wichert]

- Group countries according to EU membership status.  This fixes github tickets
  `1 <https://github.com/euphorie/Euphorie/issues/1>`_,
  `2 <https://github.com/euphorie/Euphorie/issues/2>`_ and
  `4 <https://github.com/euphorie/Euphorie/issues/4>`_.
  [cornae, wichert]

- Add another evaluation algorithm (French) for calculating risk priorities.
  [wichert]

- Upgrade client to jQuery 1.4.4 and jQuery UI 1.7.3.
  [wichert]

- Add an extra field 'workers_participation' to the Company form (and column to
  the SQL table).
  [jcbrand]

- Use z3c.zrtresource (and collective.zrtresource while still Plone < 4.1) to
  compile screen-ie6.css. This allows Cornelis to use physical paths in his
  Prototype, while zrtresource will give us the proper browserresource paths in
  Euphorie. One caveat is that we now have to minify the browserresource file
  (i.e ``http://localhost:4080/Plone2/client/++resource++screen-ie6.css``) instead
  of the filesystem file.
  [jcbrand]

- Add delete validation on a sector to check that it doesn't contain any
  published surveys.
  [jcbrand]

- Update Slovenian translations.
  [thomas_w]

Bugfixes
~~~~~~~~

- Fix positioning of comments in the inventorisation report. This fixes
  TNO ticket 192.
  [cornae]

- Fix downloadable reports to correctly show a risks problem description.
  [wichert]

- Fix HTML->RTF conversion to not duplicate texts of links/bold/italic text
  in descriptions.
  [wichert]

- Fix survey tree update code to also rebuild the session for all tree changes
  instead of only profile changes. This fixes problems KeyErrors that appeared
  after publishing a survey which removes modules or risks.
  [wichert]

- Fix check for survey changes in the client: the old code falsely assumed
  client surveys were cataloged.
  [wichert]

- Hide hover beautytips on IE6 and clicktips on IE6 and IE7
  [jcbrand]

- For extra robustness add extra check in new survey creation logic to make
  sure a valid survey was passed in.
  [wichert]

- Effect wasn't set for French risks when added to the session tree.
  [jcbrand]

- #15: AttributeError *is_region* when publishing from a country not yet in the
  client.
  [jcbrand]

- For SurveyGroup, hide Evaluation Algorithm field on @@edit.
  [jcbrand]

- Allow the default sector colours to be customized via the euphorie.ini file
  [jcbrand]

- Change ordering of countries in the client to match the `official
  EU ordering <http://publications.europa.eu/code/pdf/370000en.htm>`_).
  This fixes `github ticket 3
  <https://github.com/euphorie/Euphorie/issues/3>`_.
  [wichert]

- Fixed Terms&Conditions page for anonymouse users.
  [jcbrand]

- During action plan phase, include all measures on request when validation
  fails.
  [jcbrand]

- Updated optional modules that are now mandatory must not have their children
  skipped.
  [jcbrand]


2.7 - April 26, 2011
--------------------

- Various improvements for managing standard solutions:

  - Use a separate view to show all information, and provided a point
    where solutions can be deleted.
    [wichert]

  - Allow drag&drop ordering for standard solutions.
    [wichert]

- Use standard styling for Sphinx docs to make things more readable.
  [wichert]

- Hide removed surveys from session lists.
  [wichert]

- Fix incomplete display of errors on end dates for measures in the online
  client. This is part of `TNO ticket 150`.
  [wichert]

- Tweak screen-osha.css to show risk priorities on action plan report without
  any bells and whistles. [jcbrand]

- Fix common solution adding in the client for IE 7. This fixes the second part
  of `TNO ticket 127
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/127>`_.
  [wichert]


2.6 - April 7, 2011
-------------------

Upgrade notes
~~~~~~~~~~~~~

This release updates the profile version to *6*. Please use the upgrade
feature in ``portal_setup`` to upgrade the ``euphorie.deployment:default``
profile to this version.

Feature changes
~~~~~~~~~~~~~~~

- Add compatibility with SQLAlchemy 0.6.
  [wichert]

- Add a new EU region in addition to the existing countries.
  [wichert]

- Add unpublish feature to the CMS.
  [cornae, wichert]

- Clearly mark countries without surveys on the client frontpage.
  [cornae, wichert]

- Add options to change password, change email address or delete your account
  to the online client.
  [cornae, wichert]

Bug fixes
~~~~~~~~~

- Attempt to improve HTML->RTF conversion when generating downloadable
  reports.
  [wichert]

- Fix bug in handling of counting risk states for the client survey status screen.
  This fixes the second part of `TNO ticket 155
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/155>`_.
  [wichert]

- Added a euphorie.po for EN, so that we can also use the translation engine for
  that language, without the need to pass a default value. The file is a copy of
  euphorie.pot, with the msgstr being filled from the default entry or as a fallback
  from the msgid
  [thomasw]


2.5 - February 28, 2011
-----------------------

- Restore print button on identification report page; it seems users are
  unable to find the print function of their browser. This fixes
  `TNO ticket 159 <https://code.simplon.biz/tracker/tno-euphorie/ticket/159>`_.
  [wichert].

- Fix small errors in Dutch translation. This fixes
  `TNO ticket 175 <https://code.simplon.biz/tracker/tno-euphorie/ticket/175>`_.
  [wichert].

- Replace escape enters with proper newlines in downloadable report.  This
  fixes
  `TNO ticket 174 <https://code.simplon.biz/tracker/tno-euphorie/ticket/174>`_.
  [wichert].

- Added some ``<br/>`` tags to avoid the navigation vanishing in IE7
  [pilz]

- Update the minified css files from the originals to reflect recent
  changes cornae did to fix ie compatibility .
  [pilz]

- Add report header styles for an extra depth level. This fixes problems
  when generating reports for deeply nested surveys. This fixes
  `TNO ticket 176 <https://code.simplon.biz/tracker/tno-euphorie/ticket/176>`_.
  [wichert].


2.4 - January 25, 2011
----------------------

Feature changes
~~~~~~~~~~~~~~~

- Enable the terms and conditions features introduced in release 2.3, but
  make it possible to disable it via a settings in the ``.ini`` file. This
  fixes `ticket 107 <https://code.simplon.biz/tracker/euphorie/ticket/107>`_.
  [wichert]

- Replace downloadable action plan report with a RTF version. This solves
  problems with opening and editing the previous html fake-.doc approach.
  Downside of this approach is the loss of styling for the report.
  [wichert]

- Extend client form CSS to support percentage fields.
  [cornae]

- Added Greek translation provided by external translator for euphorie.pot;
  the latest additions are not translated yet [thomas]

Bugfixes
~~~~~~~~

- Do not loose value of the referer field on the company details form.
  [wichert]

- The i18n msgid "label_login" was used for 2 different meanings. In
  content/user.py and content/upload.py, the msgid "label_login_name"
  is now used for the LoginField
  [thomas]

- Added msgid "label_preview", Default "Preview", as disambiguation
  from "header_preview" (Preview survey) and "button_preview"
  (Create preview)
  [thomas]

- in euphorie/content/risk.py changed Default translation for
  label_problem_description to "Inversed statement", as given in
  euphorie/content/templates/risk_view.pt
  [thomas]

- in euphorie/content/upload.py added 2 new msgids, since the
  ones that were used already have a different meaning
  label_survey_title -> label_upload_survey_title
  help_surveygroup_title -> help_upload_surveygroup_title
  [thomas]


2.3 - January 11, 2011
----------------------

Feature changes
~~~~~~~~~~~~~~~

- Change title of edit form for non-toplevel modules to *Edit Submodule*.
  [wichert]

- Allow deletion of content in published surveys. The old behaviour was
  theoretically better, but turned out to be very confusing for users
  for little benefit.
  [wichert]

- Add feature to require users of the client to agree to the terms and
  conditions of the site. Disabled until the terms and conditions document
  has been written.
  [wichert]


Bugfixes
~~~~~~~~

- Fix bad workflow configuration for surveys. This is related to the fix
  for `TNO ticket 124`_.
  [wichert]

- Correct METAL macro invocation in client templates.
  [brand]


2.2 - December 7, 2010
----------------------

Feature changes
~~~~~~~~~~~~~~~

- Change the ordering of the risk types as requested by OSHA ticket 2253.
  [brand]

- Switch the client to the new OiRA logo.
  [cornae,pilz,wichert]

- When making a copy of a survey reset its workflow state back to *draft*. This
  allows deleting of content in a new survey that is based on a published
  survey. This is part of `TNO ticket 124`_.
  [wichert]

Bugfixes
~~~~~~~~

- The survey status screen could show module titles that do not match the
  current session. This fixes `TNO ticket 155`_.
  [wichert]

- Stop declaring ``eupphorie`` to be a namespace package.
  [wichert]

- Require NuPlone 1.0rc1 or later so ``formatDate`` does not raise exceptions
  for pre-1900 dates. This fixes `TNO ticket 150
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/150>`_.
  [wichert]

- Do not accept pre-1900 dates in the action plan, since they break rendering
  of the report.  This prevents `TNO ticket 150`_ from occuring.
  [wichert]



2.1 - November 6, 2010
----------------------

Feature changes
~~~~~~~~~~~~~~~

- Update Dutch translations.
  [wichert]

- Perform basic verification of email addresses in the client registration
  logic. This fixes `TNO ticket 147
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/147>`_.
  [wichert]


Bugfixes
~~~~~~~~

- Purge cached scaled logos when publishing a survey and updating the sector logo.
  This fixes `TNO ticket 136 <https://code.simplon.biz/tracker/tno-euphorie/ticket/136>`_.
  [wichert]

- Translate subject of password reminer email. This fixes
  `TNO ticket 148 <https://code.simplon.biz/tracker/tno-euphorie/ticket/148>`_.
  [wichert]

- Rewrite client company form to use z3c.form instead of repoze.formapi.
  [wichert]


2.0, October 22, 2010
---------------------

No changes.


2.0rc5, October 11, 2010
------------------------

Bugfixes
~~~~~~~~

- Fix rendering of profile questions in the client. This was caused by a bad
  fix for `TNO ticket 135`_.
  [wichert]

- When creating a XML export of a survey use the title of the survey group
  instead of the survey version.
  [wichert]

- Fix javascript syntax on the client frontpage which broke IE7.
  [wichert]

- Added translation for the profile content type description
  [pilz]


2.0rc4, October 7, 2010
-----------------------

Bugfixes
~~~~~~~~

- Fix spelling error in Dutch translation. This fixes `TNO ticket 131
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/131>`_.
  [wichert]

- Correct bad image scaling test when displaying a module in the client, which
  prevented images from being visible in action plan and evaluation phases. This
  fixes `TNO ticket 135 <https://code.simplon.biz/tracker/tno-euphorie/ticket/135>`_.
  [wichert]


2.0rc3, October 5, 2010
-----------------------

Upgrade notes
~~~~~~~~~~~~~

This release updates the profile version to *4*. Please use the upgrade
feature in portal_setup to upgrade the ``euphorie.deployment:default``
profile to this version.

Feature changes
~~~~~~~~~~~~~~~

- Update the French translation of the survey creation guide.
  [pilz]

- Replace the collected company details with more generic information. The
  previous list is still used in the `Dutch RI&E site <http://instrumenten.rie.nl>`_
  and is now implemented in `tno.euphorie <http//pypi.python.org/pypi/tno.euphorie/>`_.
  This fixes `ticket 142 <https://code.simplon.biz/tracker/euphorie/ticket/142>`_.
  [wichert]

- Add missing question field to profile questions, and update the XML export
  code to export it. The XML import code and format specification already
  described this field.
  [wichert]

Bugfixes
~~~~~~~~

- Use longer input boxes for title and question fields in the CMS.
  [pilz]

- Improve various texts.
  [pilz]

- Fix creation of report downloads for sessions with non-ASCII characters in
  their title. This fixes `ticket 156
  <https://code.simplon.biz/tracker/euphorie/ticket/156>`_.
  [wichert]

- Handle multiple buttons as returned by IE correctly in the company detail
  form. This could lead to site errors before.
  [wichert]

- Fix handling of partial date fields in company details forms.
  [wichert]

- Add publish permission to country managers. This fixes
  `TNO ticket 126 <https://code.simplon.biz/tracker/tno-euphorie/ticket/126>`_
  [wichert]

- Declare dependency for question field in the module edit screen: it should
  only be shown for optional modules.
  [wichert]

- Fix bug in upgrade step for migration to 2.0rc2 which broke updating of
  security settings for existing content.
  [wichert]


2.0rc2, September 29, 2010
--------------------------

Upgrade notes
~~~~~~~~~~~~~

This release updates the profile version to *3*. Please use the upgrade
feature in portal_setup to upgrade the ``euphorie.deployment:default``
profile to this version.

Bugfixes
~~~~~~~~

- Add ``Copy or Move`` permission information to the published state of
  the survey workflow. This fixes
  `TNO ticket 124 <https://code.simplon.biz/tracker/tno-euphorie/ticket/124>`_
  [wichert]

- Correct link colour in the reports. This fixes
  `TNO ticket 104 <https://code.simplon.biz/tracker/tno-euphorie/ticket/104>`_
  [cornae]

- Fix accidental yes/no swap in translations. This fixes
  `TNO ticket 121 <https://code.simplon.biz/tracker/tno-euphorie/ticket/121>`_
  [wichert]

- Add french translations
  [pilz]


2.0rc1, September 23, 2010
--------------------------

- Improve IE8 rendering in the client.
  [cornae]

- Improve rendering on iOs devices (iPhone/iPod).
  [cornae]

- Multiple layout fixes for Internet Explorer browsers.
  [cornae]

- No longer rotate navtree in client for Firefox since Firefox renders the
  badly (more information can be found in `Mozilla bug 492214
  <https://bugzilla.mozilla.org/show_bug.cgi?id=492214>`_).
  [cornae]

- Add XML import and export options to the site menu. This implements
  `ticket 121 <https://code.simplon.biz/tracker/euphorie/ticket/121>`_
  [wichert]

- Include policy and Top5 risks in identification. There is no need to
  evaluate them, but we do want to know if they are present in an
  organisation.
  [wichert]

- Include images in XML export of surveys. This fixes the last part of
  `ticket 126 <https://code.simplon.biz/tracker/euphorie/ticket/126>`_
  [wichert]

- Work around jQuery selector bug on IE which caused a javascript error
  on the company form in the report step of the client.
  [wichert]

- Add DOCTYPE to all CMS templates. This fixes rendering problems on IE8.
  [wichert]

- Modify login form to use a link instead of a button to go back. This fixes
  `TNO ticket 107 <https://code.simplon.biz/tracker/tno-euphorie/ticket/107>`_
  [wichert]

- Replace lorem ipsum text on profile page in the client with proper
  instructions.
  [pilz]

- Always process all risks in identification, including top5 and policy risks.
  [wichert]

- Force the correct i18n domain in webhelper macros. This fixes
  `TNO ticket 99 <https://code.simplon.biz/tracker/tno-euphorie/ticket/99>`_
  [wichert]

- Make updated legend item in versions tile translatable. This fixes
  `TNO ticket 113 <https://code.simplon.biz/tracker/tno-euphorie/ticket/113>`_
  [wichert]

- Allow an extra depth level in surveys. This is needed for complicated
  surveys. It should not be used by normal survyes.
  [wichert]

- Fix URLs for fancybox CSS in Internet Explorer.
  [wichert]

- Update XML import to set image filenames as unicode strings, otherwise
  z3c.form would not allow you to change an object containing an image due
  to a type mismatch.
  [wichert]

- Add dependency on `Products.PasswordResetTool
  <http://pypi.python.org/pypi/Products.PasswordResetTool>`_ 2.0.3 or later and
  fix password reset API. This fixes
  `TNO ticket 111 <https://code.simplon.biz/tracker/tno-euphorie/ticket/111>`_.
  [wichert]

- Update styling in the online client to work with current versions of iOS.
  [cornae]

- Use the zopectl command registration feature from Zope 2.12.12 for the
  database initialisation and XML import commandline commands.
  [wichert]


2.0b3, September 10, 2010
-------------------------

- Improve sector styling preview: correctly display the sector logo and
  show right default colours on initial page view.
  [wichert]

- Dutch translations updates. Fixes part of `TNO ticket 71
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/71>`_.
  [wichert]

- Update client to fake a risk-present answer for top-5 risks. This prevents
  them from being listed as unanswered in reports. Part of `TNO ticket 93
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/93>`_.
  [wichert]

- Fix preview feature to create a preview instead of doing a partial publish.
  This fixes `TNO ticket 95
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/95>`_.
  [wichert]

- Adjust importrie utility script to use login name instead of sector title as
  password when no password is explcitly provided.
  [wichert]

- Add a new about page to the client. This fixes
  `ticket 153 <https://code.simplon.biz/tracker/euphorie/ticket/153>`_.
  [cornae, thomas, wichert].

- Correct test for duplicate logins when creating new sectors or country
  managers. This fixes
  `ticket 152 <https://code.simplon.biz/tracker/euphorie/ticket/152>`_.
  [wichert]

- Improve display of multiple images for a risk in the CMS.
  [cornae]


2.0b2, September 3, 2010
------------------------

- Correctly set risk type when generating a session in the client. This fixes
  `TNO ticket 02 <https://code.simplon.biz/tracker/tno-euphorie/ticket/92>`_
  and ticket `ticket 105 <https://code.simplon.biz/tracker/euphorie/ticket/105>`_.
  [wichert]

- Add an intermediate page with explanation and confirmation to the survey
  preview, similar to publication. This fixes
  `TNO ticket 52 <https://code.simplon.biz/tracker/tno-euphorie/ticket/52>`_.
  [wichert]

- Correct profile updates handling when not making any profile changes. This
  fixes problems with profile update appearing to do nothing.
  Fixes `ticket 151 <https://code.simplon.biz/tracker/euphorie/ticket/151>`_,
  `TNO ticket 36 <https://code.simplon.biz/tracker/tno-euphorie/ticket/36>`_ and
  `TNO ticket 85 <https://code.simplon.biz/tracker/tno-euphorie/ticket/85>`_.
  [wichert]

- Change *Module* to *Submodule* in the addbar when already in a module.
  Fixes `ticket 136 <https://code.simplon.biz/tracker/euphorie/ticket/136>`_.
  [wichert]


2.0b1, August 30, 2010
----------------------

This release contains a completely overhauled editing backend and several fixes.

- Implement and use a new user interface for Plone (NuPlone[r]).
  [wichert, cornae]

- Add a new system to manage survey versions and publication.
  [wichert, cornae]

- Improve handling of top-5 risks in the online client.
  [wichert]

- Add support for multiple images for risks.
  [cornae, wichert]

- Documentation update
  [pilz, nielsen]

1.0
---

Unreleased.

- Do not fire before/after copy events when publishing a survey. This speeds
  up publishing enormously.
  [wichert]

- Make sure the survey importer returns unicode everywhere.
  [wichert]

- Add SQL database setup to the installation instructions.
  [wichert]


1.0b2
-----

Released on February 24th, 2010

- Add the *guide to creating a Risk Assessment (RA) tool*,
  the online help text and the *What and Why of a Risk Assessment*
  documents.
  [wichert]

- Hide euphorie.content and euphorie.client from the list of Add-On products.
  They should never be installed by hand by normal users.
  [wichert]

- Add a table of contents to the reports. Implemented as part of the Dutch
  Euphorie extensions for TNO.
  [wichert]

- Fix site error for report pages in the client when using Plone 4. This fixes
  `ticket 95 <https://code.simplon.biz/tracker/euphorie/ticket/95>`_.
  [wichert]

- Clarify package metadata and license. Euphorie is licensed under version 2 of
  the GNU General Public License.
  [wichert]


1.0b1
-----

Released on February 23rd, 2010

- Initial release.
  [wichert]

