# -*- coding: utf-8 -*-
#
# inventory/projects/api/tests/test_projects.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

import random

from rest_framework.reverse import reverse
from rest_framework import status

from inventory.common.api.tests.base_test import BaseTest


class TestProject(BaseTest):

    def __init__(self, name):
        super(TestProject, self).__init__(name)

    def setUp(self):
        super(TestProject, self).setUp()
        # Use API to create a test user.
        uri = reverse('user-list')
        new_data = {'username': "TEMP-{}".format(random.randint(10000, 99999)),
                    'password': "TEMP-{}".format(random.randint(10000, 99999))}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        user_pk = data.get('id')
        self.assertTrue(isinstance(user_pk, int))
        # Use API to create the user's profile.
        uri = reverse('user-profile-list')
        self.user_uri = reverse('user-detail', kwargs={'pk': user_pk})
        profile_data = {'user': self.user_uri, 'role': 0}
        response = self.client.post(uri, profile_data, format='json')
        data = response.data
        msg = "Response Data: {}".format(data)
        self.assertEquals(data.get('role'), profile_data.get('role'), msg)

    def test_create_post_project(self):
        uri = reverse('project-list')
        new_data = {'name': 'Test Project', 'public': False, 'active': True,
                    'members': [self.user_uri,]}
        response = self.client.post(uri, new_data, format='json')
        data = response.data
        msg = "Response: {} should be {}, content: {}".format(
            response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg)
