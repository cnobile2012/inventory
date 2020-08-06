# -*- coding: utf-8 -*-
#
# inventory/common/api/permissions.py
#
"""
Authorization permissions.
"""
__docformat__ = "restructuredtext en"

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

        log.debug("IsAdminSuperUser: %s, method: %s, user: %s, view: %s",
                  result, request.method, user, view.__class__.__name__)
        return result


class IsAdministrator(permissions.BasePermission):
    """
    Allows access only to an administrator.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if (user and hasattr(user, 'role') and
            user.role == UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]):
            result = True

        log.debug("IsAdministrator: %s, method: %s, user: %s, view: %s",
                  result, request.method, user, view.__class__.__name__)
        return result


class IsDefaultUser(permissions.BasePermission):
    """
    Allows access only to a logged in user with a profile.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if (user and hasattr(user, 'role') and
            user.role == UserModel.ROLE_MAP[UserModel.DEFAULT_USER]):
            result = True

        log.debug("IsDefaultUser: %s, method: %s, user: %s, view: %s",
                  result, request.method, user, view.__class__.__name__)
        return result


class IsAnyUser(permissions.BasePermission):
    """
    Allows any registered user.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        # This permission is broken
        if (user and hasattr(user, 'role') and
            (user.is_superuser or user.role in (UserModel.ROLE_MAP_REV))):
            result = True

        log.debug("IsAnyUser: %s, method: %s, user: %s, view: %s",
                  result, request.method, user, view.__class__.__name__)
        return result


#
# Project based permissions
#

class BaseProjectPermission(permissions.BasePermission):
    """
    Handles project level permissions.
    """

    def has_project_permission(self, request, level):
        result = False
        user = get_user(request)

        if user:
            if not isinstance(level, (list, tuple)):
                level = (level,)

            if (hasattr(user, 'memberships') and
                user.memberships.filter(role__in=level).count()):
                result = True

        return result

    def has_project_object_permission(self, request, obj, level):
        result = False
        project = None
        user = get_user(request)

        if user:
            if isinstance(obj, Project):
                project = obj
            elif hasattr(obj, 'project'):
                project = obj.project
            elif hasattr(obj, 'memberships'):
                members = obj.memberships.filter(user=user)
                if members: project = members[0].project
                #print('POOP', members, project)

            if project:
                if not isinstance(level, (list, tuple)):
                    level = (level,)

                if user.memberships.filter(project=project,
                                           role__in=level).count():
                    result = True

        return result


class IsProjectOwner(BaseProjectPermission):
    """
    Allows access only to the project owner.
    """

    def has_permission(self, request, view):
        result = self.has_project_permission(request, Membership.PROJECT_OWNER)
        log.debug("IsProjectOwner: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
        return result

    def has_object_permission(self, request, view, obj):
        result = self.has_project_object_permission(
            request, obj, Membership.PROJECT_OWNER)
        log.debug("IsProjectOwner: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
        return result


class IsProjectManager(BaseProjectPermission):
    """
    Allows access only to the project managers.
    """

    def has_permission(self, request, view):
        result = self.has_project_permission(
            request, Membership.PROJECT_MANAGER)
        log.debug("IsProjectManager: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
        return result

    def has_object_permission(self, request, view, obj):
        result = self.has_project_object_permission(
            request, obj, Membership.PROJECT_MANAGER)
        log.debug("IsProjectManager: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
        return result


class IsProjectDefaultUser(BaseProjectPermission):
    """
    Allows access only to a logged in user with a profile.
    """

    def has_permission(self, request, view):
        result = self.has_project_permission(
            request, Membership.PROJECT_USER)
        log.debug("IsProjectDefaultUser: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
        return result

    def has_object_permission(self, request, view, obj):
        result = self.has_project_object_permission(
            request, obj, Membership.PROJECT_USER)
        log.debug("IsProjectDefaultUser: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
        return result


class IsAnyProjectUser(BaseProjectPermission):
    """
    Allows any registered user.
    """

    def has_permission(self, request, view):
        result = self.has_project_permission(
            request, list(Membership.ROLE_MAP))
        log.debug("IsAnyProjectUser: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
        return result

    def has_object_permission(self, request, view, obj):
        result = self.has_project_object_permission(
            request, obj, list(Membership.ROLE_MAP))
        log.debug("IsAnyProjectUser: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
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

        log.debug("IsReadOnly: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user,
                  view.__class__.__name__)
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

        log.debug("IsUserActive: %s, method: %s, user: %s, view: %s",
                  result, request.method, user, view.__class__.__name__)
        return result


## class IsUserRecord(permissions.BasePermission):
##     """
##     Disallows writing to non-user-own record.
##     """

##     def has_permission(self, request, view):
##         result = False
##         user = get_user(request)
##         instance = view.get_object()

##         if user == instance:
##             result = True

##         log.debug(": %s, method: %s, user: %s, view: %s",
##                   result, request.method, user, view.__class__.__name__)
##         return result


class CanDelete(permissions.BasePermission):
    """
    Allows deletion of records.
    """

    def has_permission(self, request, view):
        result = False

        if request.method == 'DELETE':
            result = True

        log.debug("CanDelete: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user, view.__class__.__name__)
        return result


class IsPostOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        result = False

        if request.method == 'POST':
            result = True

        log.debug("IsPostOnly: %s, method: %s, user: %s, view: %s",
                  result, request.method, request.user, view.__class__.__name__)
        return result
