# -*- coding: utf-8 -*-
#
# inventory/common/__init__.py
#
"""
Provide application functionality.
"""
__docformat__ = "restructuredtext en"

import string

from .key_generator import KeyGenerator

__all__ = (
    'generate_public_key',
    'generate_sku_fragment',
    )


def generate_public_key():
    gen = KeyGenerator(length=20)
    return gen.generate()

def generate_sku_fragment():
    gen = KeyGenerator(length=7)
    return gen.generate(domain=string.digits)
