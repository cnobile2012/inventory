#
# inventory/user_profiles/api/tests/test_users.py
#

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class TestUser(APITestCase):
    _TEMP_USERNAME = 'TestUser'
    _TEMP_PASSWORD = 'TestPassword_007'

    def setUp(self):
        pass

    def tearDown(self):
        self.client.logout()

    def test_create_account(self):
        """
        Ensure we can create a new account.
        """
        self._create_user()
        self._set_user_auth(use_token=False)
        self.client.force_authenticate(user=self.user)
        uri = reverse('user-list')
        data = {'username': 'NewUser',}
        response = self._get_response_value_POST(uri, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)






    ## def test_user_list_no_permissions(self):
    ##     """
    ##     Test the user_list endpoint with no permissions.
    ##     """
    ##     self._create_user()
    ##     self._set_user_auth(use_token=False)
    ##     values = self._get_response_value('?format=json', 'username',
    ##                                       num_records=0)
    ##     self.assertEqual(values, [])





    def _create_user(self, username=_TEMP_USERNAME, password=_TEMP_PASSWORD):
        self.user = User.objects.create(username=username, password=password)
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

    def _set_user_auth(self, username=_TEMP_USERNAME, password=_TEMP_PASSWORD,
                       use_token=True):
        self.client = APIClient()

        if use_token:
            token = Token.objects.create(user__username=username)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        else:
            self.client.login(username=username, password=password)

    def _get_response_value_POST(self, uri, data, format='json'):
        return self.client.post(uri, data, format=format)

    def _get_response_value_GET(self, uri, format, field, num_records=1):
        response = self.client.get(uri, format=format)
        results = response.data.get('results', [])
        self.assertTrue(len(results) == num_records)
        values = []

        for num in range(num_records):
            values.append(results[num].get(field))

        return values
