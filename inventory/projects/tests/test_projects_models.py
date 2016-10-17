# -*- coding: utf-8 -*-
#
# inventory/projects/tests/test_projects_models.py
#

from django.core.exceptions import ValidationError

from inventory.common.tests.base_tests import BaseTest

from ..models import Project, Membership


class TestProjectModels(BaseTest):

    def __init__(self, name):
        super(TestProjectModels, self).__init__(name)

    def setUp(self):
        super(TestProjectModels, self).setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)

    def test_process_members(self):
        """
        Test that project members get added and removed properly.
        """
        #self.skipTest("Temporarily skipped")
        username_0 = 'Test_User_00'
        user_0 = self._create_user(username=username_0,
                                   password='0123456',
                                   is_superuser=False)
        username_1 = 'Test_User_01'
        user_1 = self._create_user(username=username_1,
                                   password='1234567',
                                   is_superuser=False)
        # Test that there are no members.
        msg = "Members: {}".format(self.project.members.all())
        self.assertEqual(self.project.members.count(), 0, msg)
        # Test that there is one members.
        self.project.process_members([user_0])
        msg = "Members: {}".format(self.project.members.all())
        self.assertEqual(self.project.members.count(), 1, msg)
        # Test that there are two members.
        self.project.process_members([user_0, user_1])
        msg = "Members: {}".format(self.project.members.all())
        self.assertEqual(self.project.members.count(), 2, msg)
        # Test that removing a member results in one member.
        self.project.process_members([user_1])
        users = self.project.members.all()
        msg = "Members: {}".format(users)
        self.assertEqual(self.project.members.count(), 1, msg)
        self.assertEqual(users[0].username, username_1, msg)

    def test_role(self):
        """
        Test that the role is set properly on the Membership object.
        """
        #self.skipTest("Temporarily skipped")
        # Test that the user is not a member.
        with self.assertRaises(Membership.DoesNotExist) as cm:
            self.project.get_role(self.user)

        # Add user to membership.
        self.project.process_members([self.user])
        # Test that the member has a role.
        role = self.project.get_role(self.user)
        msg = "This user has role {} which does not conform to '{}'.".format(
            Membership.ROLE_MAP.get(role),
            Membership.ROLE_MAP.get(Membership.PROJECT_OWNER))
        self.assertEqual(role, Membership.PROJECT_OWNER, msg)
        # Change the user's role.
        self.project.set_role(self.user, Membership.PROJECT_MANAGER)
        msg = "This user has role {} which does not conform to '{}'.".format(
            Membership.ROLE_MAP.get(role),
            Membership.ROLE_MAP.get(Membership.PROJECT_MANAGER))
        role = self.project.get_role(self.user)
        self.assertEqual(role, Membership.PROJECT_MANAGER, msg)
        # Test the clean for role on the Membership model.
        with self.assertRaises(ValidationError) as cm:
            self.project.set_role(self.user, 100)

    def test_has_authority(self):
        """
        Test that the user has authority to change objects in this project.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user
        username = "TestUser_02"
        user = self._create_user(username=username, password="123456789")
        # Test user with project.
        msg = "User {} should not have permission to access project {}".format(
            user, self.project)
        self.assertFalse(self.project.has_authority(user), msg)
        # Test that user has authority.
        self.project.process_members([user])
        msg = "User {} should have permission to access project {}".format(
            user, self.project)
        self.assertTrue(self.project.has_authority(user), msg)
