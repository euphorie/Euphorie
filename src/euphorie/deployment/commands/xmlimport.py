import logging
from optparse import OptionParser
import os.path
import sys
import lxml.etree
import lxml.objectify
import transaction
import zExceptions
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from Testing.makerequest import makerequest
from zope.site import hooks
from plone.namedfile.file import NamedBlobImage
from euphorie.content.upload import SurveyImporter
from euphorie.content.user import UserProvider
from euphorie.client import publish

log = logging.getLogger(__name__)


class Abort(RuntimeError):
    def __init__(self, message, exitcode=1):
        self.message = message
        self.exitcode = exitcode


def GetCountry(plone, options):
    sectors = plone.sectors
    if not hasattr(sectors, options.country):
        log.info("Creating missing country %s", options.country)
        sectors.invokeFactory("euphorie.country", options.country,
                title=options.country)
    return getattr(sectors, options.country)


def GetSector(country, xml_sector, options):
    if options.sector is None:
        if not hasattr(xml_sector, "account"):
            return None
        login = xml_sector.account.get("login").lower()
        password = xml_sector.account.get("password")
    else:
        password = None
        login = options.sector.lower()

    if options.login is not None:
        login = options.login
    if password is None:
        password = login

    sector = getattr(country, login, None)
    if sector is not None:
        return sector

    log.info("Creating new sector '%s' with password '%s'", login, password)
    id = country.invokeFactory("euphorie.sector", login,
            title=options.sector or xml_sector.title.text.strip())
    sector = getattr(country, id)
    sector.login = login
    sector.password = password

    if hasattr(xml_sector, "contact"):
        xml_contact = xml_sector.contact
        if hasattr(xml_contact, "name"):
            sector.contact_name = unicode(xml_contact.name.text)
        if hasattr(xml_contact, "email"):
            sector.contact_email = unicode(xml_contact.email.text)
    if options.logo is not None:
        sector.logo = NamedBlobImage(data=open(options.logo, "r").read(),
                filename=unicode(os.path.basename(options.logo)))
    if options.main_colour:
        sector.main_colour = options.main_colour
    if options.support_colour:
        sector.support_colour = options.support_colour
    return sector


def ImportSector(plone, options, filename):
    input = open(filename, "r")
    dom = lxml.objectify.parse(input)
    xml_sector = dom.getroot()
    country = GetCountry(plone, options)
    if not hasattr(xml_sector, "survey"):
        return

    sector = GetSector(country, xml_sector, options)
    if sector is None:
        raise Abort("No sector specified and no account information found.")

    # Login as the sector
    sup = UserProvider(sector)
    sectoruser = plone.acl_users.getUserById(sup.getUserId())
    sm = getSecurityManager()
    try:
        newSecurityManager(None, sectoruser)
        name = options.name or unicode(xml_sector.survey.title.text)

        if hasattr(sector, name):
            raise Abort("There is already a survey named '%s'" % name)

        log.info(u"Importing survey '%s' with version '%s'",
                name, options.version)
        importer = SurveyImporter(sector)
        survey = importer(xml_sector, name, options.version)

        if options.publish:
            log.info("Publishing survey")
            publisher = publish.PublishSurvey(survey, None)
            publisher.publish()
    finally:
        setSecurityManager(sm)


def main(app, args):
    parser = OptionParser(
            usage="Usage: bin/instance xmlimport [options] <XML-files>")
    parser.add_option("-p", "--publish",
            help="Publish the imported sector.",
            action="store_true", dest="publish", default=False)
    parser.add_option("-S", "--site",
            help="id of the Plone site. Defaults to Plone",
            action="store", type="string", dest="site",
            default="Plone")
    parser.add_option("-L", "--logo",
            help="Filename for the sector logo.",
            action="store", type="string", dest="logo")
    parser.add_option("--main-colour",
            help="Main colour used for client pages.",
            action="store", type="string", dest="main_colour")
    parser.add_option("--support-colour",
            help="Support colour used for client pages.",
            action="store", type="string", dest="support_colour")
    parser.add_option("-c", "--country",
            help="The country where the branch/model should be created. "
                 "Defaults to nl.",
            action="store", type="string", dest="country", default="nl")
    parser.add_option("-s", "--sector",
            help="The name of the sector where the survey should be created.",
            action="store", type="string", dest="sector")
    parser.add_option("-l", "--login",
            help="Login name for the sector. Also used as sector id.",
            action="store", type="string", dest="login")
    parser.add_option("-n", "--name",
            help="Override name for the imported survey.",
            action="store", type="string", dest="name")
    parser.add_option("-v", "--version-name",
            help="Name of the new survey version. Defaults to 'default'.",
            action="store", type="string", dest="version",
            default="default")

    (options, args) = parser.parse_args(args)

    if not args:
        raise Abort("Please specify a (single) XML file to import.")

    # The magic Zope2 setup dance
    zope2 = makerequest(app)
    hooks.setHooks()
    plone = getattr(zope2, options.site)
    hooks.setSite(plone)

    # Login as admin
    admin = zope2.acl_users.getUserById("admin")
    newSecurityManager(None, admin)

    for arg in args:
        transaction.begin()
        try:
            log.info("Importing %s", arg)
            ImportSector(plone, options, arg)
            trans = transaction.get()
            trans.setUser("-commandline-")
            trans.note("Import of %s" % arg)
            trans.commit()
        except lxml.etree.XMLSyntaxError as e:
            transaction.abort()
            log.error(e.message)
            log.error("Invalid input file")
        except RuntimeError as e:
            transaction.abort()
            log.error(e.message)
        except zExceptions.Unauthorized as e:
            transaction.abort()
            log.error(e.message)
            log.error("This is mostly likely due to too deep nesting "
                      "in the survey.")
        except zExceptions.BadRequest as e:
            transaction.abort()
            log.error(e.message)
            log.error("This is mostly likely due to illegal input data.")
        except Exception as e:
            transaction.abort()
            raise


if __name__ == "__main__":
    # We can not use logging.basicConfig since Zope2 has already configured
    # things.
    rootlog = logging.getLogger()
    rootlog.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    for handler in rootlog.handlers:
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

    main(app, sys.argv[1:])
