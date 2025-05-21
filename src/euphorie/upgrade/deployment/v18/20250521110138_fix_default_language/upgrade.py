from ftw.upgrade import UpgradeStep
from plone import api


class FixDefaultLanguage(UpgradeStep):
    """Fix default language."""

    def __call__(self):
        default_language = api.portal.get_registry_record("plone.default_language")
        available_languages = api.portal.get_registry_record(
            "plone.available_languages"
        )
        if default_language in available_languages:
            # No need to change the default language
            return

        # Try to pick a sane default language
        if "en" in available_languages:
            # Set the default language to English if it's available
            api.portal.set_registry_record("plone.default_language", "en")
        elif available_languages and len(available_languages) == 1:
            # If we have just one language available, set it as the default
            api.portal.set_registry_record(
                "plone.default_language", available_languages[0]
            )
        else:
            # If we have zero or more than one language available,
            # we require manual intervention
            raise ValueError(
                f"Cannot safely replace the default language {default_language}. "
                f"Please set up manually the registry records "
                f"`plone.default_language` and `plone.available_languages`."
            )
