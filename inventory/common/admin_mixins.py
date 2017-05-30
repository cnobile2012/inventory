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
    This mixin should be placed in the MRO of an admin class.
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


class UserInlineAdminMixin(object):
    """
    This mixin shopuld be placed in the MRO of the parent admin class not
    the inline classes.
    """

    def save_formset(self, request, form, formset, change):
        for i_form in formset.forms:
            if not change or i_form.instance.pk is None:
                i_form.instance.creator = request.user

            i_form.instance.updater = request.user

        super(UserInlineAdminMixin, self).save_formset(
            request, form, formset, change)


#
# Filters
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
        return [(obj.creator.id, obj.creator_producer())
                for obj in model_admin.model.objects.select_related(
                    'creator').order_by('creator_id').distinct('creator_id')]

    def queryset(self, request, queryset):
        result = queryset

        if self.value():
            result = queryset.filter(creator__id__exact=self.value())

        return result


class UpdaterFilter(SimpleListFilter):
    # Human-readable title to appear in the right sidebar.
    title = _("Updater")
    # The parameter that should be used in the query string for that filter.
    parameter_name = 'updater'

    def lookups(self, request, model_admin):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        return [(obj.updater.id, obj.updater_producer())
                for obj in model_admin.model.objects.select_related(
                    'updater').order_by('updater_id').distinct('updater_id')]

    def queryset(self, request, queryset):
        result = queryset

        if self.value():
            result = queryset.filter(creator__id__exact=self.value())

        return result
