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

from ..models import Question, Answer, create_hash

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

    def _create_question_record(self, question, active=True):
        kwargs = {}
        kwargs['question'] = question
        kwargs['active'] = active
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

    def _create_project_record(self, name, public=True):
        kwargs = {}
        kwargs['name'] = name
        kwargs['public'] = public
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Project.objects.create(**kwargs)


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
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, True, msg)
        self.assertEqual(user.role, User.DEFAULT_USER, msg)

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
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, False, msg)
        self.assertEqual(user.role, User.DEFAULT_USER, msg)

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
        name = self.user.get_full_name_reversed()
        msg = "Username: {}, First Name: {}, Last Name: {}".format(
            self.user.username, self.user.first_name, self.user.last_name)
        self.assertEqual(name, "{}, {}".format(self.user.last_name,
                                                self.user.first_name), msg)

    def test_process_projects(self):
        """
        Test that projects can be added and removed from a user.
        """
        # Create a project.
        p1 = self._create_project_record("My Electronic Parts")
        p2 = self._create_project_record("My Music")
        p3 = self._create_project_record("My Stamp Collection")
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
        self.user.process_answers((a1, a2))
        answers = self.user.answers.all()
        msg = "Answers: {}".format(answers)
        pks = [a.pk for a in answers]
        self.assertEqual(answers.count(), 2, msg)
        self.assertTrue(a1.pk in pks and a2.pk in pks, msg)
        # Remove one answer.
        self.user.process_answers((a1,))
        answers = self.user.answers.all()
        msg = "Answers: {}".format(answers)
        pks = [a.pk for a in answers]
        self.assertEqual(answers.count(), 1, msg)
        self.assertTrue(a1.pk in pks, msg)
        # Add a new answer.
        self.user.process_answers((a1, a3))
        answers = self.user.answers.all()
        msg = "Answers: {}".format(answers)
        pks = [a.pk for a in answers]
        self.assertEqual(answers.count(), 2, msg)
        self.assertTrue(a1.pk in pks and a3.pk in pks, msg)

    def test_get_unused_questions(self):
        """
        Test that only unused questions are returned as choices.
        """
        # Create some stupid questions.
        q1 = self._create_question_record("What is your favorite color?")
        q2 = self._create_question_record("What is your favorite animal?")
        q3 = self._create_question_record("In what country is New York?")
        # Create two answers.
        a1 = self._create_answer_record("Blue", q1)
        a2 = self._create_answer_record("Dog", q2)
        # Set the anwers on the user object.
        self.user.process_answers((a1, a2))
        # Get any remaining questions that have not been used yet.
        questions = self.user.get_unused_questions()
        msg = "Unused Questions: {}".format(questions)
        self.assertEqual(len(questions), 1, msg)
        self.assertTrue(q3.pk in [q.pk for q in questions], msg)


class TestQuestion(BaseAccounts):

    def __init__(self, name):
        super(TestQuestion, self).__init__(name)

    def test_get_active_questions(self):
        """
        Test that only active questions are returned.
        """
        # Create some stupid questions.
        q1 = self._create_question_record("What is your favorite color?")
        q2 = self._create_question_record("What is your favorite animal?",
                                          active=False)
        q3 = self._create_question_record("In what country is New York?")
        # Get the active questions.
        questions = Question.objects.get_active_questions()
        msg = "Active Questions: {}".format(questions)
        self.assertEqual(len(questions), 2, msg)
        self.assertTrue(q2.pk not in [q.pk for q in questions], msg)


class TestAnswer(BaseAccounts):

    def __init__(self, name):
        super(TestAnswer, self).__init__(name)

    def test_model_validation(self):
        """
        Test that the validation works for the answer field.
        """
        # Create a stupid question.
        q1 = self._create_question_record("What is your favorite color?")
        # Create an answer to the question.
        answer = "Blue"
        a1 = self._create_answer_record(answer, q1)
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

    def test_process_owner(self):
        """
        Test that the owner of the answer gets attached to the answer.
        """
        # Create a stupid question.
        q1 = self._create_question_record("What is your favorite color?")
        # Create an answer to the question.
        a1 = self._create_answer_record("Blue", q1)
        # Test that there is no owner associated with this answer.
        msg = "Question: {}".format(a1)
        self.assertFalse(a1.owners.all().count(), msg)
        # Attach user to the answer.
        a1.process_owner([self.user])
        self.assertTrue(a1.owners.all().count() == 1, msg)
        self.assertTrue(self.user.answers.all().count() == 1, msg)
