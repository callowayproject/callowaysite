from djangopypi import settings
from django.contrib import admin

from djangopypi.models import (Release, Package, Classifier, Distribution, Review,
                                MasterIndex, MirrorLog)


class PackageAdmin(admin.ModelAdmin):
    '''
    Admin View for Package
    '''
    list_display = ('name', )
    search_fields = ['name']

admin.site.register(Package, PackageAdmin)


class ReleaseAdmin(admin.ModelAdmin):
    '''
    Admin View for Release
    '''
    list_display = ('package', 'version', 'created')
    search_fields = ['package', 'version']

admin.site.register(Release, ReleaseAdmin)

admin.site.register(Classifier)


class DistributionAdmin(admin.ModelAdmin):
    '''
    Admin View for Release
    '''
    list_display = ('release', 'created')
    search_fields = ['release', ]
    raw_id_fields = ['release', ]


admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Review)

if settings.MIRRORING:
    admin.site.register(MasterIndex)
    admin.site.register(MirrorLog)
