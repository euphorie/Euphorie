Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

19.1.4 (2025-11-18)
-------------------

Bug fixes:


- Add upgrade step to fix inconsistencies in UID index.  [maurits] (`Issue #3987 <https://github.com/syslabcom/scrum/issues/3987>`_)
- Add upgrade step to ensure all current content has a UID.  [maurits] (`Issue #3987 <https://github.com/syslabcom/scrum/issues/3987>`_)
- Fixed translations to avoid breaking preview URL. [cirosilvano] (`Issue #4065 <https://github.com/syslabcom/scrum/issues/4065>`_)
- PPT and training generation is more resilient (`Issue #4089 <https://github.com/syslabcom/scrum/issues/4089>`_)


19.1.3 (2025-10-07)
-------------------

Bug fixes:


- Make sure the preferences page never shows any splash page overlays. (`Issue #3399 <https://github.com/syslabcom/scrum/issues/3399>`_)
- Fix the appearance of the checkboxes for the measures in place.
  [ale-rt] (`Issue #3427 <https://github.com/syslabcom/scrum/issues/3427>`_)


19.1.2 (2025-09-30)
-------------------

Bug fixes:


- Replace Twitter icon with X icon (`Issue #3573 <https://github.com/syslabcom/scrum/issues/3573>`_)
- Restore the possibility to display the training slides without the questions.
  This was not possible anymore since 19.0.0.
  [ale-rt] (`Issue #3887 <https://github.com/syslabcom/scrum/issues/3887>`_)
- Updated translations


19.1.1 (2025-09-15)
-------------------

Bug fixes:


- The 19.1.0 release on PyPI is not consistent with the tag on Github.
  This release fixes the mismatch.


19.1.0 (2025-09-15)
-------------------

New features:


- Allow requesting an email reminder with a link to the current session (`Issue #3238 <https://github.com/syslabcom/scrum/issues/3238>`_)
- Allow the backend users to authenticate on the client, provided that they have a valid email


Bug fixes:


- Add a slot for custom_css provided by customization packages. (`Issue #0 <https://github.com/syslabcom/scrum/issues/0>`_)
- Fix the XML export by adding adding the recently added ``report_completion_threshold`` and ``enable_email_reminder`` fields. [reinhardt] (`Issue #3237 <https://github.com/syslabcom/scrum/issues/3237>`_)
- Show Cancel button in survey upload form. (`Issue #3489 <https://github.com/syslabcom/scrum/issues/3489>`_)
- Add 'Cancel' button on XML export page of survey. (`Issue #3604 <https://github.com/syslabcom/scrum/issues/3604>`_)
- PPT and training generation is more resilient

  Fixes an issue for archived sessions when the survey is republished with a removed risk. (`Issue #3800 <https://github.com/syslabcom/scrum/issues/3800>`_)
- Create the `euphorie.use_clone_feature` registry record if it is not there
- Survey upload: check for errors before handling upload.


Internal:


- Complete translations for various languages using AI (`Issue #0 <https://github.com/syslabcom/scrum/issues/0>`_)
- Cleanup code that was checking use_clone_feature.

  This feature is now always on. (`Issue #3751 <https://github.com/syslabcom/scrum/issues/3751>`_)
- Remove the colour module


19.0.0 (2025-07-15)
-------------------

Breaking changes:


- Activate duplication feature if not already active (`Issue #3674 <https://github.com/syslabcom/scrum/issues/3674>`_)


New features:


- Allow hiding the report phase until assessment is completed to a certain percentage (`Issue #3237 <https://github.com/syslabcom/scrum/issues/3237>`_)
- Training is not shown at all in the client if disabled on the tool (`Issue #3645 <https://github.com/syslabcom/scrum/issues/3645>`_)
- Update plone.patternslib to 9.10.3.
  [thet]


Bug fixes:


- Fixed wording (“unpublished” → “unlocked”) (`Issue #3574 <https://github.com/syslabcom/scrum/issues/3574>`_)
- Fix reporting page for guest sessions (`Issue #3709 <https://github.com/syslabcom/scrum/issues/3709>`_)


Tests


- Test Products.membrane 7.0.0


18.2.0 (2025-05-26)
-------------------

New features:


- Matomo custom dimensions endpoint (`Issue #3351 <https://github.com/syslabcom/scrum/issues/3351>`_)


Bug fixes:


- Fix the default language when installing Euphorie


18.1.0 (2025-05-19)
-------------------

Breaking changes:


- Change the logo widget

  Do not use anymore the logo widget because the help text is not updated anymore.
  Update the field help text.


Bug fixes:


- Do not break if we have unexpected fieldsets.
  This might happen, e.g., if you add a behavior to your content type.
  [@ale-rt]
- Hide external editor action.
  And fix its condition to not fail when the ``externalEditorEnabled`` skin script is not available.


18.0.0 (2025-04-30)
-------------------

Breaking changes:


- Only support Plone 6.1 and Python 3.11+ [ale-rt]
- Directly use the WYSIWYG widget from plonetheme.nuplone 4.0.1.
  [thet]


New features:


- If there is no organisation for the user yet, add one to avoid the "Add Organisation" button step.


Bug fixes:


- Add a link to the maintenance view for the admin users. [ale-rt]
- Fix missing i18n:name that was preventing a translation to happen
- Merging of more precise prototype translations into euphorie
- Merging happened using polib, which also formatted the pofiles according to standard.
- Fix wrong translations in dutch where edit was translated with view.
- Fill empty dutch translation file with entries from nl_BE where available
- Fix wrong translation for request validation
- fixing two i18n_translate to i18n:translate
- Make sure that RI&E doesn't appear in BE translations, it is a dutch acronym
- Added more guidelines for other use cases on the consultancy screen. Texts are only displayed to the right role.
- The info that you can request consultancy is only for your own organisation.
- All external users cannot request validation, so they don't need to know about that when on the tool (and they are likely consultants anyway)
- If user is consultant, inform that there is currently no validation requested. Otherwise the consultant keeps searching for work.
- Do not display measures-in-place fieldset if there are no measures.
- Missing div makes back button show on right instead of left
- fix another wrap problem in the french method part
- markup fix: modal medium width
- missing pat-bumper classes on button-bars
- clean duplicated tag
- fix the help injection statement
- added missing label to edit organisation panel
- Fix problem of all tabs being current. There is no such thing as repeat.first, should be repeat.start
- If there are no tools, the available tools portlet should not show. But if the condition is on the main node, the dashboard injection fails and we get an eternal spinner. Therefore the condition goes one item down and we have a stub left to inject.
- make the add panel medium instead of small
- adding link to the help section for organisations
- Remove obsolete Class
- Fix the full sentence and correct a few uppercases in the Translations. (Even if there are no sessions to clone yet, user needs to know that it will be possible)
- make the well stick to its state - open or closed - as user desires
- Better fix for no existing measures (the condition checked only if there are measures, but not the flag whether measures should show in place at all). Avoiding an empty fieldset, thus saving space, which proves important for users to see more below.Add a check to the referrer if the menu is called from the dashboard. In that case, don't show the exit action.
- In the risk views lazy load properties rather than initializing them with a function call.
  Deprecates the method ``set_parameter_values``. [ale-rt]
- Remove a warning on our custom Enum type

  Removes:

  ```
  SAWarning: TypeDecorator Enum(...) will not produce a cache key because the ``cache_ok`` attribute is not set to True
  ```

  Switches the value of the Enum type to a tuple to make it cachable.

  See:

  -  https://docs.sqlalchemy.org/en/14/core/custom_types.html#sqlalchemy.types.TypeDecorator.cache_ok


17.0.3 (2025-04-01)
-------------------

New features:


- Upgrade to Plone 6.1


Bug fixes:


- When on the tools overview, there is no need to have the selection modal to pick a tool, because the users clicks the button from within the tool tile. Therefore we can skip the selection and create the chosen tool immediately. (`Issue #3384 <https://github.com/syslabcom/scrum/issues/3384>`_)


Internal:


- Use the Wysiwyg widget from NuPlone if available. [ale-rt]
- Remove unused import


17.0.2 (2025-03-20)
-------------------

New features:


- Add a tool_type_data property in the risk view class.

  While this is not directly used in Euphorie code, it is convenient for customers code.


Bug fixes:


- Fix the password validation


17.0.1 (2025-03-06)
-------------------

Bug fixes:


- Fixed error in report when custom risks are present (`Issue #3288 <https://github.com/syslabcom/scrum/issues/3288>`_)


17.0.0 (2025-02-25)
-------------------

Breaking changes:


- Support only Plone 6 and Python 3.11 and 3.12
  [ale-rt]


Bug fixes:


- Add missing icons in the backend
- Change the location of the OiRA logo shown in the powerpoint.
  [ale-rt]
- Update the link to the certificates help page
  [ale-rt]


Internal:


- Add towncrier for better changelog management.


New features:


- Use plone.patternslib in the client and remove the Patternslib resources from
  Euphorie.
  (`#2990 <https://github.com/syslabcom/scrum/issues/2990>`_)
  [thet]

- Update Patternslib to 9.10.1-alpha.2.
  Ref: scrum-2726.
  [thet]

- Custom labels in company survey for France
  (`#2375 <https://github.com/syslabcom/scrum/issues/2375>`_)
  [reinhardt]

- Depend on plonestatic.euphorie for the static resources that have been removed from this package.
  [ale-rt]

- Support translations of compact report table headers
  (`#3105 <https://github.com/syslabcom/scrum/issues/3105>`_)
  [reinhardt]

- Compact report: Only refer to Measures in Place if supported
  (`#3090 <https://github.com/syslabcom/scrum/issues/3090>`_)
  [reinhardt]

- Updated resources from proto and applied a number of markup fixes in a review session with Daniel
  [pilz]



16.2.8 (2025-02-19)
-------------------

- Fix for profile questions (changed title)
  (`#3038 <https://github.com/syslabcom/scrum/issues/3038>`_)
  [reinhardt]

- Don't try to send notifications for sessions of depublished tools.
  (`#3024 <https://github.com/syslabcom/scrum/issues/3024>`_)
  [reinhardt]

- Don't allow editing training slides when user doesn't have edit permission on the session
  (`#3188 <https://github.com/syslabcom/scrum/issues/3188>`_)
  [reinhardt]

- Don't try updating after tool change when user doesn't have edit permission on the session
  (`#3187 <https://github.com/syslabcom/scrum/issues/3187>`_)
  [reinhardt]


16.2.7 (2025-01-15)
-------------------

- Removed leading empty lines from compact report
  (`#2815 <https://github.com/syslabcom/scrum/issues/2815>`_)
  [reinhardt]


16.2.6 (2025-01-10)
-------------------

- Add legal and policy references as an option for the compact report
  (`#2815 <https://github.com/syslabcom/scrum/issues/2815>`_)
  [reinhardt]
- German translations related to locking
  (`#3015 <https://github.com/syslabcom/scrum/issues/3015>`_)
  [reinhardt]
- Support openpyxl 3.x
  [reinhardt]


16.2.5 (2024-12-09)
-------------------

- Fix the plone.displayed_types registry record that was previously only updated
  through upgrade steps.
  This fixes the navigation on the CMS side for freshly installed sites and
  for sites that have been deployed with recent versions of the package.
  [ale-rt]

- Report: Fix lists of risks (“parked” / not present)
  (`#2800 <https://github.com/syslabcom/scrum/issues/2800>`_)
  [reinhardt]


16.2.4 (2024-11-21)
-------------------

- Translation fix (nl-BE)
  Ref: scrum-2769
  [reinhardt]
- Action Plan: Strip HTML from comments
  (`#2763 <https://github.com/syslabcom/scrum/issues/2763>`_)
  [reinhardt]


16.2.3 (2024-10-25)
-------------------

- Support inspecting sessions: show edit forms in read-only mode when you have no edit permission.
  To use this, override the ``webhelpers`` view and change the new ``allow_inspecting_archived_sessions``
  or ``allow_inspecting_locked_sessions`` variables to True, or implement your own logic in the
  ``can_inspect_session`` method.
  [maurits]


16.2.2 (2024-10-01)
-------------------

- The conditional fields have now widgets that can be customized as needed
  [ale-rt]

- removed the target=_blank from the form that opens the email client. That broke the feature for firefox.
  Fixes #2559
  [pilz]

- Fixed typo in feedback message
  Ref: scrum-2669
  [reinhardt]

- Similar titles: Store results until explicit refresh
  Ref: scrum-2517
  [reinhardt]

- Psychosocial: Fix issue when rebuilding session after change in tool
  Ref: scrum-2695
  [reinhardt]


16.2.1 (2024-07-31)
-------------------

- Fix the i18n labels
  [ale-rt]

- Fix the last modifier id for guest users that have been converted to registered users
  [ale-rt]

- Adjusted column layout for certificates overview
  [reinhardt]


16.2.0 (2024-06-12)
-------------------

- Add ``euphorie.htmllaundry`` module.
  The original ``htmllaundry`` package fails with ``lxml`` 5.2.
  [ale-rt, maurits]

- Use a rich term for vocabulary items in the survey group forms
  [ale-rt]

- Improve the widget for the sector logo
  [ale-rt]

- CSV download of similar title details.
  Ref: scrum-2198

- When creating an OiRa tool from a template, reset the UIDs to avoid complaints from the catalog
  [ale-rt]

- Add registry setting `euphorie.notifications__allow_user_settings` to allow users to change their notification settings.
  The default is set to `True` to allow users to do changes on their own.
  This can be prevented if internal policies require so by changing this setting to `False`.
  Ref: scrum-2193
  [thet]

- Support scaled answers.
  These are answers on a scale from usually 1-5, instead of only yes/no.
  [ale-rt, maurits]

- Do not do linkintegrity checks when removing contents
  (Fix regression introduced in https://github.com/euphorie/Euphorie/pull/692)
  [ale-rt]

- Remove an obsolete traverser that was shadowing the plone.restapi traverser
  [ale-rt]

- Remove the template "sector_edit.pt" which is not used anymore
  [ale-rt]

- Delete guest account after sessions have been transferred
  Ref: scrum-2155

- Add certificates overview
  Ref: scrum-2142

- Show certificates on assessment status page
  Ref: scrum-2143

- Show organisation logo on training certificate
  Ref: scrum-2142

- Run the tests with Plone 6.0.11.1
  [ale-rt]


16.1.2 (2024-03-20)
-------------------

- Allow country managers to use duplication finder tools.
  Ref: scrum-2082


16.1.1 (2024-03-07)
-------------------

- Fix change detection when tool has been updated
  Ref: scrum-2030


16.1.0 (2024-03-05)
-------------------

- Short report can be activated per country
  Ref: scrum-1297
  [reinhardt]

- Fixed locking information in status view
  Ref: scrum-2001
  [reinhardt]

- Updated help
  Ref: scrum-1785
  [reinhardt]

- Use Plone 6.0.10.1


16.0.1 (2024-02-20)
-------------------

- Updated translations


16.0.0 (2024-02-15)
-------------------

- Custom widgets for choice fields in the session @@start view
  [ale-rt, maurits]

- Fix problem with the identification report not being generated for certain survey sessions.
  Ref: scrum-1846
  Fixes: #688
  [thet]

- Do not log anymore not found exceptions
  [ale-rt]

- Allow the client skin layer to be customized by other packages.
  [ale-rt]

- Allow the company model to be customized by other packages.
  [ale-rt]

- Update nl translations.
  [ale-rt, angeldasangel]

- Short report: Mark postponed risks
  Ref: scrum-1852
  [reinhardt]

- Changed PDF generation engine to weasyprint
  Ref: scrum-732
  [reinhardt]

- Add an alias in another risk query.
  See also https://github.com/euphorie/Euphorie/issues/609
  Ref: scrum-1888
  [reinhardt]


15.2.0 (2024-01-08)
-------------------

- Fix obsolete import
  [ale-rt]

- Support Plone 6.0
  [ale-rt]

- Update from prototype commit d8248ecdc6b17eb584610ff5690679ed6a17ea13.
  Refs: scrum-1817
  [thet]

- Update Patternslib to 9.9.10.
  [thet]


15.1.1 (2023-12-13)
-------------------

- Update help from prototype commit 2a995e4c01f7e6f49ef159e601b8e3131d816a19.
  Refs: scrum-1672
  [thet]


15.1.0 (2023-12-12)
-------------------

- Allow to enable/disable personal details settings via registry settings.
- Notifications:
  - Allow to enable/disable notifications via registry settings.
    Note: the notification system is per default disabled.
  - Allow to customize the default's subscription setting for "ra not modified".
  - Allow to customize the notification mail's sender name and address.
  - Add translations.
  - Add basic notification for risk assessments which were not modified since a configurable number of days.
    Note: This notification is disabled by default.
  - Add script to send notifications via cron.
  - Add basic notifications infrastructure.
  - Allow to set notification subscription settings in the preferences panel.
  - Add BaseEmail class to unify sending emails.
  Ref: scrum-1572
  [thet, reinhardt]
- Add behavior to hide modules from trainings.
  Ref: scrum-1573
  [thet]
- Cleanup: Reuse similar code for survey related views.
  [thet]
- Fix incorrect named entity in configure.zcml.
  [thet]
- Use NuPlone 2.2.2.
  [thet]
- Make alembic upgrades fail-safe.
  [thet]
- Fix error when freshly installing a Plone site where `getNonInstallableProfiles` is missing.
  Ref: https://github.com/plone/Products.CMFPlone/issues/3862
  [thet]
- Updated styles.
- Short report tweaks
  Ref: scrum-1295
- Added views to find measure title duplications
  Refs: scrum-1550
- Make the login plone 6 compatible
  [ale-rt]


15.0.8 (2023-10-24)
-------------------

- Fix sidebar error when there is no root group.
  [thet]
- Add a custom CSS slot.
- Add a view to check for risks with similar titles.
  (https://github.com/syslabcom/scrum/issues/1583)
  [ale-rt]


15.0.7 (2023-10-12)
-------------------

- Short report tweaks
  Ref: scrum-1295
- Fix error in Italy report
- Change report download file names
  Refs: scrum-1551


15.0.6 (2023-10-11)
-------------------

- Updated translations
- Short report tweaks
  Ref: scrum-1295
  [reinhardt]


15.0.5 (2023-09-27)
-------------------

- Use NuPlone 2.2.1.
  [cillianderoiste]


15.0.4 (2023-09-25)
-------------------

- Use Plone 5.2.14
  [reinhardt]
- Fixed glitch in sessions list on tool info page
  Ref: scrum-1555
  [reinhardt]


15.0.3 (2023-09-05)
-------------------

- Fix download a tool preview, related to #1245
  Ref: scrum-1508
  [cillianderoiste]


15.0.2 (2023-08-08)
-------------------

- Fix missing factory invocation that prevented to download docx reports.
  [ale-rt]


15.0.1 (2023-07-27)
-------------------

- No longer try to add a Message-Id header in the sent email because it might fail.
  It will be added anyway.
  [ale-rt]

- Use NuPlone 2.2.0
  [ale-rt]

- Use Plone 5.2.13
  [ale-rt]


15.0.0 (2023-07-25)
-------------------

- Show solution descriptions (also known as measure titles) in the Word report,
  except for France and Italy when measures in place are active
  Ref: `scrum-1245 <https://github.com/syslabcom/scrum/issues/1245>`_
  [reinhardt]

- Fix selected measure text spanning whole page instead of bein shown in training module.
  Ref: scrum-1205 item 2)
  [thet]

- Align with prototype to fix form style issues.
  Ref: scrum-1205
  Ref: scrum-1266
  [thet]

- Update Prototype from 55f072619c03f603b1b2227081dacec7efad9684
  [reinhardt]

- Updated Patternslib to 9.9.1, fixing pat-display-time issue
  [reinhardt]

- Allow activating consultancy per country.
  Ref: `scrum-1265 <https://github.com/syslabcom/scrum/issues/1265>`_
  [reinhardt]

- Don't show consultant role if consultancy phase is disabled.
  Ref: `scrum-1225 <https://github.com/syslabcom/scrum/issues/1225>`_
  [reinhardt]

- Fix rendering certificate in portlet when tool has been updated.
  Ref: scrum-1219
  [reinhardt]

- Align with recent changes in prototype.
  Ref: scrum-1205
  [thet]

- When creating a new assessment users can choose to duplicate an existing one
  [reinhardt]

- Makefile resource update: Improve reproducibility.
  Add and commit generated resources from "resources-install" and
  "update-patterns" targets.
  For "make resources-install" add the prototype commit id to a new
  PROTOTYPE_COMMIT_ID file and the commit message.
  For "make update-patterns" add the Patternslib version to the commit message.

- Update Patternslib to 9.9.0-alpha.4.
  Ref: scrum-1135
  [thet]

- Update prototype from commit 377b0ce137546abb7a766154c39aea56fa467cb7
  Ref: scrum-1135
  [thet]

- Adapt training view to prototype and add scroll-marker functionality to TOC.
  Ref: scrum-1135
  [thet]

- The publication feature has been renamed to locking and it is now more powerful.
  Ref.: scrum-1097
  [ale-rt]

- Fix the translation in the title attribute of listed assessments
  [ale-rt]

- When there is no measure to select, do not show the "Training" module
  [ale-rt]

- Ask for confirmation when following an organisation invite link.
  [reinhardt]

- Remove from templates hardcoded date values.
  [ale-rt]

- Use SQLAlchemy 1.4.
  [ale-rt]

- Add some alias in exists query. Remove the need to delete from the scope the aliased instances by using factory methods.
  Fixes #609.
  [ale-rt]

- Use Plone 5.2.12

- Drop support for Python 3.7 that reached its EOL


14.3.4 (2023-04-26)
-------------------

- Do not display the note "The risk evaluation has been automatically done by the tool"
  if there is an integrated action plan.
  [ale-rt]


14.3.3 (2023-04-12)
-------------------

- Fix typo in translation label.
  [ale-rt]

- Make the get_safe_html methods safer.
  [ale-rt]

- Updated translations
  [angeldasangel]

- Add a redirection mechanism to the point the user to an updated link
  when a session tool is updated
  [reinhardt]


14.3.2 (2023-03-27)
-------------------

- Survey navigation: When survey is archived or otherwise disabled the report,
  training and status menu items should still be active.
  [thet]

- Survey navigation: Fix class when navigation menu is active and disabled to
  not render as "activedisabled".
  [thet]

- Upgrade Plone to 5.2.11.
  [thet]

- @@assessments: Change the default sort order to newest first
  Ref: scrum-1040
  [cillianderoiste]

- Render siblings of the selected profile question module in the sidebar
  Ref: scrum-1041
  [cillianderoiste]

- Fix the assessments view to properly handle the account organisations
  and restrict it to authenticated users.
  Refs: `#1043 <https://github.com/syslabcom/scrum/issues/1043>`_.
  [ale-rt]


14.3.1 (2023-03-13)
-------------------

- Upgrade to Patternslib 9.8.3-alpha.0, fixing auto-submit issues with pat-clone.
  [thet]

- Foresee the possibility to have banners in the tool homepage
  Refs: `#1025 <https://github.com/syslabcom/scrum/issues/1025>`_.
  [ale-rt]

- Add a save button in the identification form
  Refs: `#996 <https://github.com/syslabcom/scrum/issues/996>`_.
  [ale-rt]

- Remove some obsolete JavaScript.
  Remove the polyfills-loader (IE11 compatibility) and the patternslib public
  path (base directory for JavaScript assets) variable. Both are not used
  anymore.
  [thet]

- HtmlToWord: Fix problem with different documents for each report compilation.
  This fixes a problem where a bullet number counter was not reset among
  multiple docx compilations, resulting in different documents for the same
  report when downloaded multiple times.
  [thet]

- Update CSS and scripts to latest from prototype.
  [thet]

- Survey tree navigation: Fix status entry switch statement, simplify templates.
  Ref: scrum-953
  [thet]

- Cleanup: Move is_new_session to webhelpers view.
  [thet]

- Only display the survey tree toggler within survey sessions.
  Ref: scrum-953
  [thet]

- Add `is_survey` to the webhelper to determine if the webhelper's context is within a survey or not.
  [thet]

- Align with proto: Survey toolbar needs class auto-hide.
  [thet]

- Cleanup: Remove unused template report_identification.pt.
  [thet]

- Add headings for existing and planned measures, respectively.
  Refs: `#997 <https://github.com/syslabcom/scrum/issues/997>`_.
  [reinhardt]

- Add info paragraph to the country-tools view.
  Ref: scrum-956
  [reinhardt]

- Fix issue where custom risk could not be added.
  Ref: scrum-911
  [reinhardt]

- Fix the layout of the Budget field for measures
  Ref: scrum-901
  [cillianderoiste]

- Fix password reset link when called on session
  Ref: scrum-1026
  [reinhardt]

- Fix “loading” spinner when training dashboard is not displayed.
  Ref: scrum-1027
  [reinhardt]


14.3.0 (2023-01-26)
-------------------

- Add the @@country-tools view to the site menu.
  [thet]
- Fix json export of session to extend the risk and module serialized data with
  the info coming from the tree table
  [ale-rt]
- Add the postgres user to the Authenticated Users,
  allow the user to be checked for the reader role
  [ale-rt]
- Allow a session to be traversed in the context of its own tool only
  [ale-rt]
- Docx report: fix for in-place measures.
  [reinhardt]
- Upgrade plone to 5.2.10
  [ale-rt]
- CSV download for tool overview on country level.
  [reinhardt]
- Organisation: Reflect whether training is enabled when adding a user.
  [reinhardt]
- Decoupled loading of the dashboard portlets.
  Refs: `#712 <https://github.com/syslabcom/scrum/issues/712>`_.
  [reinhardt, thet]


14.2.1 (2022-11-25)
-------------------

- Prepare the dashboard to have banners
  Refs: `#747 <https://github.com/syslabcom/scrum/issues/747>`_.
  [ale]
- Fix a padding issue in the risk evaluation template.
  Refs: `#688 <https://github.com/syslabcom/scrum/issues/688>`_.
  [thet]
- Fix issue where tiptap context menu didn't load.
  Refs: `#477 <https://github.com/euphorie/Euphorie/issues/477>`_.
  [thet]
- Formatting is available for in-place measures.
  [reinhardt]


14.2.0 (2022-11-09)
-------------------

- Disable the cache control settings on the certificate pages.
  Refs. `#475 <https://github.com/euphorie/Euphorie/issues/475>`_.
  [ale-rt]
- Upgrade Patternslib to 9.7.0-alpha.5
  [thet]
- Export/import training questions
  `#435 <https://github.com/euphorie/Euphorie/pull/435>`_.
- Introduce the concept of "organisations"
- Sanitize the permissions handling in the client section
  [ale-rt]
- Added an `@@export.json` view that allows to export a session and the related content in a single json file.
  [ale-rt]
- Upgrade plone to 5.2.10
- Clean up warnings
  [ale-rt]
- Fix the way ``get_survey_templates`` handles a survey with an unset category.
- Remove the ghost module and its tests
  because it is not used since quite some time
  [ale-rt]
- scrum/378 Add a robots.txt view to the client
  [cillianderoiste]
- Upgrade step to handle the decomissioning of the ``training_notes`` field
  `#426 <https://github.com/euphorie/Euphorie/pull/426>`_.
  [ale-rt]
- The training certificate shows the fullname of the user if present
  [ale-rt]
- Measures that are deleted in the CMS stay visible in the client.
  [reinhardt]
- Improved dashboard tab marker.
  [reinhardt]
- Remove the home and help link when the user is not authenticated
  [ale-rt]
- Formatting is available in measures description.
  [reinhardt]
- Transform risk notes (comment field) to safe HTML when saving.
  [reinhardt]
- Added filters to the assessments view.
  [reinhardt]


14.1.6 (2022-09-21)
-------------------

- Tool overview on country level.
  [reinhardt]


14.1.5 (2022-07-13)
-------------------

- Fix label_custom_risks on client status page https://github.com/syslabcom/scrum/issues/370
- Deprecate the @@update-completion-percentage view
  `#419 <https://github.com/euphorie/Euphorie/pull/419>`_.
- “Show more” button on tool view if there are existing sessions.


14.1.4 (2022-07-06)
-------------------

- Updated CSS to latest version of prototype.


14.1.3 (2022-06-29)
-------------------

- Stricter password reset handling.
- Users can enter and edit their first name and last name.
- Fixed statusbar scrolling.
- Updated translations.
- Updated styles.
- Updated help.


14.1.2 (2022-06-15)
-------------------

- Fixed permission check in tabs.
- Updated help/javascript/styles from prototype.
- Updated translations.


14.1.1 (2022-06-07)
-------------------

- Fixed error message in wrong language after login.
- Fixed issue with “Start a new risk assessment” link.


14.1.0 (2022-05-30)
-------------------

- Upgrade plone to 5.2.8
- Reactivate previously deactivated pat-validation for radio inputs. The Bug described in https://github.com/Patternslib/Patterns/issues/744 is fixed.
- New bundle based on Patternslib 7.10.0 with pat-validation fixes.
- New feature: A "Training" page is available per risk assessment that assembles all modules
  and risks into cards / slides for an online training
- For the Training, the user can define which of the planned or in-place measures are part of the
  training
- The Training can be enhanced with a set of questions that are shown to the user at the end.
  If they are answered correctly, the user earns a certificate
- Further tweaks to the involve phase previews.


14.0.4 (2022-05-05)
-------------------

- Reactivate previously deactivated pat-validation for radio inputs. The Bug described in https://github.com/Patternslib/Patterns/issues/744 is fixed.
- New bundle based on Patternslib 7.10.0.
- Restore all pat-validation. The bug with date validation in Chrome is fixed in Patternslib 7.10.0.


14.0.3 (2022-05-04)
-------------------

- Disable pat-validation due to a bug in Chrome with date validation.


14.0.2 (2022-03-30)
-------------------

- Password Reset: Verify IP address validity
- Consolidate the "survey view" in the CMS by merging back developments done in
  subprojects (OSHA-OiRA and Daimler).
  This includes the possibility to export the complete contents of an OiRA tool as Word file
- For the XML export of Surveys, give the user the posibility of de-selecting
  certain parts (images, legal texts, etc)
- Fix image display on risk assessment page, allowing for different aspect ratios
- Fix bug that prevented deleting Omega risks
- Update JavaScript used in CMS bundle (which now comes from NuPlone)
- Code: apply black 22.3.0
- Consolidated involve phase previews.


14.0.1 (2022-03-17)
-------------------

- Do not use the guest_account_id in the login and register forms
  because we have better ways to know it
- Improved redirect security
- Improved error handling
- Fix injection-related problem on tools with integrated action plan that also
  use measures in place


14.0.0 (2022-03-16)
-------------------

- Further improvements in the UI (use of color highlights, etc)
- Rich editing (pat-tiptap) is now used for the Notes and custom risk description
- Officially drop support for python2.7
- When a user tries to operate on a session without enough rights,
  they are redirected to the sessions overview


13.0.9 (2022-02-23)
-------------------

- upgrade plone to 5.2.7
- MOI-510, Adjust translations in on-screen Help


13.0.8 (2022-02-09)
-------------------

- Fix data import (see #348)
  [ale-rt]
- Translation fixes (MOI-534, MOI-535)
- Make XML upload more forgiving towards mistakes (MOI-533)


13.0.7 (2022-01-19)
-------------------

- Fix display of language name on tools page

13.0.6 (2022-01-19)
-------------------

- Profile page: if none of the profile questions uses the location question, do
  not show the intro text that informs about multiple locations
  Refs #MOI-532
- On the OiRA tools page, show the language of each individual tool translated
  to the currently active language
  Refs #MOI-529

13.0.5 (2022-01-11)
-------------------

- Internal: re-organised package


13.0.4 (2022-01-05)
-------------------

- Several translation updates and fixes

13.0.3 (2021-12-22)
-------------------

- Fix all tests.
- Updated translations
- Let country Malta (MT) use English (EN) as default language


13.0.2 (2021-12-15)
-------------------

- Updated translations
- Fix for print contents of tool modal

13.0.1 (2021-12-13)
-------------------

- Fixes regarding translations and language handling

13.0.0 (2021-12-08)
-------------------

BREAKING CHANGE: UI freshup

- Prevent redirect to default country after registration.
- Various Translation fixes
- Show a warning when republishing a tool with changed structure.
- Prevent execution of malicious code entered as custom measure or training notes.
- Only allow users to create an new account in the client if self-registration is enabled

12.0.16 (2021-11-11)
--------------------

- Cleaned out unnecessary files from the package.


12.0.15 (2021-11-03)
--------------------

- Translation fixes for Involve phase (FI and BE)

12.0.14 (2021-10-20)
--------------------

- Record the date of last login (client) in a more canonical way

12.0.13 (2021-10-20)
--------------------

- Fix a language problem in the date picker for multilungual countries (happens
  with cached sites)
- Record the timestamp of when a client user logs in

12.0.12 (2021-10-13)
--------------------

- date-picker: use "medium" output format that gives less problems in translations.
- upgrade plone to 5.2.5
- table "group": replace boolean column 'active' with date column 'deactivated'

12.0.11 (2021-09-29)
--------------------

- Translation fixed for LT

12.0.10 (2021-09-29)
--------------------

- The euphorie user factory plugin is enabled now only in the client
- If the user has entered a general comment, make sure it appears in the report.


12.0.9 (2021-09-08)
-------------------

- re-do FR report for MSA with three (!) logos
- Cosmetic changes

12.0.8 (2021-08-21)
-------------------

- Added py2 compat code in PDF view for RIE

12.0.7 (2021-08-18)
-------------------

- Add custom Word template for another FR sector
- Cosmetic changes

12.0.6 (2021-06-25)
-------------------

- Fixed a bug that caused problems with Greek description texts

12.0.5 (2021-06-23)
-------------------

- Fix a bug with reordering of items in the CMS

12.0.4 (2021-06-10)
-------------------

- When creating a test session, don't fail if the link to a session is
  passed in via the came_from parameter.
  Fixes #MPL-533

12.0.3 (2021-06-10)
-------------------

- Fix a display issue on the Risk view, introduced in the last version

12.0.2 (2021-06-02)
-------------------

- Try to fix display issues in the CMS by using upper case version of Title and Desctipion

12.0.1 (2021-05-29)
-------------------

- Updated date-picker (from Patternslib): we now display date according to localized format

12.0.0 (2021-05-27)
-------------------

MAJOR BREAKING CHANGE

This version requires Plone 5.2 and is intended to run in Python 3.8
All traces of Grok have been removed.
We require a new version of NuPlone that also is grok-free.
z3c.appconfig is no longer used; site specific config is handled via the portal_registry


11.6.12 (unreleased)
-------------------

- The deprecated About page is still used by TNO/RIE. Fix https warning by

11.6.11 (2021-04-21)
--------------------

- Translation updates

11.6.10 (2021-04-13)
--------------------

- Added timestamp to company survey (needed for statistics)

11.6.9 (2021-03-24)
-------------------

- Translation fix

11.6.8 (2021-03-17)
-------------------

- Circumvent a bug in recent Firefox (86+)that broke the view on Action Plan


11.6.7 (2021-03-03)
-------------------

- Help texts: added Catalan (CA), corrected Castillan (ES)


11.6.6 (2021-02-10)
-------------------

- Fix Safari-related bug that prevented adding Omega risks
- Full-table report: include risk priority in "risk" column, not in "measures"
- Translation updates

11.6.5 (2021-02-02)
-------------------

- Don't pre-fill a session's title with the Survey name. Let the user choose their
  own name
- Omega risks: when a risk is added or deleted, make sure that the original order is
  correct, and that gaps in numbering are closed
- Full-table report: include risk priority

11.6.4 (2021-01-19)
-------------------

- New styles from proto

11.6.3 (2020-12-21)
-------------------

- Translation changes
- Contents of tool (docx / print): always show all contents, even deactivated
  modules

11.6.2 (2020-12-15)
-------------------

- Fix some issues in Help the are related to the way OSHA OiRA is hosted


11.6.1 (2020-12-15)
-------------------

- Completely new Help section
- Translation updates


11.6.0 (2020-12-07)
-------------------

- Upgrade from Plone 5.1.5 to Plone 5.1.7
- Groups (in the client user management) can be marked as inactive
- Fix a bug on "Omega" page when we have integrated action plan

11.5.0 (2020-11-18)
-------------------

Technical: Update to Patternslib version supporting ECMAScript 6+


11.4.3 (2020-10-15)
-------------------

- Bugfix for measures in ActionPlan on custom risks
- The answers "No, more measures required" and "Yes, sufficient" (for the measures
  in place RAs) can be different if the Action Plan is integrated

11.4.2 (2020-10-14)
-------------------

- Translation updates

11.4.1 (2020-09-23)
-------------------

- Translation updates

11.4.0 (2020-09-15)
-------------------

- New Hungarian translations (provided by client)
- Further translation updates
- New Help section, currently EN only. Not exposed (linked) yet, but already
  available via @@oira-help
- Make sure that an update to the title of a module or risk gets propagated
  to existing sessions.
- Updated styles and bundle (fixes validation error)

Major changes:
- The Action Plan can be combined with Identifcation into a single Assessment phase.
  A setting per survey in the CMS can be used to enable this.
  Note: the feature-switch `use_integrated_action_plan=True` needs to be present
  in euphorie.ini to make this new option available.
- New main navigation item "Involve" that comes after "Preparation"
  It replaces the former start page of the Identification phase with a more
  explicit call to action.
  Note: the feature-switch `use_involve_phase=True` needs to be present in
  euphorie.ini to make this new feature available.

11.3.13 (2020-07-17)
--------------------

- Updated CS translations

11.3.12 (2020-07-08)
--------------------

- Don't allow uploading new images smaller than 1000x430 pixels. Warn about smaller
  existing images, but allow keeping them.
- Bugfix: make sure that when the user submits the profile, the session always get
  refreshed. This prevents a potential infinite loop of "The tool has been updated"
- Translation updates

11.3.11 (2020-07-01)
--------------------

- Translation updates


11.3.10 (2020-06-26)
--------------------

- Translation updates

11.3.9 (2020-06-24)
-------------------

- Translation updates

11.3.8 (2020-06-24)
-------------------

- Docx report: make it possible to define extra text for the title per sector;
  add a custom template for the French COVID tool
- Translation updates
- Prevent logout of active users

11.3.7 (2020-06-18)
-------------------

- Fix broken bundle

11.3.6 (2020-06-18)
-------------------

- Excel report: make sure risk numbers are always treated as string
- Fix broken bundle

11.3.5 (2020-06-17)
-------------------

- Fix XML export/import: adjust to new action-plan
- Translation updates

11.3.4 (2020-06-10)
-------------------

- Measures in place: if training module is used, measures can be de-selected
  from appearing in the training
- Add a simple shell for content that will be offered for inclusion via iframe
- Translation updates

11.3.3 (2020-05-26)
-------------------

- Add configuration per country which reports are available.
- Define per country which sections are open by default.
- Translation updates


11.3.2 (2020-05-20)
-------------------

- Translation updates

11.3.1 (2020-05-15)
-------------------

- Report: Make it possible to define an alterative .docx template based on
  combination of country and sector. Start with Sea Trade in France
- Translation updates


11.3.0 (2020-05-12)
-------------------

BREAKING CHANGE
Rework of how action plan data is saved; also Measures in Place now
get saved in the same way.
The fields action_plan and prevention_plan are merged into a single field action

11.2.0 (2020-04-22)
-------------------

BREAKING CHANGE
All assets (CSS and JS bundles) are now present under euphorie.client.resources
Brand-support is handled via folders under resources.
This follows the new paradigm of prototype.

- Fixes for the reports (XLSX, PDF) regarding file name
- Change logic of "Overview of Measures" report to use end date instead of start date
- Fix a layout issue in the "Overview of Risks" report

11.1.20 (2020-03-31)
--------------------

- With the new unique session id exposed in the URL, we can actually redirect
  to the exact location inside a session after login, if this is present as
  a came_from parameter. We already have the security checks in place that ensure
  that a session can only be viewed by an authorised user.
- (Re-)enable a custom tool notification, shown on the Preparation page
- The progress indicator also gets updated when the user is progressing from one risk
  to the next.


11.1.19 (2020-03-23)
--------------------

- Fix broken release

11.1.18 (2020-03-23)
--------------------

- Improve starting a new session for the "many tools" case
- Another Italy special: reduce intro text for ActionPlan


11.1.17 (2020-03-03)
--------------------

- Fix a bug that prevented browsing Identification in Safari / iOS

11.1.16 (2020-02-25)
--------------------

- Make it possible to hide progress indicator
- Fix a bug that caused a problem for resetting the password


11.1.15 (2020-02-17)
--------------------

- Show progress indicator in sidebar.


11.1.14 (2020-01-21)
--------------------

- Fix bug that caused users in different timezones to see strange dates
 ("Last saved in 2 hours")
- Update FR translations

11.1.13 (2020-01-07)
--------------------

- Fix image display on Risks (Identification), caused by style update

11.1.12 (2019-12-17)
--------------------

- Save creation date of accounts, so that it is available for statistics
  When a guest converts to normal user, reset the creation date
- Move the tool's logo + info text away from the Preparation page into a popup

11.1.11 (2019-12-04)
--------------------

- Technical: use `get_current_account` instead of SecurityManager for fetching
  account in login and seversal other screens. This should fix a problem
  encountered with converted guest accounts
- When a risk gets pasted from a Copy or Cut action, make sure that it gets the
  correct interfaces according to the Evaluation method of the survey


11.1.10 (2019-11-14)
--------------------

- IT translation update
- Added a view manage-ensure-interface to get rid of editing problems on
  some risks

11.1.9 (2019-11-07)
-------------------

- Translation updates

11.1.8 (2019-10-30)
-------------------

- Translation updates

11.1.7 (2019-10-22)
-------------------

- Fix the process for changing one's email address, so that it works also when
  Memcached is used on acl_users
- IT: also skip evaluation on Omega risks
- Fix problem in docx report with unprintable characters
- Updated translations


11.1.6 (2019-10-09)
-------------------

- Always switch to a tool's language, also when redirecting to login.
- Define default language for most countries
- Better display of images on modules and image-galery on risks
- Translation updates
- Improvements in the report for measures-in-place


11.1.5 (2019-10-02)
-------------------

- Bugfix in Excel report
- Translation updates
- Image upload on omega risks: display a warning if uploaded file is not a valid
  image

11.1.4 (2019-09-25)
-------------------

- Omega risks can have an image
- Adjust OiRA process for Italy

Technical:

- Use alembic for database migrations

11.1.3 (2019-09-09)
-------------------

- Fix handling of login / register inside a guest session

11.1.2 (2019-09-09)
-------------------

- Tighten security on several client views
- Portlets are configurable (#199)
- Simplified code (removd obsolete parts)

11.1.1 (2019-09-03)
-------------------

- Fix brown-bag release that had missing templates


11.1.0 (2019-09-03)
-------------------

- Introducing deep-linking: Every session has its unique URL
- Extended Status page with general information at the top
- Status available via more-menu (3-dots menu)
- Archiving of risk assessment sessions
  (optional, enable via `use_archive_feature=True` in euphorie.ini)


11.0.5 (2019-08-27)
-------------------

- Fix standard report: use custom description on Omega risks
- All optional modules default to "skip". The user needs to actively decide that
  the module is relevant for them.

11.0.4 (2019-08-22)
-------------------

- Made the behavior for "always present" risks more flexible / easier
  to customise in the client
- Increased version number check in upgradedb, so that custom_description
  will get addedd properly

11.0.3 (2019-08-20)
-------------------

- Use autosuggest for many-tools
- New markup structure for the dashboard
- When a module is optional, don't use a floating nav-bar, so that the filter
  questsion cannot be missed.
- Sidebar: sessions are not grouped by tool any more
- Technical: the JavaScript bundle with Patternslib now uses jquery3

11.0.2 (2019-07-16)
-------------------

- Translation updates

11.0.1 (2019-07-11)
-------------------

- Bugfix on Action Plan: don't choke if a solution is None


11.0.0 (2019-06-28)
-------------------

New major release:
- Upgraded UI. The tool navigation is now completely in one column
- Custom risks ("Omega"): reworked and extended to match regular risks


10.1.13 (2019-06-18)
--------------------

- Prevent premature activation of tool navigation when a session has not been
  initialised yet.
- Translation changes
- Fix error that prevented deleting a session

10.1.12 (2019-05-20)
--------------------

- Improve Library fix from last release
- Italy special: never show evaluation statement in Action Plan or report

10.1.11 (2019-05-07)
--------------------

- Handle a bug that sometimes made it impossible to copy contents from the library
- When a new OiRA tool is created by copying, it is now possible to set the
  evaluation algorithm

10.1.10 (2019-04-08)
--------------------

- top5 risks: do not show the option to change the severity in Action Plan, they
  are always "high".
- Translation fixes (PT, IS)


10.1.9 (2019-03-29)
-------------------

- Translation change PT
- Make change of account email address more robust against side-effects

10.1.8 (2019-03-26)
-------------------

- Label changes in French report
- Fix bug on statistics page

10.1.7 (2019-03-20)
-------------------

- Bugfix for the Help tile: showing it must not depend on the CountryManager
  permission
- In the Word report: top5 risks that have not been answered yet should get the
  same text as postponed ones


10.1.6 (2019-03-18)
-------------------

- Translation fixes for IT and FR
- CMS: show date of last publication for every published tool

10.1.5 (2019-03-13)
-------------------

- Technical: Use a limit(1) clause when fetching old values in copySessionData()

10.1.4 (2019-03-13)
-------------------

- Translation fixes EL
- Login (intro) page: hide several sections of text in French, by special request
- French report (for measures in place): Fix typo
- CMS - Sector overview: only show link to "add new tool" if the user has required permissions

10.1.3 (2019-03-04)
-------------------

- Word report: add "Consultation of workers" box at the end, which had been present
  in the RTF report, but so far not in the new Word report.
- Updated IS translations


10.1.2 (2019-02-26)
-------------------

- Better logic for the text hint on top5 risks that were answered as
  yes in the report. Needed for RIE

10.1.1 (2019-02-04)
-------------------

- Re-build JS bundle / chunks to fix a problem with pat-display-time for
  the locale nl-NL
- France: create own Word report, based on the Daimler template, which is
  used by tools of type existing-measures

10.1.0 (2019-01-23)
-------------------

- Bugfix for the `treeChanges` method that determines if the SQL data
  of the tree needs to be updated: we now also check if the risk_type
  was changed, since that info determines display behaviour.
- Translation update FR
- New behavior for Survey that makes it possible to assign one or more categories
  to it. If set, the "new session" modal in the client will display that survey
  under its categories
- The reports that were formerly in RTF format are now created in docx


10.0.4 (2018-12-11)
-------------------

- Translation update IS

10.0.3 (2018-12-05)
-------------------

- Italy special: for existing measures, use both the text of the description
  and the prevention plan
- Workaround for potential error in action plan. Because pat-validation is
  flawed, no validation is applied to the measures. This allows a user to
  write any value into the date fields, resulting in a white screen for them
  because of a SQL error in the background. Therefore, we silently eliminate
  illegal date values now.
- Translation updates Dutch (NL) and Icelandic (IS)

10.0.2 (2018-11-14)
-------------------

- Translation correction NL_BE
- Let the Euphorie PAS plugin only handle requests from with the client

10.0.1 (2018-11-06)
-------------------

- Restore old javascript bundle, because pat-display-time introduces
  syntax that does not work in IE11.

10.0.0 (2018-11-05)
-------------------

Upgrade notes
~~~~~~~~~~~~~

This release is dependent on Plone 5.1 and higher.
Run the console script `upgradedb`, as well as all upgrade steps in Plone


Feature changes
~~~~~~~~~~~~~~~

- UI rework: introduction of initial dashboard, different sessions browser, mobile
  improvements, and other changes.
- Added Tool Type: apart from the "classic" OiRA Tool type with positive
  and negative statements, we can now set a tool to allow the definition
  of measures that are already in place.
- Client user passwords are no longer stored as plain text.
- Added Training module: a slide is created per module and risk, with the possibility
  to add user-defined extra notes.
- A new view ``@@refresh-resources-timestamp`` has been introduced
  to break the browser cache

Bugfixes
~~~~~~~~

- Fixed various inconsistencies



10.0.0b5 (unreleased)
---------------------

- Nothing changed yet.


10.0.0b4 (2018-10-30)
---------------------

- More translations

10.0.0b3 (2018-10-25)
---------------------

- Nothing changed yet.


10.0.0b2 (2018-10-23)
---------------------

- Upgrade to Plone 5.1.4
- Translation updates
- Bugfixes


10.0.0b1 (2018-10-10)
---------------------

- Initial work on Plone5 version

9.0.42 (unreleased)

-------------------

- Translation changes nl_BE

9.0.41 (2018-08-06)
-------------------

- Bugfix for the "measures" report: Do not rely on the pre-computed
  list of modules, since this can fail for a scenario with
  module->module->Optional module


9.0.40 (2018-07-13)
-------------------

- Italy: more translation changes
- Italy special: insert a fixed text snippet at the end of every risk description
  in the identification phase

9.0.39 (2018-07-12)
-------------------

- Italy: change labels for "green" and "dark red" on status page
- Italy special: on status page and risks overview, only show the status bar,
  but no additional box(es) about individual risks
- Italy: change labels for "green" and "dark red" on status page
- Italy special: on status page and risks overview, only show the status bar,
  but no additional box(es) about individual risks

9.0.38 (2018-07-10)
-------------------

- Translation fixes for LT
- Translation fix for the measures report: use translated month abbreviations

9.0.37 (2018-06-14)
-------------------

- Label change: "Obsolete OiRA tool" instead of "Survey"
- Translation fix for IT


9.0.36 (2018-04-26)
-------------------

- Translation updates in Castillian (es), Catalan (ca) and Dutch (nl)
- Fix undefined variable (#120)
- Major rework of how the lines for the Action Plan XLS are
  computed. We are re-using the logic from Status, so that risks in
  optional modules that are deactivated can be filtered out.
  Also, some "hand-written" SQL queries are replaced by
  sqlalchemy ones.
- Optional modules: until the user has explicitely answered the module
  question as "Yes", consider this module skipped.


9.0.35 (2018-03-16)
-------------------

Changed:

- Provide the current language code in a hidden metadata section of the body, so
  that Piwik code can pick it up easily (in addition to the already present
  country, sector and tool name.
- Identification report (RTF): formatting changes


9.0.34 (2018-02-14)
-------------------

Changed:

- In the Identification Report, handle links and lists that are present in the
  markup in a better way.
- In the Status page / Overview of Risks report: Risks answered with "Does not
  apply" are no longer counted as "no risk" or "not answered", but are not shown
  in the report at all.


9.0.33 (2018-01-17)
-------------------

Changed:

- In the Identification Report (list of all risks), show the Legal References,
  if present. (TNO only, since this report is customised for EU-OSHA)

9.0.32.1 (2018-03-06)
---------------------

- Urgent changes to the HR Translations


9.0.32 (2018-01-17)
-------------------

Changed:

- In the CMS, the sector edit form has gotten simpler. Since tool creators
  cannot influence the colour scheme any more, the colour picker and the
  preview have been removed. This allows us to get rid of the accordion
  and should help to fix recurring problems from TNO in resetting the
  password.
- Profile Questions: in 2012, optional profile questions were removed, and
  merged with the concept of repeatable profile questions. As user and tool
  creator feedback has shown, there are valid use-cases where a profile should
  be optional, but asking about one or more locations does not make sense.
  Therefore, the "location" aka repeatable part of a profile question can now
  be switched off in the CMS.


9.0.31 (2017-12-14)
-------------------

Fixed:

- When the logic to correctly skip disabled modules in the status report was
  introduced in 9.0.26, it caused a new bug for tools that contain repeatable
  profile questions. Profile questions are now handled correctly again.


Changed:

- In the CMS, conditional fields (that only appear when a checkbox is ticked)
  can now be set to "required" and properly validated. Therefore the "question"
  field for optional modules and the "tool notification" title and text fields
  are now required.
- Translations for Croatian (HR)


9.0.30 (2017-11-27)
-------------------

Changed:

- Translations for Croatian (HR)

9.0.29 (2017-11-21)
-------------------

Fixed:

- Workaraound for #114
  (by reverting the doctype on risk_actionplan to its old state)
  Needs to be fixed upstream in Patternslib/pat-clone

Changed:

- Translations for German (DE)
- It is no longer possible to pick an additional sentence to be displayed
  under the risk title via the CMS. If existing measures are present, the
  pre-defined sentence is simply shown in the client


9.0.28 (2017-11-13)
-------------------

Changed:

- Translations for Croatian (HR)
- Use HTML5 doctype in all client templates
- Special customisations per country now possible. Only used for Italy:
  - Generally skip evaluation
  - Colour adjustment in the answer-type legend

Added:

- Optional new field per risk: Existing measures; activated in euphorie.ini
  (Currently only used in an add-on)

9.0.27 (2017-10-12)
-------------------

Changed:

- Translations for Croatian (HR)


9.0.26 (2017-10-06)
-------------------

Changed:

- Updated styles, added latest Patterns

Fixed:

- The Status / Overview of Risks report had a bug that caused risks of
  disabled optional modules to be falsely shown in certain cases. The
  logic for computing the risks to consider has been improved to fix
  this bug.

9.0.25 (2017-09-27)
-------------------

Fixed:

- When a tool with a profile question was updated, and that tool has a
  custom splash message, that message now gets shown correctly instead
  of a blurred overlay.

Changed:

- Translation for Croatian (HR)


9.0.24 (2017-09-14)
-------------------

- Excel Report: Also ignore measures of risks that have been answered
  with "yes" (requested by TNO)


9.0.23 (2017-09-04)
-------------------

- Improve Excel report fix from 9.0.22: Don't write empty line when an
  entry is skipped
- Actually consider the allow_guest_accounts setting from the app-
  config. Don't allow guest login if it is not enabled.
- Translation fixes in Croatian


9.0.22 (2017-08-21)
-------------------

- CMS: Index more fields of Modules and Measures
- In the "Excel" report: don't consider risks that were answered as
  not applicable

9.0.21 (2017-07-18)
-------------------

- Added missing file

9.0.20 (2017-07-18)
-------------------

- CMS: Added a tile that provides "search in context"
  It is only shown if euphorie.search is added to the "actions" tiles
  section in euphorie.ini
- Added a new field to the Risk type: existing_measures. Text entered here
  will be used to pre-fill the new field of the same name in the client. It
  currently hidden in the Add and Edit form and needs to be activated with
  use_existing_measures in the app-config
- Added missing default translation for drag-n-drop in the CMS

9.0.19 (2017-07-17)
-------------------

BROWN-BAG RELEASE

9.0.18 (2017-07-04)
-------------------

- Make it possible to start browsing the client on a country in a different
  language than EN.
  Set French as language for France.

9.0.17 (2017-07-03)
-------------------

- Translation changes in IS and PT

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
- When a sector or country manager is created, the new user receives an e-mail
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
