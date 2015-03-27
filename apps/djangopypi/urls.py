# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from djangopypi.feeds import ReleaseFeed
from djangopypi.views.packages import (PackageListView, SimpleIndexView,
                    PackageDetailView, PackageSearchView, PackageSimpleDetailView,
                    PackageDoapView)
from djangopypi.views.releases import (ReleaseListView, ReleaseDetailView,
                    ReleaseDoapView)

urlpatterns = patterns("",
    url(r'^$', "djangopypi.views.root", name="djangopypi-root"),
    url(r'^packages/$', PackageListView.as_view(), name='djangopypi-package-index'),
    url(r'^simple/$', SimpleIndexView.as_view(), name='djangopypi-package-index-simple'),
    url(r'^search/$', PackageSearchView.as_view(), name='djangopypi-search'),
    url(r'^pypi/$', 'djangopypi.views.root', name='djangopypi-release-index'),
    url(r'^rss/$', ReleaseFeed(), name='djangopypi-rss'),

    url(r'^simple/(?P<package>[\w\d_\.\-]+)/$', PackageSimpleDetailView.as_view(),
        name='djangopypi-package-simple'),

    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/$', PackageDetailView.as_view(),
        name='djangopypi-package'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/rss/$', ReleaseFeed(),
        name='djangopypi-package-rss'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/doap.rdf$', PackageDoapView.as_view(),
        name='djangopypi-package-doap'),



    # url(r'^pypi/(?P<package>[\w\d_\.\-]+)/manage/$', 'packages.manage',
    #     name='djangopypi-package-manage'),
    # url(r'^pypi/(?P<package>[\w\d_\.\-]+)/manage/versions/$', 'packages.manage_versions',
    #     name='djangopypi-package-manage-versions'),

    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/$',
        ReleaseDetailView.as_view(), name='djangopypi-release'),
    url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/doap.rdf$',
        ReleaseDoapView.as_view(), name='djangopypi-release-doap'),
    # url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/manage/$',
    #     'releases.manage', name='djangopypi-release-manage'),
    # url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/metadata/$',
    #     'releases.manage_metadata', name='djangopypi-release-manage-metadata'),
    # url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/files/$',
    #     'releases.manage_files', name='djangopypi-release-manage-files'),
    # url(r'^pypi/(?P<package>[\w\d_\.\-]+)/(?P<version>[\w\d_\.\-]+)/files/upload/$',
    #     'releases.upload_file', name='djangopypi-release-upload-file'),
)
