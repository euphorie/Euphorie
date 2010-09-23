import re

TAG = re.compile(u"<.*?>")

def StripMarkup(markup):
    """Strip all markup from a HTML fragment."""
    return TAG.sub(u"", markup)


