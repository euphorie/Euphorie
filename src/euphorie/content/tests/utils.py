# coding=utf-8
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME


EMPTY_SURVEY = \
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <survey>
              <title>Software development</title>
            </survey>
          </sector>"""


BASIC_SURVEY = \
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>ICT</title>
             <survey>
              <title>Software development</title>
              <module optional="no">
                <title>Module one</title>
                <description>Quick description</description>
                 <risk type="policy">
                   <title>New hires are not aware of design patterns.</title>
                   <description>&lt;p&gt;Every developer should know about them..&lt;/p&gt;</description>
                   <evaluation-method>direct</evaluation-method>
                   <image caption="Key image" content-type="image/gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
                 </risk>
              </module>
            </survey>
          </sector>"""  # noqa: E501


PROFILE_SURVEY = \
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>ICT</title>
             <survey>
              <title>Software development</title>
              <profile-question>
                <title>Profile one</title>
                <question>List all your departments:</question>
                <description/>
                <risk type="policy">
                  <title>New hires are not aware of design patterns.</title>
                  <description>&lt;p&gt;Every developer should know about them..&lt;/p&gt;</description>
                  <evaluation-method>direct</evaluation-method>
                </risk>
              </profile-question>
            </survey>
          </sector>"""  # noqa: E501


def _create(container, *args, **kwargs):
    newid = container.invokeFactory(*args, **kwargs)
    obj = getattr(container, newid)
    return obj


def createSector(
    portal,
    id="sector",
    title=u"Test Sector",
    login=None,
    password=None,
    country="nl",
    **kw
):
    with api.env.adopt_user(SITE_OWNER_NAME):
        if hasattr(portal, "sectors"):
            container = portal.sectors
        else:
            with api.env.adopt_user(SITE_OWNER_NAME):
                container = _create(
                    portal,
                    "euphorie.sectorcontainer",
                    "sectors",
                )
        if "nl" in container:
            country = container["nl"]
        else:
            with api.env.adopt_user(SITE_OWNER_NAME):
                country = _create(
                    container,
                    "euphorie.country",
                    "nl"
                )

        sector = _create(country, "euphorie.sector", id, title=title, **kw)
        sector.login = login or title.lower()
        sector.password = password if password is not None else sector.login
        return sector


def addSurvey(
    sector,
    snippet=BASIC_SURVEY,
    surveygroup_title=u"Test survey",
    survey_title=u"Standard version",
):
    from euphorie.content import upload
    importer = upload.SurveyImporter(sector)
    return importer(snippet, surveygroup_title, survey_title)
