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

    def _create_user(self, username=_TEST_USERNAME, password=_TEST_PASSWORD,
                     is_superuser=True):
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

    def _create_location_default_record(self, name, description, owner=None,
                                        separator=None):
        if not owner:
            owner = self.user

        kwargs = {}
        kwargs['owner'] = owner
        kwargs['name'] = name
        kwargs['description'] = description

        if separator:
            kwargs['separator'] = separator

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
        # Create a location default.
        name = "Test Location Default"
        desc = "Test description."
        obj = self._create_location_default_record(name, desc)
        msg = "{} should be {} and {} should be {}".format(
            obj.name, name, obj.description, desc)
        self.assertEqual(obj.name, name, msg)
        self.assertEqual(obj.description, desc, msg)

    def test_clone_default_tree(self):
        #self.skipTest("Temporarily skipped")
        # Create a new user
        owner = self._create_user(username='Test_Non-Super',
                                  password='0123456789',
                                  is_superuser=False)
        # Create a location default.
        name = "Test Location Default"
        desc = "Test description."
        loc_def = self._create_location_default_record(name, desc)
        msg = "{} should be {} and {} should be {}".format(
            loc_def.name, name, loc_def.description, desc)
         # Create a location format object 0.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        fmt_obj_0 = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)
        # Create a location format object 1.
        char_definition = 'X\\d\\d'
        segment_order = 1
        description = "Test character definition."
        fmt_obj_1 = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)
        # Create a location format object 2.
        char_definition = 'B\\d\\dC\\d\\dR\\d\\d'
        segment_order = 2
        description = "Test character definition."
        fmt_obj_2 = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)
        # Make copy of location default and it's format objects.
        tree = LocationDefault.objects.clone_default_tree(
            loc_def, owner, owner)
        msg = ("Loc Default: {}, Loc Format: {}, Loc Format: {}, "
               "Loc Format: {}").format(
            loc_def, fmt_obj_0, fmt_obj_1, fmt_obj_2)
        self.assertEqual(len(tree), 4, msg)

    def test_delete_default_tree(self):
        #self.skipTest("Temporarily skipped")
        # Create a location default.
        name = "Test Location Default"
        desc = "Test description."
        loc_def = self._create_location_default_record(name, desc)
        msg = "{} should be {} and {} should be {}".format(
            loc_def.name, name, loc_def.description, desc)
         # Create a location format object 0.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        fmt_obj_0 = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)
        # Create a location format object 1.
        char_definition = 'X\\d\\d'
        segment_order = 1
        description = "Test character definition."
        fmt_obj_1 = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)
        # Create a location format object 2.
        char_definition = 'B\\d\\dC\\d\\dR\\d\\d'
        segment_order = 2
        description = "Test character definition."
        fmt_obj_2 = self._create_location_format_record(
            char_definition, segment_order, description, loc_def)
        # Create location code objects .
        code_0 = self._create_location_code_record("T01", fmt_obj_0)
        code_1 = self._create_location_code_record("X01", fmt_obj_1,
                                                   parent=code_0)
        code_1a = self._create_location_code_record("X02", fmt_obj_1,
                                                    parent=code_0)
        code_2 = self._create_location_code_record("B01C01R01", fmt_obj_2,
                                                   parent=code_1)
        code_2a = self._create_location_code_record("B01C01R01", fmt_obj_2,
                                                    parent=code_1a)
        # Test for correct number of objects.
        msg = "Location Default: {}".format(loc_def)
        self.assertEqual(LocationDefault.objects.count(), 1, msg)
        msg = "Location Formats: {}, {}, {}".format(
            fmt_obj_0, fmt_obj_1, fmt_obj_2)
        self.assertEqual(LocationFormat.objects.count(), 3, msg)
        msg = "Location Codes: {}, {}, {}".format(code_0, code_1, code_2)
        self.assertEqual(LocationCode.objects.count(), 5, msg)
        # Test delete_default_tree
        nodes = LocationDefault.objects.delete_default_tree(
            loc_def, self.user, self.user)
        #print nodes
        # Test for correct number of objects.
        msg = "Location Default: {}".format(loc_def)
        self.assertEqual(LocationDefault.objects.count(), 0, msg)
        msg = "Location Formats: {}, {}, {}".format(
            fmt_obj_0, fmt_obj_1, fmt_obj_2)
        self.assertEqual(LocationFormat.objects.count(), 0, msg)
        msg = "Location Codes: {}, {}, {}".format(code_0, code_1, code_2)
        self.assertEqual(LocationCode.objects.count(), 0, msg)

    def test_length_of_separator(self):
        """
        Test that the length of the separator is not longer than the defined
        length of the database column.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location default object.
        with self.assertRaises(ValidationError) as cm:
            obj = self._create_location_default_record(
                "Another Default", "Test Description 2", separator='--->')
            msg = "Created Object: {}".format(obj)
            self.assertFalse(obj, msg)

        msg = "Exception: {}".format(cm.exception)
        messages = [msg for msg in cm.exception.messages
                    if "The length of the separator is" in msg]
        self.assertTrue(messages, msg)


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
        formats = {
            # Should not have colon in format.
            r'A\d\d:B\d\d\d': "Invalid format, found separator ",
            r'': "Invalid format, found: ", # Empty format.
            r'[A\\\d\d]': "Invalid format, found: ", # Parse error.
            }
        segment_order = 0
        description = "Test failure."

        for fmt, message in formats.items():
            with self.assertRaises(ValidationError) as cm:
                obj = self._create_location_format_record(
                    fmt, segment_order, description, self.loc_def)
                msg = "Created object: {}".format(obj)
                self.assertFalse(obj, msg)

            msg = "Exception: {}".format(cm.exception)
            messages = [msg for msg in cm.exception.messages if message in msg]
            self.assertTrue(messages, msg)


class TestLocationCodeModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationCodeModel, self).__init__(name)

    def setUp(self):
        super(TestLocationCodeModel, self).setUp()
        # Create a valid location default object.
        self.name = "Test Location Default"
        desc = "Test description."
        self.loc_def = self._create_location_default_record(self.name, desc)
        # Create a location format object.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        self.loc_fmt = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)

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

    def test_invalid_child(self):
        #self.skipTest("Temporarily skipped")
        segment = "T01"
        obj_0 = self._create_location_code_record(segment, self.loc_fmt)
        msg = "{} should be {} and {} should be {}".format(
            obj_0.segment, segment,
            obj_0.char_definition.location_default.name, self.name)
        self.assertEqual(obj_0.segment, segment, msg)
        # Try to create a child to itself.
        with self.assertRaises(ValidationError):
            segment = "T01"
            obj_1 = self._create_location_code_record(segment, self.loc_fmt,
                                                      parent=obj_0)
            msg = "{} should be {} and {} should be {}".format(
                obj_1.segment, segment,
                obj_1.char_definition.location_default.name, self.name)
            self.assertFalse(obj_1, msg)

    def test_invalid_number_of_segments(self):
        #self.skipTest("Temporarily skipped")
        # Create a location code object.
        segment = "T01"
        obj_0 = self._create_location_code_record(segment, self.loc_fmt)
        msg = "{} should be {} and {} should be {}".format(
            obj_0.segment, segment,
            obj_0.char_definition.location_default.name, self.name)
        self.assertEqual(obj_0.segment, segment, msg)
        # Create 2nd location format object.
        char_definition = 'C\\d\\d' # Container nn
        segment_order = 1
        description = "Test character definition."
        loc_fmt_1 = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        # Create a 2nd location code parent.
        segment = "C01" # Container 01
        obj_1 = self._create_location_code_record(segment, loc_fmt_1,
                                                  parent=obj_0)
        msg = "{} should be {} and {} should be {}".format(
            obj_1.segment, segment,
            obj_1.char_definition.location_default.name, self.name)
        self.assertEqual(obj_1.segment, segment, msg)
        # Create 3rd location format object.
        char_definition = 'B\\d\\d' # Container nn
        segment_order = 2
        description = "Test character definition."
        loc_fmt_2 = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        # Create a 3nd location code parent.
        segment = "B01" # Bin 01
        obj_2 = self._create_location_code_record(segment, loc_fmt_2,
                                                  parent=obj_1)
        msg = "{} should be {} and {} should be {}".format(
            obj_2.segment, segment,
            obj_2.char_definition.location_default.name, self.name)
        self.assertEqual(obj_2.segment, segment, msg)
        # Try to create a 4nd parent, but with no new format object.
        with self.assertRaises(ValidationError):
            segment = "B02" # Bin 02
            obj_3 = self._create_location_code_record(segment, loc_fmt_2,
                                                      parent=obj_2)
            msg = "{} should be {} and {} should be {}".format(
                obj_3.segment, segment,
                obj_3.char_definition.location_default.name, self.name)
            self.assertFalse(obj_3, msg)

    def test_get_parents(self):
        #self.skipTest("Temporarily skipped")
        # Create a location code object.
        segment = "T01"
        obj_0 = self._create_location_code_record(segment, self.loc_fmt)
        msg = "{} should be {} and {} should be {}".format(
            obj_0.segment, segment,
            obj_0.char_definition.location_default.name, self.name)
        self.assertEqual(obj_0.segment, segment, msg)
        # Test get_parent
        parents = LocationCode.objects.get_parents(obj_0)
        msg = "parents: {}".format(parents)
        self.assertEqual(len(parents), 0, msg)
        # Create 2nd location format object.
        char_definition = 'C\\d\\d' # Container nn
        segment_order = 1
        description = "Test character definition."
        loc_fmt_1 = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        # Create a 2nd location code parent.
        segment = "C01" # Container 01
        obj_1 = self._create_location_code_record(segment, loc_fmt_1,
                                                  parent=obj_0)
        msg = "{} should be {} and {} should be {}".format(
            obj_1.segment, segment,
            obj_1.char_definition.location_default.name, self.name)
        self.assertEqual(obj_1.segment, segment, msg)
        # Test get_parent
        parents = LocationCode.objects.get_parents(obj_1)
        msg = "parents: {}".format(parents)
        self.assertEqual(len(parents), 1, msg)
        # Create 3rd location format object.
        char_definition = 'B\\d\\d' # Container nn
        segment_order = 2
        description = "Test character definition."
        loc_fmt_2 = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        # Create a 3nd location code parent.
        segment = "B01" # Bin 01
        obj_2 = self._create_location_code_record(segment, loc_fmt_2,
                                                  parent=obj_1)
        msg = "{} should be {} and {} should be {}".format(
            obj_2.segment, segment,
            obj_2.char_definition.location_default.name, self.name)
        self.assertEqual(obj_2.segment, segment, msg)
        # Test get_parent
        parents = LocationCode.objects.get_parents(obj_2)
        msg = "parents: {}".format(parents)
        self.assertEqual(len(parents), 2, msg)

    def test_get_all_root_trees(self):
        #self.skipTest("Temporarily skipped")
        # Create 1st tree.
        # Create a location code object.
        segment = "T01"
        obj_0 = self._create_location_code_record(segment, self.loc_fmt)
        msg = "{} should be {} and {} should be {}".format(
            obj_0.segment, segment,
            obj_0.char_definition.location_default.name, self.name)
        self.assertEqual(obj_0.segment, segment, msg)
        # Create 2nd location format object.
        char_definition = 'C\\d\\d' # Container nn
        segment_order = 1
        description = "Test character definition."
        loc_fmt_1 = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        # Create a 2nd location code parent.
        segment = "C01" # Container 01
        obj_1 = self._create_location_code_record(segment, loc_fmt_1,
                                                  parent=obj_0)
        msg = "{} should be {} and {} should be {}".format(
            obj_1.segment, segment,
            obj_1.char_definition.location_default.name, self.name)
        self.assertEqual(obj_1.segment, segment, msg)
        # Create 2nd tree.
        segment = "T02"
        obj_0 = self._create_location_code_record(segment, self.loc_fmt)
        msg = "{} should be {} and {} should be {}".format(
            obj_0.segment, segment,
            obj_0.char_definition.location_default.name, self.name)
        self.assertEqual(obj_0.segment, segment, msg)
        # Create 2nd location format object.
        char_definition = 'C\\d\\d' # Container nn
        segment_order = 1
        description = "Test character definition."
        loc_fmt_1 = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        # Create a 2nd location code parent.
        segment = "C01" # Container 01
        obj_1 = self._create_location_code_record(segment, loc_fmt_1,
                                                  parent=obj_0)
        msg = "{} should be {} and {} should be {}".format(
            obj_1.segment, segment,
            obj_1.char_definition.location_default.name, self.name)
        self.assertEqual(obj_1.segment, segment, msg)
        # get_all_root_trees
        trees = LocationCode.objects.get_all_root_trees(segment, self.user)
        msg = "Root trees: {}".format(trees)
        self.assertEqual(len(trees), 2, msg)

    def test_invalid_segment(self):
        """
        Test that the segment validates properly.
        """
        #self.skipTest("Temporarily skipped")
        segments = ('T:01', 'S01')

        for segment in segments:
            with self.assertRaises(ValidationError) as cm:
                obj = self._create_location_code_record(segment, self.loc_fmt)
                msg = "Created object: {}".format(obj)
                self.assertFalse(obj, msg)

            msg = "Exception: {}".format(cm.exception)
            messages = [msg for msg in cm.exception.messages
                        if "does not conform to" in msg]
            self.assertTrue(messages, msg)

    def test_segment_not_parent_to_itself(self):
        """
        Test that a segment is not a parent to itself.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location code object.
        segment = "T01"
        obj0 = self._create_location_code_record(segment, self.loc_fmt)

        with self.assertRaises(ValidationError) as cm:
            obj = self._create_location_code_record(
                segment, self.loc_fmt, parent=obj0)
            msg = "Created object: {}".format(obj)
            self.assertFalse(obj, msg)

        msg = "Exception: {}".format(cm.exception)
        self.assertTrue("child to itself." in cm.exception.messages[0], msg)

    def test_segments_have_same_location_default(self):
        """
        Test that all the segments in a given tree have the same location
        default.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location default object.
        loc_def1 = self._create_location_default_record(
            "Another Default", "Test Description 2")
        # Create a location format object with loc_def1.
        char_definition = 'C\\d\\dR\\d\\d'
        segment_order = 1
        description = "Test character definition level 1."
        loc_fmt1 = self._create_location_format_record(
            char_definition, segment_order, description, loc_def1)
        # Create two location codes.
        obj0 = self._create_location_code_record("T01", self.loc_fmt)

        with self.assertRaises(ValidationError) as cm:
            obj1 = self._create_location_code_record("C01R01", loc_fmt1,
                                                     parent=obj0)
            msg = "Created object: {}".format(obj)
            self.assertFalse(obj, msg)

        msg = "Exception: {}".format(cm.exception)
        self.assertTrue("same location default." in cm.exception.messages[0],
                        msg)

    def test_number_segments_number_formats(self):
        """
        Test that the number of segments defined are equal to or less than
        the number of formats for this location default.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location format object.
        char_definition = 'C\\d\\dR\\d\\d'
        segment_order = 1
        description = "Test character definition level 1."
        loc_fmt1 = self._create_location_format_record(
            char_definition, segment_order, description, self.loc_def)
        # Create three location codes, last one will fail.
        obj0 = self._create_location_code_record(
            "T01", self.loc_fmt)
        obj1 = self._create_location_code_record(
            "C01R01", loc_fmt1, parent=obj0)

        with self.assertRaises(ValidationError) as cm:
            obj2 = self._create_location_code_record(
                "C02R02", loc_fmt1, parent=obj1)
            msg = "Created Object: {}".format(obj2)
            self.assertFalse(obj2, msg)

        msg = "Exception: {}".format(cm.exception)
        self.assertTrue("There are more segments " in cm.exception.messages[0],
                        msg)
