from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from z3c.saconfig import Session


class BaseView(BrowserView):
    default_target_view = ""

    @property
    @memoize
    def sqlsession(self):
        return Session()

    def redirect(self, target=None, msg="", msg_type="notice"):
        """Redirect the user to a meaningfull place and add a status
        message."""
        if target is None:
            target = self.context.absolute_url()
            if self.default_target_view:
                target = f"{target}/{self.default_target_view}"
        if msg:
            api.portal.show_message(msg, self.request, msg_type)

        self.request.response.redirect(target)

    def handle_POST(self):
        """This is just a hook for subclasses to implement.

        By default do nothing special.
        """
        return super().__call__()

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    def validate(self):
        """This is just a hook for subclasses to implement.

        By default do nothing special.
        """
        pass

    def __call__(self):
        self.validate()
        if self.request.method == "POST":
            return self.handle_POST()
        return super().__call__()
