from ftw.upgrade import UpgradeStep
from plone import api


class FixDefaultLanguage(UpgradeStep):
    """Fix default language."""

    def __call__(self):
        default_language = api.portal.get_registry_record("plone.default_language")
        available_languages = api.portal.get_registry_record(
            "plone.available_languages"
        )
        if default_language not in available_languages:

            if "en" in available_languages:
                # Set the default language to English if it's available
                api.portal.set_registry_record("plone.default_language", "en")
            elif available_languages and len(available_languages) == 1:
                # Set the default language to the first available language
                api.portal.set_registry_record(
                    "plone.default_language", available_languages[0]
                )
            else:
                raise ValueError(
                    f"Cannot safely replace the default language {default_language}. "
                    f"Please set up manually the registry records "
                    f"`plone.default_language` and `plone.available_languages`."
                )
