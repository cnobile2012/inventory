#
# utils/widget.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2010-08-29 22:22:56 -0400 (Sun, 29 Aug 2010) $
# $Revision: 12 $
#----------------------------------

from django.forms.widgets import Widget
from django.utils.safestring import mark_safe

from inventory.settings import getLogger


log = getLogger()


class TextDisplay(Widget):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        """
        Returns this Widget rendered as HTML, as a Unicode string.

        The 'value' given is not guaranteed to be valid input, so subclass
        implementations should program defensively.
        """
        attrs = self.build_attrs(attrs)
        #log.debug("name: %s, value: %s, attrs: %s", name, value, attrs)
        text = u'<span id="%s">%s</span>' % (attrs['id'], value)
        return mark_safe(text)


class TextareaDisplay(Widget):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        """
        Returns this Widget rendered as HTML, as a Unicode string.

        The 'value' given is not guaranteed to be valid input, so subclass
        implementations should program defensively.
        """
        attrs = self.build_attrs(attrs)
        #log.debug("name: %s, value: %s, attrs: %s", name, value, attrs)
        text = u'<div id="%s">%s</div>' % (attrs['id'], value)
        return mark_safe(text)
