# -*- coding: utf-8 -*-
#
# inventory/accounts/tests/test_accounts.py
#

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from inventory.projects.models import Project

from inventory.common.tests.base_tests import BaseTest

from ..models import Question, Answer, create_hash

UserModel = get_user_model()


class BaseAccountModels(BaseTest):

    def __init__(self, name):
        super(BaseAccountModels, self).__init__(name)

    def setUp(self):
        super(BaseAccountModels, self).setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)


class TestUser(BaseAccountModels):

    def __init__(self, name):
        super(TestUser, self).__init__(name)

    def test_create_superuser(self):
        """
        Test that a superuser was created.
        """
        #self.skipTest("Temporarily skipped")
        username = "TestSuperuser"
        email = "TSU@example.com"
        password = "{TSU_999}"
        user = UserModel.objects.create_superuser(username, email, password)
        msg = "Username: {}, email: {}, is_superuser: {}, role: {}".format(
            user.username, user.email, user.is_superuser, user.role)
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, True, msg)
        self.assertEqual(user.role, UserModel.ADMINISTRATOR, msg)

    def test_create_user(self):
        """
        Test that a user was created.
        """
        #self.skipTest("Temporarily skipped")
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = UserModel.objects.create_user(username, email, password)
        msg = "Username: {}, email: {}, is_superuser: {}, role: {}".format(
            user.username, user.email, user.is_superuser, user.role)
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, False, msg)
        self.assertEqual(user.role, UserModel.DEFAULT_USER, msg)

        # No username
        with self.assertRaises(ValueError) as cm:
            user = UserModel.objects.create_user('', email, password)

        # No password with email
        user = UserModel.objects.create_user("SecondTestUser", email, None)
        msg = "send_email: {}, need_password: {}".format(
            user.send_email, user.need_password)
        self.assertTrue(user.send_email, msg)
        self.assertTrue(user.need_password, msg)

        # No password and email
        with self.assertRaises(ValueError) as cm:
            user = UserModel.objects.create_user("ThirdTestUser", '', None)

    def test_invalid_role(self):
        """
        Test that for invalid role.
        """
        #self.skipTest("Temporarily skipped")
        kwargs = {}
        kwargs['username'] = "TestUser_01"
        kwargs['password'] = "9876543210"
        kwargs['role'] = 999
        user = UserModel(**kwargs)

        with self.assertRaises(ValidationError) as cm:
            user.save()

        msg = "Found: {}".format(cm.exception)
        self.assertTrue(" is not a valid choice." in str(cm.exception), msg)

    def test_get_full_name_or_username(self):
        """
        Test that the users full name is returned or the username.
        """
        #self.skipTest("Temporarily skipped")
        # Test the full name.
        name = self.user.get_full_name_or_username()
        msg = "Username: {}, First Name: {}, Last Name: {}".format(
            self.user.username, self.user.first_name, self.user.last_name)
        fullname = "{} {}".format(self.user.first_name, self.user.last_name)
        self.assertEqual(name, fullname, msg)
        # Test the username.
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = UserModel.objects.create_user(username, email, password)
        name = user.get_full_name_or_username()
        msg = "name: {}, username: {}".format(name, username)
        self.assertTrue(name == username, msg)

    def test_get_full_name_reversed(self):
        """
        Test that the users name gets reversed so last name is first.
        """
        #self.skipTest("Temporarily skipped")
        name = self.user.get_full_name_reversed()
        msg = "Username: {}, First Name: {}, Last Name: {}".format(
            self.user.username, self.user.first_name, self.user.last_name)
        reversed_name = "{}, {}".format(self.user.last_name,
                                        self.user.first_name)
        self.assertEqual(name, reversed_name, msg)
        self.assertTrue(reversed_name == str(self.user), msg)
        # Test with no first and last names
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = UserModel.objects.create_user(username, email, password)
        name = user.get_full_name_reversed()
        msg = "name: {}, username: {}".format(name, username)
        self.assertTrue(name == username, msg)

    def test_get_absolute_url(self):
        """
        Test that the users API uri is returned.
        """
        #self.skipTest("Temporarily skipped")
        uri = self.user.get_absolute_url()
        msg = "URI: {}, public_id: {}".format(uri, self.user.public_id)
        self.assertTrue(self.user.public_id in uri, msg)

    def test_process_projects(self):
        """
        Test that projects can be added and removed from a user.
        """
        #self.skipTest("Temporarily skipped")
        # Create a project.
        p1 = self._create_project(self.inventory_type, "My Electronic Parts")
        p2 = self._create_project(self.inventory_type, "My Music")
        p3 = self._create_project(self.inventory_type, "My Stamp Collection")
        # Set two projects on the user.
        self.user.process_projects((p1, p2))
        projects = self.user.projects.all()
        msg = "Projects: {}".format(projects)
        pks = [p.pk for p in projects]
        self.assertEqual(projects.count(), 2, msg)
        self.assertTrue(p1.pk in pks and p2.pk in pks, msg)
        # Remove one project.
        self.user.process_projects((p1,))
        projects = self.user.projects.all()
        msg = "Projects: {}".format(projects)
        pks = [p.pk for p in projects]
        self.assertEqual(projects.count(), 1, msg)
        self.assertTrue(p1.pk in pks, msg)
        # Add a new project.
        self.user.process_projects((p1, p3))
        projects = self.user.projects.all()
        msg = "Projects: {}".format(projects)
        pks = [p.pk for p in projects]
        self.assertEqual(projects.count(), 2, msg)
        self.assertTrue(p1.pk in pks and p3.pk in pks, msg)

    def test_get_unused_questions(self):
        """
        Test that only unused questions are returned as choices.
        """
        #self.skipTest("Temporarily skipped")
        # Create some questions.
        q1 = self._create_question("What is your favorite color?")
        q2 = self._create_question("What is your favorite animal?")
        q3 = self._create_question("In what country is New York?")
        # Create two answers.
        a1 = self._create_answer(q1, "Blue", self.user)
        a2 = self._create_answer(q2, "Dog", self.user)
        # Get any remaining questions that have not been used yet.
        questions = self.user.get_unused_questions()
        msg = "Unused Questions: {}".format(questions)
        self.assertEqual(len(questions), 1, msg)
        self.assertTrue(q3.pk in [q.pk for q in questions], msg)

    def test_full_name_reversed_producer(self):
        """
        Test that the full_name_reversed_producer() method produces the
        reversed full name for the admin.
        """
        #self.skipTest("Temporarily skipped")
        name = self.user.full_name_reversed_producer()
        msg = "Username: {}, First Name: {}, Last Name: {}".format(
            self.user.username, self.user.first_name, self.user.last_name)
        reversed_name = "{}, {}".format(self.user.last_name,
                                        self.user.first_name)
        self.assertEqual(name, reversed_name, msg)
        self.assertTrue(reversed_name == str(self.user), msg)
        # Test with no first and last names
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = UserModel.objects.create_user(username, email, password)
        name = user.full_name_reversed_producer()
        msg = "name: {}, username: {}".format(name, username)
        self.assertTrue(name == username, msg)

    def test_projects_producer(self):
        """
        Test that the projects_producer() method produces the projects the
        user has for the admin.
        """
        #self.skipTest("Temporarily skipped")
        self.user.process_projects((self.project,))
        projects = self.user.projects_producer()
        msg = "Projects found: {}, has: {}".format(projects, self.project)
        self.assertTrue(len(projects.split('<br />')) == 1, msg)

    def test_image_url_producer(self):
        """
        Test that the image_url_producer() method displays an image from the
        admin.
        """
        #self.skipTest("Temporarily skipped")
        # Test no image.
        image = self.user.image_url_producer()
        msg = "Image: {}".format(image)
        self.assertEqual(image, "No Image URL", msg)
        self.user.picture = "Test Image"
        self.user.save()
        image = self.user.image_url_producer()
        msg = "Image: {}".format(image)
        self.assertTrue('href' in image, msg)

    def test_image_thumb_producer(self):
        """
        Test that the image_thumb_producer() method displays an image in the
        admin.
        """
        image = self.user.image_thumb_producer()
        msg = "Image: {}".format(image)
        self.assertEqual(image, "No Image", msg)
        self.user.picture = "Test Image"
        self.user.save()
        image = self.user.image_thumb_producer()
        msg = "Image: {}".format(image)
        self.assertTrue('src' in image, msg)


class TestQuestion(BaseAccountModels):

    def __init__(self, name):
        super(TestQuestion, self).__init__(name)

    def test_get_active_questions(self):
        """
        Test that only active questions are returned.
        """
        #self.skipTest("Temporarily skipped")
        # Create some questions.
        q1 = self._create_question("What is your favorite color?")
        q2 = self._create_question("What is your favorite animal?",
                                   active=False)
        q3 = self._create_question("In what country is New York?")
        # Get the active questions.
        questions = Question.objects.get_active_questions()
        msg = "Active Questions: {}".format(questions)
        self.assertEqual(len(questions), 2, msg)
        self.assertTrue(q2.pk not in [q.pk for q in questions], msg)


class TestAnswer(BaseAccountModels):

    def __init__(self, name):
        super(TestAnswer, self).__init__(name)

    def test_model_validation(self):
        """
        Test that the validation works for the answer field.
        """
        #self.skipTest("Temporarily skipped")
        # Create a question.
        q1 = self._create_question("What is your favorite color?")
        # Create an answer to the question.
        answer = "Blue"
        a1 = self._create_answer(q1, answer, self.user)
        # Check that the answer is encripted.
        algorithum, hash_value = create_hash(answer, Answer.ANSWER_SALT)
        msg = "Question: {}, algorithum: {}".format(a1, algorithum)
        self.assertEqual(hash_value, a1.answer, msg)
        # Check that the hash of the answer does not change on subsequent
        # updates to the answer where the answer itself does not change.
        a1.save()
        self.assertEqual(hash_value, a1.answer, msg)
        # Check that the hash of the answer does change on subsequent
        # updates to the answer where the answer itself does change.
        a1.answer = "Green"
        a1.save()
        self.assertTrue(algorithum in a1.answer, msg)
        self.assertNotEqual(hash_value, a1.answer, msg)
