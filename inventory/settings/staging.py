from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inventory',
        'USER': 'inventory',
        'PASSWORD': 'inventory',
        'HOST': 'localhost',
        'PORT': '',
        }
    }


## KEY_PREFIX = 'stg'
## #KEY_FUNCTION = 'testsite.common.caching.make_key'

# Add to the INSTALLED_APPS here.
#INSTALLED_APPS.append('debug_toolbar')

ALLOWED_HOSTS = [
    '.tetrasys-design.net',
    '45.76.60.126',
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
LOG_CMD_FILE = '{}/{}-commands.log'.format(LOG_DIR, LOG_ENV)

LOGGING.get('handlers', {}).get('inventory_file', {})['filename'] = LOG_FILE
LOGGING.get('handlers', {}).get('api_file', {})['filename'] = LOG_API_FILE
LOGGING.get('handlers', {}).get('command_file', {})['filename'] = LOG_CMD_FILE

LOGGING.get('loggers', {}).get('inventory', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('api', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('commands', {})['level'] = 'DEBUG'
