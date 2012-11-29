import martian
from five import grok
from euphorie.json import JsonView as BaseJsonView
from .interfaces import ICMSAPISkinLayer


class JsonView(BaseJsonView):
    martian.baseclass()
    grok.layer(ICMSAPISkinLayer)
