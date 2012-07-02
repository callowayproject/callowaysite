from django.db import models
from projects.settings import LOGO_STORAGE, PROJECT_TYPES, STATUSES


class Project(models.Model):
    """Something that we work on"""
    name = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    code_url = models.CharField(blank=True, max_length=255)
    docs_url = models.CharField(blank=True, max_length=255)
    logo = models.FileField(blank=True, upload_to='projects/logos', storage=LOGO_STORAGE())
    is_fork = models.BooleanField(default=False)
    external_id = models.IntegerField(blank=True, null=True)
    project_type = models.IntegerField(choices=PROJECT_TYPES, default=1)
    status = models.IntegerField(choices=STATUSES, default=1)

    def __unicode__(self):
        return self.name
