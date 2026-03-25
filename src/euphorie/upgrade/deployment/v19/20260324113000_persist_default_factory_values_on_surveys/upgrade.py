from euphorie.content.survey import ISurvey
from ftw.upgrade import UpgradeStep
from logging import getLogger
from plone import api


logger = getLogger(__name__)


class PersistDefaultFactoryValuesOnSurveys(UpgradeStep):
    """Persist defaultFactory-backed values on existing surveys."""

    # Extract the fields that have a defaultFactory
    fields_to_persist = [
        name for name in ISurvey.names() if ISurvey[name].defaultFactory is not None
    ]

    def persist(self, obj):
        """Persist defaultFactory-backed values for the given survey."""
        for field in self.fields_to_persist:
            try:
                # __getattribute__ bypasses the dexterity machinery
                # that would invoke the defaultFactory when an attribute is missing
                obj.__getattribute__(field)
            except AttributeError:
                logger.info(
                    "Persisting defaultFactory value for field %r on survey %r",
                    field,
                    obj,
                )
                # Here getattr will invoke the defaultFactory
                # and set the value on the object
                setattr(obj, field, getattr(obj, field))

    def __call__(self):
        brains = api.content.find(portal_type="euphorie.survey")
        objs = (brain.getObject() for brain in brains)
        for obj in objs:
            self.persist(obj)
