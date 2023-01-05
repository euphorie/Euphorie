from euphorie.client.model import Risk
from euphorie.client.model import Session
from ftw.upgrade import UpgradeStep
from logging import getLogger

import sqlalchemy as sa


logger = getLogger()


class DecommissionTheTrainingNotesField(UpgradeStep):
    """Decommission the training_notes field.

    For the moment we are not going to remove the field from the
    database, but we copy the values to the comment column if it has no
    entry.
    """

    def __call__(self):
        session = Session()
        query = session.query(Risk).filter(
            sa.and_(Risk.training_notes != "", sa.func.coalesce(Risk.comment, "") == "")
        )
        for risk in query:
            logger.info("Copying training_notes to comment for risk %r", risk.id)
            risk.comment = risk.training_notes
