from euphorie.client import model
from ftw.upgrade import UpgradeStep


class SetThePublishedSessionsToLocked(UpgradeStep):
    """Set the published sessions to locked."""

    def __call__(self):
        sasession = model.Session()
        for session in sasession.query(model.SurveySession).filter(
            model.SurveySession.published != None  # noqa: E711
        ):
            session_event = model.SessionEvent(
                time=session.published,
                account_id=session.last_publisher_id,
                session_id=session.id,
                action="lock_set",
            )
            sasession.add(session_event)

            # Clean up the old publication data
            session.published = None
            session.last_publisher_id = None
