#
# utils/utilities.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2011-12-14 23:02:54 -0500 (Wed, 14 Dec 2011) $
# $Revision: 55 $
#----------------------------------

import string, re


class FormatParser(object):
    """
    This class parses a format string into rules to validate category fields.
    """
    __FMT_MAP = {
        r'\d': r'\d',
        r'\a': r'[a-zA-Z]',
        r'\p': r"""[!"#\$%&'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~]"""
        }
    __REGEX_RESERVED_MAP = {
        '[': '\[',
        ']': '\]',
        '\\': r'\\',
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

    def __init__(self, formats, delimiter):
        """
        FormatParser constructor.

        @param formats: A sequence of various formats that this mini
                        language can parse.
        @param delimiter: The delimiter used between formats.
        """
        self.__formats = formats
        self.__delimiter = delimiter
        self.__currentFormat = None
        self.__fmtRegEx = self.__buildRegEx()

    def __buildRegEx(self):
        splitRegEx = r"""(\\[adp]|[a-zA-Z%s])""" % \
                     self.__removeDelimiter(self.__FMT_MAP.get('\p')[1:-1])
        result = []

        for fmt in self.__formats:
            segList = [x for x in re.split(splitRegEx, fmt) if x]
            regex = ''

            for seg in segList:
                tmp = self.__FMT_MAP.get(seg)
                if tmp: regex += self.__removeDelimiter(tmp)
                else: regex += self.__removeDelimiter(seg)

            regex = "(" + regex + ")"
            result.append(re.compile(regex))
            #print regex

        return result

    def __removeDelimiter(self, value):
        for c in self.__delimiter:
            if c in self.__REGEX_RESERVED_MAP:
                c = self.__REGEX_RESERVED_MAP.get(c)

            value = value.replace(c, '')

        return value

    def validate(self, value):
        result = None
        count = -1

        for fmt in self.__fmtRegEx:
            count += 1
            match = fmt.search(value)

            if match:
                result = match.group(0)
                self.__currentFormat = count
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


if __name__ == "__main__":
    formats = (r"T\d\d", r"X\d\d", r"B\d\dR\d\dC\d\d", r"\a\p\d\d\d",
               r"0\d\p\p\p!A\a", r"TBD")
    delimiter = ':'
    fp = FormatParser(formats, delimiter)

    for seq in ('T01', 'X55', 'B01R05C09', 'A!339', '01###!AQ', 'TBD'):
        print "Validate: %s, %s" % (seq, fp.validate(seq))
        print "Format: %s, from: %s\n" % (fp.getFormat(seq), seq)
