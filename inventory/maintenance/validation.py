# -*- coding: utf-8 -*-
#
# maintenance/validation.py
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
        r'\p': r'!"#$%&\'\(\)*+,-./:;<=>?@\[\]^_`{|}~\\'
        }
    __REGEX_RESERVED_MAP = {
        '[': '\[',
        ']': '\]',
        '\\': '\\',
        '^': '\^',
        '$': '\$',
        '.': '\.',
        '|': '\|',
        '?': '\?',
        '*': '\*',
        '+': '\+',
        '(': '\(',
        ')': '\)',
        }

    def __init__(self, fmt=None, delimiter=None):
        """
        FormatValidator constructor.

        @param format: The format that is being considered for this location
                       code.
        @param delimiter: The delimiter used between formats.
        """
        self.__format = fmt
        self.__delimiter = self.validate_separator(delimiter)
        #self.__currentFormat = None
        #self.__fmtRegEx = self._buildRegEx()

    ## def _buildRegEx(self):
    ##     splitRegEx = r"(\\[adp]|[a-zA-Z{}])".format(
    ##         self._removeDelimiter(self.__FMT_MAP.get('\p')[1:-1]))
    ##     result = []

    ##     for fmt in self.__formats:
    ##         segList = [x for x in re.split(splitRegEx, fmt) if x]
    ##         regex = ''

    ##         for seg in segList:
    ##             tmp = self.__FMT_MAP.get(seg)
    ##             if tmp: regex += self._removeDelimiter(tmp)
    ##             else: regex += self._removeDelimiter(seg)

    ##         regex = "(" + regex + ")"
    ##         result.append(re.compile(regex))
    ##         #print regex

    ##     return result

    ## def _removeDelimiter(self, value):
    ##     for c in self.__delimiter:
    ##         if c in self.__REGEX_RESERVED_MAP:
    ##             c = self.__REGEX_RESERVED_MAP.get(c)

    ##         value = value.replace(c, '')

    ##     return value

    def validate_char_definition(self, value):
        value = temp = value.replace('\x07', '\\a')
        a = self.__FMT_MAP.get(r'\a', '')
        p = self._remove_delimiter(self.__FMT_MAP.get(r'\p', ''))
        regex = r'([{}{}])|(\\[dap])'.format(a, p)
        iterator = re.finditer(regex, value)
        operators = []

        try:
            while True:
                for j in iterator.next().groups():
                    if j: operators.append(j)
        except StopIteration:
            pass

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

    def validate_separator(self, value):
        from .models import LocationDefault

        if not value:
            raise ValidationError(
                _("A separator cannot be empty or a None value."))

        size = len(value)
        separator = LocationDefault._meta.get_field('separator')

        if size > separator.max_length:
            raise ValidationError(
                _("The length of the separator is {}, the max length "
                  "is {}").format(size, separator.max_length))

        return value

    def validate(self, value):
        result = None

        for idx, fmt in enumerate(self.__fmtRegEx, start=0):
            match = fmt.search(value)

            if match:
                result = match.group(0)
                self.__currentFormat = idx
                break




        return result is not None

    def getFormat(self, value):
        """
        Find the user entered format that would define the location code.

        @param value: The user entered segment used in the location code.
        @return: The valid character definition matching a Location Code
                 Default.
        """
        result = None

        if self.validate(value) and self.__currentFormat is not None:
            result = self.__formats[self.__currentFormat]
        else:
            msg = "Invalid value [%s] or format [%s]."
            raise ValueError(msg % (value, self.__currentFormat))

        return result

    def _remove_delimiter(self, value):
        if self.__delimiter in value:
            value = value.replace(self.__delimiter, '')

        return value
