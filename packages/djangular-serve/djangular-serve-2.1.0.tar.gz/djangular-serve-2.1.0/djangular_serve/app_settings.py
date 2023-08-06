"""
Default settings
"""

# -------------------------------------
# TDD
# -------------------------------------
# try:
#    from example import settings
# except NameError:
#    from django.conf import settings
# ------------------------------------

import os

from django.core.exceptions import ImproperlyConfigured

try:
    from django.conf import settings
except ImproperlyConfigured:
    from .management.utils import Helpers
    export_settings = Helpers.export_settings
    exec(export_settings())
    from django.conf import settings

from django.shortcuts import resolve_url
from django.urls import get_script_prefix
from django.utils.functional import lazy
from pathlib import Path  # noqa

# Lazy-evaluate URLs so including app.urls in root urlconf works
resolve_url = lazy(resolve_url, str)

# Get script prefix for apps not mounted under /
_SCRIPT_PREFIX = get_script_prefix()
# ----------------------------------------------------------------------------------
# Set your relevant paths to allow Djangular-Serve, find templates and static
# This is one way.  Do it in whatever way it works for you.
# ----------------------------------------------------------------------------------
# Build paths inside the project like this: APP_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent  # Absolute root path
# APP_DIR = Path(__file__).resolve(strict=True).parent  # 'example' project
# URL = os.path.relpath(APP_DIR / "static")  # example/static
# ANGULAR_DIR = os.path.join(BASE_DIR, ".")  # root/ngservetest

""" 
Angular project root. 
"""
NG_ROOT_PATH = getattr(settings, 'NG_ROOT_PATH', '')

""" 
Static root to distribute Angular app as static. 
"""
STATIC_ROOT = getattr(settings, 'STATIC_ROOT', 'static')

""" 
Serve CDN or static css files to your template. 
"""
CSS_PATH = getattr(settings, 'STYLESHEETS', [
    {
        'src': ''
    },
])

""" 
Serve CDN or static js files to your template. 
"""
JAVASCRIPT_PATH = getattr(settings, 'JAVASCRIPT', [
    {
        'src': ''
    },
])

""" 
Serve CDN or static fonts files to your template. 
"""
FONT_PATH = getattr(settings, 'FONTS', [
    {
        'src': ''
    },
])

""" 
Path and name of the service worker.
"""
SERVICE_WORKER_PATH = getattr(
    settings, 'SERVICE_WORKER_PATH',
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates/manifest', 'serviceworker.js'))

SERVICE_WORKER_NAME = getattr(
    settings, 'SERVICE_WORKER_NAME', os.path.basename('{}'.format(SERVICE_WORKER_PATH)))

""" 
App parameters to include in manifest.json and appropriate meta tags. 
"""
APP_NAME = getattr(settings, 'APP_NAME', 'Djangular-Serve')
APP_DESCRIPTION = getattr(settings, 'APP_DESCRIPTION', 'App to distribute angular to django')
APP_ROOT_URL = resolve_url(getattr(settings, 'APP_ROOT_URL', _SCRIPT_PREFIX))
APP_THEME_COLOR = getattr(settings, 'APP_THEME_COLOR', '#000')
APP_BACKGROUND_COLOR = getattr(settings, 'APP_BACKGROUND_COLOR', '#fff')
APP_DISPLAY = getattr(settings, 'APP_DISPLAY', 'standalone')
APP_SCOPE = resolve_url(getattr(settings, 'APP_SCOPE', _SCRIPT_PREFIX))
APP_DEBUG_MODE = getattr(settings, 'APP_DEBUG_MODE', True)
APP_ORIENTATION = getattr(settings, 'APP_ORIENTATION', 'any')
APP_START_URL = resolve_url(getattr(settings, 'APP_START_URL', _SCRIPT_PREFIX))
APP_FETCH_URL = resolve_url(getattr(settings, 'APP_FETCH_URL', _SCRIPT_PREFIX))
APP_STATUS_BAR_COLOR = getattr(settings, 'APP_STATUS_BAR_COLOR', 'default')
APP_ICONS = getattr(settings, 'APP_ICONS', [
    {
        'src': '/assets/images/icon-72x72.png',
        'size': '72x72'
    },
    {
        'src': '/assets/images/icon-96x96.png',
        'size': '96x96'
    },
    {
        'src': '/assets/images/icon-128x128.png',
        'size': '128x128'
    },
    {
        'src': '/assets/images/icon-144x144.png',
        'size': '144x144'
    },
    {
        'src': '/assets/images/icon-152x152.png',
        'size': '152x152'
    },
    {
        'src': '/assets/images/icon-192x192.png',
        'size': '192x192'
    },
    {
        'src': '/assets/images/icon-384x384.png',
        'size': '384x384'
    },
    {
        'src': '/assets/images/icon-512x512.png',
        'size': '512x512'
    }
])
APP_SPLASH_SCREEN = getattr(settings, 'APP_SPLASH_SCREEN', [
    {
        'src': '/assets/images/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/assets/images/splash-750x1334.png',
        'media': '(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/assets/images/splash-1242x2208.png',
        'media': '(device-width: 621px) and (device-height: 1104px) and (-webkit-device-pixel-ratio: 3)'
    },
    {
        'src': '/assets/images/splash-1125x2436.png',
        'media': '(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)'
    },
    {
        'src': '/assets/images/splash-828x1792.png',
        'media': '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/assets/images/splash-1242x2688.png',
        'media': '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3)'
    },
    {
        'src': '/assets/images/splash-1536x2048.png',
        'media': '(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/assets/images/splash-1668x2224.png',
        'media': '(device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/assets/images/splash-1668x2388.png',
        'media': '(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/assets/images/splash-2048x2732.png',
        'media': '(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2)'
    }

])
APP_DIR = getattr(settings, 'APP_DIR', 'auto')
APP_LANG = getattr(settings, 'APP_LANG', settings.LANGUAGE_CODE)
APP_CONFIG = getattr(settings, 'APP_CONFIG', 'serve.config')  # TODO:
