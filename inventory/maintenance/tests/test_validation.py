# -*- coding: utf-8 -*-
#
# inventory/maintenance/tests/test_validation.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from django.test import TestCase
from django.core.exceptions import ValidationError

from ..validation import FormatValidator


class TestValidation(TestCase):

    def __init__(self, name):
        super(TestValidation, self).__init__(name)

    def test_validate_char_definition(self):
        #self.skipTest("Temporarily skipped")
        formats = [
            (':', r'T\d\d'),
            (':', r'B\d\dC\d\dR\d\d'),
            ('->', r'\a\d\d@B\d\d'),
            ('&', r'(\a\d\d)'),
            (':', r'[B\d\d\d]'),
            (':', r'{&\a\d}'),
            (':', r'\p\d\d'),
            (':', r'\a\d\p'),
            (':', 'T\d\d'),
            (':', 'B\d\dC\d\dR\d\d'),
            (':', '\a\d\d@B\d\d'),
            (':', '(\a\d\d)'),
            (':', '[B\d\d\d]'),
            (':', '{&\a\d}'),
            (':', '\p\d\d'),
            (':', '\a\d\p'),
            ]

        for delim, fmt in formats:
            value = FormatValidator(
                delimiter=delim).validate_char_definition(fmt)
            msg = "{} should be {}".format(value, fmt.replace('\x07', '\\a'))
            self.assertEqual(value, fmt.replace('\x07', '\\a'), msg)

    def test_validate_char_definition_failures(self):
        #self.skipTest("Temporarily skipped")
        formats = [
            ('', r'T\d\d',), # Empty separator
            (':', r'',), # Empty format
            (':', r'T:\d\d',), # Separator in format, 1st case
            ('->', r'T\d->\d',), # Separator in format 2nd case
            ('--->', r'T\d\d',), # Separator too long
            ]

        for delim, fmt in formats:
            with self.assertRaises(ValidationError):
                FormatValidator(delimiter=delim).validate_char_definition(fmt)


