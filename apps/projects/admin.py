from django.contrib import admin

from projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_type', 'status', 'is_fork')
    list_filter = ('project_type', 'status', )
    search_fields = ('name',)
    actions = ['make_live', 'archive']
    list_editable = ('status', 'project_type')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'logo')
        }),
        ('URLs', {
            'fields': ('code_url', 'docs_url')
        }),
        ('Info', {
            'fields': ('is_fork', 'why_forked', 'external_id', 'project_type',
                       'status', )
        })
    )

    def make_live(self, request, queryset):
        queryset.update(status=0)

    def archive(self, request, queryset):
        queryset.update(status=1)

admin.site.register(Project, ProjectAdmin)
