from lxml import etree
from pathlib import posixpath
from plone.namedfile.file import NamedBlobImage
from urllib.parse import unquote
from zope.component.hooks import setSite
import logging
import requests
import sys
import transaction

log = logging.getLogger(__name__)


if len(sys.argv) > 3:
    images_path = posixpath.abspath(sys.argv[3])
else:
    images_path = posixpath.abspath(".")

app = locals()["app"]
setSite(app["Plone2"])
wt = app["Plone2"]["portal_workflow"]

__import__("pdb").set_trace()
for page_num in range(26):
    url = (
        "https://oiraproject.eu/en/oira-tools?search_api_fulltext=&sort_by=title"
        "&page={}".format(page_num)
    )
    page = requests.get(url).text
    tree = etree.HTML(page)
    for elem in tree.findall(".//div[@class='views-field views-field-nothing']"):
        link = elem.find(".//div[@class='tool-link']/a")
        if link is not None:
            path = "/".join(unquote(link.attrib["href"]).strip().split("/")[-3:])
        else:
            __import__("pdb").set_trace()
            continue

        img = elem.find(".//div[@class='views-field views-field-field-image']/img")
        if img is None:
            log.warning("No image for {}".format(path))
            continue
        basename = unquote(img.attrib["src"].split("/")[-1].split(".")[0]).strip()
        if not basename:
            __import__("pdb").set_trace()
        name = " ".join([part for part in basename.split(" ")[:-1]])
        filename = "{} 300.png".format(name)
        filepath = posixpath.join(images_path, filename)
        if not posixpath.exists(filepath):
            log.warning("Image file not found: {} ({})".format(filepath, basename))
            continue

        try:
            surveygroup = app.unrestrictedTraverse("/".join(("/Plone2/sectors", path)))
        except KeyError:
            log.warning("Tool not found: {}".format(path))
            continue

        with open(filepath, "rb") as imagefile:
            blob_image = NamedBlobImage(data=imagefile.read(), filename=filename)

        for survey in surveygroup.values():
            if getattr(survey, "image", None):
                log.info("Already has image: {}".format(path))
                continue
            else:
                setattr(survey, "image", blob_image)

            if getattr(surveygroup, "published", None) == survey.getId():
                try:
                    wt.doActionFor(survey, "update")
                except Exception as e:
                    log.exception(e)
                    continue

transaction.commit()
