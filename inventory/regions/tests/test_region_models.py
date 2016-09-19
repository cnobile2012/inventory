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

    def _create_country_record(self, country, code, active=True):
        kwargs = {}
        kwargs['country'] = country
        kwargs['code'] = code
        kwargs['active'] = active
        return Country.objects.create(**kwargs)


## class TestCountry(BaseRegions):

##     def __init__(self, name):
##         super(TestCountry, self).__init__(name)
