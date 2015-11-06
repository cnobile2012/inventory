# -*- coding: utf-8 -*-
#
# inventory/maintenance/api/tests/test_locations.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest
from inventory.maintenance.models import (
    LocationDefault, LocationFormat, LocationCode)
from inventory.projects.models import Project

User = get_user_model()


class BaseLocation(BaseTest):

    def __init__(self, name):
        super(BaseLocation, self).__init__(name)

    def _create_location_default(self):
        new_data = {
            'name': 'Test Location Default', 'owner': self.user,
            'shared': True, 'description': "Test Location Default",
            'separator': ':', 'creator': self.user, 'updater': self.user
            }
        return LocationDefault.objects.create(**new_data)

    def _create_location_format(self, location_default):
        new_data = {
            'location_default': location_default, 'char_definition': r'T\d\d',
            'segment_order': 0, 'description': "Test Location Format",
            'creator': self.user, 'updater': self.user
            }
        return LocationFormat.objects.create(**new_data)

    def _create_location_code(self, location_format):
        new_data = {
            'char_definition': location_format, 'segment': 'T01',
            'parent': None, 'creator': self.user, 'updater': self.user
            }
        return LocationCode.objects.create(**new_data)


class TestLocationDefault(BaseLocation):

    def __init__(self, name):
        super(TestLocationDefault, self).__init__(name)

    def test_create_post_location_default(self):
        # Create LocationDefault with POST.
        #self.skipTest("Temporarily skipped")
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
        self.assertEquals(data.get('name'), new_data.get('name'), msg)

    def test_get_location_default_with_no_permissions(self):
        """
        Test the location_default_list endpoint with no permissions. We don't
        use the self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
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
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_location_default_post_token_superuser(self):
        """
        Test LocationDefault with API with token.
        """
        #self.skipTest("Temporarily skipped")
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
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=User.ADMINISTRATOR)
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
        #self.skipTest("Temporarily skipped")
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
        kwargs = {}
        kwargs['name'] = "My Test Project"
        kwargs['public'] = True
        kwargs['creator'] = user
        kwargs['updater'] = user
        project = Project.objects.create(**kwargs)
        project.process_members([user])
        project.process_managers([user])
        # Get the user, to be sure we get the updated members and managers.
        user = User.objects.get(pk=user.pk)
        msg = "user.role: {} sould be {}.".format(
            user.role,  User.PROJECT_MANAGER)
        self.assertEqual(user.role, User.PROJECT_MANAGER, msg)
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
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=User.DEFAULT_USER)
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
        #self.skipTest("Temporarily skipped")
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
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertEquals(data.get('shared'), new_data.get('shared'), msg)

    def test_update_put_location_default_default_user(self):
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=User.DEFAULT_USER)
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
        #self.skipTest("Temporarily skipped")
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
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertEquals(data.get('separator'), updated_data.get('separator'),
                          msg)

    def test_delete_location_default(self):
        #self.skipTest("Temporarily skipped")
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
        #self.skipTest("Temporarily skipped")
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


class TestLocationFormat(BaseLocation):

    def __init__(self, name):
        super(TestLocationFormat, self).__init__(name)

    def test_create_post_location_format(self):
        # Create LocationDefault with POST.
        #self.skipTest("Temporarily skipped")
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
        self.assertEquals(data.get('name'), new_data.get('name'), msg)

    def test_get_location_format_with_no_permissions(self):
        """
        Test the location_format_list endpoint with no permissions. We don't
        use the self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
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
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_location_format_post_token_superuser(self):
        """
        Test LocationFormat with API with token.
        """
        #self.skipTest("Temporarily skipped")
        app_name = 'Token Test'
        data = self._make_app_token(
            self.user, app_name, self.client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a LocationDefault.
        ld = self._create_location_default()
        ld_uri = reverse('location-default-detail', kwargs={'pk': ld.id})
        uri = reverse('location-format-list')
        owner_uri = reverse('user-detail', kwargs={'pk': self.user.pk})
        new_data = {'location_default': ld_uri, 'char_definition': r'T\d\d' ,
                    'segment_order': 0, 'description': "Test POST"}
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
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=User.ADMINISTRATOR)
        app_name = 'Token Test'
        data = self._make_app_token(
            user, app_name, client, client_type='public',
            grant_type='client_credentials')
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

    def test_create_location_format_post_token_project_manager(self):
        """
        Test LocationFormat with API with token. We don't use the self.client
        created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
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
        kwargs = {}
        kwargs['name'] = "My Test Project"
        kwargs['public'] = True
        kwargs['creator'] = user
        kwargs['updater'] = user
        project = Project.objects.create(**kwargs)
        project.process_members([user])
        project.process_managers([user])
        # Get the user, to be sure we get the updated members and managers.
        user = User.objects.get(pk=user.pk)
        msg = "user.role: {} sould be {}.".format(
            user.role,  User.PROJECT_MANAGER)
        self.assertEqual(user.role, User.PROJECT_MANAGER, msg)
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
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=User.DEFAULT_USER)
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
        #self.skipTest("Temporarily skipped")
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
        self.assertEquals(data.get('char_definition'),
                          new_data.get('char_definition'), msg)

    def test_update_put_location_format_default_user(self):
        #self.skipTest("Temporarily skipped")
        # Create a non-logged in user, but one that has a valid token.
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(
            username, password, email='test@example.com',
            role=User.DEFAULT_USER)
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
        #self.skipTest("Temporarily skipped")
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
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertEquals(data.get('description'),
                          updated_data.get('description'), msg)

    def test_delete_location_format(self):
        #self.skipTest("Temporarily skipped")
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
        #self.skipTest("Temporarily skipped")
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


class TestLocationCode(BaseLocation):

    def __init__(self, name):
        super(TestLocationCode, self).__init__(name)








