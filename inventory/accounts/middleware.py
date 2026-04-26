# -*- coding: utf-8 -*-
#
# realm/common/middleware.py
#

from django.contrib.auth.middleware import RemoteUserMiddleware


class PingRemoteMiddleware(RemoteUserMiddleware):
    header = 'HTTP_REMOTE_USER'
