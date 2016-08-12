#
# items/admin.py
#
# Inventory admin registery.
#
# SVN/CVS Keywords
#------------------------------
# $Author: cnobile $
# $Date: 2014-12-05 17:46:21 -0500 (Fri, 05 Dec 2014) $
# $Revision: 95 $
#------------------------------

from django import forms
from django.forms.fields import EMPTY_VALUES
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import six

from inventory.apps.items.models import Manufacturer, Distributor, \
     Category, Currency, Cost, Specification, Item
from inventory.apps.regions.models import Region, Country
from inventory.apps.utils.admin import BaseAdmin
from inventory.setupenv import getLogger

log = getLogger()


# Custom field types
class RegionTypedChoiceField(forms.TypedChoiceField):

    def __init__(self, *args, **kwargs):
        empty_label = kwargs.pop('empty_label', None)

        if isinstance(empty_label, six.string_types):
            choices = list(kwargs.get('choices', ()))
            choices.insert(0, (0, empty_label))
            kwargs['choices'] = choices
            log.debug("choices: %s", choices)

        super(RegionTypedChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Validates that the input is in self.choices.
        """
        if self.required and value in EMPTY_VALUES:
            raise ValidationError(self.error_messages['required'])

        if value in EMPTY_VALUES:
            value = u''

        #value = smart_unicode(value)

        if value == self.empty_value or value in EMPTY_VALUES:
            return self.empty_value

        return value


# Forms
class BusinessAdminForm(forms.ModelForm):
    state = RegionTypedChoiceField(
        required=None, empty_label=_("Choose a country first."))
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
                                     empty_label=_("Choose a country."),
                                     required=False)

    def clean_state(self):
        region = None

        try:
            region = Region.objects.get(id=int(self.cleaned_data['state']))
        except (Region.DoesNotExist, ValueError):
            pass

        return region

    class Meta:
        exclude = ()


class DistributorAdminForm(BusinessAdminForm):
    class Meta:
        model = Distributor
        exclude = ()


class ManufacturerAdminForm(BusinessAdminForm):
    class Meta:
        model = Manufacturer
        exclude = ()


class CostAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ()

    def clean(self):
        mfg = self.cleaned_data.get('manufacturer')
        dst = self.cleaned_data.get('distributor')
        log.debug("mfg: %s, dst: %s, cleaned_data: %s", mfg, dst,
                  self.cleaned_data)

        if mfg and dst:
            msg = _("A cost can only be assigned to one business type, " +
                    "either a distributor or a manufacturer.")
            raise forms.ValidationError(msg)

        return self.cleaned_data


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()

    def clean(self):
        parent = self.cleaned_data.get('parent')
        name = self.cleaned_data.get('name')
        names = Category.objects.filter(name=name)
        log.debug("All %s names in all trees: %s", name, names)

        if Category.getSeparator() in name:
            msg = "A category name cannot contain the category delimiter '%s'."
            raise ValidationError(msg % Category.getSeparator())

        if parent:
            # Test saving a category to itself.
            if name == parent.name:
                msg = _("You cannot save a category in itself.")
                raise forms.ValidationError(msg)

            # Test that this name does not already exist at this leaf
            # in this tree.
            if not self.initial:
                nameSets = Category.getAllRootTrees(name)
                log.debug("All root trees: %s", nameSets)
                parents = Category.getParents(parent)
                parents.append(parent)
                log.debug("Parents: %s", parents)
                flag = False

                for nSet in nameSets:
                    try:
                        flag = all([nSet[c].name == parents[c].name
                                    for c in range(len(parents))])

                        if flag:
                            msg = _("A category at this level with name [%s] " +
                                    "already exists.")
                            raise forms.ValidationError(_(msg % name))
                    except IndexError:
                        continue
        # Test that there is not already a root category with this value.
        elif not self.initial and name in [item.name for item in names
                                           if not item.parent]:
            msg = _("A root level category name [%s] already exists.")
            raise forms.ValidationError(msg % name)

        return self.cleaned_data


class ItemAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemAdminForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'size': 100})

    class Meta:
        model = Item
        exclude = ()


# Admin and Inline
class DistributorAdmin(BaseAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'address_01', 'address_02', 'city',
                'state', 'postal_code', 'country', 'phone', 'fax', 'email',
                'url',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('user', 'ctime', 'mtime',)}),
        )
    list_display = ('name', 'phone', 'fax', 'email', 'url',)
    readonly_fields = ('user', 'ctime', 'mtime',)
    ordering = ('name',)
    form = DistributorAdminForm

    class Media:
        js = ('js/jquery-1.10.1.min.js', 'js/jquery.cookie.js',
              'js/ajaxbase.js', "js/regions.js",)

admin.site.register(Distributor, DistributorAdmin)


class ManufacturerAdmin(BaseAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'address_01', 'address_02', 'city',
                'state', 'postal_code', 'country', 'phone', 'fax', 'email',
                'url',)}),
        (_('Status'), {'classes': ('collapse',),
                       'fields': ('user', 'ctime', 'mtime',)}),
        )
    list_display = ('name', 'phone', 'fax', 'email', 'url',)
    readonly_fields = ('user', 'ctime', 'mtime',)
    ordering = ('name',)
    form = ManufacturerAdminForm

    class Media:
        js = ("js/jquery-1.10.1.min.js", 'js/jquery.cookie.js',
              'js/ajaxbase.js', "js/regions.js",)

admin.site.register(Manufacturer, ManufacturerAdmin)


class CategoryAdmin(BaseAdmin):
    list_display = ('name', '_parentsProducer', '_levelProducer',)
    search_fields = ('name',)
    ordering = ('path',)
    form = CategoryAdminForm

admin.site.register(Category, CategoryAdmin)


class CurrencyAdmin(BaseAdmin):
    list_display = ('symbol', 'currency',)
    ordering = ('currency',)

admin.site.register(Currency, CurrencyAdmin)


#class CostAdmin(BaseAdmin):
#    list_display = ('item', 'value', 'invoice_number', 'date_acquired',)
#    ordering = ('item__title', 'invoice_number', 'date_acquired',)
#    form = CostAdminForm

#admin.site.register(Cost, CostAdmin)


#class SpecificationAdmin(BaseAdmin):
#    list_display = ('name', 'value', '_displayItemTitle',)
#    list_display_links = ('name',)
#    list_editable = ('value',)

#admin.site.register(Specification, SpecificationAdmin)


class CostInline(admin.StackedInline):
    model = Cost
    extra = 1
    max_num = 1
    form = CostAdminForm


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


class ItemAdmin(BaseAdmin):
    form = ItemAdminForm
    fieldsets = (
        (None, {'fields': ('title', 'item_number', 'distributor',
                           'item_number_dst', 'manufacturer',
                           'item_number_mfg', 'quantity', 'condition',
                           'location_code', 'categories',)}),
        ('Description', {'classes': ('collapse',),
                         'fields': ('package', 'notes',)}),
        ('Status', {'classes': ('collapse',),
                    'fields': ('active', 'obsolete', 'purge', 'user', 'ctime',
                               'mtime',)}),
        )
    list_display = ('item_number', 'title', 'quantity', 'condition',
                    '_categoryProducer', '_locationCodeProducer',
                    '_aquiredDateProducer',)
    readonly_fields = ('user', 'ctime', 'mtime',)
    search_fields = ('item_number', 'item_number_dst', 'categories__path',
                     'item_number_mfg', 'title', 'package', 'condition',
                     'distributor__name', 'manufacturer__name', 'notes',)
    list_display_links = ('item_number',)
    list_editable = ('quantity', 'title',)
    list_filter = ('location_code__path', 'distributor__name',
                   'manufacturer__name', 'condition',)
    ordering = ('categories__path',)
    filter_horizontal = ('categories', 'location_code',)
    inlines = (CostInline, SpecificationInline,)
    save_as = True

    class Media:
        css = {'all': ('css/hozFilter.css',)}

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            instance.user = request.user
            instance.save()

        formset.save_m2m()

admin.site.register(Item, ItemAdmin)
