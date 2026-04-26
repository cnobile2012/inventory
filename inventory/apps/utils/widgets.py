#
# utils/widget.py
#

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
        # log.debug("name: %s, value: %s, attrs: %s", name, value, attrs)
        text = f"""<span id="{attrs['id']}">{value}</span>"""
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
        # log.debug("name: %s, value: %s, attrs: %s", name, value, attrs)
        return mark_safe(f'<div id="{attrs['id']}">{value}</div>')
