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
    def certificates(self):
        certificates = []
        for training in self.trainings:
            link = (
                f"{training.session.absolute_url()}/@@training-certificate-view"
                f"?training_id={training.id}"
            )
            content = self.get_certificate(training)
            certificates.append({"link": link, "content": content})
        return certificates
