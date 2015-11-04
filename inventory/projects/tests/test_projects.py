# -*- coding: utf-8 -*-
#
# inventory/projects/tests/test_projects.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Project

User = get_user_model()


class TestProjects(TestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(TestProjects, self).__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    def test_process_members(self):
        #self.skipTest("Temporarily skipped")
        project = self._create_project_record('Test Project')
        username_0 = 'Test User 00'
        user_0 = self._create_user(username=username_0,
                                   password='0123456',
                                   is_superuser=False)
        username_1 = 'Test User 01'
        user_1 = self._create_user(username=username_1,
                                   password='1234567',
                                   is_superuser=False)
        # Test that there are no members.
        msg = "Members: {}".format(project.members.all())
        self.assertEqual(project.members.count(), 0, msg)
        # Test that there is one members.
        project.process_members([user_0])
        msg = "Members: {}".format(project.members.all())
        self.assertEqual(project.members.count(), 1, msg)
        # Test that there are two members.
        project.process_members([user_0, user_1])
        msg = "Members: {}".format(project.members.all())
        self.assertEqual(project.members.count(), 2, msg)
        # Test that removing a member results in one member.
        project.process_members([user_1])
        users = project.members.all()
        msg = "Members: {}".format(users)
        self.assertEqual(project.members.count(), 1, msg)
        self.assertEqual(users[0].username, username_1, msg)

    def test_process_managers(self):
        #self.skipTest("Temporarily skipped")
        project = self._create_project_record('Test Project')
        username_0 = 'Test User 00'
        user_0 = self._create_user(username=username_0,
                                   password='0123456',
                                   is_superuser=False)
        pk_0 = user_0.pk
        username_1 = 'Test User 01'
        user_1 = self._create_user(username=username_1,
                                   password='1234567',
                                   is_superuser=False)
        pk_1 = user_1.pk
        # Test that there are no managers.
        msg = "Managers: {}".format(project.managers.all())
        self.assertEqual(project.managers.count(), 0, msg)
        user_0 = User.objects.get(pk=pk_0)
        user_1 = User.objects.get(pk=pk_1)
        self.assertEqual(user_0.role, User.DEFAULT_USER, msg)
        self.assertEqual(user_1.role, User.DEFAULT_USER, msg)
        # Test that there is one managers.
        project.process_managers([user_0])
        msg = "Managers: {}".format(project.managers.all())
        self.assertEqual(project.managers.count(), 1, msg)
        user_0 = User.objects.get(pk=pk_0)
        user_1 = User.objects.get(pk=pk_1)
        self.assertEqual(user_0.role, User.PROJECT_MANAGER, msg)
        self.assertEqual(user_1.role, User.DEFAULT_USER, msg)
        # Test that there are two managers.
        project.process_managers([user_0, user_1])
        msg = "Managers: {}".format(project.managers.all())
        self.assertEqual(project.managers.count(), 2, msg)
        user_0 = User.objects.get(pk=pk_0)
        user_1 = User.objects.get(pk=pk_1)
        self.assertEqual(user_0.role, User.PROJECT_MANAGER, msg)
        self.assertEqual(user_1.role, User.PROJECT_MANAGER, msg)
        # Test that removing a member results in one member.
        project.process_managers([user_1])
        users = project.managers.all()
        msg = "Managers: {}".format(users)
        self.assertEqual(project.managers.count(), 1, msg)
        self.assertEqual(users[0].username, username_1, msg)
        user_0 = User.objects.get(pk=pk_0)
        user_1 = User.objects.get(pk=pk_1)
        self.assertEqual(user_0.role, User.DEFAULT_USER, msg)
        self.assertEqual(user_1.role, User.PROJECT_MANAGER, msg)

    def _create_project_record(self, name, public=True):
        kwargs = {}
        kwargs['name'] = name
        kwargs['public'] = public
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Project.objects.create(**kwargs)

    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True,
                     role=User.DEFAULT_USER):
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.role = role
        user.save()
        return user
