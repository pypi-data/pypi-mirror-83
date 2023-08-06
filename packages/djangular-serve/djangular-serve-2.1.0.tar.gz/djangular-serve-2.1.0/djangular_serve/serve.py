#!/usr/bin/python3
"""""
DJANGULAR SERVE MAIN
"""""
import argparse

try:
    from djangular_serve.management.functions import \
        AngularBuild, \
        ng_deploy, \
        move_js, \
        move_css, \
        move_img, \
        move_all, \
        make_directory
    from djangular_serve.management.exceptions import ArgDoesNotExist
except (ModuleNotFoundError, ValueError):
    from .management.functions import \
        AngularBuild, \
        ng_deploy, \
        move_js, \
        move_css, \
        move_img, \
        move_all, \
        make_directory
    from .management.exceptions import ArgDoesNotExist


def main():
    """""
    DJANGULAR SERVE
    """""
    parser = argparse.ArgumentParser(
        prog='serve',
        description='Automate your Django / Angular projects'
                    ' with DJANGULAR-SERVE.'
    )

    parser.add_argument(
        '-s',
        '--serve',
        type=str,
        help='Build Angular to Django static.'
    )

    parser.add_argument(
        '-mv',
        '--move',
        type=str,
        help='Move files to respective directories.'
    )

    parser.add_argument(
        '-mk',
        '--mkdir',
        type=str,
        help='Make a new sub directory in your static files folder.'
    )

    args = parser.parse_args()

    """""
    Serve args
    """""
    serve = args.serve
    move = args.move
    mkdir = args.mkdir

    arg_is_none = ArgDoesNotExist("\n\nArgument does not exist. Did you mean...\n"
                                  "serve -s ng\n"
                                  "serve -mv js, css, img or all\n"
                                  "serve -mk <any-dir>\n")
    if not args:
        raise arg_is_none

    try:

        """""
        Serve
        """""
        if serve:
            if serve == "ng":
                ng_deploy()
        else:
            pass

        """""
        Move
        """""
        if move:
            if move == "js":
                move_js()

            if move == "css":
                move_css()

            if move == "img":
                move_img()

            if move == "all":
                move_all()
        else:
            pass

        """""
        Make
        """""

        if mkdir:
            make_directory(mkdir)
        else:
            pass

    except KeyboardInterrupt:
        print("\n => You have force cancelled the session.\n")


if __name__ == '__main__':
    main()
