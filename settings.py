# Django settings for project project.

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('coordt', 'coreyoordt@gmail.com'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'webmaster@callowayproject.com'
SERVER_EMAIL = 'webmaster@callowayproject.com'

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SITE_ID = 1

ROOT_URLCONF = 'urls'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

try:
    from local_settings import MEDIA_URL_PREFIX
except ImportError:
    MEDIA_URL_PREFIX = "/media/"
try:
    from local_settings import MEDIA_ROOT_PREFIX
except ImportError:
    MEDIA_ROOT_PREFIX = os.path.join(PROJECT_ROOT, 'media')
try:
    from local_settings import MEDIA_ROOT
except ImportError:
    MEDIA_ROOT = os.path.join(MEDIA_ROOT_PREFIX, 'uploads')
try:
    from local_settings import STATIC_ROOT
except ImportError:
    STATIC_ROOT = os.path.join(MEDIA_ROOT_PREFIX, 'static')

MEDIA_URL = '%suploads/' % MEDIA_URL_PREFIX
STATIC_URL = "%sstatic/" % MEDIA_URL_PREFIX
ADMIN_MEDIA_PREFIX = "%sadmin/" % STATIC_URL

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

AUTH_PROFILE_MODULE = ''

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

#CACHE_BACKEND = 'versionedcache.backend://localhost:11211/'
CACHE_BACKEND = 'dummy:///'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'robots',
    'djangopypi',
    'projects',
    'analytical',
    'south',
    'mystaff',
)

ADMIN_TOOLS_THEMING_CSS = 'admin/css/theming.css'

ADMIN_TOOLS_MENU = 'adminmenu.CustomMenu'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

try:
    from local_settings import *
except ImportError:
    pass
