from lxml import etree
from pathlib import posixpath
from plone.namedfile.file import NamedBlobImage
from tempfile import TemporaryDirectory
from urllib.parse import unquote
from urllib.parse import urlparse
from zope.component.hooks import setSite

import logging
import requests
import sys
import transaction
import urllib.request


log = logging.getLogger(__name__)

BASE_URL = "https://oiraproject.eu"


if len(sys.argv) > 3:
    images_path = posixpath.abspath(sys.argv[3])
else:
    images_path = posixpath.abspath(".")

app = locals()["app"]
setSite(app["Plone2"])
wt = app["Plone2"]["portal_workflow"]

for page_num in range(255):
    url = "{}/en/oira-tools?search_api_fulltext=&sort_by=title" "&page={}".format(
        BASE_URL, page_num
    )
    page = requests.get(url).text
    tree = etree.HTML(page)
    tool_elements = tree.findall(".//div[@class='views-field views-field-nothing']")
    if not tool_elements:
        log.warning("Stopping at page {} (no more tools found)".format(page_num))
        break
    for elem in tool_elements:
        link = elem.find(".//div[@class='tool-link']/a")
        if link is not None:
            path = "/".join(
                urlparse(unquote(link.attrib["href"]))
                .path.strip()
                .rstrip("/")
                .split("/")[-3:]
            )
        else:
            continue

        try:
            surveygroup = app.unrestrictedTraverse("/".join(("/Plone2/sectors", path)))
        except KeyError:
            log.warning("Tool not found: {}".format(path))
            continue

        img = elem.find(".//div[@class='views-field views-field-field-image']//img")
        if img is None:
            log.warning("No image for {}".format(path))
            continue
        sourcename = urlparse(img.attrib["src"]).path.split("/")[-1]
        basename = unquote(sourcename.split(".")[0]).strip()
        if " " in basename:
            name = " ".join([part for part in basename.split(" ")[:-1]])
        else:
            name = basename
        filename = "{} 300.png".format(name)
        filepath = posixpath.join(images_path, filename)
        blob_image = None
        if not posixpath.exists(filepath):
            log.warning(
                "{}: Image file not found: {} ({}). Attempting download".format(
                    path, filepath, sourcename
                )
            )
            with TemporaryDirectory(prefix="euphorieimage") as tmpdir:
                urllib.request.urlretrieve(
                    "{}{}".format(BASE_URL, img.attrib["src"]), filepath
                )
                try:
                    with open(filepath, "rb") as imagefile:
                        blob_image = NamedBlobImage(
                            data=imagefile.read(), filename=filename
                        )
                except Exception as e:
                    log.warning(
                        "Unable to download image from website. Error: {}".format(e)
                    )
                    continue
        else:
            with open(filepath, "rb") as imagefile:
                blob_image = NamedBlobImage(data=imagefile.read(), filename=filename)

        if not blob_image:
            continue
        for survey in surveygroup.values():
            if getattr(survey, "image", None):
                # log.warning("Already has image: {}".format(path))
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
