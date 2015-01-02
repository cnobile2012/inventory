#
# useraccounts/models.py
#
# User Account models
#
# SVN Keywords
#----------------------------------
# $Author: $
# $Date: $
# $Revision: $
#----------------------------------

from django.db import models
from django.utils.translation import ugettext_lazy as _

from inventory.apps.utils.models import Base
from inventory.apps.items.models import Items, Category, Cost
from inventory.apps.maintenance.models import (
    LocationCodeDefault, LocationCodeCategory,)


class UserProfile(Base):
    item = models.ForeignKey(Items, verbose_name=_("Item"))
    category = models.ForeignKey(Catigory, verbose_name=_("Category"))
    cost = models.ForeignKey(Cost, verbose_name=_("Cost"))
    loc_code_default = models.ForeignKey(
        LocationCodeDefault, verbose_name=_("Location Code Default"))
    loc_code_category = models.ForeignKey(
        LocationCodeCategory, verbose_name=_("Location Code Category"))
