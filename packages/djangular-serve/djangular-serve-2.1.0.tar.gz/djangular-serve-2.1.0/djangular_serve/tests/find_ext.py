import os

from example.settings import STATIC_ROOT


class ImageExtension(object):
    """
    Find image extension in static files to move to sub dir.
    """

    ICO = '.ico'
    JPG = '.jpg'
    JPEG = '.jpeg'
    PNG = '.png'
    GIF = '.gif'
    SVG = '.svg'
    types = [ICO, JPG, JPEG, PNG, GIF, SVG]


def get_img_extension():
    """
    Find the image types and match it with our list
    """

    list_of_files = os.listdir(STATIC_ROOT)
    t = ImageExtension.types

    for image in list_of_files:
        found_types = os.path.splitext(image)[1]
        for extension in t:
            if extension.endswith(found_types):
                try:
                    print(extension.lower())
                except FileNotFoundError:
                    print(extension.upper())


print(get_img_extension())
