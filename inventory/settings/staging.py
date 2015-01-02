from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testsite_stg',
        'USER': 'testsite_stg',
        'PASSWORD': 'testsite_stg',
        'HOST': '',
        'PORT': '',
        }
    }


## CACHES = {
##     'default': {
##         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
##         'LOCATION': '127.0.0.1:11211',
##         },
##     }

## KEY_PREFIX = 'stg'
## #KEY_FUNCTION = 'testsite.common.caching.make_key'

# Add to the MIDDLEWARE_CLASSES here.
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Setup the IP address from the internal clients.
INTERNAL_IPS = IPList(['127.0.0.1', '10.10.10.1', '192.168.1.0/24'])

# Add to the INSTALLED_APPS here.
INSTALLED_APPS.append('debug_toolbar')

# email settings
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_REPLY_TO = 'donotreply@'

# Document Email Contacts
DOC_CONTACTS = (
    )

LOGGING.get('loggers', {}).get('django.request', {})['level'] = 'INFO'
#LOGGING.get('loggers', {}).get('search.views', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('testsite.views', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('testsite.admin', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('testsite.models', {})['level'] = 'INFO'
