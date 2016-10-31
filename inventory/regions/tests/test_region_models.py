# -*- coding: utf-8 -*-
#
# inventory/regions/tests/test_region_models.py
#

from django.core.exceptions import ValidationError

from inventory.common.tests.base_tests import BaseTest

from ..models import Country, Subdivision, Language, TimeZone, Currency


class BaseRegions(BaseTest):

    def __init__(self, name):
        super(BaseRegions, self).__init__(name)

    def setUp(self):
        super(BaseRegions, self).setUp()


class TestCountry(BaseRegions):

    def __init__(self, name):
        super(TestCountry, self).__init__(name)

    def test_str(self):
        """
        Test that __str__ on the class returns the record's name.
        """
        #self.skipTest("Temporarily skipped")
        c_name = "United States"
        code = "US"
        country = self._create_country(country=c_name, code=code)
        name = str(country)
        result = "{} ({})".format(c_name, code)
        msg = "__str__ name: {}, object name: {}".format(name, result)
        self.assertEqual(name, result, msg)


class TestSubdivision(BaseRegions):

    def __init__(self, name):
        super(TestSubdivision, self).__init__(name)

    def setUp(self):
        super(TestSubdivision, self).setUp()
        self.country = self._create_country()

    def test_str(self):
        """
        Test that __str__ on the class returns the record's name.
        """
        #self.skipTest("Temporarily skipped")
        state = "New York"
        code = "NY"
        subdivision = self._create_subdivision(
            self.country, subdivision_name=state, code=code)
        name = str(subdivision)
        msg = "__str__ name: {}, object name: {}".format(
            name, subdivision.subdivision_name)
        self.assertEqual(name, subdivision.subdivision_name, msg)


class TestLanguage(BaseRegions):

    def __init__(self, name):
        super(TestLanguage, self).__init__(name)

    def setUp(self):
        super(TestLanguage, self).setUp()
        self.country = self._create_country()

    def test_str(self):
        """
        Test that __str__ on the class returns the record's name.
        """
        #self.skipTest("Temporarily skipped")
        code = "en"
        language = self._create_language(self.country, code=code)
        name = str(language)
        msg = "__str__ name: {}, object name: {}".format(name, language.locale)
        self.assertEqual(name, language.locale, msg)


class TestTimeZone(BaseRegions):

    def __init__(self, name):
        super(TestTimeZone, self).__init__(name)

    def setUp(self):
        super(TestTimeZone, self).setUp()
        self.country = self._create_country()

    def test_str(self):
        """
        Test that __str__ on the class returns the record's name.
        """
        #self.skipTest("Temporarily skipped")
        zone = "America/New_York"
        coor = "+404251-0740023"
        timezone = self._create_timezone(self.country, zone, coor)
        name = str(timezone)
        msg = "__str__ name: {}, object name: {}".format(name, timezone.zone)
        self.assertEqual(name, timezone.zone, msg)


class TestCurrency(BaseRegions):

    def __init__(self, name):
        super(TestCurrency, self).__init__(name)

    def setUp(self):
        super(TestCurrency, self).setUp()
        self.country = self._create_country()

    def test_str(self):
        """
        Test that __str__ on the class returns the record's name.
        """
        #self.skipTest("Temporarily skipped")
        cur = "US Dollar"
        a_code = "USD"
        n_code = 840
        unit = 2
        currency = self._create_currency(
            self.country, cur, a_code, n_code, unit)
        name = str(currency)
        result = "{} ({})".format(self.country.country, cur)
        msg = "__str__ name: {}, object name: {}".format(name, result)
        self.assertEqual(name, result, msg)
