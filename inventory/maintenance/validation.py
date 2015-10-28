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

    def __init__(self, fmt=None, delimiter=None):
        """
        FormatValidator constructor.

        @param format: The format that is being considered for this location
                       code.
        @param delimiter: The delimiter used between formats.
        """
        self.__format = fmt

        if delimiter is not None:
            self.__delimiter = self.validate_separator(delimiter)
        else:
            self.__delimiter = ''

    def validate_separator(self, value):
        from .models import LocationDefault

        if not value:
            raise ValidationError(
                _("A separator cannot be empty or a None value."))

        size = len(value)
        separator_obj = LocationDefault._meta.get_field('separator')

        if size > separator_obj.max_length:
            raise ValidationError(
                _("The length of the separator is {}, the max length "
                  "is {}").format(size, separator_obj.max_length))

        return value

    def validate_char_definition(self, value):
        value = temp = value.replace('\x07', '\\a')
        operators = self._split_char_definition(value)
        tmp = ''.join(operators)

        if self.__delimiter in tmp:
             raise ValidationError(
                _("Invalid format, found: {} in {}").format(
                     self.__delimiter, tmp))

        if tmp != value or len(value) <= 0:
            raise ValidationError(
                _("Invalid format, found: {}, parsed: {}").format(
                    value, operators))

        return value

    def validate_segment(self, value):
        if self.__delimiter in value:
            raise ValidationError(
                _("A separator cannot be in a segment."))

        operators = self._split_char_definition(self.__format)
        regex = ''.join([r'([{}])'.format(self.__FMT_MAP.get(op, op))
                         for op in operators])
        rx_obj = re.match(regex, value)

        if not rx_obj:
            raise ValidationError(
                _("Invalid segment '{}', does not conform to '{}'.").format(
                    value, self.__format))

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
        if self.__delimiter in value:
            value = value.replace(self.__delimiter, '')

        return value
