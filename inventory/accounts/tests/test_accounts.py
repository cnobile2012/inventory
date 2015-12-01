# -*- coding: utf-8 -*-
#
# inventory/accounts/tests/test_accounts.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Question, Answer

User = get_user_model()


class BaseAccounts(TestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(BaseAccounts, self).__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True,
                     role=User.DEFAULT_USER):
        user = User.objects.create_user(username=username, password=password)
        user.first_name = "Test"
        user.last_name = "User"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.role = role
        user.save()
        return user

    def _create_question_record(self, question):
        kwargs = {}
        kwargs['question'] = question
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Question.objects.create(**kwargs)

    def _create_answer_record(self, answer, question_obj):
        kwargs = {}
        kwargs['answer'] = answer
        kwargs['question'] = question_obj
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Answer.objects.create(**kwargs)


class TestUser(BaseAccounts):

    def __init__(self, name):
        super(TestUser, self).__init__(name)


    def test_create_superuser(self):
        """
        Test that a superuser was created.
        """
        username = "TestSuperuser"
        email = "TSU@example.com"
        password = "{TSU_999}"
        user = User.objects.create_superuser(username, email, password)
        msg = "Username: {}, email: {}, is_superuser: {}, role: {}".format(
            user.username, user.email, user.is_superuser, user.role)
        self.assertEquals(user.username, username, msg)
        self.assertEquals(user.email, email, msg)
        self.assertEquals(user.is_superuser, True, msg)
        self.assertEquals(user.role, User.DEFAULT_USER, msg)

    def test_create_user(self):
        """
        Test that a user was created.
        """
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = User.objects.create_user(username, email, password)
        msg = "Username: {}, email: {}, is_superuser: {}, role: {}".format(
            user.username, user.email, user.is_superuser, user.role)
        self.assertEquals(user.username, username, msg)
        self.assertEquals(user.email, email, msg)
        self.assertEquals(user.is_superuser, False, msg)
        self.assertEquals(user.role, User.DEFAULT_USER, msg)

    def test_update_user(self):
        """
        Test that a user is updated.
        """
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
        self.assertEquals(user.username, username, msg)
        self.assertEquals(user.email, email, msg)
        self.assertEquals(user.is_superuser, True, msg)
        self.assertEquals(user.role, User.ADMINISTRATOR, msg)
        self.assertEquals(user.address_01, extra_fields.get('address_01'), msg)
        self.assertEquals(user.postal_code, extra_fields.get('postal_code'),
                          msg)

    def test_get_full_name_reversed(self):
        """
        Test that the users name gets reversed so last name is first.
        """
        name = self.user.get_full_name_reversed()
        msg = "Username: {}, First Name: {}, Last Name: {}".format(
            self.user.username, self.user.first_name, self.user.last_name)
        self.assertEquals(name, "{}, {}".format(self.user.last_name,
                                                self.user.first_name), msg)

    def test_process_answers(self):
        """
        Test that answers get added and removed properly from the user.
        """
        # Create some questions.
        q1 = self._create_question_record("What is your favorite color?")
        q2 = self._create_question_record("What is your favorite animal?")
        q3 = self._create_question_record("In what country is New York?")
        # Create answers.
        a1 = self._create_answer_record("Blue", q1)
        a2 = self._create_answer_record("Dog", q2)
        a3 = self._create_answer_record("USA", q3)
        # Set the two answers on the user.
        self.user.process_answers((q1, q2))
        answers = [a.pk for a in self.user.answers.all()]
        msg = "q1: {}, q2: {}, q3: {}".format(q1, q2, q3)
        self.assertEquals(self.user.answers.count(), 2, msg)
        self.assertTrue(q1.pk in answers and q2.pk in answers, msg)
        # Remove one answer.
        self.user.process_answers((q1,))
        answers = [a.pk for a in self.user.answers.all()]
        self.assertEquals(self.user.answers.count(), 1, msg)
        self.assertTrue(q1.pk in answers, msg)
        # Add a new answer.
        self.user.process_answers((q1, q3))
        answers = [a.pk for a in self.user.answers.all()]
        self.assertEquals(self.user.answers.count(), 2, msg)
        self.assertTrue(q1.pk in answers and q3.pk in answers, msg)


