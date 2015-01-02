#
# app.wsgi
#
# mod_wsgi hook file
#
# SVN/CVS keywords
#------------------------------
# $Author: cnobile $
# $Date: 2014-01-16 21:17:19 -0500 (Thu, 16 Jan 2014) $
# $Revision: 87 $
#------------------------------
#
# Configure values assuming the following.
#
# |-- Django-x.x.x  (BASE_DJANGO_PATH)
# `-- apps  (BASE_PACKAGE_PATH)
#     |-- site-packages  (SITE_PACKAGES)
#     `-- <project>  (BASE_SITE_PATH)
#         |-- db
#         |-- django  (symlink to ../../Django-x.x.x/django)
#         |-- logs
#         |-- apache  (APACHE_CONF)
#         |   |-- app.wsgi
#         |   `-- <project>.conf
#         `-- <site>
#             |--__init__.py
#             |--settings.py
#             |--setupenv.py
#             |--urls.py
#             '-- <app>
#                 |--views.py
#                 |--models.py
#                 `--tests.py
#

import os, sys, pprint

SITE = "inventory"
APACHE_CONF = os.path.dirname(__file__)
BASE_SITE_PATH = os.path.abspath(os.path.join(APACHE_CONF, '..'))
BASE_PACKAGE_PATH = os.path.abspath(os.path.join(BASE_SITE_PATH, '..'))

# DO NOT EDIT BELOW THIS LINE
SITE_PACKAGES = os.path.join(BASE_PACKAGE_PATH, 'site-packages')

# Add to the path the application, 3rd party apps, and django itself.
not sys.path.count(BASE_SITE_PATH) and sys.path.insert(0, BASE_SITE_PATH)
not sys.path.count(SITE_PACKAGES) and sys.path.insert(0, SITE_PACKAGES)

# Dynamic module import function.
def importMods(path, fromList, asList=None):
    modules = __import__(path, globals(), locals(), fromList, -1)
    if not asList: asList = fromList
    if len(asList) != len(fromList): raise ValueError('asList != fromList')

    for asMod, mod in zip(asList, fromList):
        exec "importMods.func_globals['%s'] = modules.%s" % (asMod, mod)

# Import and setup logger.
importPath = '%s.setupenv' % SITE
importMods(importPath, ['initializeLogging', 'getLogger', 'LOGGER_NAME'])

initializeLogging()
log = getLogger()
log.debug("Done setting up logger: %s", LOGGER_NAME)
log.debug("os.path: %s", sys.path)
# End setup of logger.

#from django.core.handlers import wsgi
from django.core.wsgi import get_wsgi_application
#import MySQLdb

class LoggingMiddleware:
    def __init__(self, application):
        self.__application = application

    def __call__(self, environ, start_response):
        errors = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errors)

        def _start_response(status, headers):
            pprint.pprint(('RESPONSE', status, headers), stream=errors)
            return start_response(status, headers)

        return self.__application(environ, _start_response)

os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % SITE
log.debug("DJANGO_SETTINGS_MODULE: %s", os.getenv('DJANGO_SETTINGS_MODULE'))
#application = wsgi.WSGIHandler()
application = get_wsgi_application()

#application = LoggingMiddleware(application)
