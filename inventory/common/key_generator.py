# -*- coding: utf-8 -*-
#
# inventory/common/key_generator.py
#

"""
Generates keys used throughout the system.
"""
__docformat__ = "restructuredtext en"

import logging
import random
from string import ascii_lowercase, ascii_uppercase, digits

from django.utils.translation import gettext, gettext_lazy as _

log = logging.getLogger('inventory.common.key-generator')


class KeyGenerator:
    """
    Create various keys used in the system
    """
    _ERROR_MSGS = {
        'invalid_length': _("Invalid key length value."),
        }
    _UNKNOWN_MSG = _("Unknown")
    _KEY_DOMAIN = ascii_lowercase + ascii_uppercase + digits

    def __init__(self, length):
        """
        Set the key *length*.
        """
        self._length = length
        self.__key = ''

    @property
    def _generator(self):
        """
        Try to access the system random number generator if exists else
        return the pseudo random number generator.
        """
        try:
            rand = random.SystemRandom()
        except NotImplementedError: # pragma: no cover
            log.warn("Using the pseudo number generator.") # pragma: no cover
            rand = random # pragma: no cover

        return rand

    def generate(self, length=0, regen=False, domain=_KEY_DOMAIN):
        """
        Generates a key of the given length using the default domain and
        random number generator.
        """
        if not self.__key or regen:
            if not length:
                length = self._length
            else:
                self._length = length

            if not isinstance(length, int):
                msg = self._ERROR_MSGS.get('invalid_length', self._UNKNOWN_MSG)
                log.error(gettext(msg))
                raise ValueError(msg)

            if length <= 0:
                msg = self._ERROR_MSGS.get('invalid_length', self._UNKNOWN_MSG)
                log.error(gettext(msg))
                raise ValueError(msg)

            self.__key = ''.join(self._generator.choice(domain)
                                 for i in range(length))

        return self.__key

    @property
    def length(self):
        """
        Length of the key
        """
        return self._length
