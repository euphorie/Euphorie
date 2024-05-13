from euphorie.client.model import SurveySession
from euphorie.client.model import Training
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from z3c.saconfig import Session


class View(BrowserView):
    """Certificates Overview Page"""

    @property
    @memoize
    def trainings(self):
        """Get all trainings from all the current user's organisations."""
        organisation_view = api.content.get_view(
            name="organisation",
            context=self.context,
            request=self.request,
        )
        account_ids = [
            organisation.owner_id for organisation in organisation_view.organisations
        ]
        return [
            training
            for training in (
                Session.query(Training)
                .filter(
                    Training.session_id == SurveySession.id,
                    SurveySession.account_id.in_(account_ids),
                )
                .filter(Training.status == "correct")
                .order_by(Training.time.desc())
                .all()
            )
            if training.session.tool
        ]

    def get_certificate(self, training):
        traversed_session = training.session.traversed_session
        certificate_view = api.content.get_view(
            name="training-certificate-inner",
            context=traversed_session,
            request=self.request,
        )
        return certificate_view.index(training_id=training.id)

    @property
    @memoize
    def my_certificates(self):
        """Get all certificates that I am allowed to view, grouped by year."""
        certificates = {}
        for training in self.trainings:
            year = training.time.year
            link = (
                f"{training.session.absolute_url()}/@@training-certificate-view"
                f"?training_id={training.id}"
            )
            content = self.get_certificate(training)
            certificates.setdefault(year, []).append(
                {"link": link, "content": content, "date": training.time}
            )
        for year, year_certificates in certificates.items():
            certificates[year] = sorted(
                year_certificates, key=lambda c: c["date"], reverse=True
            )
        return certificates.items()
