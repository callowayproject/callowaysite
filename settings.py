# Django settings for project project.

import calloway
import os
import sys

CALLOWAY_ROOT = os.path.abspath(os.path.dirname(calloway.__file__))
sys.path.insert(0, os.path.join(CALLOWAY_ROOT, 'apps'))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

from calloway.settings import *

ADMINS = (
    ('coordt', 'webmaster@washingtontimes.com'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL='webmaster@washingtontimes.com'
SERVER_EMAIL='webmaster@washingtontimes.com'

SECRET_KEY = 'k74n3t@dpe*6aw_wzwukybfem56f7q=bocqdpyy72hflmp-3#n'

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dev.db'       # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'media2')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'ugc')
MEDIA_URL = '/media/ugc/'
STATIC_URL = '/media/'

AUTH_PROFILE_MODULE = ''

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
) + CALLOWAY_TEMPLATE_DIRS

#CACHE_BACKEND = 'versionedcache.backend://localhost:11211/'
CACHE_BACKEND = 'dummy:///'

INSTALLED_APPS = APPS_CORE + \
    APPS_ADMIN + \
    APPS_STAFF + \
    APPS_CALLOWAY_DEFAULT + \
    APPS_MEDIA + \
    APPS_UTILS + \
    APPS_REGISTRATION + \
    APPS_TINYMCE

ADMIN_TOOLS_THEMING_CSS = 'admin/css/theming.css'

TINYMCE_JS_URL = '%sjs/tiny_mce/tiny_mce.js' % STATIC_URL

TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'js/tiny_mce')

STATIC_MEDIA_COPY_PATHS = (
    {'from': os.path.join(CALLOWAY_ROOT, 'media'), 'to': 'media'},
    {'from': 'static', 'to': 'media'},
)

STATIC_MEDIA_COMPRESS_CSS = False
STATIC_MEDIA_COMPRESS_JS = False
STATIC_MEDIA_APP_MEDIA_PATH = os.path.join(PROJECT_ROOT, 'media')

ADMIN_TOOLS_MENU = 'adminmenu.CustomMenu'

try:
    from local_settings import *
except ImportError:
    pass

VERSION = '0.1'