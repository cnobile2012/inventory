# -*- coding: utf-8 -*-
#
# inventory/common/api/permissions.py
#

import logging

from rest_framework.permissions import BasePermission


log = logging.getLogger('api.common.permissions')


class IsAdminSuperUser(BasePermission):
    """
    Allows access only to admin super users.
    """

    def has_permission(self, request, view):
        result = False

        if request.user and request.user.is_superuser:
            result = True

        log.debug("IsAdminSuperUser: %s", result)
        return result


class IsAdministrator(BasePermission):
    """
    Allows access only to an administrator.
    """

    def has_permission(self, request, view):
        result = False

        if (hasattr(request, 'user') and
            hasattr(request.user, 'userprofile') and
            request.user.userprofile.role == UserProfile.ADMINISTRATOR):
            result = True

        log.debug("IsAdministrator: %s", result)
        return result


class IsProjectManager(BasePermission):
    """
    Allows access only to project managers.
    """

    def has_permission(self, request, view):
        result = False

        if (hasattr(request, 'user') and
            hasattr(request.user, 'userprofile') and
            request.user.project_managers.count()):
            result = True

        log.debug("IsProjectManager: %s", result)
        return result


class IsUser(BasePermission):
    """
    Allows access only to a logged in user with a profile.
    """

    def has_permission(self, request, view):
        result = False

        if (hasattr(request, 'user') and
            hasattr(request.user, 'userprofile') and
            request.user.userprofile.role == UserProfile.DEFAULT):
            result = True

        log.debug("IsUser: %s", result)
        return result
