import os
from pathlib import Path  # noqa

try:
    from djangular_serve import app_settings
    from djangular_serve.management.utils import Helpers
except (ModuleNotFoundError, ValueError):
    from .utils import Helpers
    from .. import app_settings


def move_files(files, dest):
    """
    Function as a constant to move static files to destination of choice
    """

    if not os.path.isfile(files):
        try:
            print(f"\nAll {os.path.basename(files)} files have been moved.")
        except FileExistsError as no_files:
            assert no_files
        else:
            if os.path.exists(dest):
                run = os.system("mv {} {}".format(files, dest))
                print(f'\nDirectory {os.path.relpath(dest)} already exists. Moving {os.path.basename(files)}')
                return run
            else:
                run = os.mkdir(dest), os.system("mv {} {}".format(files, dest))
                print(f'\nMaking directory {os.path.relpath(dest)} and moving {os.path.basename(files)}')
                return run


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
    h = Helpers()
    get_project_static_root = h.get_project_static_root()

    list_of_files = os.listdir(get_project_static_root)

    t = ImageExtension.types

    for image in list_of_files:
        found_types = os.path.splitext(image)[1]
        found_to_str = ''.join(str('*' + e + ' ') for e in found_types)
        type_to_str = ''.join(str('*' + e + ' ') for e in t)

        if found_types or found_to_str in t:
            os.chdir(get_project_static_root)
            return type_to_str
