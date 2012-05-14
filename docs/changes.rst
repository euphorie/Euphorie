Changelog
=========

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
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/194>`_.
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
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/205>`_.
  [wichert]

- Add a new column with the risk number to the Action plan xlsx rendering. This
  fixes `TNO ticket 203
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/203>`_.
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
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/208>`_.
  [wichert]

- Fix colour of bold text in reports. This fixes 
  `TNO ticket 208
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/208>`_.
  [wichert]

- The identification report wrongly showed the problem description for
  unanswered risks. This fixes
  `TNO ticket 207
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/207>`_.
  [wichert]

- Fix broken translations on risk action plan template. This fixes
  `TNO ticket 201
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/201>`_.
  [wichert]

- Use problem description instead of risk title in action timeline. This fixes
  `TNO ticket 202
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/202>`_.
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
  (i.e http://localhost:4080/Plone2/client/++resource++screen-ie6.css) instead
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
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/127>`_.
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
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/155>`_.
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
  `TNO ticket 159 <http://code.simplon.biz/tracker/tno-euphorie/ticket/159>`_.
  [wichert].

- Fix small errors in Dutch translation. This fixes
  `TNO ticket 175 <http://code.simplon.biz/tracker/tno-euphorie/ticket/175>`_.
  [wichert].

- Replace escape enters with proper newlines in downloadable report.  This
  fixes
  `TNO ticket 174 <http://code.simplon.biz/tracker/tno-euphorie/ticket/174>`_.
  [wichert].

- Added some ``<br/>`` tags to avoid the navigation vanishing in IE7
  [pilz]

- Update the minified css files from the originals to reflect recent 
  changes cornae did to fix ie compatibility .
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
  current session. This fixes `TNO ticket 155`_.
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

