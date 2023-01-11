from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory',
        'USER': 'inventory',
        'PASSWORD': 'inventory',
        'HOST': 'localhost',
        #'HOST': '/var/run/mysqld/mysqld.sock',
        'PORT': '3306',
         'OPTIONS': {
            #'init_command': ("SET sql_mode='STRICT_TRANS_TABLES';"
            #                 "SET default_storage_engine=InnoDB;"),
            'charset': 'utf8'
            },
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
    '45.76.60.126',
    '.vultr.com',
    ]

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
