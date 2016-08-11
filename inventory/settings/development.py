from .base import *


DEBUG = True

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or
        # 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
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
        'OPTIONS': {
            'init_command': ("SET sql_mode='STRICT_TRANS_TABLES';"
                             "SET default_storage_engine=INNODB;"),
            'charset': 'utf8'
            },
        }
    }

#KEY_PREFIX = 'dev'
#KEY_FUNCTION = 'inventory.common.caching.make_key'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(BASE_DIR, 'dev/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = os.path.join(SITE_URL, 'dev/')

###############################################################################
# Django Debug Toolbar
###############################################################################
# Add to the MIDDLEWARE_CLASSES here.
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Add to the INSTALLED_APPS here.
INSTALLED_APPS.append('debug_toolbar')

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Setup the IP address from the internal clients.
#INTERNAL_IPS = IPList(['127.0.0.1', '10.10.10.1', '192.168.1.0/24'])

# If it were working, set it to follow redirects by default.
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    }

# email settings
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_REPLY_TO = 'donotreply@'

# Document Email Contacts
DOC_CONTACTS = (
    )

LOGGING.get('loggers', {}).get('django.request', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('inventory.views', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('inventory.admin', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('inventory.models', {})['level'] = 'DEBUG'
