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
# |-- <project>  (BASE_SITE_PATH)
#     |-- db
#     |-- logs
#     |-- apache  (APACHE_CONF)
#     |   |-- app.wsgi
#     |   `-- <project>.conf
#     `-- <site>
#         |--__init__.py
#         |--settings.py
#         |--setupenv.py
#         |--urls.py
#         '-- <app>
#             |--admin.py
#             |--models.py
#             `--views.py
#

import os, sys

SITE = "inventory"
APACHE_CONF = os.path.dirname(__file__)
BASE_SITE_PATH = os.path.abspath(os.path.join(APACHE_CONF, '..'))

# DO NOT EDIT BELOW THIS LINE
not sys.path.count(BASE_SITE_PATH) and sys.path.insert(0, BASE_SITE_PATH)

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % SITE

application = get_wsgi_application()
