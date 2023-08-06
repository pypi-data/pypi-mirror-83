from django.http import HttpResponse
from django.shortcuts import render

from djangular_serve import app_settings


def serve_funnel(request):
    """
    Angular app distribution template
    """
    return render(request, "_index.html")  # this is the base template to extend through other html pages.


def router_link(request, path=""):
    """
    Allow compatibility between RouterLinks and Django url and path.
    """
    return serve_funnel(request)


def service_worker(request):
    """
    Service worker support
    """
    response = HttpResponse(
        open(
            app_settings.SERVICE_WORKER_PATH).read(),
        content_type='application/javascript')
    return response


def manifest(request):
    """
    App manifest
    """
    return render(request, 'manifest/manifest.json', {
        find_attr: getattr(app_settings, find_attr)
        for find_attr in dir(app_settings)
        if find_attr.startswith('APP_')
    })


def offline(request):
    """
    Offline support
    """
    return render(request, "manifest/offline.html")
