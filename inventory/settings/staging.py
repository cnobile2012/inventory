from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory',
        'USER': 'inventory',
        'PASSWORD': 'inventory',
        'HOST': '',
        'PORT': '',
        # Only Use when DB is created then comment.
        #'OPTIONS': {'init_command': 'SET storage_engine=InnoDB;',
        #            'charset': 'utf8'},
        }
    }


## KEY_PREFIX = 'stg'
## #KEY_FUNCTION = 'testsite.common.caching.make_key'

# Add to the MIDDLEWARE_CLASSES here.
#MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Setup the IP address from the internal clients.
#INTERNAL_IPS = IPList(['127.0.0.1', '10.10.10.1', '192.168.1.0/24'])

# Add to the INSTALLED_APPS here.
#INSTALLED_APPS.append('debug_toolbar')

ALLOWED_HOSTS = [
    '.tetrasys-design.net',
    '162.209.110.28',
    ]

# email settings
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_REPLY_TO = 'donotreply@'

# Document Email Contacts
DOC_CONTACTS = (
    )

# Logging
LOG_ENV = 'stage'
LOG_FILE = '{}/{}-general.log'.format(LOG_DIR, LOG_ENV)
LOG_API_FILE = '{}/{}-api.log'.format(LOG_DIR, LOG_ENV)

LOGGING.get('handlers', {}).get('inventory_file', {})['filename'] = LOG_FILE
LOGGING.get('handlers', {}).get('api_file', {})['filename'] = LOG_API_FILE

LOGGING.get('loggers', {}).get('inventory', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('api', {})['level'] = 'INFO'
