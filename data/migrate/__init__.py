# -*- coding: utf-8 -*-
#
# __init__.py
#

import logging

from django.contrib.auth import get_user_model

try:
    from inventory.projects.models import Project, Membership, InventoryType
except:
    pass

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
    _INVENTORY_NAME = "Electronics"
    _PROJECT_NAME = "Carl's Electronics Inventory"
    _LD_NAME = "Home Inventory Location Formats"
    _LD_DESC = "My DIY Inventory."

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

    def _create_inventory_type(self):
        user = self.get_user()
        name = self._INVENTORY_NAME
        kwargs = {}
        kwargs['description'] = ("Inventory for electronic parts and "
                                 "related items.")
        kwargs['creator'] = user
        kwargs['updater'] = user
        in_type, created = InventoryType.objects.get_or_create(
            name=name, defaults=kwargs)
        return in_type

    def _create_project(self):
        if not self._options.noop:
            user = self.get_user()
            name = self._PROJECT_NAME
            kwargs = {}
            kwargs['inventory_type'] = self._create_inventory_type()
            kwargs['creator'] = user
            kwargs['updater'] = user
            project, created = Project.objects.get_or_create(
                name=name, defaults=kwargs)
            project.process_members([user])


        return project

    def _fix_boolean(self, value):
        value = value.decode('utf-8').strip()
        result = value

        if value.lower() == 'true':
            result = True
        elif value.lower() == 'false':
            result = False

        return result

    def _fix_numeric(self, value):
        value = value.decode('utf-8').strip()
        result = ''

        if value.isdigit():
            result = int(value)

        return result

    def _yes_no(self, value):
        value = value.decode('utf-8').strip().lower()
        
        if value == 'false':
            value = 0
        elif value == 'true':
            value = 1
        else:
            value = 0

        return value
