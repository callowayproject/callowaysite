from django.conf import settings

DEFAULT_SETTINGS = {
    'ALLOW_VERSION_OVERWRITE': False,
    'RELEASE_UPLOAD_TO': 'dists',
    'OS_NAMES': (
        ("aix", "AIX"),
        ("beos", "BeOS"),
        ("debian", "Debian Linux"),
        ("dos", "DOS"),
        ("freebsd", "FreeBSD"),
        ("hpux", "HP/UX"),
        ("mac", "Mac System x."),
        ("macos", "MacOS X"),
        ("mandrake", "Mandrake Linux"),
        ("netbsd", "NetBSD"),
        ("openbsd", "OpenBSD"),
        ("qnx", "QNX"),
        ("redhat", "RedHat Linux"),
        ("solaris", "SUN Solaris"),
        ("suse", "SuSE Linux"),
        ("yellowdog", "Yellow Dog Linux"),
    ),
    'ARCHITECTURES': (
        ("alpha", "Alpha"),
        ("hppa", "HPPA"),
        ("ix86", "Intel"),
        ("powerpc", "PowerPC"),
        ("sparc", "Sparc"),
        ("ultrasparc", "UltraSparc"),
    ),
    'DIST_FILE_TYPES': (
        ('sdist', 'Source'),
        ('bdist_dumb', '"dumb" binary'),
        ('bdist_rpm', 'RPM'),
        ('bdist_wininst', 'MS Windows installer'),
        ('bdist_egg', 'Python Egg'),
        ('bdist_dmg', 'OS X Disk Image'),
    ),
    'PYTHON_VERSIONS': (
        ('any', 'Any i.e. pure python'),
        ('2.1', '2.1'),
        ('2.2', '2.2'),
        ('2.3', '2.3'),
        ('2.4', '2.4'),
        ('2.5', '2.5'),
        ('2.6', '2.6'),
        ('2.7', '2.7'),
        ('3.0', '3.0'),
        ('3.1', '3.1'),
        ('3.2', '3.2'),
    ),
    'METADATA_FIELDS': {
        '1.0': ('platform', 'summary', 'description', 'keywords', 'home_page',
                'author', 'author_email', 'license', ),
        '1.1': ('platform', 'supported_platform', 'summary', 'description',
                'keywords', 'home_page', 'download_url', 'author', 'author_email',
                'license', 'classifier', 'requires', 'provides', 'obsoletes',),
        '1.2': ('platform', 'supported_platform', 'summary', 'description',
                'keywords', 'home_page', 'download_url', 'author', 'author_email',
                'maintainer', 'maintainer_email', 'license', 'classifier',
                'requires_dist', 'provides_dist', 'obsoletes_dist',
                'requires_python', 'requires_external', 'project_url')
    },
    'METADATA_FORMS': {
        '1.0': 'djangopypi.forms.Metadata10Form',
        '1.1': 'djangopypi.forms.Metadata11Form',
        '1.2': 'djangopypi.forms.Metadata12Form',
    },
    'FALLBACK_VIEW': 'djangopypi.views.releases.ReleaseListView',
    'ACTION_VIEWS': {
        "file_upload": 'djangopypi.views.distutils.register_or_upload',  # ``sdist`` command
        "submit": 'djangopypi.views.distutils.register_or_upload',  # ``register`` command
        "list_classifiers": 'djangopypi.views.distutils.list_classifiers',  # ``list_classifiers`` command
    },
    'XMLRPC_COMMANDS': {
        'list_packages': 'djangopypi.views.xmlrpc.list_packages',
        'package_releases': 'djangopypi.views.xmlrpc.package_releases',
        'release_urls': 'djangopypi.views.xmlrpc.release_urls',
        'release_data': 'djangopypi.views.xmlrpc.release_data',
        # 'search': xmlrpc.search, Not done yet
        # 'changelog': xmlrpc.changelog, Not done yet
        # 'ratings': xmlrpc.ratings, Not done yet
    },
    'MIRRORING': False,
    'PROXY_BASE_URL': 'http://pypi.python.org',
    'PROXY_MISSING': False,
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'DJANGOPYPI_SETTINGS', {}))

# This is disabled on pypi.python.org, can be useful if you make mistakes
if hasattr(settings, 'DJANGOPYPI_ALLOW_VERSION_OVERWRITE'):
    USER_SETTINGS['ALLOW_VERSION_OVERWRITE'] = settings.DJANGOPYPI_ALLOW_VERSION_OVERWRITE

""" The upload_to argument for the file field in releases. This can either be
a string for a path relative to your media folder or a callable. For more
information, see http://docs.djangoproject.com/ """
if hasattr(settings, 'DJANGOPYPI_RELEASE_UPLOAD_TO'):
    USER_SETTINGS['RELEASE_UPLOAD_TO'] = settings.DJANGOPYPI_RELEASE_UPLOAD_TO

if hasattr(settings, 'DJANGOPYPI_OS_NAMES'):
    USER_SETTINGS['OS_NAMES'] = settings.DJANGOPYPI_OS_NAMES

if hasattr(settings, 'DJANGOPYPI_ARCHITECTURES'):
    USER_SETTINGS['ARCHITECTURES'] = settings.DJANGOPYPI_ARCHITECTURES

if hasattr(settings, 'DJANGOPYPI_DIST_FILE_TYPES'):
    USER_SETTINGS['DIST_FILE_TYPES'] = settings.DJANGOPYPI_DIST_FILE_TYPES

if hasattr(settings, 'DJANGOPYPI_PYTHON_VERSIONS'):
    USER_SETTINGS['PYTHON_VERSIONS'] = settings.DJANGOPYPI_PYTHON_VERSIONS

if hasattr(settings, 'DJANGOPYPI_METADATA_FIELDS'):
    USER_SETTINGS['METADATA_FIELDS'] = settings.DJANGOPYPI_METADATA_FIELDS

if hasattr(settings, 'DJANGOPYPI_METADATA_FORMS'):
    USER_SETTINGS['METADATA_FORMS'] = settings.DJANGOPYPI_METADATA_FORMS

if hasattr(settings, 'DJANGOPYPI_FALLBACK_VIEW'):
    USER_SETTINGS['FALLBACK_VIEW'] = settings.DJANGOPYPI_FALLBACK_VIEW

if hasattr(settings, 'DJANGOPYPI_ACTION_VIEWS'):
    USER_SETTINGS['ACTION_VIEWS'] = settings.DJANGOPYPI_ACTION_VIEWS

if hasattr(settings, 'DJANGOPYPI_XMLRPC_COMMANDS'):
    USER_SETTINGS['XMLRPC_COMMANDS'] = settings.DJANGOPYPI_XMLRPC_COMMANDS

""" These settings enable proxying of packages that are not in the local index
to another index, http://pypi.python.org/ by default. This feature is disabled
by default and can be enabled by setting DJANGOPYPI_PROXY_MISSING to True in
your settings file. """
if hasattr(settings, 'DJANGOPYPI_PROXY_BASE_URL'):
    USER_SETTINGS['PROXY_BASE_URL'] = settings.DJANGOPYPI_PROXY_BASE_URL

if not hasattr(settings, 'DJANGOPYPI_PROXY_MISSING'):
    USER_SETTINGS['PROXY_MISSING'] = settings.DJANGOPYPI_PROXY_MISSING = False


# USER_SETTINGS['FALLBACK_VIEW'] = import_item(USER_SETTINGS['FALLBACK_VIEW'])
# USER_SETTINGS['METADATA_FORMS'] = import_item(USER_SETTINGS['METADATA_FORMS'])
# action_views_dict = {}
# for key, val in USER_SETTINGS['ACTION_VIEWS'].items():
#     action_views_dict[key] = import_item(USER_SETTINGS['ACTION_VIEWS'][key])
# USER_SETTINGS['ACTION_VIEWS'] = action_views_dict
# xmlrpc_commands = {}
# for key, val in USER_SETTINGS['XMLRPC_COMMANDS'].items():
#     xmlrpc_commands[key] = import_item(USER_SETTINGS['XMLRPC_COMMANDS'][key])
# USER_SETTINGS['XMLRPC_COMMANDS'] = xmlrpc_commands

globals().update(USER_SETTINGS)
