#
# utils/modelfields.py
#
# SVN Keywords
#------------------------------
# $Author: cnobile $
# $Date: 2011-05-18 19:02:58 -0400 (Wed, 18 May 2011) $
# $Revision: 47 $
#------------------------------

from django.db import models

from inventory.apps.utils import formfields
from inventory.settings import getLogger


log = getLogger()


class PostalCodeField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        self.input_size = kwargs.pop('input_size', 10)
        log.debug("kwargs: %s", kwargs)
        super(PostalCodeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'input_size': self.input_size,
                    'form_class': formfields.PostalCodeField}
        defaults.update(kwargs)
        log.debug("defaults: %s", defaults)
        return super(PostalCodeField, self).formfield(**defaults)


class SizableCharField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.input_size = kwargs.pop('input_size', 50)
        log.debug("kwargs: %s", kwargs)
        super(SizableCharField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'input_size': self.input_size,
                    'form_class': formfields.SizableCharField}
        defaults.update(kwargs)
        log.debug("defaults: %s", defaults)
        return super(SizableCharField, self).formfield(**defaults)


class SizableTextField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.rows = kwargs.pop('rows', 10)
        self.cols = kwargs.pop('cols', 83)
        log.debug("kwargs: %s", kwargs)
        super(SizableTextField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'rows': self.rows, 'cols': self.cols,
                    'form_class': formfields.SizableTextField}
        defaults.update(kwargs)
        log.debug("defaults: %s", defaults)
        return super(SizableTextField, self).formfield(**defaults)
