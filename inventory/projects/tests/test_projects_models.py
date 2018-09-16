# -*- coding: utf-8 -*-
#
# inventory/projects/tests/test_projects_models.py
#

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from inventory.common.tests.base_tests import BaseTest

from ..models import InventoryType, Project, Membership

UserModel = get_user_model()


class TestInventoryType(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()

    def test_str(self):
        """
        Test that __str__ on the class returns the record's name.
        """
        #self.skipTest("Temporarily skipped")
        inventory_type = self._create_inventory_type()
        name = str(inventory_type)
        msg = "__str__ name: {}, object name: {}".format(
            name, inventory_type.name)
        self.assertEqual(name, inventory_type.name, msg)


class TestProject(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
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
        # Test that there is one members.
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

    def test_get_role(self):
        """
        Test that get_role returns the correct role from the Membership
        model.
        """
        #self.skipTest("Temporarily skipped")
        # Create a new user
        kwargs = {}
        kwargs['username'] = "AnotherTestUser"
        kwargs['password'] = "AVeryBadPassword"
        user = self._create_user(**kwargs)
        # Test that the user is not a member.
        with self.assertRaises(Membership.DoesNotExist) as cm:
            self.project.get_role(user)

        # Add user to membership.
        self.project.process_members([user])
        # Change the user's role.
        self.project.set_role(user, Membership.PROJECT_OWNER)
        role = self.project.get_role(user)
        # Test that the member has a role.
        msg = "This user has role '{}' which does not conform to '{}'.".format(
            Membership.ROLE_MAP.get(role),
            Membership.ROLE_MAP.get(Membership.PROJECT_OWNER))
        self.assertEqual(role, Membership.PROJECT_OWNER, msg)

    def test_set_role(self):
        """
        Test that set_role sets the correct role on the Membership model.
        """
        # Create a new user
        kwargs = {}
        kwargs['username'] = "AnotherTestUser"
        kwargs['password'] = "AVeryBadPassword"
        user = self._create_user(**kwargs)
        # Test that Membership.DoesNotExist is raised.
        with self.assertRaises(Membership.DoesNotExist) as cm:
            self.project.set_role(user, Membership.PROJECT_MANAGER)

        # Add user to membership.
        self.project.process_members([user])
        # Change the user's role.
        self.project.set_role(user, Membership.PROJECT_MANAGER)
        role = self.project.get_role(user)
        msg = "This user has role {} which does not conform to '{}'.".format(
            Membership.ROLE_MAP.get(role),
            Membership.ROLE_MAP.get(Membership.PROJECT_MANAGER))
        role = self.project.get_role(user)
        self.assertEqual(role, Membership.PROJECT_MANAGER, msg)

        # Test clean on the Membership model for the proper exception.
        with self.assertRaises(ValidationError) as cm:
            self.project.set_role(user, 100)

    def test_superuser_has_authority(self):
        """
        Test that the superuser has authority to change objects in
        this project.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user
        username = "TestUser_02"
        user = self._create_user(
            username=username, password="123456789", is_superuser=True)
        msg = "User {} should have permission to access project {}".format(
            user, self.project)
        self.assertTrue(self.project.has_authority(user), msg)

    def test_ADMINISTRATOR_has_authority(self):
        """
        Test that an ADMINISTRATOR has authority to change objects in
        this project.
        """
        #self.skipTest("Temporarily skipped")
        # Create a user
        username = "TestUser_02"
        user = self._create_user(
            username=username, password="123456789", is_superuser=False,
            role=UserModel.ADMINISTRATOR)
        msg = "User {} should have permission to access project {}".format(
            user, self.project)
        self.assertTrue(self.project.has_authority(user), msg)

    def test_DEFAULT_USER_has_authority(self):
        """
        Test that an DEFAULT_USER has authority to change objects in
        this project.
        """
        #self.skipTest("Temporarily skipped")
        username = "TestUser_02"
        user = self._create_user(
            username=username, password="123456789", is_superuser=False)
        # Test that user has no authority with project.
        msg = "User {} should not have permission to access project {}".format(
            user, self.project)
        self.assertFalse(self.project.has_authority(user), msg)
        # Test that user has authority with project.
        self.project.process_members([user])
        msg = "User {} should have permission to access project {}".format(
            user, self.project)
        self.assertTrue(self.project.has_authority(user), msg)

    def test_image_thumb_producer(self):
        """
        Test that the image thumb producer works properly.
        """
        #self.skipTest("Temporarily skipped")
        # Test no image
        thumb = self.project.image_thumb_producer()
        msg = "Invalid result '{}', should be 'No Image'".format(thumb)
        self.assertEqual(self.project.image_thumb_producer(), "No Image", msg)
        # Test with image
        self.project.image.name = "T0-92.jpg"
        self.project.save()
        filename = "/media/T0-92.jpg"
        thumb = self.project.image_thumb_producer()
        msg = "Invalid filename '{}', should be {}".format(thumb, filename)
        self.assertTrue(filename in thumb, msg)


class TestMembership(BaseTest):

    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)

    def test_str(self):
        """
        Test that __str__ on the class returns the record's name.
        """
        #self.skipTest("Temporarily skipped")
        membership = Membership.objects.get(
            user=self.user, project=self.project)
        result = str(membership)
        obj_result = "{} ({})".format(
            self.user.get_full_name_reversed(), self.project.name)
        msg = "__str__ result: {}, object result: {}".format(
            result, obj_result)
        self.assertEqual(result, obj_result, msg)
