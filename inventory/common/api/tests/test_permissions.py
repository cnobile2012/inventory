# -*- coding: utf-8 -*-
#
# inventory/categories/api/tests/test_category_api.py
#

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from django.contrib.auth import get_user_model

from inventory.common.api.tests.base_test import BaseTest
from inventory.accounts.api.views import user_list

from ..permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsReadOnly, IsUserActive)

UserModel = get_user_model()


class TestPermissions(BaseTest):

    def __init__(self, name):
        super(TestPermissions, self).__init__(name)

    def test_IsAdminSuperUser(self):
        """
        Test that the IsAdminSuperUser permission only works with super users.
        """
        #self.skipTest("Temporarily skipped")
        # Test that a superuser has access.
        factory = APIRequestFactory()
        request = factory.get('user-list')
        request.user = self.user
        force_authenticate(request, user=self.user)
        auth = IsAdminSuperUser()
        msg = "User '{}', superuser: {}".format(request.user,
                                                request.user.is_superuser)
        self.assertTrue(auth.has_permission(request, user_list), msg)
        # Test that a non superuser does not have access
        kwargs = {'is_superuser': False}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = "User '{}', superuser: {}".format(
            request.user, request.user.is_superuser)
        self.assertFalse(auth.has_permission(request, user_list), msg)

    def test_IsAdministrator(self):
        """
        Test that only an ADMINISTRATOR role has access.
        """
        #self.skipTest("Temporarily skipped")
        # Test that a ADMINISTRATOR role does not have access.
        factory = APIRequestFactory()
        request = factory.get('user-list')
        request.user = self.user
        force_authenticate(request, user=self.user)
        auth = IsAdministrator()
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertFalse(auth.has_permission(request, user_list), msg)
        # Test that an ADMINISTRATOR role has access.
        kwargs = {'role': UserModel.ADMINISTRATOR}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertTrue(auth.has_permission(request, user_list), msg)

    def test_IsDefaultUser(self):
        """
        Test that only a DEFAULT_USER role has access.
        """
        #self.skipTest("Temporarily skipped")
        # Test that a DEFAULT_USER role does not have access.
        factory = APIRequestFactory()
        request = factory.get('user-list')
        kwargs = {'role': UserModel.ADMINISTRATOR}
        user, client = self._create_user(**kwargs)
        request.user = user
        auth = IsDefaultUser()
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertFalse(auth.has_permission(request, user_list), msg)
        # Test that an DEFAULT_USER role has access.
        kwargs = {'role': UserModel.DEFAULT_USER}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertTrue(auth.has_permission(request, user_list), msg)

    def test_IsAnyUser(self):
        """
        Test that any user has access.
        """
        #self.skipTest("Temporarily skipped")
        # Test that a superuser has access.
        factory = APIRequestFactory()
        request = factory.get('user-list')
        request.user = self.user
        force_authenticate(request, user=self.user)
        auth = IsAnyUser()
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertTrue(auth.has_permission(request, user_list), msg)
        # Test that an ADMINISTRATOR role has access.
        kwargs = {'role': UserModel.ADMINISTRATOR}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertTrue(auth.has_permission(request, user_list), msg)
        # Test that an DEFAULT_USER role has access.
        kwargs = {'role': UserModel.DEFAULT_USER}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertTrue(auth.has_permission(request, user_list), msg)

    def test_IsProjectOwner(self):
        """
        Test that a project owner has access.
        """
        #self.skipTest("Temporarily skipped")
        # Test that a project owner has access.
        factory = APIRequestFactory()
        request = factory.get('user-list')
        request.user = self.user
        force_authenticate(request, user=self.user)
        auth = IsAnyUser()
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertTrue(auth.has_permission(request, user_list), msg)
