# -*- coding: utf-8 -*-
#
# inventory/locations/api/tests/test_locations_api.py
#

import random

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest
from inventory.locations.models import (
    LocationDefault, LocationFormat, LocationCode)
from inventory.projects.models import Project

UserModel = get_user_model()


class BaseLocation(BaseTest):

    def __init__(self, name):
        super(BaseLocation, self).__init__(name)

    def _create_location_default(self, name=None):
        new_data = {
            'name': 'Test Location Default', 'owner': self.user,
            'shared': True, 'description': "Test Location Default",
            'separator': ':', 'creator': self.user, 'updater': self.user
            }

        if name:
            new_data['name'] = name

        return LocationDefault.objects.create(**new_data)

    def _create_location_format(self, location_default, char_definition=None,
                                segment_order=None):
        new_data = {
            'location_default': location_default, 'char_definition': r'T\d\d',
            'segment_order': 0, 'description': "Test Location Format",
            'creator': self.user, 'updater': self.user
            }

        if char_definition:
            new_data['char_definition'] = char_definition

        if segment_order:
            new_data['segment_order'] = segment_order

        return LocationFormat.objects.create(**new_data)

    def _create_location_code(self, location_format):
        new_data = {
            'char_definition': location_format, 'segment': 'T01',
            'parent': None, 'creator': self.user, 'updater': self.user
            }
        return LocationCode.objects.create(**new_data)

    def _create_project(self, user):
        kwargs = {}
        kwargs['name'] = "My Test Project"
        kwargs['public'] = True
        kwargs['creator'] = user
        kwargs['updater'] = user
        project = Project.objects.create(**kwargs)
        project.process_members([user])
        project.process_managers([user])
        return project

class TestLocationDefault(BaseLocation):

    def __init__(self, name):
        super(TestLocationDefault, self).__init__(name)

    def test_create_post_location_default(self):
        """
        Test that we can create a new location_default with a POST.
        """
        # Create LocationDefault with POST.
        self.skipTest("Temporarily skipped")
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('location-default-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)

    def test_get_location_default_with_no_permissions(self):
        """
        Test the location_default_list endpoint with no permissions. We don't
        use the self.client created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        ld = self._create_location_default()
        # Use API to get user list with unauthenticated user.
        uri = reverse('location-default-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_location_default_post_token_superuser(self):
        """
        Test LocationDefault with API with token.
        """
        self.skipTest("Temporarily skipped")
        app_name = 'Token Test'
        data = self._make_app_token(
            self.user, app_name, self.client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a LocationDefault.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_default_post_token_administrator(self):
        """
        Test LocationDefault with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.ADMINISTRATOR)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_default_post_token_project_manager(self):
        """
        Test LocationDefault with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Create a project for this user.
        project = self._create_project(user)
        # Get the user, to be sure we get the updated members and managers.
        user = UserModel.objects.get(pk=user.pk)
        msg = "user.role: {} sould be {}.".format(
            user.role,  UserModel.PROJECT_MANAGER)
        self.assertEqual(user.role, UserModel.PROJECT_MANAGER, msg)
        # Use API to create a supplier.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_default_post_token_default_user(self):
        """
        Test LocationDefault with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.DEFAULT_USER)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_put_location_default(self):
        """
        Teat that we can do an update with a PUT.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationDefault with POST.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('location-default-detail', kwargs={'pk': pk})
        new_data['shared'] = False
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)
        self.assertEqual(data.get('shared'), new_data.get('shared'), msg)

    def test_update_put_location_default_default_user(self):
        """
        Teat that we can do an update with a PUT by a default user.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.DEFAULT_USER)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Create LocationDefault with POST by superuser.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PUT by default role.
        pk = data.get('id')
        uri = reverse('location-default-detail', kwargs={'pk': pk})
        new_data['shared'] = False
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_patch_location_default(self):
        """
        Test that we can do an update with a PATCH.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationDefault with POST.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('location-default-detail', kwargs={'pk': pk})
        updated_data = {'separator': '->'}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)
        self.assertEqual(data.get('separator'), updated_data.get('separator'),
                         msg)

    def test_delete_location_default(self):
        """
        Test that we can remove a record with a DELETE.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationDefault with POST.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the User.
        pk = data.get('id')
        uri = reverse('location-default-detail', kwargs={'pk': pk})
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        code = response.status_code
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_location_default(self):
        """
        Test that the OPTIONS method returns the correct data.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationDefault with POST.
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': ':'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Location Default List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('location-default-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Location Default Detail', msg)

    def test_length_of_separator(self):
        """
        Test that the length of the separator is not longer than the defined
        length of the database column.
        """
        self.skipTest("Temporarily skipped")
        uri = reverse('location-default-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'name': 'Test Location Default', 'owner': owner_uri,
                    'shared': True, 'description': "Test POST",
                    'separator': '--->'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("Ensure this field has " in data.get('separator')[0],
                        msg)


class TestLocationFormat(BaseLocation):

    def __init__(self, name):
        super(TestLocationFormat, self).__init__(name)

    def test_create_post_location_format(self):
        """
        Test that a record can be created with a POST.
        """
        # Create LocationFormat with POST.
        self.skipTest("Temporarily skipped")
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('location-format-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)

    def test_get_location_format_with_no_permissions(self):
        """
        Test the location_format_list endpoint with no permissions. We don't
        use the self.client created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        # Use API to get user list with unauthenticated user.
        uri = reverse('location-format-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_location_format_post_token_superuser(self):
        """
        Test LocationFormat with API with token.
        """
        self.skipTest("Temporarily skipped")
        app_name = 'Token Test'
        data = self._make_app_token(
            self.user, app_name, self.client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a LocationDefault.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_format_post_token_administrator(self):
        """
        Test LocationFormat with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.ADMINISTRATOR)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_format_post_token_project_manager(self):
        """
        Test LocationFormat with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Create a project for this user.
        project = self._create_project(user)
        # Get the user, to be sure we get the updated members and managers.
        user = User.objects.get(pk=user.pk)
        msg = "user.role: {} sould be {}.".format(
            user.role,  UserModel.PROJECT_MANAGER)
        self.assertEqual(user.role, UserModel.PROJECT_MANAGER, msg)
        # Use API to create a supplier.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        uri = reverse('location-format-list')
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_format_post_token_default_user(self):
        """
        Test LocationFormat with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.DEFAULT_USER)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_put_location_format(self):
        """
        Test that an update can be done with a PUT.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationFormat with POST.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('location-format-detail', kwargs={'pk': pk})
        new_data['char_definition'] = r'T\d\d\d'
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}, new_data: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data),
            new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('char_definition'),
                         new_data.get('char_definition'), msg)

    def test_update_put_location_format_default_user(self):
        """
        Test that an update can be done with a PUT by a default user.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.DEFAULT_USER)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Create LocationFormat with POST by superuser.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PUT by default role.
        pk = data.get('id')
        uri = reverse('location-format-detail', kwargs={'pk': pk})
        new_data['char_definition'] = r'T\d\d\d'
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_patch_location_format(self):
        """
        Test that an update can e dome with a PATCH.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationFormat with POST.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('location-format-detail', kwargs={'pk': pk})
        updated_data = {'description': 'Test PATCH LocationFormat'}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), new_data.get('name'), msg)
        self.assertEqual(data.get('description'),
                         updated_data.get('description'), msg)

    def test_delete_location_format(self):
        """
        Test that a record can be removed with a DELETE.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationFormat with POST.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the User.
        pk = data.get('id')
        uri = reverse('location-format-detail', kwargs={'pk': pk})
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        code = response.status_code
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_location_format(self):
        """
        Test that the correct data is returned with OPTIONS.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationFormat with POST.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Location Format List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('location-format-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Location Format Detail', msg)

    def test_delimitor_in_char_definition(self):
        """
        Test that the delimitor is not in the character definition.
        """
        self.skipTest("Temporarily skipped")
        # Test delimitor in char_definition.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri,
                    'char_definition': r'T{}\d\d'.format(ld.separator),
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(
            "Invalid format, found separator" in data.get('char_definition')[0],
            msg)

    def test_char_definition_length_is_not_zero(self):
        """
        Test that the char_definition length is not zero.
        """
        self.skipTest("Temporarily skipped")
        # Test that character_definition length is not zero.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        new_data = {'location_default': ld_uri, 'char_definition': r'',
                    'segment_order': 0, 'description': "Test POST"}
        uri = reverse('location-format-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(
            "This field may not be blank." in data.get('char_definition'),
            msg)


class TestLocationCode(BaseLocation):

    def __init__(self, name):
        super(TestLocationCode, self).__init__(name)

    def test_create_post_location_code(self):
        """
        Test that a record can be created with a POST.
        """
        # Create LocationCode with POST.
        self.skipTest("Temporarily skipped")
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        #, 'parent': None} This should be permitted
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('segment'), new_data.get('segment'), msg)

    def test_get_location_code_with_no_permissions(self):
        """
        Test the location_code_list endpoint with no permissions. We don't
        use the self.client created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lc = self._create_location_code(lf)
        # Use API to get user list with unauthenticated user.
        uri = reverse('location-code-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_location_code_post_token_superuser(self):
        """
        Test LocationCode with API with token.
        """
        self.skipTest("Temporarily skipped")
        app_name = 'Token Test'
        data = self._make_app_token(
            self.user, app_name, self.client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a LocationDefault.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        #, 'parent': None} This should be permitted
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_code_post_token_administrator(self):
        """
        Test LocationCode with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.ADMINISTRATOR)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        #, 'parent': None} This should be permitted
        uri = reverse('location-code-list')
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_code_post_token_project_manager(self):
        """
        Test LocationCode with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com')
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Create a project for this user.
        project = self._create_project(user)
        # Get the user, to be sure we get the updated members and managers.
        user = UserModel.objects.get(pk=user.pk)
        msg = "user.role: {} sould be {}.".format(
            user.role,  UserModel.PROJECT_MANAGER)
        self.assertEqual(user.role, UserModel.PROJECT_MANAGER, msg)
        # Use API to create a supplier.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        #, 'parent': None} This should be permitted
        uri = reverse('location-code-list')
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_location_code_post_token_default_user(self):
        """
        Test LocationCode with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.DEFAULT_USER)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_put_location_code(self):
        """
        Test that a record can be updated with a PUT.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationCode with POST.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        new_data['segment'] = r'T02'
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}, new_data: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data),
            new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('segment'), new_data.get('segment'), msg)

    def test_update_put_location_code_default_user(self):
        """
        Test that a record can be updated with a PUT for a default user.
        """
        self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=UserModel.DEFAULT_USER)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
        # Create LocationCode with POST by superuser.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PUT by default role.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        new_data['segment'] = 'T02'
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)


    def test_update_patch_location_code(self):
        """
        Test that a record can be updated with a PATCH.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationCode with POST.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        updated_data = {'segment': 'T02'}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('segment'), updated_data.get('segment'), msg)

    def test_delete_location_code(self):
        """
        Test that a record can be removed with a DELETE.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationCode with POST.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the User.
        pk = data.get('id')
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        response = self.client.delete(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertTrue(data is None, msg)
        # Get the same record through the API.
        response = self.client.get(uri, format='json')
        code = response.status_code
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_404_NOT_FOUND,
            self._clean_data(data))
        self.assertEqual(code, status.HTTP_404_NOT_FOUND, msg)

    def test_options_location_code(self):
        """
        Test that OPTIONS returns the correct data.
        """
        self.skipTest("Temporarily skipped")
        # Create LocationCode with POST.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        pk = data.get('id')
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Get the API list OPTIONS.
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Location Code List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('location-code-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Location Code Detail', msg)

    def test_invalid_segment(self):
        """
        Test that a segment obays the rules.
        """
        self.skipTest("Temporarily skipped")
        # Test delimitor in segment.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        new_data = {
            'char_definition': lf_uri, 'segment': 'T{}01'.format(ld.separator)
            }
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("does not conform to " in data.get('segment')[0], msg)
        # Test inconsistant format.
        new_data = {'char_definition': lf_uri, 'segment': 'S01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("does not conform to " in data.get('segment')[0], msg)

    def test_segment_not_parent_to_itself(self):
        """
        Test that a segment is not a parent to itself.
        """
        self.skipTest("Temporarily skipped")
        # Create the location default and format objects.
        ld = self._create_location_default()
        lf = self._create_location_format(ld)
        lf_uri = reverse('location-format-detail', kwargs={'pk': lf.id})
        # Create the first location code.
        new_data = {'char_definition': lf_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create a second location code.
        lc_uri = reverse('location-code-detail', kwargs={'pk': data.get('id')})
        new_data = {'char_definition': lf_uri, 'segment': 'T01',
                    'parent': lc_uri}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("child to itself." in data.get('__all__')[0], msg)

    def test_segments_have_same_location_default(self):
        """
        Test that all the segments in a given tree have the same location
        default.
        """
        self.skipTest("Temporarily skipped")
        # Create the location default and format objects.
        ld0 = self._create_location_default()
        lf0 = self._create_location_format(ld0)
        lf0_uri = reverse('location-format-detail', kwargs={'pk': lf0.id})
        # Create second set of location default and format objects.
        ld1 = self._create_location_default(name="This one fails")
        lf1 = self._create_location_format(ld1, char_definition=r'C\d\dR\d\d',
                                           segment_order=1)
        lf1_uri = reverse('location-format-detail', kwargs={'pk': lf1.id})
        # Create first location code.
        new_data = {'char_definition': lf0_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create second location code.
        lc0_uri = reverse('location-code-detail', kwargs={'pk': data.get('id')})
        new_data = {'char_definition': lf1_uri, 'segment': 'C01R01',
                    'parent': lc0_uri}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue(
            "All segments must be derived" in data.get('__all__')[0], msg)

    def test_number_segments_number_formats(self):
        """
        Test that the number of segments defined are equal to or less than
        the number of formats for this location default.
        """
        self.skipTest("Temporarily skipped")
        # Create the location default and format objects.
        ld0 = self._create_location_default()
        lf0 = self._create_location_format(ld0)
        lf0_uri = reverse('location-format-detail', kwargs={'pk': lf0.id})
        # Create second set of location format object.
        lf1 = self._create_location_format(ld0, char_definition=r'C\d\dR\d\d',
                                           segment_order=1)
        lf1_uri = reverse('location-format-detail', kwargs={'pk': lf1.id})
        # Create first location code.
        new_data = {'char_definition': lf0_uri, 'segment': 'T01'}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create second location code.
        lc0_uri = reverse('location-code-detail', kwargs={'pk': data.get('id')})
        new_data = {'char_definition': lf1_uri, 'segment': 'C01R01',
                    'parent': lc0_uri}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Create third location code which will fail.
        lc1_uri = reverse('location-code-detail', kwargs={'pk': data.get('id')})
        new_data = {'char_definition': lf1_uri, 'segment': 'C01R01',
                    'parent': lc1_uri}
        uri = reverse('location-code-list')
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg)
        self.assertTrue("as a child to itself." in data.get('__all__')[0], msg)
