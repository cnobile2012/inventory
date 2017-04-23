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

from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


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


#
# CreatorFilter
#
class CreatorFilter(SimpleListFilter):
    # Human-readable title to appear in the right sidebar.
    title = _("Creator")
    # The parameter that should be used in the query string for that filter.
    parameter_name = 'creator'

    def lookups(self, request, model_admin):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        return set([(obj.id, obj.creator_producer())
                        for obj in model_admin.model.objects.all()])

    def queryset(self, request, queryset):
        result = queryset

        if self.value():
            result = queryset.filter(creator__id__exact=self.value())

        return queryset


#
# UpdaterFilter
#
class UpdaterFilter(SimpleListFilter):
    # Human-readable title to appear in the right sidebar.
    title = _("Updater")
    # The parameter that should be used in the query string for that filter.
    parameter_name = 'updater'

    def lookups(self, request, model_admin):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        return set([(obj.id, obj.updater_producer())
                        for obj in model_admin.model.objects.all()])

    def queryset(self, request, queryset):
        result = queryset

        if self.value():
            result = queryset.filter(creator__id__exact=self.value())

        return queryset
