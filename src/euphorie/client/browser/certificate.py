from euphorie.client.model import SurveySession
from euphorie.client.model import Training
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from z3c.saconfig import Session


class Certificate(BrowserView):
    @property
    @memoize
    def trainings(self):
        """Get all trainings for this session."""
        session_id = self.context.session.id
        return (
            Session.query(Training)
            .filter(Training.session_id == session_id, Training.status == "correct")
            .order_by(Training.time.desc())
            .all()
        )

    def get_certificate_info(self, training):
        traversed_session = training.session.traversed_session
        certificate_view = api.content.get_view(
            name="training-certificate-inner",
            context=traversed_session,
            request=self.request,
        )
        content = certificate_view.index(training_id=training.id)
        link = (
            f"{training.session.absolute_url()}/@@training-certificate-view"
            f"?training_id={training.id}"
        )
        return {"link": link, "content": content, "date": training.time}

    @property
    @memoize
    def certificates(self):
        certificates = []
        for training in self.trainings:
            certificates.append(self.get_certificate_info(training))
        return certificates


class CertificateOverview(Certificate):
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
        account_ids = {
            organisation.owner_id for organisation in organisation_view.organisations
        }
        account_ids.add(api.user.get_current().getId())
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

    @property
    @memoize
    def certificates(self):
        """Get all certificates that I am allowed to view, grouped by year."""
        certificates = {}
        for training in self.trainings:
            year = training.time.year
            certificates.setdefault(year, []).append(
                self.get_certificate_info(training)
            )
        for year, year_certificates in certificates.items():
            certificates[year] = sorted(
                year_certificates, key=lambda c: c["date"], reverse=True
            )
        return certificates.items()

    def get_num_columns(self, num_items):
        return 2 if num_items < 3 else 3
