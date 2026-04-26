#
# utils/admin.py
#

import datetime

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.forms.utils import ErrorList

ErrorList.__str__ = lambda self: '' if not self else super(
    ErrorList, self).__str__()


class ReadPermissionModelAdmin(admin.ModelAdmin):
    """
    This is Django admin with read-only permission by Gregor Muellegger and
    was published on 1st July 2010.
    """
    def has_change_permission(self, request, obj=None):
        if getattr(request, 'readonly', False):
            return True

        return super().has_change_permission(request, obj)

    def changelist_view(self, request, extra_context=None):
        try:
            return super().changelist_view(request,
                                           extra_context=extra_context)
        except PermissionDenied:
            pass

        if request.method == 'POST':
            raise PermissionDenied

        request.readonly = True
        return super().changelist_view(request, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super().add_view(request, form_url,
                                    extra_context=extra_context)
        except PermissionDenied:
            pass

        if request.method == 'POST':
            raise PermissionDenied

        request.readonly = True
        return super().add_view(request, form_url, extra_context=extra_context)

    # def change_view(self, request, object_id, extra_context=None):
    #     try:
    #         return super().change_view(request, object_id,
    #                    extra_context=extra_context)
    #     except PermissionDenied:
    #         pass

    #     if request.method == 'POST':
    #         raise PermissionDenied

    #     request.readonly = True
    #     return super().change_view(request, object_id,
    #        extra_context=extra_context)


class BaseAdmin(ReadPermissionModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user

        # Just in case an external import was done.
        if obj.ctime is None:
            obj.ctime = datetime.datetime.now()

        super().save_model(request, obj, form, change)
