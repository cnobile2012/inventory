from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory',
        'USER': 'inventory',
        'PASSWORD': 'inventory',
        'HOST': '',
        'PORT': '',
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

# email settings
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_REPLY_TO = 'donotreply@'

# Document Email Contacts
DOC_CONTACTS = (
    )

LOGGING.get('loggers', {}).get('django.request', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('inventory.views', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('inventory.admin', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('inventory.models', {})['level'] = 'INFO'
