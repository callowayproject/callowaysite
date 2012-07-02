from django.contrib import admin

from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_type', 'status', 'is_fork')
    list_filter = ('project_type', 'status', )
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'logo')
        }),
        ('URLs', {
            'fields': ('code_url', 'docs_url')
        }),
        ('Info', {
            'fields': ('is_fork', 'external_id', 'project_type', 'status')
        })
)


admin.site.register(Project, ProjectAdmin)