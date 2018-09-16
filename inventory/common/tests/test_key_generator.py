# -*- coding: utf-8 -*-
#
# inventory/common/tests/test_key_generator.py
#

import string

from django.test import TestCase

from ..key_generator import KeyGenerator


class TestKeyGenerator(TestCase):

    def __init__(self, name):
        super().__init__(name)

    def test_length(self):
        #self.skipTest("Temporarily skipped")
        length = 18
        kg = KeyGenerator(length)
        msg = "Found length: {}, should be: {}".format(kg.length, length)
        self.assertEqual(kg.length, length, msg)

    def test_valid_generate(self):
        #self.skipTest("Temporarily skipped")
        length = 18
        kg = KeyGenerator(length)
        key = kg.generate()
        size = len(key)
        msg = "Found key length: {}, should be: {}".format(size, length)
        self.assertEqual(size, length, msg)

    def test_override_key_length(self):
        #self.skipTest("Temporarily skipped")
        length = 18
        kg = KeyGenerator(length)
        key0 = kg.generate(length=2)
        size = len(key0)
        msg = "Found key length: {}, should be: {}".format(size, 2)
        self.assertEqual(size, 2, msg)
        # Try again without args, should be same key and length.
        key1 = kg.generate()
        size = len(key1)
        msg = "Found key length: {}, should be: {}".format(size, 2)
        self.assertEqual(size, 2, msg)
        msg = "Found key: {}, should be: {}".format(key1, key0)
        self.assertEqual(key1, key0, msg)

    def test_regenerate(self):
        #self.skipTest("Temporarily skipped")
        length = 18
        kg = KeyGenerator(length)
        # Get first key
        key0 = kg.generate()
        # Get second key
        key1 = kg.generate(regen=True)
        msg = "Found key: {}, should not be: {}".format(key1, key0)
        self.assertNotEqual(key0, key1, msg)

    def test_change_domain(self):
        #self.skipTest("Temporarily skipped")
        length = 18
        kg = KeyGenerator(length)
        key = kg.generate(domain=string.digits)
        invalid_chars = [c for c in key if c not in string.digits]
        msg = "Key '{}' with characters '{}' are not in domain '{}'.".format(
            key, invalid_chars, string.digits)
        self.assertTrue(invalid_chars == [], msg)

    def test_invalid_length(self):
        #self.skipTest("Temporarily skipped")
        length = '1A'
        kg = KeyGenerator(length)
        with self.assertRaises(ValueError) as cm:
            key0 = kg.generate()

    def test_invalid_length_value(self):
        #self.skipTest("Temporarily skipped")
        length = 0
        kg = KeyGenerator(length)
        with self.assertRaises(ValueError) as cm:
            key0 = kg.generate()

        with self.assertRaises(ValueError) as cm:
            key0 = kg.generate(-1)
