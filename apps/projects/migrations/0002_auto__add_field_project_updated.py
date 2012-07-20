# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.updated'
        db.add_column('projects_project', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.updated'
        db.delete_column('projects_project', 'updated')


    models = {
        'projects.project': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Project'},
            'code_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'docs_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_fork': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'logo_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'logo_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'project_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'why_forked': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['projects']