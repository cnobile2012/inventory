# -*- coding: utf-8 -*-
#
# inventory/common/api/permissions.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission


log = logging.getLogger('api.common.permissions')
User = get_user_model()


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
            hasattr(request.user, 'role') and
            request.user.role == User.ADMINISTRATOR):
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
            hasattr(request.user, 'role') and
            request.user.role == User.PROJECT_MANAGER):
            result = True

        log.debug("IsProjectManager: %s", result)
        return result


class IsDefaultUser(BasePermission):
    """
    Allows access only to a logged in user with a profile.
    """

    def has_permission(self, request, view):
        result = False

        if (hasattr(request, 'user') and
            hasattr(request.user, 'role') and
            request.user.role == User.DEFAULT_USER):
            result = True

        log.debug("IsDefaultUser: %s", result)
        return result


class IsAnyUser(BasePermission):
    """
    Allows any registered user.
    """

    def has_permission(self, request, view):
        result = False

        if (hasattr(request, 'user') and (
            hasattr(request.user, 'role') and
            request.user.role in (User.DEFAULT_USER, User.PROJECT_MANAGER,
                                  User.ADMINISTRATOR,))):
            result = True

        log.debug("IsAnyUser: %s", result)
        return result


class IsReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS',)

    def has_permission(self, request, view):
        result = False

        if request.method in self.SAFE_METHODS:
            result = True

        return result


class IsUserActive(BasePermission):
    """
    The request is authenticated if user is active.
    """

    def has_permission(self, request, view):
        result = False

        if hasattr(request, 'user') and request.user.is_active:
            result = True

        log.debug("IsUserActive: %s", result)
        return result
