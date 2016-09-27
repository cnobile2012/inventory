# -*- coding: utf-8 -*-
#
# inventory/categories/api/tests/test_category_api.py
#

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from django.contrib.auth import get_user_model

from inventory.accounts.api.views import user_list
from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.api.views import project_list, inventory_type_list
from inventory.projects.models import Membership

from ..permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser, IsReadOnly,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsUserActive)

UserModel = get_user_model()


class TestPermissions(BaseTest):

    def __init__(self, name):
        super(TestPermissions, self).__init__(name)

    #
    # User level roles
    #

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
        # Test that an ADMINISTRATOR role does not have access.
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
        # Test that a DEFAULT_USER role has access.
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
        # Test that a DEFAULT_USER role has access.
        kwargs = {'role': UserModel.DEFAULT_USER}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = "User '{}', role: {}".format(request.user, request.user.role)
        self.assertTrue(auth.has_permission(request, user_list), msg)

    #
    # Project level roles
    #

    def test_IsProjectOwner(self):
        """
        Test that a project owner has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType and a Project
        in_type = self._create_inventory_type()
        project = self._create_project(in_type)
        kwargs = {'username': 'Test_IsProjectOwner',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        # Test that a non-project user does not have access.
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=self.user)
        auth = IsProjectOwner()
        members = user.memberships.filter(project=project,
                                          role=Membership.OWNER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertFalse(auth.has_object_permission(
            request, project_list, project), msg)
        # Add the user to the project's membership list.
        project.process_members([user])
        # Test that an OWNER role has access.
        members = user.memberships.filter(project=project,
                                          role=Membership.OWNER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertTrue(auth.has_object_permission(
            request, project_list, project), msg)

    def test_IsProjectManager(self):
        """
        Test that a project manager has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        project = self._create_project(in_type, members=[self.user])
        kwargs = {'username': 'Test_IsProjectManager',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        # Test that non-project user does not have access.
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsProjectManager()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertFalse(auth.has_object_permission(
            request, project_list, project), msg)
        # Add the user to the project's membership list.
        project.process_members([user])
        # Test that a PROJECT_MANAGER role has access.
        project.set_role(user, Membership.PROJECT_MANAGER)
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertTrue(auth.has_object_permission(
            request, project_list, project), msg)

    def test_IsProjectDefaultUser(self):
        """
        Test that a project default user has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        project = self._create_project(in_type, members=[self.user])
        kwargs = {'username': 'Test_DefaultUser',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        # Test that non-project user does not have access.
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsProjectDefaultUser()
        members = user.memberships.filter(project=project,
                                          role=Membership.DEFAULT_USER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertFalse(auth.has_object_permission(
            request, project_list, project), msg)
        # Add the user to the project's membership list.
        project.process_members([user])
        # Test that a DEFAULT_USER role has access.
        project.set_role(user, Membership.DEFAULT_USER)
        members = user.memberships.filter(project=project,
                                          role=Membership.DEFAULT_USER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertTrue(auth.has_object_permission(
            request, project_list, project), msg)

    def test_IsAnyProjectUser(self):
        """
        Test that any project user has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        project = self._create_project(in_type, members=[self.user])
        kwargs = {'username': 'Test_IsAnyProjectUser',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        # Test that non-project user does not have access.
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsAnyProjectUser()
        members = user.memberships.filter(project=project,
                                          role=Membership.DEFAULT_USER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertFalse(auth.has_object_permission(
            request, project_list, project), msg)
        # Add the user to the project's membership list.
        project.process_members([user])
        # Test that a DEFAULT_USER role has access.
        project.set_role(user, Membership.DEFAULT_USER)
        members = user.memberships.filter(project=project,
                                          role=Membership.DEFAULT_USER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertTrue(auth.has_object_permission(
            request, project_list, project), msg)
        # Test that a PROJECT_MANAGER role has access.
        project.set_role(user, Membership.PROJECT_MANAGER)
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertTrue(auth.has_object_permission(
            request, project_list, project), msg)
        # Test that an OWNER role has access.
        project.set_role(user, Membership.OWNER)
        members = user.memberships.filter(project=project,
                                          role=Membership.OWNER)
        role = members[0].role if members else None
        msg = "User '{}', role: {}, members: {}".format(
            request.user, role, members)
        self.assertTrue(auth.has_object_permission(
            request, project_list, project), msg)

    #
    # Miscellaneous level roles
    #

    def test_IsReadOnly(self):
        """
        Test that the access is read only.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        kwargs = {'username': 'Test_IsReadOnly',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        in_type = self._create_inventory_type()
        project = self._create_project(in_type, members=[self.user])
        project.process_members([user])
        project.set_role(user, Membership.OWNER)
        # Setup the GET request.
        factory = APIRequestFactory()
        request = factory.get('inventory-type-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsReadOnly()
        # Test that a READ operation works.
        msg = "User: {}".format(user)
        self.assertTrue(auth.has_permission(request, inventory_type_list), msg)
        # Setup the POST request.
        factory = APIRequestFactory()
        kwargs = {'name': 'Test IsReadOnly',
                  'description': "A test Inventory Type"}
        request = factory.post('inventory-type-list', **kwargs)
        request.user = user
        force_authenticate(request, user=user)
        auth = IsReadOnly()
        # Add the user to the project's membership list.
        project.process_members([user])
        # Test that the user cannot post to this endpoint.
        msg = "User: {}".format(user)
        self.assertFalse(auth.has_permission(request, inventory_type_list), msg)

    def test_IsUserActive(self):
        """
        Test that an inactive user can not access the endpoint.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        kwargs = {'username': 'Test_IsUserActive',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        in_type = self._create_inventory_type()
        project = self._create_project(in_type, members=[self.user])
        project.process_members([user])
        project.set_role(user, Membership.OWNER)
        # Setup the GET request.
        factory = APIRequestFactory()
        request = factory.get('inventory-type-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsUserActive()
        # Test that an active user has access.
        msg = "User: {}".format(user)
        self.assertTrue(auth.has_permission(request, inventory_type_list), msg)
        # Test that an inactive user does not have access.
        user.is_active = False
        user.save()
        msg = "User: {}".format(user)
        self.assertFalse(auth.has_permission(request, inventory_type_list), msg)
