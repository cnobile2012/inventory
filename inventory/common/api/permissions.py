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

        return result


class IsProjectManager(BasePermission):
    """
    Allows access only to project managers.
    """

    def has_permission(self, request, view):
        result = False

        if request.user and request.user.userprofile.manager:
            result = True

        return result


class IsProjectMember(BasePermission):
    """
    Check that the project is authorized for this user.
    """
    def has_object_permission(self, request, view, obj):
        result = False
        check_results = []

        # DO STUFF HERE

        return result
