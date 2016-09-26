# -*- coding: utf-8 -*-
#
# inventory/common/api/permissions.py
#

import logging

from django.contrib.auth import get_user_model

from rest_framework import permissions

from inventory.projects.models import Membership, Project


log = logging.getLogger('api.common.permissions')
UserModel = get_user_model()


def get_user(request):
    user = None

    if hasattr(request, 'user'):
        user = request.user

    return user


#
# User based permissions
#

class IsAdminSuperUser(permissions.BasePermission):
    """
    Allows access only to admin super users.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if user and user.is_superuser:
            result = True

        log.debug("IsAdminSuperUser: %s", result)
        return result


class IsAdministrator(permissions.BasePermission):
    """
    Allows access only to an administrator.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if user and user.role == UserModel.ADMINISTRATOR:
            result = True

        log.debug("IsAdministrator: %s", result)
        return result


class IsDefaultUser(permissions.BasePermission):
    """
    Allows access only to a logged in user with a profile.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if user and user.role == UserModel.DEFAULT_USER:
            result = True

        log.debug("IsDefaultUser: %s", result)
        return result


class IsAnyUser(permissions.BasePermission):
    """
    Allows any registered user.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        # This permission is broken
        if user and (user.is_superuser or user.role in (
            UserModel.DEFAULT_USER, UserModel.ADMINISTRATOR)):
            result = True

        log.debug("IsAnyUser: %s", result)
        return result


#
# Project based permissions
#

class BaseProjectPermission(permissions.BasePermission):
    """
    Handles project level permissions.
    """

    def has_project_permission(self, request, obj, level):
        result = False
        project = None
        user = get_user(request)

        if isinstance(obj, Project):
            project = obj
        elif hasattr(obj, 'project'):
            project = obj.project

        if not isinstance(level, (list, tuple)):
            level = (level,)

        if user and project and user.memberships.filter(
            project=project, role__in=level):
            result = True

        return result


class IsProjectOwner(BaseProjectPermission):
    """
    Allows access only to the project owner.
    """

    def has_object_permission(self, request, view, obj):
        result = self.has_project_permission(request, obj, Membership.OWNER)
        log.debug("IsProjectOwner: %s", result)
        return result


class IsProjectManager(BaseProjectPermission):
    """
    Allows access only to the project managers.
    """

    def has_object_permission(self, request, view, obj):
        result = self.has_project_permission(request, obj,
                                             Membership.PROJECT_MANAGER)
        log.debug("IsProjectManager: %s", result)
        return result


class IsProjectDefaultUser(BaseProjectPermission):
    """
    Allows access only to a logged in user with a profile.
    """

    def has_object_permission(self, request, view, obj):
        result = self.has_project_permission(request, obj,
                                             Membership.DEFAULT_USER)
        log.debug("IsProjectDefaultUser: %s", result)
        return result


class IsAnyProjectUser(BaseProjectPermission):
    """
    Allows any registered user.
    """

    def has_object_permission(self, request, view, obj):
        result = self.has_project_permission(
            request, obj, (UserModel.DEFAULT_USER,
                           UserModel.PROJECT_MANAGER,
                           UserModel.ADMINISTRATOR))
        log.debug("IsAnyProjectUser: %s", result)
        return result


#
# Miscellaneous permissions
#

class IsReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        result = False

        if request.method in permissions.SAFE_METHODS:
            result = True

        log.debug("IsReadOnly: %s", result)
        return result


class IsUserActive(permissions.BasePermission):
    """
    The request is authenticated if user is active.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if user and user.is_active:
            result = True

        log.debug("IsUserActive: %s", result)
        return result
