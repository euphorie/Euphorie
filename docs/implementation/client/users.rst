User management
===============

Users must register before they can start a survey. Registration is used
to provide a persistent state for a user, allowing them to stop working
on a survey and continue it at a later point in time, or to manage
multiple surveys at the same time.

.. attention:: The old RIE system did not use registration, but required users
   to manually download and upload a file with status information. This has
   proven to be confusing for users.

Registration is very simple: users only need to provide a preferred account
name name and a password. No identifying information is required. Users can
opt to provide an email address, which will only be used for password
reminders.

Euphorie accounts are stored in the session SQL database. They are also
exposed as very minimal Plone accounts: they do not get the standard
*Member* role but a new *EuphorieUser* role.

The standard `mutable_properties` PAS plugin should be disabled in an
Euphorie site since it can be a big performance bottleneck. Euphorie has
two types of users, neither of which need the mutable properties
plugin: Euphorie sector accounts provide their own properties directly
and Euphorie users will never have any properties beyond their login name
and password. Since we know that for Euphorie users the login name
is their email address we do not need to have a separate email property.


