from os.path import join, abspath, dirname, relpath, realpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = abspath(dirname(__name__))  # .../DimeAPI
PROJECT_DIR = dirname(dirname(abspath(__file__)))  # .../DimeAPI/DimeAPI
SETTINGS_DIR = dirname(realpath(__file__))  # .../DimeAPI/DimeAPI/settings
PROJECT_NAME = relpath(PROJECT_DIR)  # DimeAPI

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DJANGO_LOG_LEVEL = DEBUG

SECURE = 'https://'
UNSECURE = 'http://'
WEBSITE_IP_ADDRESS = "127.0.0.1"
WEBSITE_HOSTNAME = 'www.dime.yogishouse.com'
WEBSITE_PORT = 10004
WEBSITE_HOSTNAME_AND_PORT = WEBSITE_HOSTNAME + ":" + str(WEBSITE_PORT)
WEBSITE_HOSTNAME_URL = UNSECURE + WEBSITE_HOSTNAME + ":" + str(WEBSITE_PORT)

DASHBOARD_IP_ADDRESS = "127.0.0.1"
DASHBOARD_HOSTNAME = 'dashboard.dime.yogishouse.com'
DASHBOARD_PORT = 10004
DASHBOARD_HOSTNAME_AND_PORT = DASHBOARD_HOSTNAME + ":" + str(DASHBOARD_PORT)
DASHBOARD_HOSTNAME_URL = UNSECURE + DASHBOARD_HOSTNAME + ":" + str(DASHBOARD_PORT)

LOCAL_HOST = 'localhost'
LOCAL_HOST_PORT = 10004
LOCAL_HOST_AND_PORT = LOCAL_HOST + str(LOCAL_HOST_PORT)

ENGINE_IP_ADDRESS = "127.0.0.1"
ENGINE_DOMAIN = 'yogishouse.com'
ENGINE_HOSTNAME = 'api.dime' + "." + ENGINE_DOMAIN
ENGINE_PORT = 10006
ENGINE_HOSTNAME_AND_PORT = ENGINE_HOSTNAME + ":" + str(ENGINE_PORT)
ENGINE_HOSTNAME_URL = SECURE + ENGINE_HOSTNAME + ":" + str(ENGINE_PORT)

ALLOWED_HOSTS = [ENGINE_HOSTNAME]

# Application definition

INSTALLED_APPS = [
    'DimeAPI',
    'reset_migrations',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'web3',
    'django_user_agents',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 'django_otp.middleware.OTPMiddleware',

SECURE_HSTS_INCLUDE_SUBDOMAINS = 'True'
TWO_FACTOR_PATCH_ADMIN = False
LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = 'two_factor:profile'

# this one is optional

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

USER_AGENTS_CACHE = 'default'
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = True
CSRF_COOKIE_DOMAIN = '.' + ENGINE_DOMAIN
CSRF_TRUSTED_ORIGINS = (
    ENGINE_HOSTNAME,
    WEBSITE_HOSTNAME,
    DASHBOARD_HOSTNAME
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

INTERNAL_IPS = [
    ENGINE_IP_ADDRESS,
    WEBSITE_IP_ADDRESS,
    DASHBOARD_IP_ADDRESS
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(asctime)s:%(module)s:%(name)s:%(process)d:%(thread)d:%(message)s'
        },
        'simple': {
            'format': '%(levelname)s:%(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': join(PROJECT_DIR, 'log', 'debug.log'),
            'formatter': 'verbose',
        },
        'request_handler': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(PROJECT_DIR, 'log', 'debug-request.log'),
            'formatter': 'verbose',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

CORS_ORIGIN_WHITELIST = (
    LOCAL_HOST_AND_PORT,
    WEBSITE_HOSTNAME_AND_PORT,
    DASHBOARD_HOSTNAME_AND_PORT,
    ENGINE_HOSTNAME_AND_PORT
)

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'Access-Control-Allow-Origin',
    'accept',
    'origin',
    'accept-encoding',
    'csrftoken',
    'Redirect',
    'authorization',
    'X-CSRFToken',
    'X-CSRF-TOKEN'
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': 'dimeapi-dev',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
        'PORT': 3306,
        'OPTIONS': {
            'read_default_file': join('C:/', 'ProgramData/', 'MySQL', 'MySQL Server 5.7/', 'my.ini'),
        },
    },
    'coins': {
        'NAME': 'dimecoins-dev',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
        'PORT': 3306,
        'OPTIONS': {
            'read_default_file': join('C:/', 'ProgramData/', 'MySQL', 'MySQL Server 5.7/', 'my.ini'),
        },
    }
}


OAUTH2_PROVIDER = {
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication'
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}

# 'DEFAULT_FILTER_BACKENDS':  ('rest_framework.filters.DjangoFilterBackend',),

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'DimeAPI.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
STATIC_URL = '/static/'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

GEOIP_PATH = join(PROJECT_DIR, 'assets')
GOOGLE_MAPS_API_KEY = 'AIzaSyCdQe4RDmD4pYXiYJihZf90s-8tdQX4EwU'

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = False

EMAIL_SERVER = {
    'HOST': 'smtp.mailtrap.io',
    'USER': 'c8bed2fa6aecd1',
    'PASSWORD': '4eaf0f51577f20',
    'PORT': 2525
}
PASSWORD_LENGTH = 20
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'c8bed2fa6aecd1'
EMAIL_HOST_PASSWORD = '4eaf0f51577f20'
EMAIL_TIMEOUT = 10
EMAIL_LENGTH = 100

EMAIL_TEMPLATE_DIR = join(PROJECT_NAME, 'EmailTemplates')
EMAIL_FROM_DOMAIN = 'yogishouse.com'
EMAIL_LOGIN_URL = WEBSITE_HOSTNAME_URL + '/auth/login'
EMAIL_VERIFY_ACCOUNT_URL = WEBSITE_HOSTNAME_URL + '/register/verify/'
EMAIL_VERIFY_TRACK_URL = WEBSITE_HOSTNAME_URL + '/api/statistics/track.png?auth='
FORGOT_PASSWORD_URL = WEBSITE_HOSTNAME_URL + '/account/forgotPassword/'
PASSWORD_RESET_URL = WEBSITE_HOSTNAME_URL + '/account/resetPassword/'
AUTHORIZATION_CODE_VALID_TIME_IN_SECONDS = 60 * 60 * 24  # 1 day
#  User Status
USER_STATUS = {
    'ACTIVE': 1,
    'INACTIVE': 2,
    'SUSPENDED': 3,
    'BLOCKED': 4,
    'VISITOR': 5
}

#  Register User Status
REGISTER_STATUS = {
    'INVALID': 1,
    'NEW': 2,
    'SENT': 3,
    'VERIFIED': 4,
    'EXPIRED': 5,
    'VERIFY': 6,
    'RECEIVED': 7
}

#  Name types
NAME_TYPE = {
    'FIRST': 1,
    'LAST': 2,
    'MAIDEN': 3,
    'MIDDLE': 4,
    'NICKNAME': 5,
    'SALUTATION': 6,
    'SUFFIX': 7
}

#  Notification types
NOTIFICATION_TYPE = {
    'EMAIL': 1,
    'TEXT': 2,
    'PHONE': 3
}

#  Email Address Status
EMAIL_ADDRESS_STATUS = {
    'ACTIVE': 1,
    'INACTIVE': 2,
    'SUSPENDED': 3,
    'BLOCKED': 4,
    'EXISTS': 5,
    'NOTFOUND': 6
}

#  Password Status
PASSWORD_STATUS = {
    'ACTIVE': 1,
    'INACTIVE': 2,
    'USED': 3,
    'FAILED': 4,
    'SUCCESS': 5
}

#  Password Reset Status
PASSWORD_RESET_STATUS = {
    'ACTIVE': 1,
    'EXPIRED': 2,
    'CLICKED': 3,
    'FINISHED': 4
}

#  Notification Status
NOTIFICATION_STATUS = {
    'READY': 1,
    'QUEUED': 2,
    'SENT': 3,
    'FAILED': 4
}
#  Email Templates
EMAIL_TEMPLATE = {
    'VERIFY': 1,
    'WELCOME': 2,
    'FORGOT': 3,
    'RESET': 4
}

XCHANGE = {
    'CRYPTO_COMPARE': 1,
    'GDAX': 2,
    'COINBASE': 3,
    'COINDESK': 4,
    'COIN_MARKET_CAP': 5
}
IPFS_LENGTH = 64
ADDRESS_LENGTH = 42
TRANSACTION_HASH_LENGTH = 66
URL_LENGTH = 100
FIRST_NAME_LENGTH = 50
LAST_NAME_LENGTH = 50
AUTHORIZATION_CODE_LENGTH = 20
CURRENCY_NAME_LENGTH = 50
COIN_SYMBOL_LENGTH = 10
COIN_NAME_LENGTH = 50
COIN_FULL_NAME_LENGTH = 100
IMAGE_DIR = "images/"
ICON_NAME_LENGTH = 30