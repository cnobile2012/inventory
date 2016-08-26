# -*- coding: utf-8 -*-
#
# inventory/common/__init__.py
#
"""
Provide application functionality.
"""
__docformat__ = "restructuredtext en"

from .key_generator import KeyGenerator

__all__ = (
    'generate_public_key',
    )


def generate_public_key():
    gen = KeyGenerator(length=20)
    return gen.generate()
