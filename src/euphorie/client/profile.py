from Acquisition import aq_inner
from five import grok
from z3c.saconfig import Session
from sqlalchemy.orm import object_session
from euphorie.content.interfaces import IQuestionContainer
from euphorie.content.module import IModule
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.risk import IRisk, IFrenchRisk
from euphorie.content.survey import ISurvey
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client import model
from euphorie.client.update import treeChanges
from euphorie.client.session import create_survey_session
from euphorie.client.session import SessionManager
from euphorie.client.utils import HasText
from euphorie.client.utils import RelativePath


grok.templatedir("templates")


def AddToTree(root, node, zodb_path=[], title=None, profile_index=0):
    """Add a new node to the session tree.

    :param root: parent node of the new child
    :type root: py:class:`euphorie.client.model.SurveySession` or
          :py:class:`euphorie.client.model.SurveyTreeItem`
    :param node: ZODB object to add to the node.
    :type node: one of the :py:mod:`euphorie.content` content types
    :param zodb_path: list of ids of all parents of the root in the session
           tree
    :param title: title for the generated node. Defaults to the title of the
           ZODB object
    :type title: unicode or None
    :param profile_index: profile answer index (for repetable profile
           questions)
    :param profile_index: int
    """
    title = title or node.title

    if title:
        title = title[:500]

    if IQuestionContainer.providedBy(node):
        child = model.Module(title=title, module_id=node.id)
        child.has_description = HasText(node.description)
        if IModule.providedBy(node):
            child.solution_direction = HasText(node.solution_direction)
            if node.optional:
                child.skip_children = False
                child.has_description = True
            else:
                child.postponed = False
    elif IRisk.providedBy(node):
        priority = getattr(node, "default_priority", None)
        if priority == "none":
            priority = None

        if IFrenchRisk.providedBy(node):
            effect = node.default_severity
        else:
            effect = node.default_effect

        child = model.Risk(title=title,
                         risk_id=node.id,
                         risk_type=node.type,
                         probability=node.default_probability,
                         frequency=node.default_frequency,
                         effect=effect,
                         priority=priority)
        child.skip_children = False
        child.postponed = False
        child.has_description = HasText(node.description)
        if node.type in ['top5', 'policy']:
            child.priority = 'high'
    else:
        return

    zodb_path = zodb_path + [node.id]
    child.zodb_path = "/".join(zodb_path)
    child.profile_index = profile_index
    root.addChild(child)

    if IQuestionContainer.providedBy(node):
        for grandchild in node.values():
            AddToTree(child, grandchild, zodb_path, None, profile_index)


def BuildSurveyTree(survey, profile={}, dbsession=None):
    """(Re)build the survey SQL tree. The existing tree for the
    session is deleted before a new tree is created.

    :param survey: survey to build tree for
    :type survey: :py:class:`euphorie.content.survey.Survey`
    :param profile: desired profile to be used for the tree
    :type profile: dictionary
    :param dbsession: session to build tree in. Defaults to currently active
          session.
    :type dbsession: :py:class:`euphorie.client.model.SurveySession`
    """
    if dbsession is None:
        dbsession = SessionManager.session
    dbsession.reset()

    for child in survey.values():
        if IProfileQuestion.providedBy(child):
            p = profile.get(child.id)
            if not p:
                continue

            if isinstance(p, bool):
                AddToTree(dbsession, child)
            elif isinstance(p, list):
                for i in range(len(p)):
                    AddToTree(dbsession, child, title=p[i], profile_index=i)
        else:
            AddToTree(dbsession, child)


def extractProfile(survey, survey_session):
    """Determine the current profile for given current survey session.

    :param survey: current survey
    :type survey: :py:class:`euphorie.content.survey.Survey`
    :param survey_session: current survey session
    :type survey_session: :py:class:`euphorie.client.model.SurveySession`
    :rtype: dictionary with profile answers

    The profile is returned as a dictionary. The id of the profile questions
    are used as keys. For optional profile questions the value is a boolean.
    For repetable profile questions the value is a list of titles as provided
    by the user. This format is compatible with
    :py:meth:`Profile.getDesiredProfile`.

    """
    questions = [{'id': child.id, 'type': child.type}
                 for child in survey.ProfileQuestions()]
    if not questions:
        return {}

    session_modules = {}
    query = Session.query(model.SurveyTreeItem.zodb_path,
                            model.SurveyTreeItem.title)\
            .filter(model.SurveyTreeItem.type == 'module')\
            .filter(model.SurveyTreeItem.session == survey_session)\
            .filter(model.SurveyTreeItem.depth == 1)\
            .all()
    for row in query:
        session_modules.setdefault(row.zodb_path, []).append(row)

    profile = {}
    for question in questions:
        nodes = session_modules.get(question['id'], [])
        if question['type'] == 'optional':
            profile[question['id']] = bool(nodes)
        else:
            profile[question['id']] = [node.title for node in nodes]

    return profile


def set_session_profile(survey, survey_session, profile):
    """Setup the survey session using a given profile.

    :param survey: the survey to use
    :type survey: :py:class:`euphorie.content.survey.Survey`
    :param survey_session: survey session to update
    :type survey_session: :py:class:`euphorie.client.model.SurveySession`
    :param dict profile: desired profile
    :rtype: :py:class:`euphorie.client.model.SurveySession`
    :return: the update session (this might be a new session)
    
    This will rebuild the survey session tree if the profile has changed.
    """
    if not survey_session.hasTree():
        BuildSurveyTree(survey, profile, survey_session)
        return survey_session

    current_profile = extractProfile(survey, survey_session)
    if current_profile == profile and not treeChanges(survey_session, survey):
        survey_session.touch()
        return survey_session

    new_session = create_survey_session(
            survey_session.title, survey, survey_session.account)
    BuildSurveyTree(survey, profile, new_session)
    new_session.copySessionData(survey_session)
    object_session(survey_session).delete(survey_session)
    return new_session


class Profile(grok.View):
    """Determine the profile for the current survey and build the session tree.

    All profile questions in the survey are shown to the user in one screen.
    The user can then determine the profile for his organisation. If there
    are no profile questions user is directly forwarded to the inventory
    phase.

    This view assumes there already is an active session for the current
    survey.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("profile")

    def getDesiredProfile(self):
        """Get the requested profile from the request.

        The profile is returned as a dictionary. The id of the profile
        questions are used as keys. For optional profile questions the value is
        a boolean.  For repetable profile questions the value is a list of
        titles as provided by the user. This format is compatible with
        :py:func:`extractProfile`.

        :rtype: dictionary with profile answers
        """
        profile = {}
        for (id, answer) in self.request.form.items():
            question = self.context.get(id)
            if not IProfileQuestion.providedBy(question):
                continue

            if isinstance(answer, list):
                profile[id] = filter(None, (a.strip() for a in answer))
            else:
                profile[id] = answer
        return profile

    def setupSession(self):
        """Setup the session for the context survey. This will rebuild the
        session tree if the profile has changed.
        """
        survey = aq_inner(self.context)
        new_profile = self.getDesiredProfile()
        self.session = set_session_profile(survey, self.session, new_profile)
        SessionManager.resume(self.session)


    def ProfileQuestions(self):
        """Return information for all profile questions in this survey.

        The data is returned as a list of dictionaries with the following
        keys:

        - ``id``: object id of the question
        - ``title``: title of the question
        - ``type``: question type, one of `repeat` or `optional`
        """
        return [{'id': child.id,
                 'question': child.question or child.title,
                 'type': child.type}
                for child in self.context.ProfileQuestions()]

    def update(self):
        survey = aq_inner(self.context)
        self.profile_questions = self.ProfileQuestions()
        self.session = SessionManager.session
        self.current_profile = extractProfile(survey, SessionManager.session)
        assert self.session is not None
        assert self.session.zodb_path == \
                RelativePath(self.request.client, aq_inner(self.context))

        if not self.profile_questions or \
                self.request.environ["REQUEST_METHOD"] == "POST":
            self.setupSession()
            self.request.response.redirect(survey.absolute_url() +
                    "/identification")


class Update(Profile):
    """Update a survey session after a survey has been republished. If a
    the survey has a profile the user is asked to confirm the current
    profile before continueing.

    The behaviour is exactly the same as the normal start page for a session
    (see the :py:class:`Profile` view), but uses a different template with more
    detailed instructions for the user.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("updated")
