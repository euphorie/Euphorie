Changelog
=========

2.0rc2, September 29, 2010
--------------------------

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

- added french translations
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

