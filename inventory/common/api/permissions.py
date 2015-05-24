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


class IsProjectManager(BasePermission):
    """
    Allows access only to project managers or an administrator.
    """

    def has_permission(self, request, view):
        result = False

        if (request.user.is_superuser or hasattr(request, 'user') and
            ((hasattr(request.user, 'userprofile') and
              request.user.userprofile.role == UserProfile.ADMINISTRATOR) or
            request.user.project_managers.count())):
            result = True

        return result


class IsProjectMember(BasePermission):
    """
    Check that the project is authorized for this user.
    """
    def has_object_permission(self, request, view, obj):
        result = False

        if (request.user and
            request.user.userprofile.role == UserProfile.DEFAULT):
            result = True

        return result
