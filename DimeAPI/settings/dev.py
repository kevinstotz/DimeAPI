from DimeAPI.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'NAME' : "dimeapi-dev",
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': join('C:/', 'ProgramData/', 'MySQL', 'MySQL Server 5.7/', 'my.ini'),
        },
    }
}

try:
    from DimeAPI.settings.local import *
except ImportError:
    local = None
    raise ImportError('local settings import not found')
