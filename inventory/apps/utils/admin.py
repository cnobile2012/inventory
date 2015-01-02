#
# utils/admin.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2012-05-16 15:01:25 -0400 (Wed, 16 May 2012) $
# $Revision: 61 $
#----------------------------------

import datetime

from django.contrib import admin
from django.core.exceptions import PermissionDenied


class ReadPermissionModelAdmin(admin.ModelAdmin):
    """
    This is Django admin with read-only permission by Gregor Muellegger and
    was published on 1st July 2010.

    http://gremu.net/BS
    """
    def has_change_permission(self, request, obj=None):
        if getattr(request, 'readonly', False):
            return True

        return super(ReadPermissionModelAdmin, self).has_change_permission(
            request, obj)

    def changelist_view(self, request, extra_context=None):
        try:
            return super(ReadPermissionModelAdmin, self).changelist_view(
                request, extra_context=extra_context)
        except PermissionDenied:
            pass

        if request.method == 'POST':
            raise PermissionDenied

        request.readonly = True
        return super(ReadPermissionModelAdmin, self).changelist_view(
            request, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super(ReadPermissionModelAdmin, self).add_view(
                request, form_url, extra_context=extra_context)
        except PermissionDenied:
            pass

        if request.method == 'POST':
            raise PermissionDenied

        request.readonly = True
        return super(ReadPermissionModelAdmin, self).add_view(
              request, form_url, extra_context=extra_context)

    ## def change_view(self, request, object_id, extra_context=None):
    ##     try:
    ##         return super(ReadPermissionModelAdmin, self).change_view(
    ##             request, object_id, extra_context=extra_context)
    ##     except PermissionDenied:
    ##         pass

    ##     if request.method == 'POST':
    ##         raise PermissionDenied

    ##     request.readonly = True
    ##     return super(ReadPermissionModelAdmin, self).change_view(
    ##         request, object_id, extra_context=extra_context)


class BaseAdmin(ReadPermissionModelAdmin): # admin.ModelAdmin
    def save_model(self, request, obj, form, change):
        obj.user = request.user

        # Just in case an external import was done.
        if obj.ctime is None:
            obj.ctime = datetime.datetime.now()

        #obj.save()
        super(BaseAdmin, self).save_model(request, obj, form, change)
