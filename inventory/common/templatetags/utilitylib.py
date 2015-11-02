#
# tags/utilitylib.py
#
# SVN/CVS Keywords
#----------------------------------
# $Author: cnobile $
# $Date: 2010-10-05 12:28:39 -0400 (Tue, 05 Oct 2010) $
# $Revision: 26 $
#----------------------------------

import logging

from django import template

log = logging.getLogger('inventory.common.templatetags')

register = template.Library()

@register.tag
def hideNoValueField(parser, token):
    """
    This tag hides fields that have no data.

    Arguments:

     1. field = The field to be worked on.
     2. fieldList = A list or tuple of valid field names. Can be a literal
        string on the page or from the context.
     3. tag = The tag type. ie. li, td, etc.

    Examples:

     * {% hideNoValueField field "('Distributor', 'Manufacturer')" li %}
     * {% hideNoValueField field fieldList li %}
     """
    tokens = token.split_contents()
    size = len(tokens)

    if size < 4:
        msg = "Invalid number of arguments, found %s should be three."
        raise template.TemplateSyntaxError(msg % (size-1))

    tagName = tokens[0]
    field = tokens[1]
    cmpLabels = tokens[2].strip('"')
    tagType = tokens[3]
    #log.debug("tagName: %s, field: %s, cmpLabels: %s, tageType: %s",
    #          tagName, field, cmpLabels, tagType)
    return NoValueFieldNode(tagName, field, cmpLabels, tagType)


class NoValueFieldNode(template.Node):
    def __init__(self, tagName, field, cmpLabels, tagType):
        self._tagName = tagName
        self._fieldVar = template.Variable(field)
        self._cmpLabelsVar = template.Variable(cmpLabels)
        self._tagTypeVar = template.Variable(tagType)

    def render(self, context):
        field = self._fieldVar.resolve(context)
        label = field.label
        labelTag = field.label_tag()
        tagType = self._tagTypeVar.var

        try:
            cmpLabels = self._cmpLabelsVar.resolve(context)
        except:
            cmpLabels = eval(self._cmpLabelsVar.var)

        #log.debug("%s: label: %s, field: %s, labelTag: %s, cmpLabels: %s",
        #          self._tagName, label, field, labelTag, cmpLabels)

        result = ""

        if 'value' in str(field) or 'None' not in str(field):
            result = "<%s>%s%s</%s>" % (tagType, labelTag, field, tagType)

        return result


@register.tag
def assign(parser, token):
    """
    Assign an expression to a variable in the current context.

    Arguments:

     1. name = The variable name.
     2. value = The value to assign to the name.

    Examples:

     * {% assign [name] [value] %}
     * {% assign list entry.get_related %}
    """
    bits = token.contents.split()

    if len(bits) != 3:
        msg = "%s: tag takes two arguments"
        raise template.TemplateSyntaxError(msg % bits[0])

    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)


class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''
