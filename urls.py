from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings

from django.views.generic import TemplateView
admin.autodiscover()

sitemaps = {}

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^admin_tools/', include('admin_tools.urls')),
    url(
        r'^robots.txt$',
        'robots.views.rules_list',
        name='robots_rule_list'),
    url(
        r'^$',
        TemplateView.as_view(template_name='homepage.html'),
        name='homepage'),
    url(
        r'^projects/$',
        'projects.views.project_list',
        name='project_list'),
    (r'^people/', include('mystaff.urls')),
)

urlpatterns += patterns('',
    url(r'', include('djangopypi.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^media/static/(?P<path>.*)$', 'serve'),
    )
