from .base import *

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

#KEY_PREFIX = 'prod'
#KEY_FUNCTION = 'testsite.common.caching.make_key'

# Where is the root of the site? This can be a root-relative URL.
SITE_URL = 'static://inventory.homelinx.org/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = os.path.join(SITE_URL, 'static/')

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
LOG_ENV = 'production'
LOG_FILE = '{}/{}-general.log'.format(LOG_DIR, LOG_ENV)
LOG_API_FILE = '{}/{}-api.log'.format(LOG_DIR, LOG_ENV)
LOG_CMD_FILE = '{}/{}-commands.log'.format(LOG_DIR, LOG_ENV)

LOGGING.get('handlers', {}).get('inventory_file', {})['filename'] = LOG_FILE
LOGGING.get('handlers', {}).get('api_file', {})['filename'] = LOG_API_FILE
LOGGING.get('handlers', {}).get('command_file', {})['filename'] = LOG_CMD_FILE
