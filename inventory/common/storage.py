# -*- coding: utf-8 -*-
#
# inventory/common/storage.py
#
"""
Global file storage
"""
__docformat__ = "restructuredtext en"

from django.core.files.storage import FileSystemStorage


def create_file_path(instance, filename):
    return "{}/{}/{}".format(instance._meta.app_label, instance.public_id,
                             filename)


class InventoryFileStorage(FileSystemStorage):
    """
    We override `FileSystemStorage` so we can change this later without
    having to do migrations.
    """
    pass
