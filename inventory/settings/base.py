#
# base.py
#
# Django settings for inventory project.
#
# SVN keywords
#------------------------------
# $Author: $
# $Date: $
# $Revision: $

import os
from inventory.setupenv import *
from inventory.apps.items.settings import *
from inventory.apps.login.settings import *
from django.template import add_to_builtins


class IPList(list):

    def __init__(self, ips):
        try:
            #http://software.inl.fr/trac/wiki/IPy
            #ubuntu: apt-get install python-ipy
            from IPy import IP
            for ip in ips:
                self.append(IP(ip))
        except ImportError:
            pass

    def __contains__(self, ip):
        try:
            for net in self:
                if ip in net:
                    return True
        except:
            pass
        return False


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sysadmins', 'sysadminclient@capstrat.com'),
    )

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

SITE_NAME = "TetraSys Inventory"

# Where is the 'website' directory with settings dir, apps, urls.py, etc. are.
SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Where is the root of the site? This can be a root-relative URL.
SITE_URL = '/'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = os.path.join(SITE_URL, 'media/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = os.path.join(SITE_URL, 'static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'dev/'),
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bjwykl6a7km26!0bsx%$v8g#s=+s5-(v2&d0^r8tl5++4ip$u4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = [
    # UpdateCacheMiddleware must be first on the list
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # This must be last
    ]

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '/var/run/redis/redis.sock',
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

###############################################################################
# Django Debug Toolbar
###############################################################################

# Disable it!
INTERNAL_IPS = ()

# If it were working, set it to follow redirects by default.
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    }

ROOT_URLCONF = 'inventory.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'inventory.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
    )

TEMPLATE_TAGS = (
    'inventory.tags.breadcrumbs',
    'inventory.tags.utilitylib',
)

try:
    for lib in TEMPLATE_TAGS:
        add_to_builtins(lib)
except AttributeError:
    pass

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory.apps.items',
    'inventory.apps.regions',
    'inventory.apps.login',
    'inventory.apps.reports',
    'inventory.apps.maintenance',
    ]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOG_DIR = os.path.abspath(os.path.join(SITE_ROOT, '..', 'logs'))
not os.path.isdir(LOG_DIR) and os.mkdir(LOG_DIR, 0775)
LOG_ENV = "base"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(asctime)s %(levelname)s %(module)s %(funcName)s "
            "[line:%(lineno)d] %(message)s"
            },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
            },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
            },
        },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
            },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'inventory_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': '%s/%s-search.log' % (LOG_DIR, LOG_ENV),
            'maxBytes': 50000000,  # 50 Meg bytes
            'backupCount': 5,
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'inventory.views': {
            'handlers': ('inventory_file', 'console', 'mail_admins',),
            'level': 'ERROR',
            'propagate': True,
            },
        'inventory.models': {
            'handlers': ('inventory_file', 'console', 'mail_admins',),
            'level': 'ERROR',
            'propagate': True,
            },
        'inventory.admin': {
            'handlers': ('inventory_file', 'console', 'mail_admins',),
            'level': 'ERROR',
            'propagate': True,
            },
        }
    }
