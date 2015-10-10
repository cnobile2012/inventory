# -*- coding: utf-8 -*-
#
# inventory/categories/forms.py
#

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Category


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()

    def clean(self):
        parent = self.cleaned_data.get('parent')
        name = self.cleaned_data.get('name')
        names = Category.objects.filter(name=name)
        log.debug("All %s names in all trees: %s", name, names)

        if Category.DEFAULT_SEPARATOR in name:
            msg = _(("A category name cannot contain the category delimiter"
                     " '{}'.").format(Category.DEFAULT_SEPARATOR))
            raise ValidationError(msg)

        if parent:
            # Test saving a category to itself.
            if name == parent.name:
                msg = _("You cannot save a category in itself.")
                raise forms.ValidationError(msg)

            # Test that this name does not already exist at this leaf
            # in this tree.
            if not self.initial:
                nameSets = Category.objects.get_all_root_trees(name)
                log.debug("All root trees: %s", nameSets)
                parents = Category.get_parents(parent)
                parents.append(parent)
                log.debug("Parents: %s", parents)
                flag = False

                for nSet in nameSets:
                    try:
                        flag = all([nSet[c].name == parents[c].name
                                    for c in range(len(parents))])

                        if flag:
                            msg = _(("A category at this level with name "
                                     "[{}] already exists.").format(name))
                            raise forms.ValidationError(msg)
                    except IndexError:
                        continue
        # Test that there is not already a root category with this value.
        elif not self.initial and name in [item.name for item in names
                                           if not item.parent]:
            msg = _(("A root level category name [{}] already "
                     "exists.").format(name))
            raise forms.ValidationError(msg)

        return self.cleaned_data

