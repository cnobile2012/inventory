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

    def test_validate_separator(self):
        #self.skipTest("Temporarily skipped")
        delimiters = ['-', ':', '->', '-->', '&']

        for delim in delimiters:
            value = FormatValidator().validate_separator(delim)
            msg = "{}".format(value, delim)
            self.assertEqual(value, delim, msg)

    def test_validate_separator_failures(self):
        #self.skipTest("Temporarily skipped")
        delimiters = ['', '--->', None]

        for delim in delimiters:
            msg = "{}".format(delim)

            with self.assertRaises(ValidationError):
                value = FormatValidator().validate_separator(delim)
                self.assertFalse(value, msg)

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

    def test_validate_segment(self):
        #self.skipTest("Temporarily skipped")
        segments = [
            (':', r'T\d\d', 'T01'),
            ('->', r'\a\d\d@\a\d\d', 'A01@B02'),
            ('->', r'\a\a>\d\d', 'XY>00'),
            ('-', r'%\d\d\a\d\d', '%00X00'),
            ]

        for delim, fmt, segment in segments:
            value = FormatValidator(
                fmt=fmt, delimiter=delim).validate_segment(segment)
            msg = "Segment '{}' does not conform to the '{}' rule.".format(
                value, fmt)
            self.assertEqual(value, segment, msg)

    def test_validate_segment_failures(self):
        #self.skipTest("Temporarily skipped")
        segments = [
            (':', r'T\d\d', 'T0'),
            ('->', r'\a\d\d@\a\d\d', 'A01->B02'),
            ('->', r'\a\a>\d\d', 'XY-00'),
            ('-', r'%\d\d\a\d\d', '%000000'),
            ]

        for delim, fmt, segment in segments:
            fmt = FormatValidator(delimiter=delim).validate_char_definition(fmt)
            msg = "Delimiter: {}, format: {}, segment: {}".format(
                delim, fmt, segment)
            value = ''

            with self.assertRaises(ValidationError) as cm:
                value = FormatValidator(fmt=fmt, delimiter=delim
                                        ).validate_segment(segment)
                self.assertFalse(value, msg)
