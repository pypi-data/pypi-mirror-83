import os
import time
from pathlib import Path  # noqa

from djangular_serve import app_settings


class Helpers(object):
    """
    Mixin to get commonly used Commands
    """

    def export_settings(self=None):
        get_app = os.environ.get('DJANGO_SETTINGS_MODULE')
        export = os.system(f'export DJANGO_SETTINGS_MODULE={get_app}')
        return export

    def get_ng_root_path(self):
        """
        Angular project root path.
        :return:
        """
        return getattr(app_settings, 'NG_ROOT_PATH')

    def get_project_static_root(self):
        """
        Find django static root
        """
        static_path = getattr(app_settings, "STATIC_ROOT")
        return static_path

    def query_yes_no(self=None):
        """
        Ask a yes/no question via input() and return their answer.
        """
        answer = input('Please confirm you want to continue: [Y/n]')
        if not answer or answer[0].lower() != 'y':
            print('You chose not to continue.')
            exit(1)

        else:
            print('Building Angular app to Django static...')
            time.sleep(2)

