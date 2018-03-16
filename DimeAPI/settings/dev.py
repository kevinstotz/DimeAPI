
from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'NAME' : "dimeapi-dev",
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': join('/', 'etc/', 'mysql/', 'conf.d/', 'mysql.dimeApi.cnf'),
        },
    },
    'coins': {
        'NAME': 'dimecoins-dev',
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
