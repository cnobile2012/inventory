from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory',
        'USER': 'inventory',
        'PASSWORD': 'inventory',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': ("SET sql_mode='STRICT_TRANS_TABLES';"
                             "SET default_storage_engine=INNODB;"),
            'charset': 'utf8'
            },
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
