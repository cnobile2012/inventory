# -*- coding: utf-8 -*-
#
# inventory/maintenance/api/tests/test_currencies.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest
from inventory.maintenance.models import Currency
from inventory.projects.models import Project

User = get_user_model()


class TestCurrencies(BaseTest):

    def __init__(self, name):
        super(TestCurrencies, self).__init__(name)

    def setUp(self):
        super(TestCurrencies, self).setUp()
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': "TEMP-{}".format(random.randint(10000, 99999)),
                    'password': "TEMP-{}".format(random.randint(10000, 99999))}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        user_pk = data.get('id')
        self.assertTrue(isinstance(user_pk, int))
        self.user_uri = reverse('user-detail', kwargs={'pk': user_pk})

    def test_create_post_currency(self):
        #self.skipTest("Temporarily skipped")
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('currency-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEquals(data.get('name'), new_data.get('name'), msg)

    def test_get_currency_with_no_permissions(self):
        """
        Test the currency_list endpoint with no permissions. We don't use the
        self.client created in the setUp method from the base class.
        """
        #self.skipTest("Temporarily skipped")
        username = 'Normal_User'
        password = '123456'
        user, client = self._create_normal_user(username, password, login=False)
        currency = self._create_currency()
        # Use API to get user list with unauthenticated user.
        uri = reverse('currency-list')
        response = client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            self._clean_data(data))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, msg)
        self.assertTrue('detail' in data, msg)

    def test_create_currency_post_token_superuser(self):
        """
        Test currency with API with token.
        """
        #self.skipTest("Temporarily skipped")
        app_name = 'Token Test'
        data = self._make_app_token(
            self.user, app_name, self.client, client_type='public',
            grant_type='client_credentials')
        # Use API to create a supplier.
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_currency_post_token_administrator(self):
        """
        Test currency with API with token. We don't use the self.client
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
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_currency_post_token_project_manager(self):
        """
        Test currency with API with token. We don't use the self.client
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
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)

    def test_create_currency_post_token_default_user(self):
        """
        Test currency with API with token. We don't use the self.client
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
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
        response = client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_put_currency(self):
        #self.skipTest("Temporarily skipped")
        # Create currency with POST.
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('public'), msg)
        # Update record with PUT.
        pk = data.get('id')
        uri = reverse('currency-detail', kwargs={'pk': pk})
        new_data['name'] = 'Hong Kong Dollar'
        response = self.client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('currency-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEquals(data.get('name'), new_data.get('name'), msg)
        self.assertEquals(data.get('symbol'), new_data.get('symbol'), msg)

    def test_update_put_currency_default_user(self):
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
        # Create currency with POST by superuser.
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        self.assertFalse(data.get('public'), msg)
        # Update record with PUT by default role.
        pk = data.get('id')
        uri = reverse('currency-detail', kwargs={'pk': pk})
        new_data['name'] = 'Hong Kong Dollar'
        response = client.put(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_403_FORBIDDEN,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg)

    def test_update_patch_currency(self):
        #self.skipTest("Temporarily skipped")
        # Create currency with POST.
        uri = reverse('currency-list')
        new_data = {'name': 'US Currency', 'symbol': '$'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Update record with PATCH.
        pk = data.get('id')
        uri = reverse('currency-detail', kwargs={'pk': pk})
        updated_data = {'name': 'Hong Kong Dollar'}
        response = self.client.patch(uri, updated_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        # Read record with GET.
        pk = data.get('id')
        uri = reverse('currency-detail', kwargs={'pk': pk})
        response = self.client.get(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEquals(data.get('name'), updated_data.get('name'), msg)
        self.assertEquals(data.get('symbol'), new_data.get('symbol'), msg)

    def test_delete_currency(self):
        #self.skipTest("Temporarily skipped")
        # Create currency with POST.
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED,
            self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
        # Delete the User.
        pk = data.get('id')
        uri = reverse('currency-detail', kwargs={'pk': pk})
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

    def test_options_currency(self):
        #self.skipTest("Temporarily skipped")
        # Create currency with POST.
        uri = reverse('currency-list')
        new_data = {'name': 'US Dollar', 'symbol': '$'}
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
        self.assertEqual(data.get('name'), 'Currency List', msg)
        # Get the API detail OPTIONS.
        uri = reverse('currency-detail', kwargs={'pk': pk})
        response = self.client.options(uri, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_200_OK, self._clean_data(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg)
        self.assertEqual(data.get('name'), 'Currency Detail', msg)

    def _create_currency(self):
        new_data = {'name': 'US Dollar', 'symbol': '$', 'updater': self.user,
                    'creator': self.user}
        currency = Currency.objects.create(**new_data)
        return currency
