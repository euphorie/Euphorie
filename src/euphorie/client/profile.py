"""
Profile
-------

Various classes and methods to enable the selection screen for profile
questions.
"""

from .. import MessageFactory as _
from Acquisition import aq_inner
from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.session import create_survey_session
from euphorie.client.session import SessionManager
from euphorie.client.update import treeChanges
from euphorie.client.utils import HasText
from euphorie.client.utils import RelativePath
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.interfaces import IQuestionContainer
from euphorie.content.module import IModule
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.risk import IFrenchRisk
from euphorie.content.risk import IRisk
from euphorie.content.survey import ISurvey
from five import grok
from plone import api
from sqlalchemy import sql
from sqlalchemy.orm import object_session
from z3c.saconfig import Session
from zope.i18n import translate

import re


grok.templatedir("templates")


def AddToTree(
    root,
    node,
    zodb_path=[],
    title=None,
    profile_index=0,
    skip_children=False,
):
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
    :param int profile_index: profile answer index number.
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

        child = model.Risk(
            title=title,
            risk_id=node.id,
            risk_type=node.type,
            skip_evaluation=(node.evaluation_method == 'fixed'),
            probability=node.default_probability,
            frequency=node.default_frequency,
            effect=effect,
            priority=priority,
        )
        child.skip_children = False
        child.postponed = False
        child.has_description = HasText(node.description)
        if node.type in ['top5', 'policy']:
            child.priority = 'high'
        if node.risk_always_present:
            child.identification = u"no"
    else:
        return None  # Should never happen

    zodb_path = zodb_path + [node.id]
    child.zodb_path = "/".join(zodb_path)
    child.profile_index = profile_index
    root.addChild(child)

    if IQuestionContainer.providedBy(node) and not skip_children:
        for grandchild in node.values():
            AddToTree(child, grandchild, zodb_path, None, profile_index)
    return child


def get_custom_risks(session):
    if session is None:
        return []
    query = Session.query(model.Risk).filter(
        sql.and_(
            model.Risk.is_custom_risk == True,  # noqa: E712
            model.Risk.path.startswith(model.Module.path),
            model.Risk.session_id == session.id
        )
    ).order_by(model.Risk.id)
    return query.all()


def BuildSurveyTree(survey, profile={}, dbsession=None, old_session=None):
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
        if ICustomRisksModule.providedBy(child):
            AddToTree(dbsession, child)
            # Now copy over the custom risks
            risks = get_custom_risks(old_session)
            if risks:
                # find the module that holds the custom risks
                modules = Session.query(model.Module).filter(
                    sql.and_(
                        model.Module.session_id == dbsession.id,
                        model.Module.module_id == child.id
                    )
                ).all()
                # there should only ever be 1 result
                if modules:
                    for risk in risks:
                        modules[0].addChild(risk)
        elif IProfileQuestion.providedBy(child):
            # Safeguard against double adding of profile questions
            existing = [
                getattr(item, 'module_id') for item in dbsession.children()
            ]
            if child.id in existing:
                continue
            p = profile.get(child.id)
            if not p:
                continue

            if isinstance(p, list):
                profile_question = AddToTree(
                    dbsession,
                    child,
                    title=child.title,
                    profile_index=-1,
                    skip_children=True
                )
                for (index, title) in enumerate(p):
                    AddToTree(
                        profile_question,
                        child,
                        title=title,
                        profile_index=index
                    )
            # If we get a bool, it will be True, because of `if not p` above
            # Simply add the profile to the tree, don't care about locations
            elif isinstance(p, bool):
                AddToTree(dbsession, child, title=child.title)
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
    questions = [{
        'id': child.id,
        'use_location_question': child.use_location_question
    } for child in survey.ProfileQuestions()]
    if not questions:
        return {}

    q_ids = [q['id'] for q in questions]
    session_modules = {}
    query = (
        Session.query(
            model.SurveyTreeItem.zodb_path,
            model.SurveyTreeItem.title
        ).filter(model.SurveyTreeItem.type == 'module')
        .filter(model.SurveyTreeItem.session == survey_session)
        .filter(model.SurveyTreeItem.profile_index >= 0)
        .filter(model.SurveyTreeItem.zodb_path.in_(q_ids))
        .order_by(model.SurveyTreeItem.profile_index)
    )
    for row in query:
        session_modules.setdefault(row.zodb_path, []).append(row)

    profile = {}
    for question in questions:
        nodes = session_modules.get(question['id'], [])
        if not question['use_location_question']:
            profile[question['id']] = bool(nodes)
        else:
            profile[question['id']] = [node.title for node in nodes]

    return profile


def set_session_profile(survey, survey_session, profile):
    """Set up the survey session using a given profile.

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
        # At this stage, we actually do not need to touch the session.
        # It is enough that it gets touched when a Risk is edited, or if the
        # tree gets rebuilt due to changes.
        # survey_session.touch()
        return survey_session

    params = {
        column.key: getattr(survey_session, column.key)
        for column in survey_session.__table__.columns
        if column.key not in (
            'id',
            'brand',
            'account_id',
            'title',
            'created',
            'modified',
            'zodb_path',
        )
    }
    new_session = create_survey_session(
        survey_session.title, survey, survey_session.account, **params
    )
    BuildSurveyTree(survey, profile, new_session, survey_session)
    new_session.copySessionData(survey_session)
    object_session(survey_session).delete(survey_session)
    return new_session


def _questions(context):
    return [{
        'id': child.id,
        'title': child.title,
        'question': child.question or child.title,
        'use_location_question': getattr(child, 'use_location_question', True),
        'label_multiple_present': getattr(
            child, 'label_multiple_present',
            _(u'Does this happen in multiple places?')
        ),
        'label_single_occurance': getattr(
            child, 'label_single_occurance',
            _(u'Enter the name of the location')
        ),
        'label_multiple_occurances': getattr(
            child, 'label_multiple_occurances',
            _(u'Enter the names of each location')
        ),
    } for child in context.ProfileQuestions()]


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

    id_patt = re.compile("pq([0-9]*)\.present")

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
            match = self.id_patt.match(id)
            if match:
                id = match.group(1)
            question = self.context.get(id)
            if not IProfileQuestion.providedBy(question):
                continue
            if getattr(question, 'use_location_question', True):
                # Ignore questions found via the id pattern if they profile
                # is repeatable
                if match:
                    continue
                if not self.request.form.get("pq{0}.present".format(id), ''
                                             ) == 'yes':
                    continue
                if isinstance(answer, list):
                    profile[id] = filter(None, (a.strip() for a in answer))
                    if not self.request.form.get(
                        "pq{0}.multiple".format(id), ''
                    ) == 'yes':
                        profile[id] = profile[id][:1]
                else:
                    profile[id] = answer
            else:
                profile[id] = answer in (True, 'yes')
        return profile

    def setupSession(self):
        """Setup the session for the context survey. This will rebuild the
        session tree if the profile has changed.
        """
        survey = aq_inner(self.context)
        new_profile = self.getDesiredProfile()
        new_session = set_session_profile(survey, self.session, new_profile)
        self.request.other["euphorie.session"] = new_session
        SessionManager.resume(self.session)

    def ProfileQuestions(self):
        """Return information for all profile questions in this survey.

        The data is returned as a list of dictionaries with the following
        keys:

        - ``id``: object id of the question
        - ``title``: title of the question
        - ``question``: question about the general occurance
        - ``label_multiple_present``: question about single or multiple
          occurance
        - ``label_single_occurance``: label for single occurance
        - ``label_multiple_occurances``: label for multiple occurance
        """
        return _questions(self.context)

    @property
    def session(self):
        return api.content.get_view(
            'webhelpers',
            self.context,
            self.request,
        ).session

    def update(self):
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.message_required = translate(
            _(
                u"message_field_required",
                default=u"Please fill out this field."
            ),
            target_language=lang
        )
        survey = aq_inner(self.context)
        self.profile_questions = self.ProfileQuestions()
        self.current_profile = extractProfile(survey, SessionManager.session)
        assert self.session is not None
        assert self.session.zodb_path == RelativePath(
            self.request.client,
            aq_inner(self.context),
        )

        if (
            not self.profile_questions or
            self.request.environ["REQUEST_METHOD"] == "POST"
        ):
            self.setupSession()
            if isinstance(self, Update):
                target = "/start"
            else:
                target = "/identification"
            self.request.response.redirect(
                survey.absolute_url() + target
            )


class Update(Profile):
    """Update a survey session after a survey has been republished. If a
    the survey has a profile the user is asked to confirm the current
    profile before continuing.

    The behaviour is exactly the same as the normal start page for a session
    (see the :py:class:`Profile` view), but uses a different template with more
    detailed instructions for the user.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("updated")
