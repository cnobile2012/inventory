# -*- coding: utf-8 -*-
#
# inventory/maintenance/validation.py
#

import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class FormatValidator(object):
    """
    This class parses a format string into rules to validate location code
    fields.
    """
    __FMT_MAP = {
        r'\d': r'\d',
        r'\a': r'a-zA-Z',
        r'\p': r'!"#$%&\'\(\)*+,./:;<=>?@\[\]^_`{|}~-'
        }

    def __init__(self, delimiter, fmt=None):
        """
        FormatValidator constructor.

        @param format: The format that is being considered for this location
                       code.
        @param delimiter: The delimiter used between formats.
        """
        self._format = fmt
        self._delimiter = self.__validate_separator(delimiter)

    def __validate_separator(self, value):
        """
        This method has mixed exception types.
        """
        from .models import LocationDefault

        # This is not a validation error, but could be a programming error.
        if not value:
            raise ValueError(_("A separator cannot be empty or a None value."))

        size = len(value)
        separator_obj = LocationDefault._meta.get_field('separator')

        if size > separator_obj.max_length:
            raise ValidationError(
                {'separator': _("The length of the separator is {}, the max "
                                "length is {}").format(
                     size, separator_obj.max_length)})

        return value

    def validate_char_definition(self, value):
        value = value.replace('\x07', '\\a') # Fix the \a issue.

        if self._delimiter in value:
             raise ValidationError(
                {'char_definition': _("Invalid format, found separator '{}' in"
                                      " '{}'").format(self._delimiter, value)})

        operators = self._split_char_definition(value)
        tmp = ''.join(operators)

        if tmp != value or len(value) <= 0:
            raise ValidationError(
                {'char_definition': _("Invalid format, found: {}, "
                                      "parsed: {}").format(value, operators)})

        return value

    def validate_segment(self, value):
        rx_obj = None

        if value is not None:
            operators = self._split_char_definition(self._format)
            regex = ''.join([r'([{}])'.format(self.__FMT_MAP.get(op, op))
                         for op in operators])
            rx_obj = re.match(regex, value)

        if not rx_obj:
            raise ValidationError(
                {'segment': _("Invalid segment '{}', does not conform "
                              "to '{}'.").format(value, self._format)})

        return value

    def _split_char_definition(self, fmt):
        a = self.__FMT_MAP.get(r'\a', '')
        p = self._remove_delimiter(self.__FMT_MAP.get(r'\p', ''))
        regex = r'([{}{}])|(\\[dap])'.format(a, p)
        rx_list = re.findall(regex, fmt)
        operators = []

        for group in rx_list:
            for item in group:
                if item: operators.append(item)

        return operators

    def _remove_delimiter(self, value):
        if self._delimiter in value:
            value = value.replace(self._delimiter, '')

        return value
