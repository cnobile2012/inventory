# -*- coding: utf-8 -*-
#
# inventory/common/api/tests/test_permissions.py
#

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (
    APITestCase, APIRequestFactory, force_authenticate)

from django.contrib.auth import get_user_model

from inventory.accounts.api.views import user_list
from inventory.categories.api.views import category_detail
from inventory.common.api.tests.base_test import BaseTest
from inventory.projects.api.views import (
    project_list, project_detail, inventory_type_list)
from inventory.projects.models import Membership

from ..permissions import (
    IsAdminSuperUser, IsAdministrator, IsDefaultUser, IsAnyUser, IsReadOnly,
    IsProjectOwner, IsProjectManager, IsProjectDefaultUser, IsAnyProjectUser,
    IsUserActive, CanDelete, IsPostOnly)

UserModel = get_user_model()


class TestPermissions(BaseTest, APITestCase):
    DEFAULT_USER = UserModel.ROLE_MAP[UserModel.DEFAULT_USER]
    ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]
    PROJECT_USER = Membership.ROLE_MAP[Membership.PROJECT_USER]
    PROJECT_OWNER = Membership.ROLE_MAP[Membership.PROJECT_OWNER]
    PROJECT_MANAGER = Membership.ROLE_MAP[Membership.PROJECT_MANAGER]

    def __init__(self, name):
        super().__init__(name)

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
        msg = f"User '{request.user}', superuser: {request.user.is_superuser}"
        self.assertTrue(auth.has_permission(request, user_list), msg)
        # Test that a non superuser does not have access
        kwargs = {'is_superuser': False}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = f"User '{request.user}', superuser: {request.user.is_superuser}"
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
        msg = f"User '{request.user}', role: {request.user.role}"
        self.assertFalse(auth.has_permission(request, user_list), msg)
        # Test that an ADMINISTRATOR role has access.
        kwargs = {'role': self.ADMINISTRATOR}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = f"User '{request.user}', role: {request.user.role}"
        self.assertTrue(auth.has_permission(request, user_list), msg)

    def test_IsDefaultUser(self):
        """
        Test that only a DEFAULT_USER role has access.
        """
        #self.skipTest("Temporarily skipped")
        # Test that a DEFAULT_USER role does not have access.
        factory = APIRequestFactory()
        request = factory.get('user-list')
        kwargs = {'role': self.ADMINISTRATOR}
        user, client = self._create_user(**kwargs)
        request.user = user
        auth = IsDefaultUser()
        msg = f"User '{request.user}', role: {request.user.role}"
        self.assertFalse(auth.has_permission(request, user_list), msg)
        # Test that a DEFAULT_USER role has access.
        kwargs = {'role': self.DEFAULT_USER}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = f"User '{request.user}', role: {request.user.role}"
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
        msg = f"User '{request.user}', role: {request.user.role}"
        self.assertTrue(auth.has_permission(request, user_list), msg)
        # Test that an ADMINISTRATOR role has access.
        kwargs = {'role': self.ADMINISTRATOR}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = f"User '{request.user}', role: {request.user.role}"
        self.assertTrue(auth.has_permission(request, user_list), msg)
        # Test that a DEFAULT_USER role has access.
        kwargs = {'role': self.DEFAULT_USER}
        user, client = self._create_user(**kwargs)
        request.user = user
        force_authenticate(request, user=user)
        msg = f"User '{request.user}', role: {request.user.role}"
        self.assertTrue(auth.has_permission(request, user_list), msg)

    #
    # Project level roles
    #

    def test_IsProjectOwner(self):
        """
        Test that a project owner has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType
        in_type = self._create_inventory_type()
        # Create a user
        kwargs = {'username': 'Test_IsProjectOwner',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        # Create a project
        project = self._create_project(in_type)
        # Test that a non-project user does not have access.
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=self.user)
        auth = IsProjectOwner()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_OWNER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertFalse(auth.has_permission(request, project_list), msg)
        # Add the user to the project's membership list.
        members = [
            {'user': user, 'role_text': self.PROJECT_OWNER},
            ]
        project.process_members(members)
        # Test that an PROJECT_OWNER role has access.
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_OWNER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_permission(request, project_list), msg)

    def test_IsProjectOwner_object(self):
        """
        Test that a project owner has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType
        in_type = self._create_inventory_type()
        # Create the user
        kwargs = {'username': 'Test_IsProjectOwner',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        # Create the project
        project = self._create_project(in_type)
        # Test that a non-project user does not have access.
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        factory = APIRequestFactory()
        request = factory.get(uri)
        request.user = user
        force_authenticate(request, user=self.user)
        auth = IsProjectOwner()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_OWNER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertFalse(auth.has_object_permission(
            request, project_detail, project), msg)
        # Add the user to the project's membership list.
        members = [
            {'user': user, 'role_text': self.PROJECT_OWNER},
            ]
        project.process_members(members)
        # Test that an PROJECT_OWNER role has access.
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_OWNER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_object_permission(
            request, project_detail, project), msg)

    def test_IsProjectManager(self):
        """
        Test that a project manager has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        kwargs = {'username': 'Test_IsProjectManager',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        members = [
            {'user': self.user, 'role_text': self.PROJECT_OWNER},
            ]
        project = self._create_project(in_type, members=members)
        # Test that non-project user does not have access.
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsProjectManager()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertFalse(auth.has_permission(request, project_list), msg)
        # Add the user to the project's membership list.
        members = [
            {'user': self.user, 'role_text': self.PROJECT_OWNER},
            {'user': user, 'role_text': self.PROJECT_MANAGER}
            ]
        project.process_members(members)
        # Test that a PROJECT_MANAGER role has access.
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_permission(request, project_list), msg)

    def test_IsProjectManager_object(self):
        """
        Test that a project manager has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        kwargs = {'username': 'Test_IsProjectManager',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        members = [
            {'user': self.user, 'role_text': self.PROJECT_OWNER},
            ]
        project = self._create_project(in_type, members=members)
        # Test that non-project user does not have access.
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        factory = APIRequestFactory()
        request = factory.get(uri)
        request.user = user
        force_authenticate(request, user=user)
        auth = IsProjectManager()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertFalse(auth.has_object_permission(
            request, project_detail, project), msg)
        # Add the user to the project's membership list.
        members = [
            {'user': self.user, 'role_text': self.PROJECT_OWNER},
            {'user': user, 'role_text': self.PROJECT_MANAGER}
            ]
        project.process_members(members)
        # Test that a PROJECT_MANAGER role has access.
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_object_permission(
            request, project_detail, project), msg)

    def test_IsProjectDefaultUser(self):
        """
        Test that a project default user has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        kwargs = {'username': 'Test_DefaultUser',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        members = [
            {'user': self.user, 'role_text': self.PROJECT_MANAGER},
            ]
        project = self._create_project(in_type, members=members)
        # Test that non-project user does not have access.
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsProjectDefaultUser()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_USER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertFalse(auth.has_permission(request, project_list), msg)
        # Add the user to the project's membership list.
        members = [
            {'user': self.user, 'role_text': self.PROJECT_MANAGER},
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        project.process_members(members)
        # Test that a PROJECT_USER role has access.
        project.set_role(user, self.PROJECT_USER)
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_USER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_permission(request, project_list), msg)

    def test_IsProjectDefaultUser_object(self):
        """
        Test that a project default user has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        kwargs = {'username': 'Test_DefaultUser',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        # Add the user to the project's membership list.
        members = [
            {'user': self.user, 'role_text': self.PROJECT_MANAGER},
            ]
        project = self._create_project(in_type, members=members)
        # Test that non-project user does not have access.
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        factory = APIRequestFactory()
        request = factory.get(uri)
        request.user = user
        force_authenticate(request, user=user)
        auth = IsProjectDefaultUser()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_USER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertFalse(auth.has_object_permission(
            request, project_detail, project), msg)
        # Add the user to the project's membership list.
        members = [
            {'user': self.user, 'role_text': self.PROJECT_MANAGER},
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        project.process_members(members)
        # Test that a PROJECT_USER role has access.
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_USER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_object_permission(
            request, project_detail, project), msg)

    def test_IsAnyProjectUser(self):
        """
        Test that any project user has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        # Add the user to the project's membership list.
        kwargs = {'username': 'Test_IsAnyProjectUser',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        members = [
            {'user': self.user, 'role_text': self.PROJECT_OWNER},
            ]
        project = self._create_project(in_type, members=members)
        # Test that non-project user does not have access.
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsAnyProjectUser()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_USER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertFalse(auth.has_permission(request, project_list), msg)
        # Add the 2nd user.
        members = [
            {'user': self.user, 'role_text': self.PROJECT_OWNER},
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        project.process_members(members)
        # Test that a PROJECT_USER role has access.
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_USER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_permission(request, project_detail), msg)
        # Test that a PROJECT_MANAGER role has access.
        project.set_role(user, self.PROJECT_MANAGER)
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_permission(request, project_detail), msg)
        # Test that an PROJECT_OWNER role has access.
        project.set_role(user, self.PROJECT_OWNER)
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_OWNER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_permission(request, project_list), msg)

    def test_IsAnyProjectUser_object(self):
        """
        Test that any project user has access.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user.
        in_type = self._create_inventory_type()
        kwargs = {'username': 'Test_IsAnyProjectUser',
                  'password': '1234567890',
                  'email': 'test@example.org'}
        user, client = self._create_user(**kwargs)
        members = [
            {'user': self.user, 'role_text': self.PROJECT_OWNER},
            ]
        project = self._create_project(in_type, members=members)
        # Test that non-project user does not have access.
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        factory = APIRequestFactory()
        request = factory.get(uri)
        request.user = user
        force_authenticate(request, user=user)
        auth = IsAnyProjectUser()
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_USER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertFalse(auth.has_object_permission(
            request, project_detail, project), msg)
        # Add the user to the project's membership list.
        members = [
            {'user': self.user, 'role_text': self.PROJECT_OWNER},
            {'user': user, 'role_text': self.PROJECT_USER}
            ]
        project.process_members(members)
        # Test that a PROJECT_USER role has access.
        project.set_role(user, self.PROJECT_USER)
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_USER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_object_permission(
            request, project_detail, project), msg)
        # Test that a PROJECT_MANAGER role has access.
        project.set_role(user, self.PROJECT_MANAGER)
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_MANAGER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_object_permission(
            request, project_list, project), msg)
        # Test that a PROJECT_OWNER role has access.
        project.set_role(user, self.PROJECT_OWNER)
        members = user.memberships.filter(project=project,
                                          role=Membership.PROJECT_OWNER)
        role = members[0].role_text if members else None
        msg = f"User '{request.user}', role: {role}, members: {members}"
        self.assertTrue(auth.has_object_permission(
            request, project_detail, project), msg)
        # Test that a PROJECT_OWNER role has access to a project dependent
        # model
        category = self._create_category(project, 'TestLevel-0')
        uri = reverse('category-detail',
                      kwargs={'public_id': category.public_id})
        factory = APIRequestFactory()
        request = factory.get(uri)
        request.user = user
        force_authenticate(request, user=user)
        auth = IsAnyProjectUser()
        msg = f"User '{request.user}', role: {role}"
        self.assertTrue(auth.has_object_permission(
            request, category_detail, category), msg)

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
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER},
            {'user': user, 'role_text': self.PROJECT_OWNER},
            ]
        project = self._create_project(in_type, members=members)
        # Setup the GET request.
        factory = APIRequestFactory()
        request = factory.get('inventory-type-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsReadOnly()
        # Test that a READ operation works.
        msg = f"User: {user}"
        self.assertTrue(
            auth.has_permission(request, inventory_type_list), msg)
        # Setup the POST request.
        factory = APIRequestFactory()
        kwargs = {'name': 'Test IsReadOnly',
                  'description': "A test Inventory Type"}
        request = factory.post('inventory-type-list', **kwargs)
        request.user = user
        force_authenticate(request, user=user)
        auth = IsReadOnly()
        # Test that the user cannot post to this endpoint.
        msg = f"User: {user}"
        self.assertFalse(
            auth.has_permission(request, inventory_type_list), msg)

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
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER},
            {'user': user, 'role_text': self.PROJECT_OWNER},
            ]
        project = self._create_project(in_type, members=members)
        # Setup the GET request.
        factory = APIRequestFactory()
        request = factory.get('inventory-type-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsUserActive()
        # Test that an active user has access.
        msg = f"User: {user}"
        self.assertTrue(
            auth.has_permission(request, inventory_type_list), msg)
        # Test that an inactive user does not have access.
        user.is_active = False
        user.save()
        msg = f"User: {user}"
        self.assertFalse(
            auth.has_permission(request, inventory_type_list), msg)

    def test_CanDelete(self):
        """
        Test that a user can DELETE on the endpoint.
        """
        #self.skipTest("Temporarily skipped")
        # Create an InventoryType, a Project, and a user
        kwargs = {'username': 'Test_CanDelete',
                  'password': '1234567890',
                  'email': 'test@example.org',
                  'role': self.DEFAULT_USER}
        user, client = self._create_user(**kwargs)
        in_type = self._create_inventory_type()
        members = [
            {'user': self.user, 'role_text': self.PROJECT_USER},
            {'user': user, 'role_text': self.PROJECT_MANAGER},
            ]
        project = self._create_project(in_type, members=members)
        # Setup failing DELETE request
        factory = APIRequestFactory()
        uri = reverse('project-detail',
                      kwargs={'public_id': project.public_id})
        request = factory.delete(uri)
        request.user = user
        force_authenticate(request, user=user)
        auth = CanDelete()
        # Test that an active PROJECT_USER cannot delete
        msg = f"User: {user}"
        self.assertTrue(auth.has_permission(request, project_detail), msg)
        # Setup for passing DELETE request
        request = factory.get(uri)
        request.user = user
        force_authenticate(request, user=user)
        auth = CanDelete()
        # Test that an active PROJECT_MANAGER cannot delete
        msg = f"User: {user}"
        self.assertFalse(auth.has_permission(request, project_detail), msg)

    def test_IsPostOnly(self):
        """
        Test that a user has POST only access to an endpoint.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = {'username': 'Test_IsPostOnly',
                  'password': '1234567890',
                  'email': 'test@example.org',
                  'role': self.DEFAULT_USER}
        user, client = self._create_user(**kwargs)
        in_type = self._create_inventory_type()
        in_type_uri = reverse('inventory-type-detail',
                              kwargs={'public_id': in_type.public_id})
        # Test that user can not GET the project endpoint
        factory = APIRequestFactory()
        request = factory.get('project-list')
        request.user = user
        force_authenticate(request, user=user)
        auth = IsPostOnly()
        msg = f"User: {user}"
        self.assertFalse(auth.has_permission(request, project_list), msg)
        # Test that this user can POST a new project
        factory = APIRequestFactory()
        kwargs = {
            'name': "New Project",
            'inventory_type': in_type_uri,
            }
        request = factory.post('project-list', **kwargs)
        request.user = user
        force_authenticate(request, user=user)
        auth = IsPostOnly()
        msg = f"User: {user}"
        self.assertTrue(auth.has_permission(request, project_list), msg)
