#
# inventory/regions/apps.py
#
"""
Regions App data
"""
__docformat__ = "restructuredtext en"

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RegionsConfig(AppConfig):
    name = 'inventory.regions'
    label = 'regions'
    verbose_name = _("Regions")
