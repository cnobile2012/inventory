import os

from dotenv import load_dotenv
from .base import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory',
        'USER': 'inventory',
        'PASSWORD': 'inventory',
        'HOST': 'localhost',
        # 'HOST': '/var/run/mysqld/mysqld.sock',
        'PORT': '3306',
        'OPTIONS': {
            # 'init_command': ("SET sql_mode='STRICT_TRANS_TABLES';"
            #                  "SET default_storage_engine=InnoDB;"),
            'charset': 'utf8'
            },
        }
    }

CACHES.update({
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'unix:///run/redis/redis-server.sock',
        'OPTIONS': {
            'db': 0,
            },
        },
    })

# KEY_PREFIX = 'stg'
# KEY_FUNCTION = 'testsite.common.caching.make_key'

# Add to the MIDDLEWARE_CLASSES here.
# MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Setup the IP address from the internal clients.
# INTERNAL_IPS = []

# Add to the INSTALLED_APPS here.
# INSTALLED_APPS.append('debug_toolbar')

ALLOWED_HOSTS = [
    '.tetrasys-design.net',
    '45.76.60.126',
    '.vultr.com',
    '.homelinux.org',
    ]

# email settings
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

LOGGING.get('loggers', {}).get('django.request', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('inventory.views', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('inventory.admin', {})['level'] = 'INFO'
LOGGING.get('loggers', {}).get('inventory.models', {})['level'] = 'INFO'
