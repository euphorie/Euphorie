from Products.Five import BrowserView


class RobotsView(BrowserView):
    def __call__(self):
        self.request.response.setHeader("Content-type", "text/plain")
        return self.index()
