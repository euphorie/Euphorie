# -*- coding: utf-8 -*-

from .. import MessageFactory as _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def title_extra_vocab(context):
    terms = [SimpleTerm(
        value='', token='', title=_("-- no selection --"))]
    terms.append(SimpleTerm(
        value='sufficient', token='sufficient',
        title=_(u"Are the measures that are selected above sufficient?")
    ))
    terms.sort(cmp=lambda x, y: cmp(x.title, y.title))
    return SimpleVocabulary(terms)
