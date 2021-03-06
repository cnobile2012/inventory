from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inventory',
        'USER': 'inventory',
        'PASSWORD': 'inventory',
        'HOST': 'localhost',
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

ALLOWED_HOSTS = [
    '127.0.0.1'
    ]

# Current site schema, URL and port.
SITE_SCHEMA = 'http://'
SITE_DOMAIN = 'localhost'
SITE_PORT = 8000

# email settings
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_REPLY_TO = 'donotreply@'

# Logging
LOG_ENV = 'travis'
LOG_FILE = '{}/{}-general.log'.format(LOG_DIR, LOG_ENV)
LOG_API_FILE = '{}/{}-api.log'.format(LOG_DIR, LOG_ENV)
LOG_CMD_FILE = '{}/{}-commands.log'.format(LOG_DIR, LOG_ENV)

LOGGING.get('handlers', {}).get('inventory_file', {})['filename'] = LOG_FILE
LOGGING.get('handlers', {}).get('api_file', {})['filename'] = LOG_API_FILE
LOGGING.get('handlers', {}).get('command_file', {})['filename'] = LOG_CMD_FILE

LOGGING.get('loggers', {}).get('inventory', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('api', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('commands', {})['level'] = 'DEBUG'
