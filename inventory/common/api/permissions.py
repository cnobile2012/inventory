#
# inventory/common/api/permissions.py
#

import logging

from rest_framework.permissions import BasePermission

from inventory.user_profiles.models import UserProfile


log = logging.getLogger('api.common.permissions')


class IsAdminSuperUser(BasePermission):
    """
    Allows access only to admin super users.
    """

    def has_permission(self, request, view):
        result = False

        if request.user and request.user.is_superuser:
            result = True

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

        return result
