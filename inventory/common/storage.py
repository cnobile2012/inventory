# -*- coding: utf-8 -*-
#
# inventory/common/storage.py
#

import os

from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join

class InventoryFileStorage(FileSystemStorage):

    def path(self, name):
        if not os.path.isdir(self.location):
            os.mkdir(self.location, 0o0775)

        return safe_join(self.location, name)
