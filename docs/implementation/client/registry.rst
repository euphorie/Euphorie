Registry keys
=============

This is an overview of registry keys which can be set to customize the OiRA installation.


Notifications and reminders
---------------------------

- ``euphorie.notifications__enabled``: Boolean. Default: ``False``. Set to ``True`` to enable the notification system and ``False`` to disable it. This also controls the availability of the notification subscription settings in the preferences panel.
- ``euphorie.notification__email_from_address``: String. Default: Not set. The email address from which notification mails are sent.
- ``euphorie.notification__email_from_name``: String. Default: Not set. The notification mail sender name.
- ``euphorie.notification__ra_not_modified__default``: Boolean. Default: ``False``. Setting for the "Risk assessment not modified" notification. Defines is this notification should be per default subscribed (``True``) or not (``False``).
- ``euphorie.notification__ra_not_modified__reminder_days``: Integer. Default: ``365``. Setting for the "Risk assessment not modified" notification. If subscribed a notification will be sent after this setting's number of days a risk assement was not modified.



Other settings
--------------

- ``euphorie.personal_details__enabled``: Boolean. Default: ``True``. Set to ``True`` to allow users to modify personal details in the settings panel.
