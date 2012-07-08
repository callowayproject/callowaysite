from django.db import models
from django.core.files.images import get_image_dimensions

from projects.settings import LOGO_STORAGE, PROJECT_TYPES, STATUSES


class Project(models.Model):
    """Something that we work on"""
    name = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    code_url = models.CharField(blank=True, max_length=255)
    docs_url = models.CharField(blank=True, max_length=255)
    logo = models.FileField(blank=True, upload_to='projects/logos', storage=LOGO_STORAGE())
    logo_width = models.IntegerField(editable=False, blank=True, null=True)
    logo_height = models.IntegerField(editable=False, blank=True, null=True)
    is_fork = models.BooleanField(default=False)
    why_forked = models.TextField(blank=True, null=True)
    external_id = models.IntegerField(blank=True, null=True)
    project_type = models.IntegerField(choices=PROJECT_TYPES, default=2)
    status = models.IntegerField(choices=STATUSES, default=0)

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.logo:
            width, height = get_image_dimensions(self.logo.file, close=True)
        else:
            width, height = None, None

        self.key_image_width = width
        self.key_image_height = height

        super(Project, self).save(*args, **kwargs)
