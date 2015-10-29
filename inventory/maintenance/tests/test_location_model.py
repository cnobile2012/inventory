# -*- coding: utf-8 -*-
#
# inventory/maintenance/tests/test_location_model.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import LocationDefault, LocationFormat, LocationCode

User = get_user_model()


class BaseLocation(TestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(BaseLocation, self).__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True):
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

    def _create_location_default_record(self, name, description):
        kwargs = {}
        kwargs['owner'] = self.user
        kwargs['name'] = name
        kwargs['description'] = description
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationDefault.objects.create(**kwargs)

    def _create_location_format_record(self, char_definition, segment_order,
                                       description, location_default):
        kwargs = {}
        kwargs['char_definition'] = char_definition
        kwargs['location_default'] = location_default
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationFormat.objects.create(**kwargs)

    def _create_location_code_record(self, segment, char_definition,
                                     parent=None):
        kwargs = {}
        kwargs['char_definition'] = char_definition
        kwargs['segment'] = segment
        kwargs['parent'] = parent
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return LocationCode.objects.create(**kwargs)


class TestLocationDefaultModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationDefaultModel, self).__init__(name)

    def test_create_location_default_record(self):
        #self.skipTest("Temporarily skipped")
        name = "Test Location Default"
        desc = "Test description."
        obj = self._create_location_default_record(name, desc)
        msg = "{} should be {} and {} should be {}".format(
            obj.name, name, obj.description, desc)
        self.assertEqual(obj.name, name, msg)
        self.assertEqual(obj.description, desc, msg)


class TestLocationFormatModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationFormatModel, self).__init__(name)

    def setUp(self):
        super(TestLocationFormatModel, self).setUp()
        # Create a valid location default object.
        self.name = "Test Location Default"
        desc = "Test description."
        self.loc_def = self._create_location_default_record(self.name, desc)

    def test_create_location_format_record(self):
        #self.skipTest("Temporarily skipped")
        # Create a location format object.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        obj = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        msg = "{} should be {} and {} should be {}".format(
            obj.char_definition, char_definition,
            obj.location_default.name, self.name)
        self.assertEqual(obj.char_definition, char_definition, msg)
        self.assertEqual(obj.location_default.name, self.name, msg)

    def test_get_char_definition(self):
        #self.skipTest("Temporarily skipped")
        # Create a location format object.
        char_definition = r'A\d\dB\d\d\d'
        segment_order = 0
        description = "Test character definition."
        obj = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        # Get format object.
        fmt_obj = LocationFormat.objects.get_char_definition(
            self.user, self.name, char_definition)
        msg = "Created object: {}, queried object: {}".format(obj, fmt_obj)
        self.assertEqual(obj, fmt_obj, msg)

    def test_failure_on_record_creation(self):
        #self.skipTest("Temporarily skipped")
        formats = [
            r'A\d\d:B\d\d\d', # Should not have colon in format.
            r'', # Empty format.
            r'[A\\\d\d]', # Parse error.
            ]
        segment_order = 0
        description = "Test failure."

        for fmt in formats:
            with self.assertRaises(ValidationError):
                obj = self._create_location_format_record(
                    fmt, segment_order, description, self.loc_def)
                msg = "Created object: {}".format(obj)
                self.assertFalse(obj, msg)


class TestLocationCodeModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationCodeModel, self).__init__(name)

    def setUp(self):
        super(TestLocationCodeModel, self).setUp()
        # Create a valid location default object.
        self.name = "Test Location Default"
        desc = "Test description."
        loc_def = self._create_location_default_record(self.name, desc)
        # Create a location format object.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        self.loc_fmt = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)

    def test_create_location_code(self):
        #self.skipTest("Temporarily skipped")
        # Create a location code object.
        segment = "T01"
        obj = self._create_location_code_record(segment, self.loc_fmt)
        msg = "{} should be {} and {} should be {}".format(
            obj.segment, segment,
            obj.char_definition.location_default.name, self.name)
        self.assertEqual(obj.segment, segment, msg)
        self.assertEqual(obj.char_definition.location_default.name,
                         self.name, msg)
