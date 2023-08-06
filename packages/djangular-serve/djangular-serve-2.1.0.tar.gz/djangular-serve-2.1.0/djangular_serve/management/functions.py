import os

try:
    from djangular_serve.management.utils import Helpers
    from djangular_serve.management.handlers import \
        get_img_extension, \
        move_files
except (ModuleNotFoundError, ValueError):
    from .utils import Helpers
    from .handlers import \
        get_img_extension, \
        move_files


class AngularBuild:
    """
    Build data
    """
    h = Helpers()
    static_path = h.get_project_static_root()
    ng_path = h.get_ng_root_path()

    ng_build = "ng build"
    prefix_prod = "--prod --output-path {}".format(static_path)
    prefix_hash = "--output-hashing none"


def ng_deploy():
    """
    Build Angular project to Django static and organise.
    """
    h = Helpers
    prompt = h.query_yes_no
    prompt()
    b = AngularBuild()

    ng_build = b.ng_build  # ng build
    prefix_prod = b.prefix_prod  # --prod --output-path ./../../
    prefix_hash = b.prefix_hash  # --output-hashing none
    ng_path = b.ng_path  # Path where Angular project is

    os.chdir(ng_path)  # Automatically get Angular project without CD

    # Gather data and execute command
    compile_ = "{} {} {}".format(ng_build, prefix_prod, prefix_hash)
    print(">> Running", compile_, "for {}".format(ng_path))
    command = compile_
    process = os.system(command)
    return process


def move_js():
    """
    Move all static .js files to respective sub directory.
    """
    b = AngularBuild
    static_url = b.static_path

    js_source = '{}/*.js'.format(static_url)
    js_path_input = os.path.join(static_url, input("? JS directory name: "))
    js_destination = '{}/{}'.format(static_url, move_files(files=js_source, dest=js_path_input))
    try:
        return js_destination
    except:
        print(f'There was an error moving {js_source} to {js_path_input}.')


def move_css():
    """
    Move all static .css files to respective sub directory.
    """
    b = AngularBuild
    static_url = b.static_path

    css_source = '{}/*.css'.format(static_url)
    css_path_input = os.path.join(static_url, input("? CSS directory name: "))
    css_destination = '{}/{}'.format(static_url, move_files(files=css_source, dest=css_path_input))
    try:
        return css_destination
    except:
        print(f'There was an error moving {css_source} to {css_path_input}.')


def move_img():
    """
    Move all static .img files to respective sub directory.
    """
    b = AngularBuild
    static_url = b.static_path

    img_source = '{}/{}'.format(static_url, get_img_extension())
    img_path_input = os.path.join(static_url, input("? IMAGE directory name: "))
    img_destination = '{}/{}'.format(static_url, move_files(files=img_source, dest=img_path_input))
    try:
        return img_destination
    except:
        print(f'There was an error moving {img_source} to {img_path_input}.')


def move_all():
    """
    Move all static files to respective sub directories.
    """
    move_js()
    move_css()
    move_img()


def make_directory(mkdir):
    """
    Make a new sub directory in the static folder.
    """
    b = AngularBuild
    static_url = b.static_path
    os.chdir(static_url)
    if os.path.exists(static_url + mkdir):
        raise FileExistsError
    else:
        os.mkdir(mkdir)
        print(mkdir, f'was created in {static_url}.')
