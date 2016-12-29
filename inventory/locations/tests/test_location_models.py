# -*- coding: utf-8 -*-
#
# inventory/maintenance/tests/test_location_models.py
#

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from inventory.common.tests.base_tests import BaseTest

from ..models import LocationSetName, LocationFormat, LocationCode

User = get_user_model()


class BaseLocation(BaseTest):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(BaseLocation, self).__init__(name)

    def setUp(self):
        super(BaseLocation, self).setUp()
        self.inventory_type = self._create_inventory_type()
        self.project = self._create_project(self.inventory_type)


class TestLocationSetNameModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationSetNameModel, self).__init__(name)

    def setUp(self):
        super(TestLocationSetNameModel, self).setUp()

    def test_auto_root_creation(self):
        """
        Test that when a set name is created that both ROOT format and code
        records are also created.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location set name.
        loc_set_name = self._create_location_set_name(
            self.project, name="My Set Name")
        # Test that we have a ROOT format.
        lf_root = LocationFormat.objects.get_root_format(loc_set_name)
        self.assertTrue(lf_root.char_definition == LocationCode.ROOT_NAME)
        # Test that we have a ROOT code.
        lcs = LocationCode.objects.filter(
            location_format=lf_root, segment=LocationCode.ROOT_NAME)
        msg = "Found {} LocationCode objects, should be 1".format(lcs.count())
        self.assertTrue(lcs.count() == 1, msg)

    def setup_set_name_tree(self, project, name, desc, shared):
        # Create a location default.
        kwargs = {}
        kwargs['description'] = desc
        kwargs['shared'] = shared
        loc_set_name = self._create_location_set_name(
            project, name=name, **kwargs)
        msg = "{} should be {} and {} should be {}".format(
            loc_set_name.name, name, loc_set_name.description, desc)
        # Get the root location format.
        fmt_root = LocationFormat.objects.get_root_format(loc_set_name)
        # Create a location format object 0.
        char_definition = 'T\\d\\d'
        segment_order = 0
        desc = "Test character definition."
        kwargs = {}
        kwargs['description'] = desc
        kwargs['segment_order'] = segment_order
        fmt_0 = self._create_location_format(
            loc_set_name, char_definition, **kwargs)
        # Create a location format object 1.
        char_definition = 'X\\d\\d'
        segment_order = 1
        description = "Test character definition."
        kwargs['description'] = desc
        kwargs['segment_order'] = segment_order
        fmt_1 = self._create_location_format(
            loc_set_name, char_definition, **kwargs)
        # Create a location format object 2.
        char_definition = 'B\\d\\dC\\d\\dR\\d\\d'
        segment_order = 2
        description = "Test character definition."
        kwargs['description'] = desc
        kwargs['segment_order'] = segment_order
        fmt_2 = self._create_location_format(
            loc_set_name, char_definition, **kwargs)
        return loc_set_name, fmt_root, fmt_0, fmt_1, fmt_2

    def test_create_location_set_name_record(self):
        #self.skipTest("Temporarily skipped")
        # Create a location set name.
        name = "Test Location Set Name"
        desc = "Test description."
        kwargs = {'description': desc}
        location_set_name = self._create_location_set_name(
            self.project, name=name, **kwargs)
        msg = "'{}' should be '{}' and '{}' should be '{}'".format(
            location_set_name.name, name, location_set_name.description, desc)
        self.assertEqual(location_set_name.name, name, msg)
        self.assertEqual(location_set_name.description, desc, msg)

    def test_clone_set_name_tree_ERRORS(self):
        #self.skipTest("Temporarily skipped")
        # Create a new project
        project = self._create_project(self.inventory_type,
                                       name="2nd Test Project")
        # Setup test
        name = "Test Location Set Name"
        desc = "Test description."
        loc_set_name, fmt_root, fmt_0, fmt_1, fmt_2 = self.setup_set_name_tree(
            project, name, desc, LocationSetName.NO)
        # The location_set_name is not shared and user is not in project
        # (should fail).
        with self.assertRaises(ValueError) as cm:
            tree = LocationSetName.objects.clone_set_name_tree(
                project, self.user, loc_set_name)
        # The location_set_name is shared but user is not in project
        # (should fail).
        kwargs = {}
        kwargs['description'] = desc
        kwargs['shared'] = LocationSetName.YES
        loc_set_name = self._create_location_set_name(
            self.project, name=name, **kwargs)
        with self.assertRaises(ValueError) as cm:
            tree = LocationSetName.objects.clone_set_name_tree(
                project, self.user, loc_set_name)

    def test_clone_set_name_tree(self):
        #self.skipTest("Temporarily skipped")
        # Setup test
        name = "Test Location Set Name Number 2"
        desc = "Test description."
        loc_set_name, fmt_root, fmt_0, fmt_1, fmt_2 = self.setup_set_name_tree(
            self.project, name, desc, LocationSetName.YES)
        # Make copy of 'location set name' and it's formats with a new project.
        project = self._create_project(
            self.inventory_type, name="Test Project 2", members=[self.user])
        tree = LocationSetName.objects.clone_set_name_tree(
                project, self.user, loc_set_name)
        msg = "tree: '{}', total in tree: '{}'.".format(tree, len(tree))
        self.assertEqual(len(tree), 5, msg)
        # Try a duplicate record (should fail)
        with self.assertRaises(ValueError) as cm:
            tree = LocationSetName.objects.clone_set_name_tree(
                project, self.user, loc_set_name)

    def test_delete_set_name_tree(self):
        #self.skipTest("Temporarily skipped")
        # Create a location default and tree.
        name = "Test Location Set Name"
        desc = "Test description."
        loc_set_name, fmt_root, fmt_0, fmt_1, fmt_2 = self.setup_set_name_tree(
            self.project, name, desc, LocationSetName.YES)
        code_root = LocationCode.objects.get_root_code(loc_set_name)
        # Create location code objects .
        code_0 = self._create_location_code(fmt_0, "T01", parent=code_root)
        code_1 = self._create_location_code(fmt_1, "X01", parent=code_0)
        code_1a = self._create_location_code(fmt_1, "X02", parent=code_0)
        code_2 = self._create_location_code(fmt_2, "B01C01R01", parent=code_1)
        code_2a = self._create_location_code(fmt_2, "B01C01R01", parent=code_1a)
        # Test for correct number of objects.
        count = LocationSetName.objects.count()
        msg = "Location Set Name: {}, count: {}".format(loc_set_name, count)
        self.assertEqual(count, 1, msg)
        count = LocationFormat.objects.count()
        msg = "Location Formats: {}, {}, {}, {}, count: {}".format(
            fmt_root, fmt_0, fmt_1, fmt_2, count)
        self.assertEqual(count, 4, msg)
        count = LocationCode.objects.count()
        msg = "Location Codes: {}, {}, {}, {}, count: {}".format(
            code_root, code_0, code_1, code_2, count)
        self.assertEqual(count, 6, msg)
        # Test delete_set_name_tree
        nodes = LocationSetName.objects.delete_set_name_tree(
            self.project, loc_set_name, self.user)
        #print nodes
        # Test for correct number of objects.
        msg = "Location Set Name: {}".format(loc_set_name)
        self.assertEqual(LocationSetName.objects.count(), 0, msg)
        msg = "Location Formats: {}, {}, {}, {}".format(
            fmt_root, fmt_0, fmt_1, fmt_2)
        self.assertEqual(LocationFormat.objects.count(), 0, msg)
        msg = "Location Codes: {}, {}, {}, {}".format(
            code_root, code_0, code_1, code_2)
        self.assertEqual(LocationCode.objects.count(), 0, msg)

    def test_length_of_separator(self):
        """
        Test that the length of the separator is not longer than the defined
        length of the database column.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location set name object.
        kwargs = {}
        kwargs['description'] = "Test Description 2"
        kwargs['separator'] = '--->'

        with self.assertRaises(ValidationError) as cm:
            obj = self._create_location_set_name(self.project, **kwargs)
            msg = "Created Object: {}".format(obj)
            self.assertFalse(obj, msg)

        msg = "Exception: {}".format(cm.exception)
        messages = [msg for msg in cm.exception.messages
                    if "Ensure this value has at most 3 characters " in msg]
        self.assertTrue(messages, msg)


class TestLocationFormatModel(BaseLocation):

    def __init__(self, name):
        super(TestLocationFormatModel, self).__init__(name)

    def setUp(self):
        super(TestLocationFormatModel, self).setUp()
        # Create a valid location default object.
        self.loc_set_name = self._create_location_set_name(self.project)

    def test_get_root_format(self):
        """
        Test that the root format is returned and that errors are reported
        properly.
        """
        # Test proper operation
        root = LocationFormat.objects.get_root_format(self.loc_set_name)
        msg = "Found: {}, should be: {}".format(
            root.char_definition, LocationCode.ROOT_NAME)
        self.assertTrue(root.char_definition == LocationCode.ROOT_NAME, msg)

        # Test inproper operation
        with self.assertRaises(LocationFormat.DoesNotExist) as cm:
            root = LocationFormat.objects.get_root_format(None)

    def test_create_location_format_record(self):
        #self.skipTest("Temporarily skipped")
        # Create a location format object.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        kwargs = {}
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        loc_fmt = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        msg = "{} should be {} and {} should be {}".format(
            loc_fmt.char_definition, char_definition,
            loc_fmt.location_set_name.name, self.LOCATION_SET_NAME)
        self.assertEqual(loc_fmt.char_definition, char_definition, msg)
        self.assertEqual(loc_fmt.location_set_name.name,
                         self.LOCATION_SET_NAME, msg)

    def test_get_char_definition(self):
        #self.skipTest("Temporarily skipped")
        # Create a location format object.
        char_definition = r'A\d\dB\d\d\d'
        segment_order = 0
        description = "Test character definition."
        kwargs = {}
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        loc_fmt = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        # Get format object.
        fmt_obj = LocationFormat.objects.get_char_definition(
            self.project, self.LOCATION_SET_NAME, char_definition)
        msg = "Created object: {}, queried object: {}".format(loc_fmt, fmt_obj)
        self.assertEqual(loc_fmt, fmt_obj, msg)
        # Test for non-existant record.
        fmt_obj = LocationFormat.objects.get_char_definition(
            None, self.LOCATION_SET_NAME, char_definition)
        msg = "Returned: '{}', should return a None object".format(fmt_obj)
        self.assertTrue(fmt_obj == None, msg)

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
        kwargs = {}
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description

        for fmt, message in formats.items():
            with self.assertRaises(ValidationError) as cm:
                loc_fmt = self._create_location_format(
                    self.loc_set_name, fmt, **kwargs)
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
        desc = "Test description."
        kwargs = {}
        kwargs['description'] = "Test description."
        self.loc_set_name = self._create_location_set_name(
            self.project, **kwargs)
        # Create a location format object.
        char_definition = 'T\\d\\d'
        segment_order = 0
        description = "Test character definition."
        kwargs = {}
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        self.loc_fmt = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)

    def test_get_root_code(self):
        """
        Test that the proper root object is returned and that the proper
        exception is raised.
        """
        # Test for proper operation
        root = LocationCode.objects.get_root_code(self.loc_set_name)
        msg = "Found: {}, should be: {}".format(
            root.segment, LocationCode.ROOT_NAME)
        self.assertTrue(root.segment == LocationCode.ROOT_NAME, msg)

    def test_create_location_code(self):
        #self.skipTest("Temporarily skipped")
        # Create a location code object.
        segment = "T01"
        loc_code = self._create_location_code(self.loc_fmt, segment)
        msg = "{} should be {} and {} should be {}".format(
            loc_code.segment, segment,
            loc_code.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(loc_code.segment, segment, msg)
        self.assertEqual(loc_code.location_format.location_set_name.name,
                         self.LOCATION_SET_NAME, msg)

    def test_invalid_child(self):
        #self.skipTest("Temporarily skipped")
        segment = "T01"
        code_0 = self._create_location_code(self.loc_fmt, segment)
        msg = "{} should be {} and {} should be {}".format(
            code_0.segment, segment,
            code_0.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_0.segment, segment, msg)
        # Try to create a child to itself.
        with self.assertRaises(ValidationError):
            segment = "T01"
            code_1 = self._create_location_code(
                self.loc_fmt, segment,  parent=code_0)
            msg = "{} should be {} and {} should be {}".format(
                code_1.segment, segment,
                code_1.location_format.location_set_name.name,
                self.LOCATION_SET_NAME)
            self.assertFalse(code_1, msg)

    def test_invalid_number_of_segments(self):
        #self.skipTest("Temporarily skipped")
        # Create a location code object.
        segment = "T01"
        code_0 = self._create_location_code(self.loc_fmt, segment)
        msg = "{} should be {} and {} should be {}".format(
            code_0.segment, segment,
            code_0.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_0.segment, segment, msg)
        # Create 2nd location format object.
        char_definition = 'C\\d\\d' # Container nn
        segment_order = 1
        description = "Test character definition."
        kwargs = {}
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        loc_fmt_1 = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        # Create a 2nd location code parent.
        segment = "C01" # Container 01
        code_1 = self._create_location_code(loc_fmt_1, segment, parent=code_0)
        msg = "{} should be {} and {} should be {}".format(
            code_1.segment, segment,
            code_1.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_1.segment, segment, msg)
        # Create 3rd location format object.
        char_definition = 'B\\d\\d' # Container nn
        segment_order = 2
        description = "Test character definition."
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        loc_fmt_2 = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        # Create a 3nd location code parent.
        segment = "B01" # Bin 01
        code_2 = self._create_location_code(loc_fmt_2, segment, parent=code_1)
        msg = "{} should be {} and {} should be {}".format(
            code_2.segment, segment,
            code_2.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_2.segment, segment, msg)
        # Try to create a 4nd parent, but with no new format object.
        with self.assertRaises(ValidationError):
            segment = "B02" # Bin 02
            code_3 = self._create_location_code(
                loc_fmt_2, segment, parent=code_2)
            msg = "{} should be {} and {} should be {}".format(
                code_3.segment, segment,
                code_3.location_format.location_set_name.name,
                self.LOCATION_SET_NAME)
            self.assertFalse(code_3, msg)

    def test_get_parents(self):
        #self.skipTest("Temporarily skipped")
        # Create a location code object.
        segment = "T01"
        code_0 = self._create_location_code(self.loc_fmt, segment)
        msg = "{} should be {} and {} should be {}".format(
            code_0.segment, segment,
            code_0.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_0.segment, segment, msg)
        # Test get_parent
        parents = LocationCode.objects.get_parents(self.project, code_0)
        msg = "parents: {}".format(parents)
        self.assertEqual(len(parents), 1, msg)
        # Create 2nd location format object.
        char_definition = 'C\\d\\d' # Container nn
        segment_order = 1
        description = "Test character definition."
        kwargs = {}
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        loc_fmt_1 = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        # Create a 2nd location code parent.
        segment = "C01" # Container 01
        code_1 = self._create_location_code(loc_fmt_1, segment, parent=code_0)
        msg = "{} should be {} and {} should be {}".format(
            code_1.segment, segment,
            code_1.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_1.segment, segment, msg)
        # Test get_parent
        parents = LocationCode.objects.get_parents(self.project, code_1)
        msg = "parents: {}".format(parents)
        self.assertEqual(len(parents), 2, msg)
        # Create 3rd location format object.
        char_definition = 'B\\d\\d' # Container nn
        segment_order = 2
        description = "Test character definition."
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        loc_fmt_2 = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        # Create a 3nd location code parent.
        segment = "B01" # Bin 01
        code_2 = self._create_location_code(loc_fmt_2, segment, parent=code_1)
        msg = "{} should be {} and {} should be {}".format(
            code_2.segment, segment,
            code_2.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_2.segment, segment, msg)
        # Test get_parent
        parents = LocationCode.objects.get_parents(self.project, code_2)
        msg = "parents: {}".format(parents)
        self.assertEqual(len(parents), 3, msg)

    def test_get_parents_with_invalid_project(self):
        """
        Test that an unauthorized project cannot access another projects
        location codes.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location code object.
        segment = "T01"
        code_0 = self._create_location_code(self.loc_fmt, segment)
        msg = "{} should be {} and {} should be {}".format(
            code_0.segment, segment,
            code_0.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_0.segment, segment, msg)
        # Create a second project
        project = self._create_project(self.inventory_type,
                                       name="Unauthenticated Project")
        # Test get_parent
        with self.assertRaises(ValueError) as cm:
            parents = LocationCode.objects.get_parents(project, code_0)

        message = "Trying to access a location code with an invalid project, "
        self.assertTrue(self._has_error(cm.exception, message=message))

    def test_get_all_root_trees(self):
        """
        Test that this is permitted [['T01', 'A01'], ['T02', 'A01']].
        """
        #self.skipTest("Temporarily skipped")
        # Create 1st tree.
        # Create a location code object.
        segment = "T01"
        code_0 = self._create_location_code(self.loc_fmt, segment)
        msg = "{} should be {} and {} should be {}".format(
            code_0.segment, segment,
            code_0.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_0.segment, segment, msg)
        # Create 2nd location format object.
        char_definition = 'A\\d\\d' # Container nn
        segment_order = 1
        description = "Test character definition."
        kwargs = {}
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        loc_fmt_1 = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        # Create a 2nd location code parent.
        segment = "A01" # Container 01
        code_1 = self._create_location_code(loc_fmt_1, segment, parent=code_0)
        msg = "{} should be {} and {} should be {}".format(
            code_1.segment, segment,
            code_1.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_1.segment, segment, msg)
        # Create 2nd tree.
        segment = "T02"
        code_2 = self._create_location_code(self.loc_fmt, segment)
        msg = "'{}' should be '{}' and '{}' should be '{}'".format(
            code_2.segment, segment,
            code_2.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_2.segment, segment, msg)
        # Create a 2nd location code parent.
        segment = "A01" # Container 01
        code_3 = self._create_location_code(loc_fmt_1, segment, parent=code_2)
        msg = "{} should be {} and {} should be {}".format(
            code_3.segment, segment,
            code_3.location_format.location_set_name.name,
            self.LOCATION_SET_NAME)
        self.assertEqual(code_3.segment, segment, msg)
        # get_all_root_trees
        trees = LocationCode.objects.get_all_root_trees(self.project, segment)
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
                code_0 = self._create_location_code(self.loc_fmt, segment)
                msg = "Created object: {}".format(code_0)
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
        code_0 = self._create_location_code(self.loc_fmt, segment)

        with self.assertRaises(ValidationError) as cm:
            code_1 = self._create_location_code(
                self.loc_fmt, segment, parent=code_0)
            msg = "Created object: {}".format(code_1)
            self.assertFalse(code_1, msg)

        msg = "Exception: {}".format(cm.exception)
        self.assertTrue("child to itself." in cm.exception.messages[0], msg)

    def test_segments_have_same_location_set_name(self):
        """
        Test that all the segments in a given tree have the same location
        default.
        """
        #self.skipTest("Temporarily skipped")
        # Create a location default object.
        name = "Another Set Name"
        description = "Test Description 2"
        kwargs = {}
        kwargs['description'] = description
        loc_set_name = self._create_location_set_name(
            self.project, name=name, **kwargs)
        # Create a location format object with loc_set_name1.
        char_definition = 'C\\d\\dR\\d\\d'
        segment_order = 1
        description = "Test character definition level 1."
        kwargs['segment_order'] = segment_order
        kwargs['description'] = description
        loc_fmt = self._create_location_format(
            loc_set_name, char_definition, **kwargs)
        # Create two location codes.
        code_0 = self._create_location_code(self.loc_fmt, "T01")

        with self.assertRaises(ValidationError) as cm:
            code_1 = self._create_location_code(
                loc_fmt, "C01R01", parent=code_0)
            msg = "Created object: {}".format(code_1)
            self.assertFalse(code_1, msg)

        msg = "Exception: {}".format(cm.exception)
        self.assertTrue("same location set name." in cm.exception.messages[0],
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
        kwargs = {}
        kwargs['description'] = description
        kwargs['segment_order'] = segment_order
        loc_fmt = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        # Create three location codes, last one will fail.
        code_0 = self._create_location_code(self.loc_fmt, "T01")
        code_1 = self._create_location_code(loc_fmt, "C01R01", parent=code_0)

        with self.assertRaises(ValidationError) as cm:
            code_2 = self._create_location_code(
                loc_fmt, "C02R02", parent=code_1)
            msg = "Created Object: {}".format(code_2)
            self.assertFalse(code_2, msg)

        msg = "Exception: {}".format(cm.exception)
        self.assertTrue("There are more segments " in cm.exception.messages[0],
                        msg)

    def test_fix_path_in_children(self):
        """
        Test that children path information is fixed when a parent's
        name is changed.
        """
        #self.skipTest("Temporarily skipped")
        # Create three formats.
        char_definition = 'A\d\d'
        segment_order = 1
        description = "Test character definition level 1."
        kwargs = {}
        kwargs['description'] = description
        kwargs['segment_order'] = segment_order
        loc_fmt_1 = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        char_definition = 'B\d\d'
        segment_order = 2
        description = "Test character definition level 2."
        kwargs = {}
        kwargs['description'] = description
        kwargs['segment_order'] = segment_order
        loc_fmt_2 = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        char_definition = 'C\d\dR\d\d'
        segment_order = 3
        description = "Test character definition level 3."
        kwargs = {}
        kwargs['description'] = description
        kwargs['segment_order'] = segment_order
        loc_fmt_3 = self._create_location_format(
            self.loc_set_name, char_definition, **kwargs)
        # Create three codes
        code_1 = self._create_location_code(loc_fmt_1, "A01")
        code_2 = self._create_location_code(loc_fmt_2, "B01", parent=code_1)
        code_3 = self._create_location_code(loc_fmt_3, "C01R01", parent=code_2)
        # Test that the paths and levels are correct.
        root = LocationCode.ROOT_NAME
        sep = code_1.get_separator()
        path = '{0}{1}A01'.format(root, sep)
        msg = ("Found path: {}, should be: {}, found level: {}, "
               "should be: {}").format(code_1.path, path, code_1.level, 1)
        self.assertEqual(code_1.path, path, msg)
        self.assertEqual(code_1.level, 1, msg)
        path = '{0}{1}A01{1}B01'.format(root, sep)
        msg = ("Found path: {}, should be: {}, found level: {}, "
               "should be: {}").format(code_2.path, path, code_2.level, 2)
        self.assertEqual(code_2.path, path, msg)
        self.assertEqual(code_2.level, 2, msg)
        path = '{0}{1}A01{1}B01{1}C01R01'.format(root, sep)
        msg = ("Found path: {}, should be: {}, found level: {}, "
               "should be: {}").format(code_3.path, path, code_3.level, 3)
        self.assertEqual(code_3.path, path, msg)
        self.assertEqual(code_3.level, 3, msg)
        # Test that the children update the path when the parent changes.
        code_1 = self._create_location_code(
            loc_fmt_1, "A01", parent=code_1.parent, **{'update_segment': "A02"})
        code_2 = self._create_location_code(loc_fmt_2, "B01", parent=code_1)
        code_3 = self._create_location_code(loc_fmt_3, "C01R01", parent=code_2)
        path = '{0}{1}A02'.format(root, sep)
        msg = ("Found path: {}, should be: {}, found level: {}, "
               "should be: {}").format(code_1.path, path, code_1.level, 1)
        self.assertEqual(code_1.path, path, msg)
        self.assertEqual(code_1.level, 1, msg)
        path = '{0}{1}A02{1}B01'.format(root, sep)
        msg = ("Found path: {}, should be: {}, found level: {}, "
               "should be: {}").format(code_2.path, path, code_2.level, 2)
        self.assertEqual(code_2.path, path, msg)
        self.assertEqual(code_2.level, 2, msg)
        path = '{0}{1}A02{1}B01{1}C01R01'.format(root, sep)
        msg = ("Found path: {}, should be: {}, found level: {}, "
               "should be: {}").format(code_3.path, path, code_3.level, 3)
        self.assertEqual(code_3.path, path, msg)
        self.assertEqual(code_3.level, 3, msg)

    def test_parents_producer(self):
        """
        Test that the parents_producer() method produces the parents for
        the admin.
        """
        #self.skipTest("Temporarily skipped")
        # Test first code
        root = LocationCode.ROOT_NAME
        code_1 = self._create_location_code(self.loc_fmt, 'T01')
        sep = code_1.get_separator()
        parents = code_1.parents_producer()
        msg = "Found: {}, should be: {}".format(parents, root)
        self.assertEqual(parents, root, msg)

    def test_char_def_producer(self):
        """
        Test that the char_def_producer() method produces the correct format.
        """
        #self.skipTest("Temporarily skipped")
        # Test first code
        code_1 = self._create_location_code(self.loc_fmt, 'T01')
        fmt = code_1.char_def_producer()
        cd = code_1.location_format.char_definition
        msg = "Found: {}, should be: {}".format(fmt, cd)
        self.assertEqual(fmt, cd, msg)
