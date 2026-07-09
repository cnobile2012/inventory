import os

from dotenv import load_dotenv
from .base import *
from pathlib import Path
# from inventory.setupenv import getLogger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
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
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': ("SET sql_mode='STRICT_TRANS_TABLES';"
                             "SET default_storage_engine=INNODB;"),
            'charset': 'utf8'
            },
        }
    }

CACHES.update({
    'default': {
        'BACKEND': 'redis_cache.RedisDummyCache',
        # 'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'unix:///run/redis/redis-server.sock',
        'OPTIONS': {
            'db': 0,
            },
        },
    })

KEY_PREFIX = 'dev'
# KEY_FUNCTION = 'inventory.common.caching.make_key'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, 'dev/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
# STATIC_URL = os.path.join(SITE_URL, 'dev/')

###############################################################################
# Django Debug Toolbar
###############################################################################
# Add to the MIDDLEWARE_CLASSES here.
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Add to the INSTALLED_APPS here.
INSTALLED_APPS.append('debug_toolbar')

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Setup the IP address from the internal clients.
INTERNAL_IPS = ['127.0.0.1', '192.168.1.0/24']

# If it were working, set it to follow redirects by default.
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    }

ALLOWED_HOSTS = [
    'localhost',
    '192.168.1.109',
    '172.220.244.125',
    'inventory.homelinux.org',
    'tetrasys.homelinux.org',
    ]

# Email settings
load_dotenv()
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Document Email Contacts
DOC_CONTACTS = (
    )

LOGGING.get('loggers', {}).get('django.request', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('inventory.views', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('inventory.admin', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('inventory.models', {})['level'] = 'DEBUG'

# log = getLogger()
# log.debug("EMAIL_HOST_USER: %s, EMAIL_HOST_PASSWORD: %s, BASE_DIR: %s",
#           EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, BASE_DIR)
