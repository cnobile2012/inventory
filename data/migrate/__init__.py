# -*- coding: utf-8 -*-
#
# __init__.py
#

import logging

from django.contrib.auth import get_user_model

UserModel = get_user_model()


def setup_logger(name='root', fullpath=None, fmt=None, level=logging.INFO):
    FORMAT = ("%(asctime)s %(levelname)s %(module)s %(funcName)s "
              "[line:%(lineno)d] %(message)s")
    if not fmt: fmt = FORMAT
    # Trun off logging from django db backend.
    backends = logging.getLogger('django.db.backends')
    backends.setLevel(logging.WARNING)
    # Setup logger.
    logger = logging.getLogger(name)
    logger.setLevel(level=level)
    handler = logging.FileHandler(fullpath)
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    #print(logger.getEffectiveLevel())
    return logger


class MigrateBase(object):
    _DEFAULT_USER = 'cnobile'

    def __init__(self, log):
        self._log = log

    def get_user(self, username=_DEFAULT_USER):
        user = UserModel.objects.filter(username=username, is_active=True)

        if user.count():
            user = user[0]
        else:
            user = None

        self._log.info("Found user: %s", user)
        return user
