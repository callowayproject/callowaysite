from django.conf import settings
from django.core.files.storage import get_storage_class

DEFAULT_SETTINGS = {
    'LOGO_STORAGE': settings.DEFAULT_FILE_STORAGE,
    'PROJECT_TYPES': enumerate((
        'Django Content App', 
        'Django Decorator App',
        'Django Utility',
        'Python App',
        'Web Site',
    )),
    'STATUSES': enumerate((
        'Live',
        'Archived'
    )),
    
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'PROJECTS_SETTINGS', {}))

USER_SETTINGS['LOGO_STORAGE'] = get_storage_class(USER_SETTINGS['LOGO_STORAGE'])

globals().update(USER_SETTINGS)