from django.conf.urls import url
from .views import \
    manifest, \
    service_worker, \
    offline, \
    serve_funnel, \
    router_link
from .app_settings import SERVICE_WORKER_NAME
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url('^$', serve_funnel, name='serve'),
    url('^{}$'.format(SERVICE_WORKER_NAME), service_worker, name='serviceworker'),
    url('^manifest.json$', manifest, name='manifest'),
    url('^offline/$', offline, name='offline'),
]

urlpatterns += [
    url(_(r'^(?P<path>.*)/$'), router_link, name='router_link')
]
