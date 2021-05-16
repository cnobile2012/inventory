# -*- coding: utf-8 -*-
#
# base.py
#
# Django settings for inventory project.
#

import os
import sys

from dcolumn.dcolumns.manager import dcolumn_manager

DEBUG = False

ADMINS = (
    ('Sysadmins', 'carl.nobile@gmail.com'),
    )

ALLOWED_HOSTS = []

SITE_ID = 1

# Where is the 'website' directory with settings dir, apps, urls.py, etc. are.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set the type of auto PK that is generated.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Where is the root of the site? This can be a root-relative URL.
SITE_URL = '/'

# Current site schema, URL and port.
SITE_SCHEMA = 'https://'
SITE_DOMAIN = 'inventory.tetrasys-design.net'
SITE_PORT = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

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
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media/'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = SITE_URL + 'media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static/'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = SITE_URL + 'static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(BASE_DIR, 'dev/')),
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bjwykl6a7km26!0bsx%$v8g#s=+s5-(v2&d0^r8tl5++4ip$u4'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    #'guardian.backends.ObjectPermissionBackend',
    )

# Guardian requirement
ANONYMOUS_USER_ID = -1

MIDDLEWARE = [
    # UpdateCacheMiddleware must be first on the list
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # This must be last
    ]

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '/var/run/redis/redis.sock',
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': 2,
            },
        },
    }

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

ROOT_URLCONF = 'inventory.urls'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'inventory.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Plugins
    'compressor',
    'dcolumn.dcolumns',
    'rest_framework',
    'django_filters',
    #'guardian',

    # Apps
    'inventory.accounts',
    'inventory.categories',
    'inventory.invoices',
    'inventory.locations',
    'inventory.projects',
    'inventory.regions',
    'inventory.sites',
    'inventory.suppliers',
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                ],
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                #'django.template.loaders.eggs.Loader',
                ],
            },
        },
    ]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': ('django.contrib.auth.password_validation.'
              'UserAttributeSimilarityValidator'),
     },
    {'NAME': ('django.contrib.auth.password_validation.'
              'MinimumLengthValidator'),
     },
    {'NAME': ('django.contrib.auth.password_validation.'
              'CommonPasswordValidator'),
     },
    {'NAME': ('django.contrib.auth.password_validation.'
              'NumericPasswordValidator'),
     },
    ]

# Django auth backends.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework_xml.parsers.XMLParser',
        #'rest_framework_yaml.parsers.YAMLParser',
        ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        #'rest_framework_yaml.renderers.YAMLRenderer',
        ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
        ),
    'DEFAULT_VERSIONING_CLASS': ('inventory.common.api.versioning.'
                                 'AcceptHeaderVersioning'),
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': ('inventory.common.api.negotiation.'
                                          'ContentNegotiation'),
    'DEFAULT_VERSION': 1.0,
    'ALLOWED_VERSIONS': (1.0,),
    'VERSION_PARAM': 'ver',
    'URL_FIELD_NAME': 'href',
    'DATETIME_FORMAT': None,
    'DATE_FORMAT': None,
    'TIME_FORMAT': None,
    }

# Change the URL below to your login path.
LOGIN_URL = "/admin/"

dcolumn_manager.register_css_containers(
       (('location_01', 'location-01'),
        ('location_02', 'location-02'),
        ('location_03', 'location-03'),
        ('location_04', 'location-04'),
        ('location_05', 'location-05'),
        ('location_06', 'location-06'),
        ('location_07', 'location-07'),
        ('location_08', 'location-08'),
        ('location_09', 'location-09'),
        ('location_10', 'location-10'),
        ('location_11', 'location-11'),
        ))

# django-compressor
COMPRESS_ENABLED = True
# End django-compressor

# A sample logging configuration. The only tangible logging performed by this
# configuration is to send an email to the site admins on every HTTP 500 error
# when DEBUG=False. See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'logs'))
not os.path.isdir(LOG_DIR) and os.mkdir(LOG_DIR, 0o0775)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ("%(asctime)s %(levelname)s %(name)s %(funcName)s "
                       "[line:%(lineno)d] %(message)s"),
            },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s',
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
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': 'True',
            },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'inventory_file': {
            'class': 'inventory.common.loghandlers.DeferredRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': '/dev/null',
            'maxBytes': 50000000,  # 50 Meg bytes
            'backupCount': 5,
            },
        'api_file': {
            'class': 'inventory.common.loghandlers.DeferredRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': '/dev/null',
            'maxBytes': 50000000,  # 50 Meg bytes
            'backupCount': 5,
            },
        'command_file': {
            'class': 'inventory.common.loghandlers.DeferredRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': '/dev/null',
            'maxBytes': 50000000,  # 50 Meg bytes
            'backupCount': 5,
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'inventory': {
            'handlers': ('inventory_file', 'mail_admins',),
            'level': 'ERROR',
            'propagate': True,
            },
        'api': {
            'handlers': ('api_file', 'mail_admins',),
            'level': 'ERROR',
            'propagate': True,
            },
        'commands': {
            'handlers': ('command_file', 'mail_admins',),
            'level': 'ERROR',
            'propagate': True,
            },
        'tests': {
            'handlers': ('inventory_file', 'mail_admins',),
            'level': 'DEBUG',
            'propagate': True,
            },
        }
    }
