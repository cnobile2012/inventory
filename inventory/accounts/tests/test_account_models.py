# -*- coding: utf-8 -*-
#
# inventory/accounts/tests/test_accounts.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from inventory.projects.models import Project

from inventory.common.tests.base_tests import BaseTest

from ..models import Question, Answer, create_hash

User = get_user_model()


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
        user = User.objects.create_superuser(username, email, password)
        msg = "Username: {}, email: {}, is_superuser: {}, role: {}".format(
            user.username, user.email, user.is_superuser, user.role)
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, True, msg)
        self.assertEqual(user.role, User.ADMINISTRATOR, msg)

    def test_create_user(self):
        """
        Test that a user was created.
        """
        #self.skipTest("Temporarily skipped")
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = User.objects.create_user(username, email, password)
        msg = "Username: {}, email: {}, is_superuser: {}, role: {}".format(
            user.username, user.email, user.is_superuser, user.role)
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, False, msg)
        self.assertEqual(user.role, User.DEFAULT_USER, msg)

    def test_update_user(self):
        """
        Test that a user is updated.
        """
        #self.skipTest("Temporarily skipped")
        username = self.user.username
        email = self.user.email
        extra_fields = {}
        extra_fields['role'] = User.ADMINISTRATOR
        extra_fields['address_01'] = "123 Some Place Street"
        extra_fields['postal_code'] = "12345"
        user = User.objects.update_user(username=username, email=email,
                                        **extra_fields)
        msg = ("Username: {}, email: {}, is_superuser: {}, role: {}, "
               "address_01: {}, postal_code: {}").format(
            user.username, user.email, user.is_superuser, user.role,
            user.address_01, user.postal_code)
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, True, msg)
        self.assertEqual(user.role, User.ADMINISTRATOR, msg)
        self.assertEqual(user.address_01, extra_fields.get('address_01'), msg)
        self.assertEqual(user.postal_code, extra_fields.get('postal_code'), msg)

    def test_get_full_name_reversed(self):
        """
        Test that the users name gets reversed so last name is first.
        """
        #self.skipTest("Temporarily skipped")
        name = self.user.get_full_name_reversed()
        msg = "Username: {}, First Name: {}, Last Name: {}".format(
            self.user.username, self.user.first_name, self.user.last_name)
        self.assertEqual(name, "{}, {}".format(self.user.last_name,
                                                self.user.first_name), msg)

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
        # Create some stupid questions.
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


class TestQuestion(BaseAccountModels):

    def __init__(self, name):
        super(TestQuestion, self).__init__(name)

    def test_get_active_questions(self):
        """
        Test that only active questions are returned.
        """
        #self.skipTest("Temporarily skipped")
        # Create some stupid questions.
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
        # Create a stupid question.
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
