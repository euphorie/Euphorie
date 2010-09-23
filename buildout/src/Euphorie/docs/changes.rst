Changelog
=========

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
  ticket euphorie #95 as well.
  [wichert]

- Clarify package metadata and license. Euphorie is licensed under version 2 of
  the GNU General Public License.
  [wichert]


1.0b1 
-----

Released on February 23rd, 2010

- Initial release.
  [wichert]

