from plone.app.imagecropping.browser.settings import ISettings
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import getAllowedSizes
from zope.component import getMultiAdapter
from zope.component._api import getUtility
from zope.globalrequest import getRequest


FIELDNAMES = ("image", "external_site_logo")


def _initial_size(ix, iy, sx, sy):
    """we need a best fit centered selection.

    Shamelessly copied from plone.app.imaging.browser.editor
    """
    ix, iy, sx, sy = map(float, (ix, iy, sx, sy))
    # aspect ratio of original
    if iy > 0:
        ir = ix / iy
    else:
        ir = 1

    # aspect ratio of scale
    if sy > 0:
        sr = sx / sy
    else:
        sr = 1

    # scale up to bounds
    if ir > sr:
        rx1, ry1 = ix * sr / ir, iy
    else:
        rx1, ry1 = ix, iy * ir / sr

    rx0, ry0 = 0, 0

    # center box
    if rx1 < ix:
        deltax = ix - rx1
        rx0 = deltax / 2
        rx1 = rx1 + deltax / 2
    if ry1 < iy:
        deltay = iy - ry1
        ry0 = deltay / 2
        ry1 = ry1 + deltay / 2

    # round to int
    rx0, ry0 = int(round(rx0)), int(round(ry0))
    rx1, ry1 = int(round(rx1)), int(round(ry1))
    return rx0, ry0, rx1, ry1


def _autocrop_scales(context):
    cropping_registry = getUtility(IRegistry)
    settings = cropping_registry.forInterface(ISettings)
    scale_names = settings.cropping_for
    request = getRequest()
    cropper = getMultiAdapter((context, request), name="crop-image")
    for fname in FIELDNAMES:
        field = getattr(context, fname, None)
        if not field:
            continue

        real_width, real_height = map(float, field.getImageSize())
        # some images are not initialized properly, in which case they
        # get -1 for width and height. In this case, don't crop
        if real_width == -1 or real_height == -1:
            continue
        allowed = getAllowedSizes()
        for scale_name in scale_names:
            if scale_name not in allowed:
                continue

            width, height = map(float, allowed[scale_name])

            coords = _initial_size(real_width, real_height, width, height)
            cropper._crop(fname, scale_name, coords)


def crop_on_image_edit(context, event):
    _autocrop_scales(context)
