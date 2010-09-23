from zope.interface import Interface

class IQuestionContainer(Interface):
    """Marker interface for objects that can contain questions,
    but will never show a question to the user themselve during
    any of the inventorisation, evaluation and action plan phases..
    """

