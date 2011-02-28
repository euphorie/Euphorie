Changelog
=========

2.5 - February 28, 2011
-----------------------

- Restore print button on identification report page; it seems users are
  unable to find the print function of their browser. This fixes
  `TNO ticket 159 <http://code.simplon.biz/tracker/tno-euphorie/ticket/159>`_.
  [wichert].


- Fix small errors in Dutch translation. This fixes
  `TNO ticket 175 <http://code.simplon.biz/tracker/tno-euphorie/ticket/175>`_.
  [wichert].

- Replace escape enters with proper newlines in downloadable report.  This
  fixes
  `TNO ticket 174 <http://code.simplon.biz/tracker/tno-euphorie/ticket/174>`_.
  [wichert].

- Added some <br> tags to avoid the navigation vanishing in IE7
  [pilz]

- updated the minified css files from the originals to reflect recent 
  changes cornae did to fix ie compatibility 
  [pilz]

- Add report header styles for an extra depth level. This fixes problems
  when generating reports for deeply nested surveys. This fixes
  `TNO ticket 176 <http://code.simplon.biz/tracker/tno-euphorie/ticket/176>`_.
  [wichert].


2.4 - January 25, 2011
----------------------

Feature changes
~~~~~~~~~~~~~~~

- Enable the terms and conditions features introduced in release 2.3, but
  make it possible to disable it via a settings in the ``.ini`` file. This
  fixes `ticket 107 <http://code.simplon.biz/tracker/euphorie/ticket/107>`_.
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
  current session. This fixes `TNO ticket 155
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/155>`_.
  [wichert]

- Stop declaring ``eupphorie`` to be a namespace package.
  [wichert]

- Require NuPlone 1.0rc1 or later so ``formatDate`` does not raise exceptions
  for pre-1900 dates. This fixes `TNO ticket 150
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/150>`_.
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
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/147>`_.
  [wichert]


Bugfixes
~~~~~~~~

- Purge cached scaled logos when publishing a survey and updating the sector logo.
  This fixes `TNO ticket 136 <http://code.simplon.biz/tracker/tno-euphorie/ticket/136>`_.
  [wichert]

- Translate subject of password reminer email. This fixes
  `TNO ticket 148 <http://code.simplon.biz/tracker/tno-euphorie/ticket/148>`_.
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
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/131>`_.
  [wichert]

- Correct bad image scaling test when displaying a module in the client, which
  prevented images from being visible in action plan and evaluation phases. This
  fixes `TNO ticket 135 <http://code.simplon.biz/tracker/tno-euphorie/ticket/135>`_.
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
  This fixes `ticket 142 <http://code.simplon.biz/tracker/euphorie/ticket/142>`_.
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
  <http://code.simplon.biz/tracker/euphorie/ticket/156>`_.
  [wichert]

- Handle multiple buttons as returned by IE correctly in the company detail
  form. This could lead to site errors before.
  [wichert]

- Fix handling of partial date fields in company details forms.
  [wichert]

- Add publish permission to country managers. This fixes
  `TNO ticket 126 <http://code.simplon.biz/tracker/tno-euphorie/ticket/126>`_
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
  `TNO ticket 124 <http://code.simplon.biz/tracker/tno-euphorie/ticket/124>`_
  [wichert]

- Correct link colour in the reports. This fixes 
  `TNO ticket 104 <http://code.simplon.biz/tracker/tno-euphorie/ticket/104>`_
  [cornae]

- Fix accidental yes/no swap in translations. This fixes
  `TNO ticket 121 <http://code.simplon.biz/tracker/tno-euphorie/ticket/121>`_
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
  `ticket 121 <http://code.simplon.biz/tracker/euphorie/ticket/121>`_
  [wichert]

- Include policy and Top5 risks in identification. There is no need to
  evaluate them, but we do want to know if they are present in an
  organisation.
  [wichert]

- Include images in XML export of surveys. This fixes the last part of
  `ticket 126 <http://code.simplon.biz/tracker/euphorie/ticket/126>`_
  [wichert]

- Work around jQuery selector bug on IE which caused a javascript error
  on the company form in the report step of the client.
  [wichert]

- Add DOCTYPE to all CMS templates. This fixes rendering problems on IE8.
  [wichert]

- Modify login form to use a link instead of a button to go back. This fixes
  `TNO ticket 107 <http://code.simplon.biz/tracker/tno-euphorie/ticket/107>`_
  [wichert]

- Replace lorem ipsum text on profile page in the client with proper
  instructions.
  [pilz]

- Always process all risks in identification, including top5 and policy risks.
  [wichert]

- Force the correct i18n domain in webhelper macros. This fixes
  `TNO ticket 99 <http://code.simplon.biz/tracker/tno-euphorie/ticket/99>`_
  [wichert]

- Make updated legend item in versions tile translatable. This fixes
  `TNO ticket 113 <http://code.simplon.biz/tracker/tno-euphorie/ticket/113>`_
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
  <http://pypi.python.org/pypi/PasswordResetTool>`_ 2.0.3 or later and fix
  password reset API. This fixes
  `TNO ticket 111 <http://code.simplon.biz/tracker/tno-euphorie/ticket/111>`_.
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
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/71>`_.
  [wichert]

- Update client to fake a risk-present answer for top-5 risks. This prevents
  them from being listed as unanswered in reports. Part of `TNO ticket 93
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/93>`_.
  [wichert]

- Fix preview feature to create a preview instead of doing a partial publish.
  This fixes `TNO ticket 95
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/95>`_.
  [wichert]

- Adjust importrie utility script to use login name instead of sector title as
  password when no password is explcitly provided.
  [wichert]

- Add a new about page to the client. This fixes 
  `ticket 153 <http://code.simplon.biz/tracker/euphorie/ticket/153>`_.
  [cornae, thomas, wichert].

- Correct test for duplicate logins when creating new sectors or country
  managers. This fixes
  `ticket 152 <http://code.simplon.biz/tracker/euphorie/ticket/152>`_.
  [wichert]

- Improve display of multiple images for a risk in the CMS.
  [cornae]


2.0b2, September 3, 2010
------------------------

- Correctly set risk type when generating a session in the client. This fixes
  `TNO ticket 02 <http://code.simplon.biz/tracker/tno-euphorie/ticket/92>`_
  and ticket `ticket 105 <http://code.simplon.biz/tracker/euphorie/ticket/105>`_.
  [wichert]

- Add an intermediate page with explanation and confirmation to the survey
  preview, similar to publication. This fixes
  `TNO ticket 52 <http://code.simplon.biz/tracker/tno-euphorie/ticket/52>`_.
  [wichert]

- Correct profile updates handling when not making any profile changes. This
  fixes problems with profile update appearing to do nothing.
  Fixes `ticket 151 <http://code.simplon.biz/tracker/euphorie/ticket/151>`_,
  `TNO ticket 36 <http://code.simplon.biz/tracker/tno-euphorie/ticket/36>`_ and
  `TNO ticket 85 <http://code.simplon.biz/tracker/tno-euphorie/ticket/85>`_.
  [wichert]

- Change *Module* to *Submodule* in the addbar when already in a module.
  Fixes `ticket 136 <http://code.simplon.biz/tracker/euphorie/ticket/136>`_.
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

