# -*- coding: utf-8 -*-
#
# inventory/regions/tests/test_regions_models.py
#
# Run ./manage.py test -k # Keep the DB, don't rebuild.
#

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Country, Region

User = get_user_model()


class BaseRegions(TestCase):
    _TEST_USERNAME = 'TestUser'
    _TEST_PASSWORD = 'TestPassword_007'

    def __init__(self, name):
        super(BaseRegions, self).__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True,
                     role=User.DEFAULT_USER):
        user = User.objects.create_user(username=username, password=password)
        user.first_name = "Test"
        user.last_name = "User"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.role = role
        user.save()
        return user

    def _create_region_record(self, region, region_code, country, active=True):
        kwargs = {}
        kwargs['region'] = region
        kwargs['region_code'] = region_code
        kwargs['country'] = country
        kwargs['active'] = active
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Region.objects.create(**kwargs)

    def _create_country_record(self, country, country_code_2, country_code_3='',
                               country_number_code=0, active=True):
        kwargs = {}
        kwargs['country'] = country
        kwargs['country_code_2'] = country_code_2
        kwargs['country_code_3'] = country_code_3
        kwargs['country_number_code'] = country_number_code
        kwargs['active'] = active
        kwargs['creator'] = self.user
        kwargs['updater'] = self.user
        return Country.objects.create(**kwargs)


class TestCountry(BaseRegions):

    def __init__(self, name):
        super(TestCountry, self).__init__(name)

    def test_get_regions_by_country(self):
        """
        Test that correct regions are returned with the differnt type of
        arguments.
        """
        #self.skipTest("Temporarily skipped")
        # Create a country and some states.
        c0 = self._create_country_record(
            'United States', 'US', country_code_3='USA',
            country_number_code=840)
        r0 = self._create_region_record('New York', 'NY', c0)
        r1 = self._create_region_record('New Jersey', 'NJ', c0)
        # Test with PK.
        regions = Country.objects.get_regions_by_country(c0.pk)
        msg = "Regions: {}".format(regions)
        self.assertEqual(len(regions), 2, msg)
        # Test with country_number_code.
        regions = Country.objects.get_regions_by_country(
            c0.country_number_code, code=True)
        msg = "Regions: {}".format(regions)
        self.assertEqual(len(regions), 2, msg)
        # Test 2 character country code.
        regions = Country.objects.get_regions_by_country('US')
        msg = "Regions: {}".format(regions)
        self.assertEqual(len(regions), 2, msg)
        # Test 3 character country code.
        regions = Country.objects.get_regions_by_country('USA')
        msg = "Regions: {}".format(regions)
        self.assertEqual(len(regions), 2, msg)
        # Test country name.
        regions = Country.objects.get_regions_by_country('United States')
        msg = "Regions: {}".format(regions)
        self.assertEqual(len(regions), 2, msg)
        # Test bad info.
        regions = Country.objects.get_regions_by_country('Junk')
        msg = "Regions: {}".format(regions)
        self.assertEqual(len(regions), 0, msg)


## class TestRegion(BaseRegions):

##     def __init__(self, name):
##         super(TestRegion, self).__init__(name)
