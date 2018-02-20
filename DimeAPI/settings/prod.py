from os.path import join
from os import environ
from DimeAPI.settings.base import *

DEBUG = True
SECURE = "https://"
UNSECURE = "http://"
WEBSITE_IP_ADDRESS = "127.0.0.1"
WEBSITE_HOSTNAME = 'www-dime.yogishouse.com'
WEBSITE_PORT = 10004
WEBSITE_HOSTNAME_AND_PORT = WEBSITE_HOSTNAME + ":" + str(WEBSITE_PORT)
WEBSITE_HOSTNAME_URL = UNSECURE + WEBSITE_HOSTNAME + ":" + str(WEBSITE_PORT)

DASHBOARD_IP_ADDRESS = "127.0.0.1"
DASHBOARD_HOSTNAME = 'dashboard-dime.yogishouse.com'
DASHBOARD_PORT = 10006
DASHBOARD_HOSTNAME_AND_PORT = DASHBOARD_HOSTNAME + ":" + str(DASHBOARD_PORT)
DASHBOARD_HOSTNAME_URL = UNSECURE + DASHBOARD_HOSTNAME + ":" + str(DASHBOARD_PORT)

LOCAL_HOST = 'localhost'
LOCAL_HOST_PORT = 10004
LOCAL_HOST_AND_PORT = LOCAL_HOST + str(LOCAL_HOST_PORT)

ENGINE_IP_ADDRESS = "127.0.0.1"
ENGINE_DOMAIN = 'yogishouse.com'
ENGINE_HOSTNAME = 'api-dime' + "." + ENGINE_DOMAIN
ENGINE_PORT = 10006
ENGINE_HOSTNAME_AND_PORT = ENGINE_HOSTNAME + ":" + str(ENGINE_PORT)
ENGINE_HOSTNAME_URL = SECURE + ENGINE_HOSTNAME + ":" + str(ENGINE_PORT)


SECRET_KEY = environ['SECRET_KEY']
ROOT_URLCONF='DimeAPI.urls'
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME' : 'DimeAPI',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': join('/', 'etc/', 'mysql/', 'conf.d/', 'mysql.dimeAPI.cnf'),
        },
    }
}

try:
    from DimeAPI.settings import local
except ImportError:
    local = None
    raise ImportError('local settings import not found')
