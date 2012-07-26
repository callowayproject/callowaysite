from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

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
        'django.views.generic.simple.direct_to_template',
        {'template': 'homepage.html'},
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
