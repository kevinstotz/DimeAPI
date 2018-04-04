from DimeAPI.settings.base import *


SECRET_KEY = environ['SECRET_KEY']
ROOT_URLCONF = 'DimeAPI.urls'
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME': 'DimeAPI',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': join('/', 'etc/', 'mysql/', 'conf.d/', 'mysql.dimeAPI.cnf'),
        },

    },
    'coins': {
        'NAME': 'YogisCoin',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': join('/', 'etc/', 'mysql/', 'conf.d/', 'mysql.dimeCoins.cnf'),
        },
    },
}

try:
    from .local import *
except ImportError:
    local = None
    raise ImportError('local settings import not found')
