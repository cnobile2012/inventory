import sys

# Uncomment this line when testing changes to dcolumn.
#sys.path.insert(0, '/home/cnobile/src/django/dcolumn')

from inventory.common.utils import IPList

from .base import *

DEBUG = True

ALLOWED_HOSTS.append('localhost')
ALLOWED_HOSTS.append('192.168.1.107')

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or
        # 'oracle'. Prefix all with 'django.db.backends.'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Or path to database file if using sqlite3.
        'NAME': 'inventory',
        # Not used with sqlite3.
        'USER': 'inventory',
        # Not used with sqlite3.
        'PASSWORD': 'inventory',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': 'localhost',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
        }
    }

#KEY_PREFIX = 'dev'
#KEY_FUNCTION = 'inventory.common.caching.make_key'

# Current site schema, URL and port.
SITE_SCHEMA = 'http://'
SITE_DOMAIN = 'localhost'
SITE_PORT = 8000

# Add to the MIDDLEWARE here.
MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

CACHES.update({
    'default': {
        'BACKEND': 'redis_cache.RedisDummyCache',
        #'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '/var/run/redis/redis-server.sock',
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': 2,
            },
        },
    })

# Add to the INSTALLED_APPS here.
INSTALLED_APPS.append('debug_toolbar')
INSTALLED_APPS.append('django_extensions')

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Setup the IP address from the internal clients.
INTERNAL_IPS = IPList(['127.0.0.1', '192.168.1.0/24'])

# If it were working, set it to follow redirects by default.
DEBUG_TOOLBAR_CONFIG = {
    }

# django-compressor
COMPRESS_ENABLED = False
# End django-compressor

# email settings
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_REPLY_TO = 'donotreply@'

# Document Email Contacts
DOC_CONTACTS = (
    )

# Logging
LOG_ENV = 'development'
LOG_FILE = '{}/{}-general.log'.format(LOG_DIR, LOG_ENV)
LOG_API_FILE = '{}/{}-api.log'.format(LOG_DIR, LOG_ENV)
LOG_CMD_FILE = '{}/{}-commands.log'.format(LOG_DIR, LOG_ENV)

LOGGING.get('handlers', {}).get('inventory_file', {})['filename'] = LOG_FILE
LOGGING.get('handlers', {}).get('api_file', {})['filename'] = LOG_API_FILE
LOGGING.get('handlers', {}).get('command_file', {})['filename'] = LOG_CMD_FILE

LOGGING.get('loggers', {}).get('inventory', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('api', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('commands', {})['level'] = 'DEBUG'
