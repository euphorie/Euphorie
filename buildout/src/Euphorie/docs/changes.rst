Changelog
=========

2.b30, September 10, 2010
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
  `ticket 152 <http://code.simplon.biz/tracker/euphorie/ticket/153>`_.
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

