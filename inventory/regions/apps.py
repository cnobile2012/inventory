#
# inventory/regions/apps.py
#

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RegionsConfig(AppConfig):
    name = 'inventory.regions'
    label = 'world_regions'
    verbose_name = _("Regions")
