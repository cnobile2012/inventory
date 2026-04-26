#
# regions/admin.py
#
# Location admin registery.
#

from django.contrib import admin

from inventory.apps.items.admin import BaseAdmin
from inventory.apps.regions.models import Country, Region
from inventory.setupenv import getLogger

log = getLogger()


# Admin and Inline
class RegionAdmin(BaseAdmin):
    list_display = ('country', 'region_code', 'region', 'primary_level',)
    search_fields = ('country__country', 'region_code', 'region',)
    ordering = ('country__country', 'region_code',)

admin.site.register(Region, RegionAdmin)


class RegionInline(admin.TabularInline):
    model = Region
    extra = 6


class CountryAdmin(BaseAdmin):
    list_display = ('country', 'country_code_2', 'country_code_3',
                    'country_number_code',)
    inlines = (RegionInline,)
    search_fields = ('country_code_2', 'country_code_3', 'country',)
    ordering = ('country',)

    def save_formset(self, request, form, formset, change):
        formset.save(commit=False)

        for form in formset.forms:
            form.instance.user = request.user

        formset.save()

admin.site.register(Country, CountryAdmin)
