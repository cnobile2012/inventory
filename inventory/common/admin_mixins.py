# -*- coding: utf-8 -*-
#
# inventory/common/admin_mixins.py
#

"""
Mixins used in the Django admin.

by: Carl J. Nobile

email: carl.nobile@gmail.com
"""
__docformat__ = "restructuredtext en"


class UserAdminMixin(object):
    """
    Admin mixin that should be used in any model implimented with dynamic
    columns.
    """
    def save_model(self, request, obj, form, change):
        """
        When saving a record from the admin the `creator` should be updated
        with the request user object if `change` is `False`. The `updater` is
        always updated withthe request user object.

        :Parameters:
          request : HttpRequest
            Django request object.
          obj : Model
            Django model object
          form : Form
            Django form object.
          change : bool
            If `True` the record was updated, if `False` the record was created.
        """
        if change is False:
            obj.creator = request.user

        obj.updater = request.user
        super(UserAdminMixin, self).save_model(request, obj, form, change)
